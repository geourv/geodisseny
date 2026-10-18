"""Descriptive Constantí pilot: retained municipal inputs and classroom results.

The installed QGIS producer owns execution, native inspection, checkpoints,
captures, resource closure and sealing. This activity chooses layers, checks
their statistics and provides the classroom presentation. --snapshot stages
only verified source files into a new activity run without changing originals.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

# The producer imports this one file as /sources/activity.py. Only the host
# snapshot command has a checkout-relative source location.
ROOT = Path(__file__).resolve().parents[2] if __name__ == '__main__' else None
SLUG = 'estadistica-constanti'
VERSION = '2026-10-12-pilot-01'
ARCHIVE = 'tmp/dades-docents/practica-constanti-pedagogia-20261005.zip'
ARCHIVE_SHA = 'ec2a5e4d1fa580a5633927e6ff642b85fc2d1863911dcce64e721ca8c1681ce2'
INPUTS = {
    'source-municipal': 'constanti.gpkg', 'source-ortofoto': 'ortofoto.tif',
    'source-kernel-500': 'kernel-500-raw.tif', 'source-kernel-1500': 'kernel-1500-raw.tif',
    'source-densitat-500': 'densitat-500.tif', 'source-densitat-1500': 'densitat-1500.tif',
    'source-controls': 'controls.json',
}
INITIAL = ['punts', 'coneguda', 'pesos', 'malla', 'limit']
RESOLVED = ['recompte', 'centres', 'dispersio', 'cercle', 'ellipse']


def compute(context):
    from osgeo import gdal
    from qgis.core import (QgsProject, QgsVectorLayer, QgsVectorFileWriter,
                           QgsRasterLayer, QgsCoordinateReferenceSystem)
    gdal.UseExceptions()
    shutil.copyfile('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', context.output('font-regular'))
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    project.setEllipsoid('NONE')
    for product, names in [('initial-data', INITIAL), ('resolved-data', RESOLVED)]:
        first = True
        for name in names:
            source = QgsVectorLayer(context.input('source-municipal') + '|layername=' + name, name, 'ogr')
            if not source.isValid():
                raise ValueError('Missing retained municipal layer: ' + name)
            # Public Processing records the actual, identity-preserving selection.
            result = context.processing('native:extractbyexpression', {
                'INPUT': source, 'EXPRESSION': '1=1', 'OUTPUT': 'memory:',
            })['OUTPUT']
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName, options.layerName = 'GPKG', name
            options.actionOnExistingFile = (QgsVectorFileWriter.CreateOrOverwriteFile if first
                                           else QgsVectorFileWriter.CreateOrOverwriteLayer)
            saved = QgsVectorFileWriter.writeAsVectorFormatV3(result, context.output(product),
                                                             project.transformContext(), options)
            if saved[0] != QgsVectorFileWriter.NoError:
                raise ValueError(saved)
            first = False
    ds = gdal.Translate(context.output('initial-data'), context.input('source-ortofoto'), format='GPKG',
                        creationOptions=['APPEND_SUBDATASET=YES', 'RASTER_TABLE=ortofoto', 'TILE_FORMAT=PNG'])
    if ds is None:
        raise ValueError('Unable to retain the orthophoto in the initial container')
    ds = None
    for product in ('kernel-500', 'kernel-1500', 'densitat-500', 'densitat-1500'):
        shutil.copyfile(context.input('source-' + product), context.output(product))
    products = {identity: context.output(identity) for identity in
                ('initial-data', 'resolved-data', 'font-regular', 'kernel-500', 'kernel-1500', 'densitat-500', 'densitat-1500')}
    for identity, names, slot in [('initial-data', INITIAL, 'inici'), ('resolved-data', INITIAL + RESOLVED, 'docent')]:
        project.clear()
        project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
        for name in names:
            container = products['initial-data' if name in INITIAL else 'resolved-data']
            layer = QgsVectorLayer(container + '|layername=' + name, name, 'ogr')
            if not layer.isValid():
                raise ValueError('Unable to persist classroom layer: ' + name)
            project.addMapLayer(layer)
        ortho = QgsRasterLayer('GPKG:' + products['initial-data'] + ':ortofoto', 'Ortofoto ICGC 2025')
        if not ortho.isValid():
            raise ValueError('Unable to open the embedded orthophoto')
        project.addMapLayer(ortho)
        if slot == 'docent':
            for product in ('densitat-500', 'densitat-1500'):
                layer = QgsRasterLayer(products[product], product)
                if not layer.isValid():
                    raise ValueError('Invalid retained density raster')
                project.addMapLayer(layer)
        compose(project, slot, context.parameters, products)
        context.embed_project(identity, slot, project)
    project.clear()


def verify(context):
    import numpy as np
    from osgeo import gdal, ogr
    checks = []
    def check(identity, actual, expected, tolerance=0, units='count'):
        checks.append(dict(id=identity, actual=float(actual), expected=float(expected),
                           tolerance=tolerance, units=units))
    controls = json.loads(Path(context.input('source-controls')).read_text())
    initial = ogr.Open(context.output('initial-data'), 0)
    solved = ogr.Open(context.output('resolved-data'), 0)
    if initial is None or solved is None:
        raise ValueError('Unable to reopen prepared GeoPackages')
    points = list(initial.GetLayerByName('punts'))
    xy = np.asarray([(f.GetGeometryRef().GetX(), f.GetGeometryRef().GetY()) for f in points])
    weights = np.asarray([f['w_mid'] for f in points], dtype=float)
    mean, weighted = xy.mean(axis=0), np.average(xy, axis=0, weights=weights)
    check('points-124', len(points), 124)
    known = list(initial.GetLayerByName('coneguda'))
    check('known-98', len(known), 98)
    check('published-kw', sum(f['POT_KW'] for f in known), 2770, units='kW')
    check('scenario-mid-kw', weights.sum(), 2970, units='kW')
    check('mean-coordinates', np.max(np.abs(mean - controls['centres']['all'])), 0, 1e-8, 'm')
    check('weighted-coordinates', np.max(np.abs(weighted - controls['centres']['weighted_mid'])), 0, 1e-8, 'm')
    covariance = np.cov(xy, rowvar=False, ddof=0)
    check('dispersion-radius', np.sqrt(np.trace(covariance)), controls['dispersion']['D_m'], 1e-8, 'm')
    grid = list(solved.GetLayerByName('recompte'))
    check('grid-90', len(grid), 90)
    check('grid-points-total', sum(f['n_punts'] for f in grid), 124)
    check('grid-published-total', sum(f['kw_pub'] for f in grid), 2770, units='kW')
    for name in ('cercle', 'ellipse'):
        feature = solved.GetLayerByName(name).GetNextFeature()
        vertices = np.asarray(json.loads(feature.GetGeometryRef().ExportToJson())['coordinates'][0])[:-1, :2]
        error = (np.max(np.abs(np.linalg.norm(vertices - mean, axis=1) - controls['dispersion']['D_m']))
                 if name == 'cercle' else np.max(np.abs(2 * np.cov(vertices, rowvar=False, ddof=0) - covariance)))
        check('geometry-' + name, error, 0, 1e-5 if name == 'cercle' else .01, 'm' if name == 'cercle' else 'm2')
    for row in controls['kernels']:
        raster = gdal.Open(context.output('densitat-' + str(row['radius'])), gdal.GA_ReadOnly)
        band = raster.GetRasterBand(1)
        values, nodata = band.ReadAsArray(), band.GetNoDataValue()
        mass = values[values != nodata].sum(dtype='float64') * .01
        check('density-mass-' + str(row['radius']), mass, row['mass'], 1e-6, 'records')
    return checks


def compose(project, project_id, parameters, products):
    from qgis.core import (QgsRectangle, QgsReferencedRectangle, QgsTextFormat,
                           QgsMarkerSymbol, QgsFillSymbol, QgsPalLayerSettings,
                           QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QFont
    project.setEllipsoid('NONE')
    project.setTitle('Constantí · ' + ('inici descriptiu' if project_id in ('inici', 'initial-project') else 'resultats descriptius'))
    text = QgsTextFormat()
    text.setFont(QFont('DejaVu Sans'))
    project.styleSettings().setDefaultTextFormat(text)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(
        QgsRectangle(343500, 4554000, 353500, 4563000), project.crs()))
    for layer in project.mapLayers().values():
        name = layer.name()
        if name in ('punts', 'pesos', 'coneguda', 'centres', 'dispersio'):
            layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({
                'name': 'diamond' if name == 'centres' else 'circle',
                'color': '#b42b43' if name == 'centres' else '#00739b',
                'size': '4' if name == 'centres' else '2', 'outline_color': 'white'}))
            if name in ('punts', 'centres'):
                labels = QgsPalLayerSettings()
                labels.fieldName = 'nom' if name == 'centres' else 'llegenda'
                labels.setFormat(text)
                layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
                layer.setLabelsEnabled(True)
        elif name in ('cercle', 'ellipse', 'limit', 'malla', 'recompte'):
            layer.renderer().setSymbol(QgsFillSymbol.createSimple({
                'style': 'no', 'outline_color': '#c46e17' if name == 'cercle' else '#0072b2',
                'outline_width': '.8' if name in ('cercle', 'ellipse') else '.2'}))
        node = project.layerTreeRoot().findLayer(layer.id())
        node.setItemVisibilityChecked(name in ('punts', 'limit', 'centres', 'cercle', 'ellipse', 'Ortofoto ICGC 2025'))
    # The orthophoto is context, never an opaque cover above the results.
    order = {'centres': 0, 'punts': 1, 'cercle': 2, 'ellipse': 3, 'limit': 4,
             'pesos': 5, 'coneguda': 6, 'recompte': 7, 'malla': 8,
             'densitat-500': 20, 'densitat-1500': 21, 'Ortofoto ICGC 2025': 100}
    tree = project.layerTreeRoot()
    tree.setHasCustomLayerOrder(True)
    tree.setCustomLayerOrder(sorted(project.mapLayers().values(), key=lambda layer: order.get(layer.name(), 10)))


def snapshot(run_id):
    run = ROOT / 'sandbox/practiques' / SLUG / run_id
    if run.exists() or run.is_symlink():
        raise FileExistsError('Select a new activity run')
    source = ROOT / ARCHIVE
    if hashlib.file_digest(source.open('rb'), 'sha256').hexdigest() != ARCHIVE_SHA:
        raise ValueError('Retained source archive changed')
    with zipfile.ZipFile(source) as archive:
        sealed = json.loads(archive.read('constanti/sealed.json'))
        records = {row['path']: row for row in sealed['files']}
        selected = dict(INPUTS)
        for image in ('c4-constanti-dades', 'c4-recompte-caixa', 'c4-centres-resultat', 'c4-cercle-ellipse', 'c4-kernel-caixa'):
            selected['capture-' + image] = 'captures/' + image + '.png'
        payloads = {}
        for identity, path in selected.items():
            data = archive.read('constanti/' + path)
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
        target = inputs / Path(path).name
        with target.open('xb') as stream:
            stream.write(data)
        digest = hashlib.sha256(data).hexdigest()
        inventory.append({'id': identity, 'source_member': path, 'path': str(target.relative_to(ROOT)), 'sha256': digest, 'bytes': len(data)})
        if identity in INPUTS:
            request['inputs'].append({'id': identity, 'path': target.name, 'sha256': digest})
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
