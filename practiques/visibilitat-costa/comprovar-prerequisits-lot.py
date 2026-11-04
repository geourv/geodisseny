"""Check this activity's point fields, native .batch recovery and path syntax.

Run inside the pinned QGIS engine with readonly /dades and writable /proof.
These native-widget checks are not MCP screenshots or a Windows execution.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from unittest.mock import patch

sys.path.append('/usr/share/qgis/python/plugins')
from qgis.core import (QgsApplication, QgsCoordinateReferenceSystem, QgsExpression,
                       QgsExpressionContext, QgsExpressionContextScope,
                       QgsExpressionContextUtils, QgsProject, QgsRasterLayer, QgsVectorLayer)
from qgis.PyQt.QtWidgets import QFileDialog
from processing.core.Processing import Processing
import processing

OUT = Path('/proof')
DATA = Path('/dades')
app = QgsApplication([], True)
app.initQgis()
Processing.initialize()
project = QgsProject.instance()
project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
road = QgsVectorLayer(str(DATA / 'visibilitat-costa.gpkg') + '|layername=carretera', 'Carretera', 'ogr')
assert road.isValid()
points = processing.run('native:pointsalonglines', {'INPUT': road, 'DISTANCE': 98.71,
    'START_OFFSET': 49.36, 'END_OFFSET': 0, 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
assert points.featureCount() == 37
fields = points.fields().names()
assert 'x' not in fields and 'y' not in fields
xy = processing.run('native:addxyfields', {'INPUT': points, 'CRS': 'EPSG:25831',
    'PREFIX': '', 'OUTPUT': 'TEMPORARY_OUTPUT'})['OUTPUT']
assert {'x', 'y'} <= set(xy.fields().names()) and xy.featureCount() == 37
assert all(abs(feature['x'] - feature.geometry().asPoint().x()) < 1e-8 and
           abs(feature['y'] - feature.geometry().asPoint().y()) < 1e-8 for feature in xy.getFeatures())

c = QgsVectorLayer(str(DATA / 'visibilitat-costa.gpkg') + '|layername=mostres_carretera', 'C', 'ogr')
mdt = QgsRasterLayer(str(DATA / 'rasters/mdt.tif'), 'MDT', 'gdal')
assert c.isValid() and mdt.isValid()
assert {'id', 'x', 'y'} <= set(c.fields().names())
project.addMapLayer(c)
project.addMapLayer(mdt)
workspace = OUT / 'sandbox'
workspace.mkdir()
project.setFileName(str(workspace / 'intervisibilitat.qgz'))
assert project.write()
assert QgsExpressionContextUtils.projectScope(project).variable('project_folder') == str(workspace)
identities = ('C05', 'C11', 'C13', 'C25', 'C37')
features = {feature['id']: feature for feature in c.getFeatures() if feature['id'] in identities}
assert set(features) == set(identities)

guide = Path('/guide/LLEGIU-ME.md').read_text()
blocks = re.findall(r'```[^\n]*\n(.*?)```', guide, re.S)
windows = [block for block in blocks
            if 'replace(' in block and '@project_folder' in block]
assert len(windows) == 1, 'Check the exact Windows code block from the authored guide.'
windows_expression = windows[0].strip()
windows_values = []
for base in (r'C:\Users\Nom\Documents\practica\sandbox', r'C:\Users/Nom\Documents/practica\sandbox'):
    for index, identity in enumerate(identities):
        scope = QgsExpressionContextScope()
        scope.setVariable('project_folder', base)
        scope.setVariable('row_number', index)
        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.projectScope(project))
        context.appendScope(scope)
        expression = QgsExpression(windows_expression)
        assert not expression.hasParserError(), expression.parserErrorString()
        value = expression.evaluate(context)
        assert not expression.hasEvalError(), expression.evalErrorString()
        expected = base.replace('/', '\\') + '\\conques-mdt-prova\\conca-' + identity + '-mdt.tif'
        assert value == expected and '/' not in value, (value, expected)
        windows_values.append(value)

road_outputs = [block.strip() for block in blocks if '@project_folder' in block
                and "layer := 'C'" in block and 'replace(' not in block]
assert len(road_outputs) == 3
native_paths = []
all_features = sorted(c.getFeatures(), key=lambda feature: feature['id'])
for block in road_outputs:
    selected = ([features[identity] for identity in identities] if '/conques-mdt-prova/' in block else
                [feature for feature in all_features if feature['calculable'] == 1]
                if '/cotes-minimes-carretera-mds/' in block else all_features)
    values = []
    for index, feature in enumerate(selected):
        scope = QgsExpressionContextScope()
        scope.setVariable('row_number', index)
        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.projectScope(project))
        context.appendScope(scope)
        expression = QgsExpression(block)
        assert not expression.hasParserError(), expression.parserErrorString()
        value = expression.evaluate(context)
        assert not expression.hasEvalError(), expression.evalErrorString()
        assert Path(value).is_relative_to(workspace) and feature['id'] in Path(value).name
        values.append(value)
    assert len(set(values)) == len(selected)
    native_paths.append({'expression': block, 'rows': len(values), 'outputs': values})
assert sorted(row['rows'] for row in native_paths) == [5, 28, 37]
five_expression = next(block for block in road_outputs if '/conques-mdt-prova/' in block)
(workspace / 'conques-mdt-prova').mkdir()

from processing.gui.BatchAlgorithmDialog import BatchAlgorithmDialog
algorithm = QgsApplication.processingRegistry().algorithmById('gdal:viewshed')
assert algorithm
dialog = BatchAlgorithmDialog(algorithm.create())
panel = dialog.mainWidget()
panel.addRow(4)
assert panel.batchRowCount() == 5
extra = '-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714'
expected_outputs = []
for index, identity in enumerate(identities):
    feature = features[identity]
    parameters = {'INPUT': mdt, 'BAND': 1,
        'OBSERVER': f'{feature["x"]},{feature["y"]} [EPSG:25831]',
        'OBSERVER_HEIGHT': 1.7, 'TARGET_HEIGHT': 1.7, 'MAX_DISTANCE': 0, 'EXTRA': extra}
    for name, value in parameters.items():
        panel.wrappers[index][panel.parameter_to_column[name]].setParameterValue(value, panel.processing_context)
    output = str(workspace / 'conques-mdt-prova' / ('conca-' + identity + '-mdt.tif'))
    expected_outputs.append(output)
    panel.tblParameters.cellWidget(index + 1, panel.parameter_to_column['OUTPUT']).setValue(output)
path = OUT / 'conques-prova.batch'
with patch.object(QFileDialog, 'getSaveFileName', return_value=(str(path), '')):
    panel.save()
assert path.is_file()
saved = json.loads(path.read_text())
assert saved['format'] == 'batch_3.40' and len(saved['rows']) == 5
assert all(set(row) == {'PARAMETERS', 'OUTPUTS'} for row in saved['rows'])
assert [row['OUTPUTS']['OUTPUT'] for row in saved['rows']] == expected_outputs
assert len(set(expected_outputs)) == 5
original_batch_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
reload_dialog = BatchAlgorithmDialog(algorithm.create())
reloaded = reload_dialog.mainWidget()
with patch.object(QFileDialog, 'getOpenFileName', return_value=(str(path), '')):
    reloaded.load()
assert reloaded.batchRowCount() == 5
for index, identity in enumerate(identities):
    parameters, valid = reloaded.parametersForRow(index, reloaded.processing_context, warnOnInvalid=False)
    assert valid and parameters['EXTRA'] == extra
    point = algorithm.parameterAsPoint(parameters, 'OBSERVER', reloaded.processing_context)
    assert abs(point.x() - features[identity]['x']) < 1e-8 and abs(point.y() - features[identity]['y']) < 1e-8
    assert reloaded.tblParameters.cellWidget(index + 1, reloaded.parameter_to_column['OUTPUT']).getValue() == expected_outputs[index]

# Moving the project alone leaves the batch's stored outputs unchanged. Revise
# a separate copy, including its raster input, through the native widgets.
relocated = OUT / 'trasllat'
(relocated / 'data').mkdir(parents=True)
(relocated / 'sandbox/conques-mdt-prova').mkdir(parents=True)
new_mdt_path = relocated / 'data/mdt.tif'
shutil.copyfile(DATA / 'rasters/mdt.tif', new_mdt_path)
new_mdt = QgsRasterLayer(str(new_mdt_path), 'MDT traslladat', 'gdal')
assert new_mdt.isValid()
project.addMapLayer(new_mdt)
project.setFileName(str(relocated / 'sandbox/intervisibilitat.qgz'))
assert QgsExpressionContextUtils.projectScope(project).variable('project_folder') == str(relocated / 'sandbox')
assert [reloaded.tblParameters.cellWidget(i + 1, reloaded.parameter_to_column['OUTPUT']).getValue()
        for i in range(5)] == expected_outputs
rebased_outputs = []
for index, identity in enumerate(identities):
    scope = QgsExpressionContextScope()
    scope.setVariable('row_number', index)
    context = QgsExpressionContext()
    context.appendScope(QgsExpressionContextUtils.projectScope(project))
    context.appendScope(scope)
    expression = QgsExpression(five_expression)
    value = expression.evaluate(context)
    assert not expression.hasEvalError(), expression.evalErrorString()
    assert value == str(relocated / 'sandbox/conques-mdt-prova' / ('conca-' + identity + '-mdt.tif'))
    reloaded.wrappers[index][reloaded.parameter_to_column['INPUT']].setParameterValue(new_mdt, reloaded.processing_context)
    reloaded.tblParameters.cellWidget(index + 1, reloaded.parameter_to_column['OUTPUT']).setValue(value)
    rebased_outputs.append(value)
rebased_path = OUT / 'conques-prova-trasllat.batch'
with patch.object(QFileDialog, 'getSaveFileName', return_value=(str(rebased_path), '')):
    reloaded.save()
final_dialog = BatchAlgorithmDialog(algorithm.create())
final_panel = final_dialog.mainWidget()
with patch.object(QFileDialog, 'getOpenFileName', return_value=(str(rebased_path), '')):
    final_panel.load()
assert final_panel.batchRowCount() == 5
for index in range(5):
    parameters, valid = final_panel.parametersForRow(index, final_panel.processing_context, warnOnInvalid=False)
    assert valid
    layer = algorithm.parameterAsRasterLayer(parameters, 'INPUT', final_panel.processing_context)
    assert layer and layer.isValid() and layer.source() == str(new_mdt_path)
    assert final_panel.tblParameters.cellWidget(index + 1, final_panel.parameter_to_column['OUTPUT']).getValue() == rebased_outputs[index]
assert hashlib.sha256(path.read_bytes()).hexdigest() == original_batch_sha256
assert not list(workspace.rglob('*.tif')) and not list((relocated / 'sandbox').rglob('*.tif'))
assert not list(OUT.glob('*.tif')), 'The configuration check must not run Viewshed.'
report = {'ok': True, 'qgis': QgsApplication.qgisVersion() if hasattr(QgsApplication, 'qgisVersion') else '3.44.11',
    'generated_points': 37, 'pointsalonglines_fields': fields, 'xy_fields_after_addxyfields': xy.fields().names(),
    'xy_crs': 'EPSG:25831', 'all_geometry_coordinates_match': True,
    'native_batch_format': saved['format'], 'native_saved_reloaded_rows': 5,
    'saved_batch_sha256': original_batch_sha256,
    'project_folder_scope_checked': str(workspace),
    'exact_guide_road_output_expressions': native_paths,
    'batch_project_move_does_not_rewrite_stored_paths': True,
    'rebased_batch_reloaded_rows': 5, 'rebased_raster_input_valid': True,
    'rebased_batch_sha256': hashlib.sha256(rebased_path.read_bytes()).hexdigest(),
    'original_batch_bytes_preserved': True,
    'exact_guide_windows_expression_checked': windows_expression,
    'windows_formatted_path_checks': len(windows_values), 'windows_runtime_executed': False,
    'viewshed_executed': False, 'screenshot_evidence': False}
with (OUT / 'verified.json').open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps(report, ensure_ascii=False), flush=True)
