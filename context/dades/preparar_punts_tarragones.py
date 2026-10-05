"""Prepare a private, portable C4 workshop from retained ICAEN/ICGC inputs.

Run --build in the pinned QGIS image, with repository/inputs readonly and only
OUT writable. Run --record on the host. --package seals a new ZIP, never replaces
one. Processing execution and configured UI dialogs are separate evidence.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'tmp/dades-docents/qgis/punts-tarragones-20261004'
ZIP = ROOT / 'tmp/dades-docents/practica-punts-tarragones-20261004.zip'
IMAGE = 'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'
_QGIS_APP = None
SOURCES = {
    'icaen-original.gpkg': ('tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg',
        '1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'),
    'ambit-original.gpkg': ('tmp/dades-docents/qgis/icaen-ambit.gpkg',
        '2acf61341b97e3120a6668aed34973b1238daa413efd5f281513f0e8948fa709'),
    'seccions-preparades.gpkg': ('tmp/dades-docents/seccions/seccions-analisi.gpkg',
        '84d7a33bfa8dab8089bb852e447947c92a95da3bf733161663e24a2be98523af'),
}
SHOTS = ['dades', 'centres-menu', 'centres-caixa', 'centres-parametres', 'centres-resultat',
         'dispersio-parametres', 'dispersio-resultat', 'graella-parametres',
         'recompte-parametres', 'recompte-resultat', 'kernel-parametres',
         'kernel-resultat', 'seccions-parametres', 'seccions-resultat']


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def initialise():
    assert not ZIP.exists(), 'Delivery already sealed; choose a new version.'
    OUT.mkdir(exist_ok=True)
    marker = OUT / '.punts.json'
    if marker.exists():
        assert json.loads(marker.read_text())['owner'] == Path(__file__).name
    else:
        assert not list(OUT.iterdir()), 'Unowned nonempty output directory.'
        dump(marker, {'owner': Path(__file__).name})
    for name in ['fonts', 'projectes', 'controls', 'captures', 'reproduccio']:
        (OUT / name).mkdir(exist_ok=True)


def build():
    global _QGIS_APP
    import numpy as np
    from osgeo import gdal
    from qgis.core import (QgsApplication, QgsProject, QgsCoordinateReferenceSystem,
        QgsVectorLayer, QgsVectorFileWriter, QgsMarkerSymbol, QgsFillSymbol,
        QgsRendererRange, QgsGraduatedSymbolRenderer, QgsRasterLayer,
        QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer, Qgis)
    from qgis.PyQt.QtGui import QColor
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _QGIS_APP = app = QgsApplication([], False); app.initQgis()
    sys.path.insert(0, '/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing
    gdal.UseExceptions(); initialise()
    # Existing draft output is never silently replaced after a partial build.
    assert not (OUT / 'dades.gpkg').exists(), 'Use a fresh build destination.'
    source_records = {}
    for name, (relative, expected) in SOURCES.items():
        source = ROOT / relative
        assert not Path(str(source) + '-wal').exists(), source
        assert sha(source) == expected, source
        target = OUT / 'fonts' / name
        if target.exists(): assert sha(target) == expected
        else: shutil.copyfile(source, target)
        source_records[name] = {'source': relative, 'sha256': expected}
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    project.setEllipsoid('NONE')
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    options = QgsVectorLayer.LayerOptions(); options.forceReadOnly = True
    layers = {}; operations = []

    def source(name, table):
        layer = QgsVectorLayer(str(OUT / 'fonts' / name) + '|layername=' + table,
                               table, 'ogr', options)
        assert layer.isValid() and layer.crs().authid() == 'EPSG:25831', table
        return layer

    def run(ident, **parameters):
        parameters.setdefault('OUTPUT', 'memory:')
        algorithm = QgsApplication.processingRegistry().algorithmById(ident)
        assert algorithm and set(parameters) <= {p.name() for p in algorithm.parameterDefinitions()}
        operations.append({'id': ident, 'parameters': {
            key: value.name() if isinstance(value, QgsVectorLayer) else str(value)
            for key, value in parameters.items()}})
        return processing.run(ident, parameters)['OUTPUT']

    def save(layer, name, dataset='resultats.gpkg', title=None):
        destination = OUT / dataset
        opts = QgsVectorFileWriter.SaveVectorOptions()
        opts.driverName = 'GPKG'; opts.layerName = name
        opts.actionOnExistingFile = (QgsVectorFileWriter.CreateOrOverwriteLayer if destination.exists()
                                    else QgsVectorFileWriter.CreateOrOverwriteFile)
        status = QgsVectorFileWriter.writeAsVectorFormatV3(layer, str(destination), project.transformContext(), opts)
        assert status[0] == QgsVectorFileWriter.NoError, status
        saved = QgsVectorLayer(str(destination) + '|layername=' + name, title or name, 'ogr')
        assert saved.isValid() and saved.featureCount() == layer.featureCount()
        layers[name] = saved; project.addMapLayer(saved)
        return saved

    def calc(layer, field, expression):
        return run('native:fieldcalculator', INPUT=layer, FIELD_NAME=field,
                   FIELD_TYPE=0, FIELD_LENGTH=20, FIELD_PRECISION=8, FORMULA=expression)

    original = source('icaen-original.gpkg', 'autoconsum_tarragones')
    all_points = run('native:multiparttosingleparts', INPUT=original)
    assert original.featureCount() == all_points.featureCount() == 5102
    assert len({f['gml_id'] for f in all_points.getFeatures()}) == 5102
    all_points = save(all_points, 'registre_icaen', 'dades.gpkg', 'ICAEN complet · 5102')
    known = run('native:extractbyexpression', INPUT=all_points, EXPRESSION='"POT_KW" > 0')
    known = save(known, 'icaen_coneguda', 'dades.gpkg', 'ICAEN coneguda')
    boundary = save(source('ambit-original.gpkg', 'icaen-ambit'), 'tarragones', 'dades.gpkg', 'Tarragonès')
    prepared = source('seccions-preparades.gpkg', 'seccions')
    base = run('native:retainfields', INPUT=prepared,
               FIELDS=['cusec', 'functional_n', 'age_exact_n', 'age_median_exact'])
    sections = save(base, 'seccions', 'dades.gpkg', 'Seccions censals')
    features = list(known.getFeatures())
    xy = np.array([[f.geometry().asPoint().x(), f.geometry().asPoint().y()] for f in features])
    weights = np.array([float(f['POT_KW']) for f in features])
    assert len(xy) == 3762 and weights.sum() == 36633
    centres = {}
    for name, data, weight, title in [
        ('centre_total', all_points, None, 'Centre · conjunt complet'),
        ('centre_mitja', known, None, 'Centre mitjà · mateixa selecció'),
        ('centre_ponderat', known, 'POT_KW', 'Centre ponderat · kW')]:
        centre = save(run('native:meancoordinates', INPUT=data, WEIGHT=weight), name, title=title)
        point = next(centre.getFeatures()).geometry().asPoint()
        centres[name] = [point.x(), point.y()]
    assert np.allclose(centres['centre_mitja'], xy.mean(axis=0), rtol=0, atol=1e-6)
    assert np.allclose(centres['centre_ponderat'], np.average(xy, axis=0, weights=weights), rtol=0, atol=1e-6)
    save(run('native:centroids', INPUT=boundary, ALL_PARTS=False), 'centroide', title='Centroide comarcal')
    covariance = np.cov(xy, rowvar=False, ddof=0)
    # The expressions are also usable in the Field Calculator, one field at a time.
    expressions = {
        'Sxx': "with_variable('cx',x($geometry),aggregate('ICAEN coneguda','mean',(x($geometry)-@cx)^2))",
        'Syy': "with_variable('cy',y($geometry),aggregate('ICAEN coneguda','mean',(y($geometry)-@cy)^2))",
        'Sxy': "with_variable('cx',x($geometry),with_variable('cy',y($geometry),aggregate('ICAEN coneguda','mean',(x($geometry)-@cx)*(y($geometry)-@cy))))",
        'D_m': 'sqrt("Sxx" + "Syy")',
        'delta': 'sqrt(("Sxx" - "Syy")^2 + 4 * "Sxy"^2)',
        'a_m': 'sqrt(("Sxx" + "Syy" + "delta") / 2)',
        'b_m': 'sqrt(("Sxx" + "Syy" - "delta") / 2)',
        'azimut': '90 - degrees(atan2(2 * "Sxy", "Sxx" - "Syy")) / 2',
    }
    parameters = layers['centre_mitja']
    for field, expression in expressions.items(): parameters = calc(parameters, field, expression)
    parameters = save(parameters, 'centre_dispersio', title='Centre i dispersió')
    attributes = next(parameters.getFeatures())
    assert np.allclose([attributes['Sxx'], attributes['Syy'], attributes['Sxy']],
                       [covariance[0, 0], covariance[1, 1], covariance[0, 1]], rtol=1e-10)
    for name, expression in [('cercle', 'make_circle($geometry, "D_m", 72)'),
                             ('ellipse', 'make_ellipse($geometry, "a_m", "b_m", "azimut", 72)')]:
        geometry = save(run('native:geometrybyexpression', INPUT=parameters, OUTPUT_GEOMETRY=0,
            WITH_Z=False, WITH_M=False, EXPRESSION=expression), name,
            title='Cercle · distància estàndard' if name == 'cercle' else 'El·lipse · una desviació')
        ring = np.array(json.loads(next(geometry.getFeatures()).geometry().asJson())['coordinates'][0])[:-1, :2]
        if name == 'cercle':
            assert np.allclose(np.linalg.norm(ring - xy.mean(axis=0), axis=1), np.sqrt(np.trace(covariance)), atol=1e-6)
        else: assert np.allclose(2*np.cov(ring, rowvar=False, ddof=0), covariance, rtol=1e-6, atol=.01)
    bounds = known.extent()
    grid_extent = [np.floor(bounds.xMinimum()/1000)*1000, np.ceil(bounds.xMaximum()/1000)*1000,
              np.floor(bounds.yMinimum()/1000)*1000, np.ceil(bounds.yMaximum()/1000)*1000]
    grid = save(run('native:creategrid', TYPE=2, EXTENT=','.join(map(str, grid_extent))+' [EPSG:25831]',
        HSPACING=1000, VSPACING=1000, HOVERLAY=0, VOVERLAY=0, CRS=project.crs()), 'graella', title='Graella · 1 km²')
    counted = run('native:countpointsinpolygon', POLYGONS=grid, POINTS=known, FIELD='n_punts')
    counted = run('native:countpointsinpolygon', POLYGONS=counted, POINTS=known, WEIGHT='POT_KW', FIELD='kw_coneguts')
    counted = save(counted, 'recompte', title='Recompte · registres per km²')
    for cell in counted.getFeatures():
        box = cell.geometry().boundingBox()
        mask = ((xy[:, 0] >= box.xMinimum()) & (xy[:, 0] < box.xMaximum()) &
                (xy[:, 1] >= box.yMinimum()) & (xy[:, 1] < box.yMaximum()))
        assert cell['n_punts'] == int(mask.sum()) and cell['kw_coneguts'] == float(weights[mask].sum())
        assert abs(cell.geometry().area() - 1e6) < 1e-5
    assert sum(f['n_punts'] for f in counted.getFeatures()) == 3762
    assert sum(f['kw_coneguts'] for f in counted.getFeatures()) == 36633
    building = run('native:extractbyexpression', INPUT=all_points, EXPRESSION='"UBICACIO" = \'Edifici\'')
    building_known = run('native:extractbyexpression', INPUT=building, EXPRESSION='"POT_KW" > 0')
    aggregated = sections
    for data, weight, field in [(building, None, 'n_reg'), (building_known, None, 'n_coneguts'),
                               (building_known, 'POT_KW', 'kw_coneguts')]:
        aggregated = run('native:countpointsinpolygon', POLYGONS=aggregated, POINTS=data, WEIGHT=weight, FIELD=field)
    indicator = 'CASE WHEN "functional_n" > 0 AND ("n_reg" = 0 OR "n_coneguts" > 0) THEN 100.0 * "kw_coneguts" / "functional_n" END'
    aggregated = save(calc(aggregated, 'kw_100ed', indicator), 'seccions_resum', title='Seccions · kW per 100 edificis')
    reference = {f['cusec']: f for f in prepared.getFeatures()}
    section_features = list(aggregated.getFeatures())
    assert len(section_features) == 151
    section_kw = sum(f['kw_coneguts'] for f in section_features)
    assert section_kw == 36058
    for row in section_features:
        expected = reference[row['cusec']]
        assert row['n_reg'] == expected['pv_edifici_n']
        assert row['n_coneguts'] == expected['pv_edifici_known_n']
        assert row['kw_coneguts'] == expected['pv_edifici_kw']
        if expected['pv_edifici_known_n'] > 0:
            assert abs(float(row['kw_100ed']) - float(expected['kw_per_100_buildings'])) < 1e-8
    kernels = []
    for field, suffix, total, unit in [(None, 'punts', 3762, 'registres/km²'),
                                     ('POT_KW', 'kw', 36633, 'kW coneguts/km²')]:
        for radius in [500, 1500]:
            raw = OUT / f'kernel-{suffix}-{radius}-raw.tif'
            run('qgis:heatmapkerneldensityestimation', INPUT=known, RADIUS=radius, PIXEL_SIZE=100,
                WEIGHT_FIELD=field, KERNEL=0, DECAY=0, OUTPUT_VALUE=0, OUTPUT=str(raw))
            ds = gdal.Open(str(raw)); band = ds.GetRasterBand(1); values = band.ReadAsArray()
            valid = values != band.GetNoDataValue(); factor = 3e6/(np.pi*radius**2)
            normalized = np.where(valid, values*factor, -9999).astype('float32')
            mass = float(normalized[valid].sum(dtype='float64'))*.01
            assert abs(mass-total)/total < .03, (raw, mass, total)
            path = OUT / f'densitat-{suffix}-{radius}.tif'
            dest = gdal.GetDriverByName('GTiff').Create(str(path), ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Float32,
                options=['COMPRESS=DEFLATE', 'TILED=YES'])
            dest.SetGeoTransform(ds.GetGeoTransform()); dest.SetProjection(ds.GetProjection())
            dest.GetRasterBand(1).WriteArray(normalized); dest.GetRasterBand(1).SetNoDataValue(-9999)
            dest.GetRasterBand(1).SetUnitType(unit); dest = None
            kernels.append({'path': path.name, 'radius_m': radius, 'pixel_m': 100, 'weight': field,
                'unit': unit, 'factor': factor, 'integrated_mass': mass, 'expected_mass': total,
                'maximum': float(normalized[valid].max()), 'geotransform': list(ds.GetGeoTransform()),
                'shape': [ds.RasterYSize, ds.RasterXSize], 'nodata': -9999})
            ds = None
    # Native styles in the GPKG make both the projects and independent capture loads agree.
    for name, layer in layers.items():
        if layer.geometryType() == Qgis.GeometryType.Point:
            symbol = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#59798b', 'size': '1.1', 'outline_style': 'no'})
            if name.startswith('centre') or name == 'centroide':
                shape, colour = {'centre_total': ('circle', '#7b3294'), 'centre_ponderat': ('triangle', '#c47624'),
                                 'centroide': ('cross', '#222222')}.get(name, ('diamond', '#006699'))
                symbol = QgsMarkerSymbol.createSimple({'name': shape,
                    'color': colour, 'size': '4', 'outline_color': '#222222' if name == 'centroide' else '#ffffff'})
            layer.renderer().setSymbol(symbol)
        else:
            layer.renderer().setSymbol(QgsFillSymbol.createSimple({'color': '#f2f2ed', 'outline_color': '#84918a', 'outline_width': '.25'}))
            if name in ['cercle', 'ellipse', 'graella']:
                layer.renderer().setSymbol(QgsFillSymbol.createSimple({'style': 'no', 'outline_color': '#b87924' if name == 'cercle' else '#006699',
                    'outline_width': '.7' if name != 'graella' else '.15', 'outline_style': 'dash' if name == 'cercle' else 'solid'}))
            if name in ['recompte', 'seccions_resum']:
                field = 'n_punts' if name == 'recompte' else 'kw_100ed'
                limits = [0, 10, 30, 60, 120, 100000] if name == 'recompte' else [0, 100, 250, 500, 1000, 100000]
                colours = ['#f7fbff', '#c6dbef', '#6baed6', '#2171b5', '#08306b']
                ranges = [QgsRendererRange(lo, hi, QgsFillSymbol.createSimple({'color': colour, 'outline_color': '#aaaaaa', 'outline_width': '.12'}),
                          f'{lo}–{hi}' if hi < 100000 else f'>{lo}') for lo, hi, colour in zip(limits, limits[1:], colours)]
                layer.setRenderer(QgsGraduatedSymbolRenderer(field, ranges))
        layer.saveStyleToDatabase('docent', 'C4 · dades i resultats', True, '')
    for row in kernels:
        path = OUT / row['path']; layer = QgsRasterLayer(str(path), row['path'].removesuffix('.tif'))
        maximum = max(r['maximum'] for r in kernels if r['weight'] == row['weight'])
        shader = QgsColorRampShader(0, maximum); shader.setColorRampType(QgsColorRampShader.Interpolated)
        shader.setColorRampItemList([QgsColorRampShader.ColorRampItem(maximum*f, QColor(c), f'{maximum*f:.1f}')
            for f, c in [(0, '#fff7ec'), (.25, '#fee8c8'), (.5, '#fdbb84'), (.75, '#e34a33'), (1, '#7f0000')]])
        raster_shader = QgsRasterShader(); raster_shader.setRasterShaderFunction(shader)
        renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, raster_shader)
        renderer.setClassificationMin(0); renderer.setClassificationMax(maximum)
        layer.setRenderer(renderer)
        layer.saveNamedStyle(str(path.with_suffix('.qml')))
        layers[path.stem] = layer; project.addMapLayer(layer)
    scenes = {
        '01-inventari': ['registre_icaen', 'tarragones'],
        '02-centres': ['centre_total', 'centre_mitja', 'centre_ponderat', 'centroide', 'icaen_coneguda', 'tarragones'],
        '03-dispersio': ['centre_mitja', 'cercle', 'ellipse', 'icaen_coneguda', 'tarragones'],
        '04-recompte': ['recompte', 'tarragones'],
        '05-kernel': ['densitat-punts-1500', 'tarragones'],
        '06-seccions': ['seccions_resum'],
    }
    extent = boundary.extent(); extent.scale(1.08)
    for name, visible in scenes.items():
        tree = project.layerTreeRoot()
        tree.setHasCustomLayerOrder(True)
        tree.setCustomLayerOrder([layers[key] for key in visible] + [layer for key, layer in layers.items() if key not in visible])
        for key, layer in layers.items(): tree.findLayer(layer.id()).setItemVisibilityChecked(key in visible)
        project.viewSettings().setDefaultViewExtent(__import__('qgis.core', fromlist=['QgsReferencedRectangle']).QgsReferencedRectangle(extent, project.crs()))
        assert project.write(str(OUT / 'projectes' / (name + '.qgz')))
    controls = {'runtime_image': IMAGE, 'qgis': Qgis.QGIS_VERSION, 'gdal': gdal.VersionInfo(),
        'manual_click_by_click': False, 'sources': source_records, 'n_all': 5102, 'n_known': 3762,
        'power_kw': 36633, 'centres': centres, 'centre_shift_m': float(np.linalg.norm(np.array(centres['centre_mitja'])-centres['centre_ponderat'])),
        'covariance': covariance.tolist(), 'dispersion': {k: float(attributes[k]) for k in expressions},
        'field_expressions': expressions, 'grid_extent': list(map(float, grid_extent)),
        'grid_cells': grid.featureCount(), 'grid_points': 3762, 'grid_kw': 36633, 'kernels': kernels,
        'sections': 151, 'section_records': building.featureCount(), 'section_known': building_known.featureCount(),
        'section_kw': section_kw, 'section_indicator_expression': indicator,
        'prepared_cadastral_denominators': True, 'projects': list(scenes), 'operations': operations}
    # All original data remain byte-identical; copied fonts can be remounted readonly.
    for name, (_, expected) in SOURCES.items(): assert sha(OUT / 'fonts' / name) == expected
    dump(OUT / 'controls/calculs.json', controls)
    print(json.dumps({k: v for k, v in controls.items() if k not in ['operations', 'field_expressions']}, ensure_ascii=False, indent=2))


def record(verification=None):
    controls = json.loads((OUT / 'controls/calculs.json').read_text())
    dump(ROOT / 'context/inputs/punts-tarragones.json', controls)
    if verification:
        report = json.loads(Path(verification).read_text()); assert report['ok']
        for path, expected in report['hashes'].items(): assert sha(OUT / path) == expected
        dump(OUT / 'controls/portabilitat.json', report)


def style():
    """Refine native symbology and regenerate projects from these same styles."""
    global _QGIS_APP
    from qgis.core import (QgsApplication, QgsProject, QgsVectorLayer, QgsMarkerSymbol,
        QgsRasterLayer, QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer,
        QgsRuleBasedRenderer, QgsFillSymbol, QgsMapLayerType)
    from qgis.PyQt.QtGui import QColor
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _QGIS_APP = app = QgsApplication([], False); app.initQgis(); initialise()
    centroid = QgsVectorLayer(str(OUT / 'resultats.gpkg')+'|layername=centroide', 'Centroide', 'ogr')
    centroid.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name': 'cross', 'color': '#222222',
        'outline_color': '#222222', 'outline_width': '.6', 'size': '4'}))
    centroid.saveStyleToDatabase('docent', 'Centroide geomètric', True, '')
    section = QgsVectorLayer(str(OUT / 'resultats.gpkg')+'|layername=seccions_resum', 'Seccions', 'ogr')
    if isinstance(section.renderer(), QgsRuleBasedRenderer):
        renderer = section.renderer().clone()
    else: renderer = QgsRuleBasedRenderer.convertFromRenderer(section.renderer())
    if not any(rule.label() == 'Sense indicador' for rule in renderer.rootRule().children()):
        renderer.rootRule().appendChild(QgsRuleBasedRenderer.Rule(QgsFillSymbol.createSimple({
            'color': '#bbbbbb', 'outline_color': '#666666', 'outline_width': '.15'}),
            filterExp='"kw_100ed" IS NULL', label='Sense indicador'))
    section.setRenderer(renderer); section.saveStyleToDatabase('docent', 'Inclou absència de dades', True, '')
    controls = json.loads((OUT / 'controls/calculs.json').read_text())
    for row in controls['kernels']:
        path = OUT / row['path']; layer = QgsRasterLayer(str(path), path.stem)
        maximum = max(r['maximum'] for r in controls['kernels'] if r['weight'] == row['weight'])
        shader = QgsColorRampShader(0, maximum); shader.setColorRampType(QgsColorRampShader.Interpolated)
        shader.setColorRampItemList([QgsColorRampShader.ColorRampItem(maximum*f, QColor(c), f'{maximum*f:.1f}')
            for f, c in [(0, '#fff7ec'), (.05, '#fee8c8'), (.15, '#fdbb84'), (.4, '#e34a33'), (1, '#7f0000')]])
        raster_shader = QgsRasterShader(); raster_shader.setRasterShaderFunction(shader)
        renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, raster_shader)
        renderer.setClassificationMin(0); renderer.setClassificationMax(maximum)
        shader.legendSettings().setUseContinuousLegend(False)
        layer.setRenderer(renderer); layer.saveNamedStyle(str(path.with_suffix('.qml')))
    for name in controls['projects']:
        project = QgsProject(); path = OUT / 'projectes' / (name+'.qgz'); assert project.read(str(path))
        for layer in project.mapLayers().values():
            if layer.type() == QgsMapLayerType.VectorLayer: layer.loadDefaultStyle()
            else: layer.loadNamedStyle(str(Path(layer.source()).with_suffix('.qml')))
        assert project.write(str(path))
    print('Native styles and projects updated.', flush=True)


def finalise():
    """Reopen the owned databases after QGIS exits and check persisted totals."""
    initialise()
    for name in ['dades.gpkg', 'resultats.gpkg']:
        with sqlite3.connect(OUT / name) as db:
            db.execute('PRAGMA wal_checkpoint(TRUNCATE)'); db.execute('PRAGMA journal_mode=DELETE')
            assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    with sqlite3.connect(f'file:{OUT / "resultats.gpkg"}?mode=ro', uri=True) as db:
        totals = db.execute('SELECT COUNT(*), SUM(n_reg), SUM(n_coneguts), SUM(kw_coneguts), SUM(kw_100ed IS NULL) FROM seccions_resum').fetchone()
        assert totals == (151, 5096.0, 3757.0, 36058.0, 1), totals
        assert db.execute('SELECT COUNT(*), SUM(n_punts), SUM(kw_coneguts) FROM recompte').fetchone() == (680, 3762.0, 36633.0)
    path = OUT / 'controls/calculs.json'
    controls = json.loads(path.read_text())
    if controls['section_kw'] != totals[3]:
        incident = OUT / 'controls/calculs-inicial-incidencia.json'
        assert not incident.exists()
        shutil.copyfile(path, incident)
        controls['incident'] = 'The final live iterator returned no rows after project/style writes. Reopened SQLite totals verified; subsequent builds cache the validated features before styling.'
    controls.update(section_kw=totals[3], section_null_indicators=totals[4], sqlite_integrity='ok')
    dump(path, controls)
    print('Persisted GeoPackage totals:', totals)


def verify(directory, report):
    """Run offline with this directory mounted at a different readonly path."""
    global _QGIS_APP
    from qgis.core import QgsApplication, QgsProject, QgsMapLayerType, QgsVectorLayer, QgsRasterLayer
    from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
    from osgeo import gdal
    import numpy as np
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _QGIS_APP = app = QgsApplication([], False); app.initQgis(); directory = Path(directory).resolve()
    gdal.UseExceptions()
    hashes = {str(p.relative_to(directory)): sha(p) for p in directory.rglob('*') if p.suffix in ['.gpkg', '.tif', '.qml', '.qgz']}
    controls = json.loads((directory / 'controls/calculs.json').read_text()); results = []
    for name in controls['projects']:
        project = QgsProject(); assert project.read(str(directory / 'projectes' / (name+'.qgz')))
        assert project.crs().authid() == 'EPSG:25831' and project.ellipsoid() == 'NONE'
        rows = []
        for layer in project.mapLayers().values():
            assert layer.isValid(), (name, layer.name(), layer.source())
            path = Path(layer.source().split('|')[0]).resolve(); assert path.is_relative_to(directory), path
            item = {'name': layer.name(), 'source': str(path.relative_to(directory))}
            if layer.type() == QgsMapLayerType.VectorLayer:
                features = list(layer.getFeatures()); assert features, (name, layer.name())
                assert len(features) == layer.featureCount()
                item['features'] = len(features)
                if 'layername=seccions_resum' in layer.source():
                    assert len(features) == 151 and sum(f['kw_coneguts'] for f in features) == 36058
                if 'layername=recompte' in layer.source():
                    assert len(features) == 680 and sum(f['n_punts'] for f in features) == 3762
            rows.append(item)
        assert len(rows) == 18, len(rows)
        results.append({'project': name, 'layers': rows})
    roi = QgsVectorLayer(str(directory / 'dades.gpkg') + '|layername=registre_icaen|subset="UBICACIO" = \'Edifici\' AND "POT_KW" > 0', 'Scene input', 'ogr')
    assert roi.isValid() and roi.featureCount() == 3757
    assert sum(f['POT_KW'] for f in roi.getFeatures()) == 36058
    calculator_errors = {}
    for record in controls['kernels']:
        ds = gdal.Open(str(directory / record['path'])); values = ds.ReadAsArray()
        assert list(values.shape) == record['shape']
        assert np.allclose(ds.GetGeoTransform(), record['geotransform'], rtol=0, atol=1e-8)
        valid = values != ds.GetRasterBand(1).GetNoDataValue()
        assert abs(float(values[valid].sum(dtype='float64'))*.01-record['integrated_mass']) < 1e-6
        raw_name = record['path'].replace('densitat-', 'kernel-').replace('.tif', '-raw.tif')
        raster = QgsRasterLayer(str(directory / raw_name), 'raw')
        entry = QgsRasterCalculatorEntry(); entry.ref = 'raw@1'; entry.raster = raster; entry.bandNumber = 1
        target = '/tmp/check-'+record['path']
        expression = f'"raw@1" * 3 * 1000000 / (3.141592653589793 * {record["radius_m"]}^2)'
        calculator = QgsRasterCalculator(expression, target, 'GTiff', raster.extent(), raster.crs(),
            raster.width(), raster.height(), [entry], QgsProject.instance().transformContext())
        assert calculator.processCalculation() == 0, calculator.lastError()
        check = gdal.Open(target); actual = check.ReadAsArray()
        assert np.array_equal(actual != check.GetRasterBand(1).GetNoDataValue(), valid)
        assert np.allclose(actual[valid], values[valid], rtol=1e-6, atol=1e-6)
        calculator_errors[record['path']] = float(np.max(np.abs(actual[valid]-values[valid])))
    assert controls['section_kw'] == 36058
    assert all(sha(directory / path) == expected for path, expected in hashes.items())
    dump(report, {'ok': True, 'mounted_at': str(directory), 'offline': True, 'readonly': True,
        'projects': results, 'hashes': hashes, 'scene_subset_features': 3757,
        'native_raster_calculator_max_errors': calculator_errors})
    print('Portable projects verified:', len(results), '; 18 valid layers in each.', flush=True)


def docs():
    """Build standalone handouts with the public, pinned Pandoc/XeLaTeX image."""
    initialise()
    for shot in SHOTS:
        receipt = json.loads((ROOT / 'context/qgis/manifests' / ('punts-'+shot+'.yml')).read_text())
        assert receipt['ok'] and not receipt['warnings'] and receipt['image_digest'] == IMAGE
        assert receipt['capture_id'] == shot and receipt['backend'] == 'x11' and receipt['device_pixel_ratio'] == 1
        for suffix in ['.png', '.annotations.svg']:
            shutil.copyfile(ROOT / 'assets/captures' / ('punts-'+shot+suffix), OUT / 'captures' / ('punts-'+shot+suffix))
        shutil.copyfile(ROOT / 'context/qgis/manifests' / ('punts-'+shot+'.yml'), OUT / 'captures' / ('punts-'+shot+'.yml'))
    for source, target in [('context/practiques/punts-tarragones.md', 'GUIA.md'),
                           ('context/practiques/punts-tarragones-docent.md', 'SOLUCIONS.md')]:
        shutil.copyfile(ROOT / source, OUT / target)
    for relative in ['context/dades/preparar_punts_tarragones.py', 'context/qgis/punts-tarragones.yml',
                     'context/qgis/punts-tarragones.md', 'context/inputs/seccions-resultats.json',
                     'tmp/dades-docents/moodle/manifest.json']:
        shutil.copyfile(ROOT / relative, OUT / 'reproduccio' / Path(relative).name)
    (OUT / 'COMENCA-AQUI.txt').write_text(
        'Distribucions puntuals del Tarragonès — Benito Zaragozí\n\n'
        'Descomprimeix el paquet complet i llegeix GUIA.pdf.\n'
        'Els sis projectes/ permeten consultar les fases; desa els teus resultats a treball/.\n'
        'Les connexions GeoPackage es creen al perfil QGIS seguint la guia.\n'
        'SOLUCIONS.pdf i controls/ contenen els resultats docents.\n'
        'Les seccions inclouen denominadors cadastrals ja agregats.\n'
        'Els preparadors de reproduccio/ esperen el repositori geodisseny, però els exercicis\n'
        'manuals i els projectes funcionen directament amb aquest paquet.\n')
    image = 'ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:9e0b3a45753c170b795e9a9d6df61580085c113436beac5bf6c8de69b6562097'
    for name in ['GUIA', 'SOLUCIONS']:
        command = ['docker', 'run', '--rm', '--pull=never', '--network', 'none',
            '--user', f'{os.getuid()}:{os.getgid()}', '--env', 'HOME=/tmp', '--env', 'SOURCE_DATE_EPOCH=0',
            '--mount', f'type=bind,src={OUT},dst=/data', '--workdir', '/data', '--entrypoint', 'pandoc', image,
            name+'.md', '-o', name+'.pdf', '--pdf-engine=xelatex', '-V', 'fontfamily=fontspec', '-V', 'mainfont=DejaVu Sans',
            '-V', 'monofont=DejaVu Sans Mono', '-V', 'fontsize=11pt', '-V', 'geometry=a4paper,margin=18mm']
        if name == 'GUIA': command += ['--toc', '--toc-depth=2']
        subprocess.run(command, check=True)
    dump(OUT / 'controls/handouts.json', {'image': image, 'engine': 'xelatex', 'SOURCE_DATE_EPOCH': 0})


def package():
    initialise()
    report = json.loads((OUT / 'controls/portabilitat.json').read_text())
    assert report['ok'] and len(report['projects']) == 6
    for path, expected in report['hashes'].items(): assert sha(OUT / path) == expected
    pdfs = json.loads((OUT / 'controls/verificacio-pdf.json').read_text())
    for name in ['GUIA', 'SOLUCIONS']:
        assert not pdfs[name]['overflow'] and sha(OUT / (name+'.pdf')) == pdfs[name]['sha256']
        assert sha(OUT / (name+'.md')) == pdfs[name]['source_sha256']
    for shot in SHOTS:
        for suffix in ['.png', '.annotations.svg']:
            assert sha(ROOT / 'assets/captures' / ('punts-'+shot+suffix)) == sha(OUT / 'captures' / ('punts-'+shot+suffix))
    for p in OUT.rglob('*'):
        assert not p.is_symlink() and not p.name.endswith(('-wal', '-shm')), p
    shutil.copyfile(Path(__file__), OUT / 'reproduccio' / Path(__file__).name)
    files = [{'path': str(p.relative_to(OUT)), 'bytes': p.stat().st_size, 'sha256': sha(p)}
             for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'MANIFEST.json']
    dump(OUT / 'MANIFEST.json', {'files': files, 'runtime_image': IMAGE})
    with zipfile.ZipFile(ZIP, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for file in sorted(OUT.rglob('*')):
            if file.is_file(): archive.write(file, 'punts-tarragones/'+str(file.relative_to(OUT)))
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        for entry in files: assert hashlib.sha256(archive.read('punts-tarragones/'+entry['path'])).hexdigest() == entry['sha256']
    dump(ZIP.with_suffix('.receipt.json'), {'path': str(ZIP.relative_to(ROOT)), 'sha256': sha(ZIP), 'bytes': ZIP.stat().st_size, 'files': len(files)+1})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true'); parser.add_argument('--record', action='store_true')
    parser.add_argument('--finalise', action='store_true'); parser.add_argument('--verify')
    parser.add_argument('--style', action='store_true'); parser.add_argument('--docs', action='store_true')
    parser.add_argument('--report'); parser.add_argument('--package', action='store_true'); args = parser.parse_args()
    if args.build: build()
    if args.finalise: finalise()
    if args.style: style()
    if args.docs: docs()
    if args.verify:
        assert args.report; verify(args.verify, args.report)
    if args.record: record(args.report)
    if args.package: package()
    if _QGIS_APP is not None:
        from qgis.core import QgsProject
        import gc
        QgsProject.instance().clear()
        gc.collect()
        _QGIS_APP.exitQgis()
