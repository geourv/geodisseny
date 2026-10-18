"""Visibility pilot: preserve the sealed reference, prepare recipient containers.

The shared installed QGIS producer owns native resource inspection, projects,
captures and seals. This activity selects the retained geometries/rasters,
checks its domain controls and supplies presentation. No viewshed is rerun.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2] if __name__ == '__main__' else None
SLUG = 'visibilitat-costa'
VERSION = '2026-10-12-pilot-01'
ARCHIVE = 'tmp/dades-docents/practica-visibilitat-costa-20261002-r3.zip'
ARCHIVE_SHA = 'b7f2c5f38c8ee45cca592ce35db4aaeac77a413f6ace210948e47e338c3369cc'
INITIAL = {
    'torxa': 'dades/torxa.gpkg', 'carretera': 'dades/carretera.gpkg',
    'mostres_carretera': 'dades/mostres-carretera.gpkg',
    'coberta_original': 'dades/coberta-original.gpkg',
    'receptors': 'dades/receptors.gpkg', 'ambit': 'dades/ambit.gpkg',
}
RESOLVED = {
    'poligon': 'dades/poligon.gpkg', 'buffer_positiu': 'dades/buffer-positiu.gpkg',
    'fragments_area': 'dades/fragments-area.gpkg', 'mostres_area': 'dades/mostres-area.gpkg',
    'receptors_resultats': 'resultats/receptors-resultats.gpkg',
    'carretera_torxa': 'resultats/carretera-torxa.gpkg',
    'intervisibilitat': 'resultats/intervisibilitat.gpkg',
}
INITIAL_RASTERS = {
    'mdt': 'dades/mdt-calcul.tif', 'mds': 'dades/mds-calcul.tif',
    'domini': 'dades/domini-valid.tif', 'ortofoto': 'fonts/ortofoto-context-2025.tif',
}
RESULT_RASTERS = {
    't-mdt': 'resultats/torxa-mdt.tif', 't-mds': 'resultats/torxa-mds.tif',
    'minimum-mds': 'resultats/cota-minima-mds.tif',
    'c-mdt-37': 'resultats/carretera-mdt-totes-nombre.tif',
    'c-mdt-37-percent': 'resultats/carretera-mdt-totes-percent.tif',
    'c-mdt-28': 'resultats/carretera-mdt-nombre.tif',
    'c-mds-28': 'resultats/carretera-mds-nombre.tif',
    'c-mdt-percent': 'resultats/carretera-mdt-percent.tif',
    'c-mds-percent': 'resultats/carretera-mds-percent.tif',
    'a-mdt-number': 'resultats/area-mdt-nombre.tif',
    'a-mds-number': 'resultats/area-mds-nombre.tif',
    'a-mdt-percent': 'resultats/area-mdt-percent.tif',
    'a-mds-percent': 'resultats/area-mds-percent.tif',
    'g-mdt': 'resultats/poligon-mdt-alguna.tif', 'g-mds': 'resultats/poligon-mds-alguna.tif',
}
SHOTS = ['visibilitat-costa-' + name for name in
         ('dades', 'mds', 'torxa', 'punt', 'intervisibilitat', 'carretera',
          'acumulada', 'buffer-positiu', 'perimetre', 'area', 'poligon')]


def compute(context):
    from osgeo import gdal
    from qgis.core import (QgsProject, QgsVectorLayer, QgsVectorFileWriter,
                           QgsRasterLayer, QgsCoordinateReferenceSystem)
    gdal.UseExceptions()
    shutil.copyfile('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', context.output('font-regular'))
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    project.setEllipsoid('NONE')
    for identity, names in [('initial-data', INITIAL), ('resolved-data', RESOLVED)]:
        first = True
        for name in names:
            source = QgsVectorLayer(context.input('source-' + name), name, 'ogr')
            if not source.isValid():
                raise ValueError('Invalid retained vector: ' + name)
            selected = context.processing('native:extractbyexpression', {
                'INPUT': source, 'EXPRESSION': '1=1', 'OUTPUT': 'memory:',
            })['OUTPUT']
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName, options.layerName = 'GPKG', name
            options.actionOnExistingFile = (QgsVectorFileWriter.CreateOrOverwriteFile if first
                                           else QgsVectorFileWriter.CreateOrOverwriteLayer)
            written = QgsVectorFileWriter.writeAsVectorFormatV3(selected, context.output(identity),
                                                               project.transformContext(), options)
            if written[0] != QgsVectorFileWriter.NoError:
                raise ValueError(written)
            first = False
    for name in INITIAL_RASTERS:
        options = ['APPEND_SUBDATASET=YES', 'RASTER_TABLE=' + name,
                   'TILE_FORMAT=PNG' if name == 'ortofoto' else 'TILE_FORMAT=TIFF']
        translated = gdal.Translate(context.output('initial-data'), context.input('source-' + name),
                                    format='GPKG', creationOptions=options)
        if translated is None:
            raise ValueError('Unable to retain input raster: ' + name)
        translated = None
    for identity in RESULT_RASTERS:
        # In particular Float64 minimum elevations are not quantized into tiles.
        shutil.copyfile(context.input('source-' + identity), context.output(identity))
    products = {identity: context.output(identity) for identity in
                ('initial-data', 'resolved-data', 'font-regular', *RESULT_RASTERS)}
    for identity, vectors, slot in [('initial-data', list(INITIAL), 'inici'),
                                     ('resolved-data', list(INITIAL) + list(RESOLVED), 'docent')]:
        project.clear()
        project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
        for name in vectors:
            container = products['initial-data' if name in INITIAL else 'resolved-data']
            layer = QgsVectorLayer(container + '|layername=' + name, name, 'ogr')
            if not layer.isValid():
                raise ValueError('Invalid classroom vector: ' + name)
            project.addMapLayer(layer)
        for name in INITIAL_RASTERS:
            layer = QgsRasterLayer('GPKG:' + products['initial-data'] + ':' + name,
                                   {'mdt': 'MDT', 'mds': 'MDS', 'domini': 'Domini', 'ortofoto': 'Ortofoto ICGC 2025'}[name])
            if not layer.isValid():
                raise ValueError('Invalid embedded raster: ' + name)
            project.addMapLayer(layer)
        if slot == 'docent':
            for name in RESULT_RASTERS:
                layer = QgsRasterLayer(products[name], name)
                if not layer.isValid():
                    raise ValueError('Invalid retained classroom result: ' + name)
                project.addMapLayer(layer)
        compose(project, slot, context.parameters, products)
        context.embed_project(identity, slot, project)
    project.clear()


def verify(context):
    import numpy as np
    from osgeo import gdal, ogr
    gdal.UseExceptions()
    checks = []
    def check(identity, actual, expected, tolerance=0, units='count'):
        checks.append(dict(id=identity, actual=float(actual), expected=float(expected),
                           tolerance=tolerance, units=units))
    def array(path):
        image = gdal.Open(path, gdal.GA_ReadOnly)
        band = image.GetRasterBand(1)
        return image, band.ReadAsArray(), band.GetNoDataValue()
    for name in ('mdt', 'mds', 'domini'):
        original, values, nodata = array(context.input('source-' + name))
        stored, packed, packed_nodata = array('GPKG:' + context.output('initial-data') + ':' + name)
        check(name + '-grid-columns', stored.RasterXSize, 2000)
        check(name + '-grid-rows', stored.RasterYSize, 2000)
        check(name + '-geotransform', max(abs(a-b) for a,b in zip(original.GetGeoTransform(), stored.GetGeoTransform())), 0, units='m')
        valid = np.isfinite(values) & (values != nodata)
        stored_valid = np.isfinite(packed) & (packed != packed_nodata)
        check(name + '-nodata-mask', np.count_nonzero(valid != stored_valid), 0)
        check(name + '-values', np.max(np.abs(values[valid].astype(float) - packed[valid])), 0, units='native-value')
        if name == 'domini':
            check('common-domain-cells', np.count_nonzero(valid & (values == 1)), 3490455)
    initial = ogr.Open(context.output('initial-data'), 0)
    resolved = ogr.Open(context.output('resolved-data'), 0)
    check('carretera-samples', initial.GetLayerByName('mostres_carretera').GetFeatureCount(), 37)
    check('area-fragments', resolved.GetLayerByName('fragments_area').GetFeatureCount(), 57)
    area = sum(feature.GetGeometryRef().GetArea() for feature in resolved.GetLayerByName('poligon'))
    check('recinte-area', area, 2229408.741960, .01, 'm2')
    for identity, expected in [('t-mdt', 2962199), ('t-mds', 447860), ('g-mdt', 2977704), ('g-mds', 470444)]:
        _, data, nodata = array(context.output(identity))
        check(identity + '-visible-cells', np.count_nonzero(data == 1), expected)
    _, data, nodata = array(context.output('c-mdt-37'))
    check('c-mdt-37-any-cells', np.count_nonzero((data > 0) & (data != nodata)), 1461016)
    check('c-mdt-37-max', data[data != nodata].max(), 33)
    for identity in RESULT_RASTERS:
        with Path(context.input('source-' + identity)).open('rb') as stream:
            before = hashlib.file_digest(stream, 'sha256').digest()
        with Path(context.output(identity)).open('rb') as stream:
            after = hashlib.file_digest(stream, 'sha256').digest()
        check('retained-bytes-' + identity, int(before == after), 1)
    return checks


def compose(project, project_id, parameters, products):
    from qgis.core import (QgsRectangle, QgsReferencedRectangle, QgsTextFormat,
                           QgsMarkerSymbol, QgsFillSymbol, QgsLineSymbol,
                           QgsPalLayerSettings, QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QFont
    project.setEllipsoid('NONE')
    project.setTitle('Visibilitat costa · ' + ('inici' if project_id in ('inici', 'initial-project') else 'resultats docents'))
    text = QgsTextFormat()
    text.setFont(QFont('DejaVu Sans'))
    project.styleSettings().setDefaultTextFormat(text)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(
        QgsRectangle(342000, 4549000, 352000, 4559000), project.crs()))
    for layer in project.mapLayers().values():
        name = layer.name()
        if name in ('torxa', 'mostres_carretera', 'receptors', 'mostres_area', 'receptors_resultats', 'carretera_torxa'):
            layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({'color': '#c34d28' if name == 'torxa' else '#00739b', 'size': '4' if name == 'torxa' else '2', 'outline_color': 'white'}))
        elif name in ('ambit', 'coberta_original', 'poligon', 'buffer_positiu', 'fragments_area'):
            layer.renderer().setSymbol(QgsFillSymbol.createSimple({'style': 'no', 'outline_color': '#ad472b' if name == 'poligon' else '#0072b2', 'outline_width': '.7'}))
        elif name in ('carretera', 'intervisibilitat'):
            layer.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color': '#b12f43', 'line_width': '1'}))
        if name == 'torxa':
            labels = QgsPalLayerSettings()
            labels.fieldName, labels.isExpression = "'T'", True
            labels.setFormat(text)
            layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
            layer.setLabelsEnabled(True)
        project.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(name in
            ('torxa', 'carretera', 'receptors', 'coberta_original', 'poligon', 'Ortofoto ICGC 2025'))
    order = {'torxa': 0, 'receptors': 1, 'carretera': 2, 'poligon': 3,
             'coberta_original': 4, 'mostres_carretera': 5, 'Ortofoto ICGC 2025': 100}
    tree = project.layerTreeRoot()
    tree.setHasCustomLayerOrder(True)
    tree.setCustomLayerOrder(sorted(project.mapLayers().values(), key=lambda layer: order.get(layer.name(), 20)))


def snapshot(run_id):
    run = ROOT / 'sandbox/practiques' / SLUG / run_id
    if run.exists() or run.is_symlink():
        raise FileExistsError('Select a new visibility run')
    source = ROOT / ARCHIVE
    with source.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != ARCHIVE_SHA:
            raise ValueError('Retained visibility archive changed')
    selected = {'source-' + identity: path for mapping in (INITIAL, RESOLVED, INITIAL_RASTERS, RESULT_RASTERS) for identity, path in mapping.items()}
    selected.update({'capture-' + name: 'captures/' + name + '.png' for name in SHOTS})
    payloads = {}
    with zipfile.ZipFile(source) as archive:
        manifest = json.loads(archive.read('visibilitat-costa/MANIFEST.json'))
        records = {row['path']: row for row in manifest['files']}
        for identity, path in selected.items():
            data = archive.read('visibilitat-costa/' + path)
            if hashlib.sha256(data).hexdigest() != records[path]['sha256']:
                raise ValueError('Retained member changed: ' + path)
            payloads[identity] = (path, data)
    run.mkdir(parents=True)
    inputs = run / 'inputs'
    inputs.mkdir()
    request = json.loads((ROOT / 'practiques' / SLUG / 'activitat.json').read_text())
    request['inputs'] = []
    inventory = []
    for identity, (path, data) in payloads.items():
        filename = identity + Path(path).suffix
        target = inputs / filename
        with target.open('xb') as stream:
            stream.write(data)
        digest = hashlib.sha256(data).hexdigest()
        inventory.append({'id': identity, 'source_member': path, 'path': str(target.relative_to(ROOT)), 'sha256': digest, 'bytes': len(data)})
        if identity.startswith('source-'):
            request['inputs'].append({'id': identity, 'path': filename, 'sha256': digest})
    shutil.copyfile(Path(__file__), inputs / 'preparar.py')
    with (inputs / 'activitat.json').open('x') as stream:
        json.dump(request, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    with (run / 'sources.json').open('x') as stream:
        json.dump({'archive': ARCHIVE, 'archive_sha256': ARCHIVE_SHA, 'files': inventory,
                   'human_approved': False, 'source_snapshot_only': True}, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'request': str((inputs / 'activitat.json').relative_to(ROOT)), 'source_files': len(inventory)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--snapshot', action='store_true')
    parser.add_argument('--run-id', default=VERSION)
    args = parser.parse_args()
    if args.snapshot:
        if not args.run_id or Path(args.run_id).name != args.run_id:
            raise ValueError('Run ID must be one path component')
        snapshot(args.run_id)
