"""Prepare a compact student start, retaining separate teacher checkpoints.

Run in the pinned QGIS image. Originals are read-only; every writable artefact
belongs to a new, marked private destination. Existing sealed versions are never
replaced. This source implements the teaching analysis, not a capture renderer.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'sandbox/practiques/accessibilitat-vilaseca/2026-10-14-r5-01'
PACKAGE_STEM = 'accessibilitat-vilaseca'
PRACTICE = Path(__file__).resolve().parent
LANGUAGE = 'ca'
VERSION = '2026-10-14-r5'
DIST = ROOT / 'dist/practiques' / PACKAGE_STEM / VERSION / LANGUAGE
OLD = ROOT / 'tmp/dades-docents/qgis/distancies-vilaseca-20261001-ampliada'
ADM = ROOT / 'tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg'
RTT = ROOT / 'tmp/dades-docents/practiques/rtt-original.gpkg'
IMAGE = 'sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2'
COVER_URL = 'https://datacloud.icgc.cat/datacloud/cobertes-sol/gpkg_unzip/cobertes-sol-v1r0-2024.gpkg'
RTT_URL = 'https://datacloud.icgc.cat/datacloud/topografia-territorial/gpkg_unzip/topografia-territorial-v1r0-2024.gpkg'
DEM_URL = 'https://datacloud.icgc.cat/datacloud/model-elevacions-terreny/tif_unzip/model-elevacions-terreny-lidar-catalunya-5m-2021-2023.tif'
OVERPASS = 'https://overpass-api.de/api/interpreter'
RES = 5
BOUNDS = (343000, 4552000, 346000, 4555200)
OLD_O = (344407.0, 4553668.36)
OLD_D = (344473.01, 4554030.72)
P2_RTT_ID = 1354754
MODULE = None
MODULES = {
    'xarxa': {'slug': 'accessibilitat-xarxa-vilaseca', 'projects': ['00-inici', '02-xarxa'],
              'initial_rasters': [], 'worked_rasters': []},
    'raster': {'slug': 'accessibilitat-raster-vilaseca',
               'projects': ['00-inici', '01-euclidiana', '02-xarxa', '05-friccio-oberta', '06-friccio-tancada', '07-cost'],
               'initial_rasters': [], 'worked_rasters': ['classes', 'base', 'vials', 'pas', 'barrera',
                   'origen_zero', 'origen_null', 'friccio_obert', 'friccio_tancat', 'cost_cella_obert',
                   'cost_cella_tancat', 'direccions_obert', 'direccions_tancat']},
    'temps': {'slug': 'accessibilitat-temps-vilaseca',
              'projects': ['00-inici', '03-servei-obert', '04-servei-tancat', '08-marxa', '09-isocrones-obert', '10-isocrones-tancat'],
              'initial_rasters': ['friccio_obert', 'friccio_tancat'],
              'worked_rasters': ['friccio_obert', 'friccio_tancat', 'friccio_temporal_obert',
                  'friccio_temporal_tancat', 'mdt_ambit', 'mdt_pla'] +
                  ['marxa_' + state + '_' + suffix for state in ['obert_anada', 'obert_tornada',
                      'tancat_anada', 'pla_anada', 'pla_tornada'] for suffix in ['segons', 'direccions', 'minuts']]},
}


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def record(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def initialise():
    marker = OUT / '.owner.json'
    if OUT.exists():
        assert marker.is_file() and json.loads(marker.read_text())['owner'] == Path(__file__).name, OUT
    else:
        OUT.mkdir(parents=True)
        record(marker, {'owner': Path(__file__).name, 'prepared': VERSION})
    assert not (OUT / 'sealed.json').exists(), 'Sealed delivery is immutable.'
    for name in ['fonts', 'controls', 'alumnat', 'docent', 'docent/resultats', 'docent/projectes', 'captures']:
        (OUT / name).mkdir(exist_ok=True)


def setup():
    assert (OUT / '.owner.json').is_file()
    assert json.loads((OUT / '.owner.json').read_text())['owner'] == Path(__file__).name
    assert not (OUT / 'sealed.json').exists(), 'Sealed delivery is immutable.'


def organise():
    """Seed a sandbox run from verified, immutable reconstruction material."""
    import shutil
    previous = ROOT / 'tmp/dades-docents/qgis/accessibilitat-vilaseca-20261007-guies'
    seal = json.loads((previous / 'sealed.json').read_text())
    assert sha(previous / 'MANIFEST.json') == seal['manifest_sha256']
    if OUT.exists():
        setup()
        assert json.loads((OUT / 'controls/reconstruction-source.json').read_text())['manifest_sha256'] == seal['manifest_sha256']
        return
    initialise()
    for directory in ['alumnat', 'docent', 'fonts', 'captures', 'controls']:
        for path in sorted((previous / directory).rglob('*')):
            if not path.is_file() or path.name.startswith(('.', 'failed-stage-', 'initial-before-source-revision-')):
                continue
            if path.suffix == '.pdf' or path.name.endswith(('~', '-wal', '-shm')):
                continue
            target = OUT / path.relative_to(previous)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
            assert sha(path) == sha(target)
    assert sha(OUT / 'alumnat/accessibilitat-vilaseca.gpkg') == '46d326819ad05f328eec12d34026956adcd3bfec9facbefeee226068fee03593'
    record(OUT / 'controls/reconstruction-source.json', {'manifest_sha256': seal['manifest_sha256'],
           'source': str(previous.relative_to(ROOT)), 'revision': 'layout-and-packaging',
           'student_inputs_unchanged': True, 'source_packages': seal['packages']})
    capture_config()
    print('Sandbox run prepared from the sealed, hash-verified practice.', flush=True)


def stage_icgc():
    """Retain only the verified institutional inputs for a fresh calculation."""
    import shutil
    previous = ROOT / 'sandbox/practiques/accessibilitat-vilaseca/2026-10-13-r4-01'
    seal = json.loads((previous / 'sealed.json').read_text())
    assert sha(previous / 'MANIFEST.json') == seal['manifest_sha256']
    assert not OUT.exists(), 'Select a new run; existing activity runs are retained.'
    sources = json.loads((previous / 'fonts/fonts.json').read_text())
    names = ['municipi.gpkg', 'eixos-rtt-2024.gpkg', 'cobertes-2024.gpkg',
             'mdt-5m.tif', 'ortofoto-2025.tif']
    for name in names:
        assert sha(previous / 'fonts' / name) == sources[name]['sha256'], name
    initialise()
    selected = {}
    for name in names:
        target = OUT / 'fonts' / name
        shutil.copyfile(previous / 'fonts' / name, target)
        assert sha(target) == sources[name]['sha256']
        selected[name] = sources[name]
    record(OUT / 'fonts/fonts.json', selected)
    reproduction = OUT / 'reproduccio'
    reproduction.mkdir()
    shutil.copyfile(Path(__file__), reproduction / 'preparar.py')
    record(OUT / 'controls/reconstruction-source.json', {
        'source': str(previous.relative_to(ROOT)), 'manifest_sha256': seal['manifest_sha256'],
        'operation': 'new ICGC network and recalculation', 'network_source': 'ICGC RTT 2024',
        'selected_inputs': {name: selected[name]['sha256'] for name in names},
        'source_outputs_reused': False,
    })
    print('Verified institutional input snapshots staged for a new ICGC calculation.', flush=True)


def reuse_icgc(source_run):
    """Copy this activity's sealed ICGC classroom bytes for a reading revision."""
    import shutil
    import yaml
    previous = (ROOT / 'sandbox/practiques' / PACKAGE_STEM / source_run).resolve()
    assert previous.is_relative_to((ROOT / 'sandbox/practiques' / PACKAGE_STEM).resolve())
    assert not OUT.exists(), 'Select a new run; existing activity runs are retained.'
    seal = json.loads((previous / 'sealed.json').read_text())
    assert sha(previous / 'MANIFEST.json') == seal['manifest_sha256']
    manifest = json.loads((previous / 'MANIFEST.json').read_text())
    assert manifest['runtime'] == IMAGE
    verified = json.loads((previous / 'controls/verificacio-qgis.json').read_text())
    assert verified['ok'] and verified['network_source'] == 'ICGC RTT2024'
    assert verified['network_parts'] == 7945 and verified['closed_route_empty']
    sources = json.loads((previous / 'fonts/fonts.json').read_text())
    retained = {}

    def retain(relative, expected):
        source = (previous / relative).resolve()
        target = OUT / relative
        assert source.is_relative_to(previous) and target.resolve().is_relative_to(OUT.resolve())
        assert sha(source) == expected, relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with source.open('rb') as stream, target.open('xb') as destination:
            shutil.copyfileobj(stream, destination)
        assert sha(target) == expected
        retained[relative] = expected

    # The sealed delivery inventory is the authority for classroom GIS bytes.
    for item in manifest['inventories']['docent']:
        if not item['path'].endswith('.pdf'):
            relative = item['path']
            assert relative.startswith(('alumnat/', 'docent/'))
            assert sha(previous / relative) == item['sha256'], relative
    initialise()
    for relative, digest in verified['checked_hashes'].items():
        assert relative.startswith(('alumnat/', 'docent/'))
        retain(relative, digest)
    assert sha(OUT / 'alumnat/accessibilitat-vilaseca.gpkg') == verified['student_gpkg_sha256']
    for item in manifest['inventories']['docent']:
        if not item['path'].endswith('.pdf'):
            assert retained[item['path']] == item['sha256']
    for name, evidence in sources.items():
        retain('fonts/' + name, evidence['sha256'])
    retain('fonts/fonts.json', sha(previous / 'fonts/fonts.json'))
    for name in ['preparacio.json', 'resultats-inici.json']:
        retain('controls/' + name, sha(previous / 'controls' / name))
    config = yaml.safe_load((ROOT / '_config.yml').read_text())
    readings = config['unaltraweb']['practices']['readings']
    png_hashes = {Path(binding['reference']).name: binding['sha256']
                  for reading in readings if reading['slug'] == PACKAGE_STEM
                  for binding in reading['bindings']}
    recipe = yaml.safe_load((ROOT / 'context/qgis/accessibilitat-inici.yml').read_text())
    for capture in recipe['captures']:
        name = capture['id']
        prefix = 'captures/icgc-final/rendered/' + name
        evidence = json.loads((previous / (prefix + '.manifest.yml')).read_text())
        assert evidence['ok'] and not evidence['warnings'] and evidence['image_digest'] == IMAGE
        retain(prefix + '.png', png_hashes[name + '.png'])
        for suffix in ['.annotations.svg', '.manifest.yml']:
            retain(prefix + suffix, sha(previous / (prefix + suffix)))
    reproduction = OUT / 'reproduccio'
    reproduction.mkdir()
    shutil.copyfile(Path(__file__), reproduction / 'preparar.py')
    record(OUT / 'controls/reconstruction-source.json', {
        'source': str(previous.relative_to(ROOT)), 'manifest_sha256': seal['manifest_sha256'],
        'operation': 'reading revision with unchanged ICGC classroom GIS',
        'network_source': 'ICGC RTT2024', 'student_inputs_unchanged': True,
        'source_outputs_reused': True, 'captures_reused_without_render': True,
        'source_packages': seal['packages'], 'retained_sha256': retained,
    })
    assert sha(previous / 'MANIFEST.json') == seal['manifest_sha256']
    print('Verified ICGC classroom data and captures copied without recalculation.', flush=True)


def capture_config(pass_id=None):
    """Derive confined, create-only capture paths for an owned unsealed run."""
    import yaml
    setup()
    root, out = ROOT.resolve(), OUT.resolve()
    activity_root = (root / 'sandbox/practiques' / PACKAGE_STEM).resolve()
    if not activity_root.is_relative_to(root) or out == activity_root or not out.is_relative_to(activity_root):
        raise ValueError('Capture configuration requires an activity sandbox run.')
    captures = (out / 'captures').resolve()
    staging = captures / pass_id if pass_id else captures
    if pass_id and (Path(pass_id).name != pass_id or not pass_id):
        raise ValueError('Capture pass must be one path component')
    rendered = (staging / 'rendered').resolve()
    if not captures.is_relative_to(out) or not rendered.is_relative_to(captures):
        raise ValueError('Capture output escapes the owned run.')
    if pass_id:
        staging.mkdir()
    target, config_path = staging / 'recipe.yml', staging / 'config.yml'
    if any(path.exists() or path.is_symlink() for path in [target, config_path]):
        raise FileExistsError('Capture recipe/config already exists; select a new run.')
    source = ROOT / 'context/qgis/accessibilitat-inici.yml'
    recipe = yaml.safe_load(source.read_text())
    legacy_prefixes = ['tmp/dades-docents/qgis/accessibilitat-vilaseca-20261006-inici',
                       'tmp/dades-docents/qgis/accessibilitat-vilaseca-20261007-guies']
    prefixes = legacy_prefixes + [Path(prefix).name for prefix in legacy_prefixes]

    def confined_path(value, base, boundary):
        filesystem, separator, options = value.partition('|')
        path = Path(filesystem)
        path = (path if path.is_absolute() else base / path).resolve()
        if not path.is_relative_to(boundary):
            raise ValueError('Capture path escapes its declared base: ' + value)
        return str(path) + (separator + options if separator else '')

    def rewrite(value):
        if isinstance(value, str):
            filesystem, separator, options = value.partition('|')
            for prefix in prefixes:
                if filesystem == prefix or filesystem.startswith(prefix + '/'):
                    relative = filesystem[len(prefix):].lstrip('/')
                    return confined_path(relative + (separator + options if separator else ''), out, out)
            return value
        if isinstance(value, list):
            return [rewrite(item) for item in value]
        if isinstance(value, dict):
            return {key: rewrite(item) for key, item in value.items()}
        return value

    recipe = rewrite(recipe)
    if recipe.get('source_prompt'):
        recipe['source_prompt'] = confined_path(recipe['source_prompt'], root, root)
    destinations = set()
    for capture in recipe['captures']:
        for key in ['path', 'annotations_svg', 'manifest']:
            value = capture.get('output', {}).get(key)
            if not value:
                continue
            old_output = Path(confined_path(value, out, captures))
            new_output = Path(confined_path(str(old_output.relative_to(captures)), rendered, rendered))
            if new_output.exists() or new_output.is_symlink():
                raise FileExistsError('Capture output already exists: ' + str(new_output))
            if new_output in destinations:
                raise ValueError('Duplicate capture output: ' + str(new_output))
            destinations.add(new_output)
            capture['output'][key] = str(new_output)

    def check_paths(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == 'path' and isinstance(item, str):
                    confined_path(item, out, out)
                else:
                    check_paths(item)
        elif isinstance(value, list):
            for item in value:
                check_paths(item)

    check_paths(recipe)
    config = yaml.safe_load((ROOT / '.unaltracaptura-qgis.yml').read_text())
    config['runtime']['default_image'] = IMAGE
    config['plugins'] = ['processing']
    # Inherited input bases stay rooted at the original consumer; output bases
    # belong to this run. Absolute paths are independent of config.yml's parent.
    for key, value in list(config['paths'].items()):
        if key != 'recipes' and isinstance(value, str):
            config['paths'][key] = confined_path(value, root, root)
    config['paths'].update({'recipes': ['recipe.yml'], 'output_root': str(rendered),
                            'cache_root': confined_path('cache', staging, out),
                            'director_plans': confined_path('plans', staging, out),
                            'plays': confined_path('plays', staging, out)})
    with target.open('x', encoding='utf-8') as stream:
        stream.write(yaml.safe_dump(recipe, allow_unicode=True, sort_keys=False))
    with config_path.open('x', encoding='utf-8') as stream:
        stream.write(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))


def reading_name(language=None):
    return {'ca': 'LLEGIU-ME', 'es': 'LEEME', 'en': 'README'}[language or LANGUAGE]


def delivery_name(recipient):
    assert recipient in {'alumnat', 'docent'}
    suffix = '-docent' if recipient == 'docent' else ''
    return f'{PACKAGE_STEM}{suffix}-{VERSION}-{LANGUAGE}.zip'


def fetch():
    from osgeo import gdal, ogr, osr
    setup()
    gdal.UseExceptions()
    ogr.UseExceptions()
    for key, value in {
        'GDAL_DISABLE_READDIR_ON_OPEN': 'EMPTY_DIR', 'GDAL_HTTP_TIMEOUT': '90',
        'GDAL_HTTP_MAX_RETRY': '3', 'CPL_VSIL_CURL_ALLOWED_EXTENSIONS': '.gpkg,.tif',
    }.items():
        gdal.SetConfigOption(key, value)
    manifest_path = OUT / 'fonts/fonts.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    def ready(name):
        path = OUT / 'fonts' / name
        if not path.exists():
            return False
        assert name in manifest and sha(path) == manifest[name]['sha256'], path
        return True

    def kept(name, **info):
        path = OUT / 'fonts' / name
        manifest[name] = {'bytes': path.stat().st_size, 'sha256': sha(path), 'consulta': '2026-10-06', **info}
        record(manifest_path, manifest)

    admin = ogr.Open(str(ADM), 0)
    municipalities = admin.GetLayerByName('_61_municipis-5000')
    municipalities.SetAttributeFilter("NOMMUNI = 'Vila-seca'")
    feature = municipalities.GetNextFeature()
    assert feature is not None and municipalities.GetNextFeature() is None
    municipality = feature.GetGeometryRef().Clone()
    xmin, xmax, ymin, ymax = municipality.GetEnvelope()
    full_bounds = (math.floor((xmin - 500) / 100) * 100, math.floor((ymin - 500) / 100) * 100,
                   math.ceil((xmax + 500) / 100) * 100, math.ceil((ymax + 500) / 100) * 100)
    print('MUNICIPALITY', feature.items(), full_bounds, flush=True)
    if not ready('municipi.gpkg'):
        target = ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT / 'fonts/municipi.gpkg'))
        target.CopyLayer(municipalities, 'municipi')
        target = None
        kept('municipi.gpkg', producer='ICGC', edition='2026-01-20', source=str(ADM.relative_to(ROOT)),
             source_sha256=sha(ADM), municipality=feature.items(), full_bounds=full_bounds,
             url='https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives')

    for name, url, layer_name in [
        ('cobertes-2024.gpkg', COVER_URL, 'cobertes_sol'),
        ('eixos-rtt-2024.gpkg', RTT_URL, '_35_transports_l'),
    ]:
        if ready(name):
            continue
        print('FETCH VECTOR', name, flush=True)
        source = ogr.Open('/vsicurl/' + url, 0)
        layer = source.GetLayerByName(layer_name)
        assert layer is not None
        layer.SetSpatialFilterRect(*full_bounds)
        target = ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT / 'fonts' / name))
        copy = target.CopyLayer(layer, 'original', options=['FID=source_id'])
        count = copy.GetFeatureCount()
        assert count > 0
        fields = [copy.GetLayerDefn().GetFieldDefn(i).GetName() for i in range(copy.GetLayerDefn().GetFieldCount())]
        target = None
        print('RETAINED', name, count, fields, flush=True)
        kept(name, producer='ICGC', edition=2024, url=url, source_layer=layer_name,
             selection_bounds=full_bounds, features=count,
             derivation='Whole source features intersecting the complete municipality plus 500 m; original IDs retained.')
        if name == 'cobertes-2024.gpkg':
            for i in range(source.GetLayerCount()):
                table = source.GetLayerByIndex(i)
                if table.GetName() == layer_name or table.GetGeomType() != ogr.wkbNone:
                    continue
                target = ogr.Open(str(OUT / 'fonts' / name), 1)
                target.CopyLayer(table, table.GetName())
                target = None
            kept(name, producer='ICGC', edition=2024, url=url, source_layer=layer_name,
                 selection_bounds=full_bounds, features=count, fields=fields,
                 derivation='Whole source polygons and legend tables; original feature IDs retained.')
        source = None

    if not ready('mdt-5m.tif'):
        print('FETCH MDT', flush=True)
        image = gdal.Translate(str(OUT / 'fonts/mdt-5m.tif'), '/vsicurl/' + DEM_URL,
                               format='GTiff', projWin=[full_bounds[0], full_bounds[3], full_bounds[2], full_bounds[1]],
                               xRes=RES, yRes=RES, resampleAlg='nearest',
                               creationOptions=['COMPRESS=DEFLATE', 'TILED=YES'])
        assert image is not None
        image = None
        kept('mdt-5m.tif', producer='ICGC', edition='LiDAR 2021-2023', url=DEM_URL,
             resolution_m=RES, bounds=full_bounds, derivation='Native 5 m crop, no finer invented resolution.')

    if not ready('ortofoto-2025.tif'):
        x0, y0, x1, y1 = BOUNDS
        params = {'SERVICE': 'WMS', 'VERSION': '1.3.0', 'REQUEST': 'GetMap',
                  'LAYERS': 'ortofoto_25cm_color_2025', 'STYLES': '', 'CRS': 'EPSG:25831',
                  'BBOX': ','.join(map(str, BOUNDS)), 'WIDTH': (x1 - x0) // 2, 'HEIGHT': (y1 - y0) // 2,
                  'FORMAT': 'image/png'}
        url = 'https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?' + urlencode(params)
        print('FETCH ORTHOPHOTO', flush=True)
        with urllib.request.urlopen(url, timeout=180) as response:
            content = response.read(20_000_001)
        assert len(content) <= 20_000_000 and content.startswith(b'\x89PNG\r\n\x1a\n')
        gdal.FileFromMemBuffer('/vsimem/accessibilitat-orto.png', content)
        image = gdal.Translate(str(OUT / 'fonts/ortofoto-2025.tif'), '/vsimem/accessibilitat-orto.png',
                               format='GTiff', outputSRS='EPSG:25831', outputBounds=[x0, y1, x1, y0],
                               creationOptions=['COMPRESS=DEFLATE', 'TILED=YES'])
        image = None
        gdal.Unlink('/vsimem/accessibilitat-orto.png')
        kept('ortofoto-2025.tif', producer='ICGC', edition=2025, url=url, bounds=BOUNDS,
             resolution_m=2, derivation='25 cm source WMS rendered at 2 m for contextual reading.')
    print(json.dumps(manifest, ensure_ascii=False, indent=2), flush=True)


def qgis_session():
    import sys
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsProcessingContext
    app = QgsApplication([], False)
    app.initQgis()
    sys.path.insert(0, '/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    project.setEllipsoid('NONE')
    context = QgsProcessingContext()
    context.setProject(project)
    return app, project, context


def icgc_network(full_bounds, municipality):
    """Prepare a traceable graph from RTT axes, without noding visual crossings."""
    import networkx as nx
    import numpy as np
    import shapely
    from shapely.geometry import LineString, Point, box
    from shapely.ops import substring
    from osgeo import ogr
    allowed = {'vca', 'vnc', 'vcu', 'vpu', 'vpd', 'vcd', 'cor', 'bir', 'bin'}
    clip = box(*full_bounds)
    source = ogr.Open(str(OUT / 'fonts/eixos-rtt-2024.gpkg'), 0)
    candidates, excluded = [], []
    for feature in source.GetLayerByName('original'):
        attributes = feature.items()
        if attributes['tipus'] not in allowed or attributes['estat'] != 'gen':
            excluded.append({'rtt_id': feature.GetFID(), 'tipus': attributes['tipus'],
                             'estat': attributes['estat']})
            continue
        geometry = shapely.force_2d(shapely.from_wkb(bytes(feature.GetGeometryRef().ExportToWkb()))).intersection(clip)
        for part in shapely.get_parts(geometry):
            if part.geom_type == 'LineString' and part.length > .001:
                candidates.append((part, dict(attributes, rtt_id=feature.GetFID())))
    assert candidates
    geometries = [line for line, attributes in candidates]
    tree = shapely.STRtree(geometries)
    cuts = {i: [] for i in range(len(candidates))}
    junctions = []
    for i, (line, attributes) in enumerate(candidates):
        if attributes['terreny'] != 'gen':
            continue
        for xy in (line.coords[0], line.coords[-1]):
            point = Point(xy)
            for j in tree.query(point.buffer(.005)):
                j = int(j)
                other, other_attributes = candidates[j]
                if i == j or other_attributes['terreny'] != 'gen':
                    continue
                position = other.project(point)
                if .005 < position < other.length - .005 and point.distance(other) <= .005:
                    cuts[j].append(position)
                    junctions.append({'endpoint_axis': attributes['rtt_id'],
                                      'split_axis': other_attributes['rtt_id'],
                                      'xy': list(xy), 'distance_m': point.distance(other)})
    # Use the same physical endpoints as the ICGC demonstration. Splitting at
    # these points is explicit; selecting arbitrary nearest graph nodes is not.
    for coordinates in (OLD_O, OLD_D):
        point = Point(coordinates)
        matches = []
        for i in tree.query(point.buffer(.005)):
            i = int(i)
            line = geometries[i]
            if point.distance(line) <= .005:
                cuts[i].append(line.project(point))
                matches.append(candidates[i][1]['rtt_id'])
        assert matches, ('Declared ICGC endpoint is not on an admitted axis', coordinates)
    rows, graph = [], nx.MultiGraph()
    for i, (line, attributes) in enumerate(candidates):
        positions = [0, *sorted(set(cuts[i])), line.length]
        for first, last in zip(positions, positions[1:]):
            if last - first <= .001:
                continue
            part = substring(line, first, last)
            part = LineString(np.round(shapely.get_coordinates(part), 3))
            if part.length <= .001:
                continue
            a, b = tuple(part.coords[0]), tuple(part.coords[-1])
            identity = len(rows) + 1
            row = dict(attributes, part_id=identity, node_a=','.join(map(str, a)),
                       node_b=','.join(map(str, b)), v_kmh=5.,
                       dins_muni=int(part.intersects(municipality)))
            rows.append((part, row))
            graph.add_edge(a, b, key=identity, weight=part.length)
    assert OLD_O in graph and OLD_D in graph, 'Declared endpoints changed during preparation'
    assert nx.has_path(graph, OLD_O, OLD_D), 'Inspect the disconnected ICGC network; do not enlarge tolerance blindly'
    components = sorted(nx.connected_components(graph), key=len, reverse=True)
    information = {'source': 'ICGC RTT 2024', 'source_layer': '_35_transports_l',
                   'allowed_types': sorted(allowed), 'excluded_axes': excluded,
                   'junctions': junctions, 'junction_tolerance_m': .005,
                   'coordinate_rounding_m': .001, 'origin': OLD_O, 'destination': OLD_D,
                   'opened_network_m': nx.shortest_path_length(graph, OLD_O, OLD_D, weight='weight'),
                   'component_sizes': [len(component) for component in components],
                   'walking_model': 'Admitted non-motorway axes, both directions, uniform5km/h; no legal access certification'}
    return rows, graph, information


def prepare():
    """Prepare only inputs; verify the municipal coverage and routing graph."""
    import networkx as nx
    import numpy as np
    import shapely
    from shapely.geometry import Point, LineString, Polygon, box
    from shapely.ops import nearest_points
    from osgeo import gdal, ogr, osr
    setup()
    gdal.UseExceptions()
    ogr.UseExceptions()
    full_bounds = json.loads((OUT / 'fonts/fonts.json').read_text())['municipi.gpkg']['full_bounds']
    reference = osr.SpatialReference()
    reference.ImportFromEPSG(25831)
    municipality_source = ogr.Open(str(OUT / 'fonts/municipi.gpkg'), 0)
    municipality_feature = next(iter(municipality_source.GetLayerByName('municipi')))
    municipality = shapely.from_wkb(bytes(municipality_feature.GetGeometryRef().ExportToWkb()))
    clip = box(*full_bounds)
    stage = OUT / 'alumnat/.initial-stage.gpkg'
    assert not stage.exists(), 'Inspect the retained partial stage before another attempt.'
    db = ogr.GetDriverByName('GPKG').CreateDataSource(str(stage))

    def vector(name, kind, fields, rows):
        layer = db.CreateLayer(name, reference, kind, options=['SPATIAL_INDEX=YES'])
        for field, datatype in fields:
            layer.CreateField(ogr.FieldDefn(field, datatype))
        layer.StartTransaction()
        for geometry, attributes in rows:
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetGeometry(ogr.CreateGeometryFromWkb(shapely.force_2d(geometry).wkb))
            for key, value in attributes.items():
                if value is not None:
                    feature.SetField(key, value)
            layer.CreateFeature(feature)
        layer.CommitTransaction()
        return layer.GetFeatureCount()

    vector('municipi', ogr.wkbMultiPolygon, [('nom', ogr.OFTString), ('codi', ogr.OFTString)],
           [(municipality, {'nom': 'Vila-seca', 'codi': '431711'})])
    vector('ambit_calcul', ogr.wkbPolygon, [('nom', ogr.OFTString), ('cella_m', ogr.OFTInteger)],
           [(box(*BOUNDS), {'nom': 'Àmbit de comparació O/D i passos', 'cella_m': RES})])
    source = ogr.Open(str(OUT / 'fonts/cobertes-2024.gpkg'), 0)
    categories = {f['nivell_2']: f['categoria'] for f in source.GetLayerByName('cobertes_sol_categories')}
    costs = {code: 4 for code in categories}
    costs.update({351: 1, 346: 2, 228: 2, 230: 2, 352: 2, 348: 2, 233: 3,
                  221: 6, 222: 6, 223: 6, 224: 6, 225: 6, 226: 6, 227: 6,
                  229: 6, 234: 99, 344: 6, 347: 6, 349: 99, 354: 99, 355: 99,
                  461: 99, 462: 99, 463: 99, 464: 99, 465: 99, 466: 99})
    covers = []
    industrial = []
    for feature in source.GetLayerByName('original'):
        geometry = shapely.force_2d(shapely.from_wkb(bytes(feature.GetGeometryRef().ExportToWkb())))
        if not geometry.is_valid:
            geometry = shapely.make_valid(geometry)
        geometry = geometry.intersection(clip)
        polygons = [part for part in shapely.get_parts(geometry) if part.geom_type in ['Polygon', 'MultiPolygon']]
        geometry = shapely.union_all(polygons)
        if geometry.is_empty:
            continue
        if geometry.geom_type == 'Polygon':
            geometry = shapely.MultiPolygon([geometry])
        code = feature['nivell_2']
        attributes = {'source_id': feature.GetFID(), 'classe': code, 'categoria': categories[code],
                      'data_font': feature['data_font'], 'cost_model': costs[code]}
        covers.append((geometry, attributes))
        if code == 347 and geometry.intersects(municipality):
            industrial.append({'source_id': feature.GetFID(), 'area_municipal_m2': geometry.intersection(municipality).area})
    coverage = shapely.union_all([geometry for geometry, attributes in covers])
    gap = municipality.difference(coverage)
    assert gap.area / municipality.area < .002, 'Inspect the unexpected municipal coverage gap.'
    print('COVERAGE GAP', gap.area, gap.area / municipality.area, flush=True)
    # Boundaries and the dated cover layer have small cartographic differences.
    # Preserve these as unknown coverage, never manufacture a land-cover class.
    if gap.geom_type == 'Polygon':
        gap = shapely.MultiPolygon([gap])
    vector('cobertura_sense_dades', ogr.wkbMultiPolygon, [('nom', ogr.OFTString)],
           [(gap, {'nom': 'Diferència de cobertura municipal/cobertes; conservar NoData'})])
    cover_count = vector('cobertes', ogr.wkbMultiPolygon,
                        [('source_id', ogr.OFTInteger64), ('classe', ogr.OFTInteger), ('categoria', ogr.OFTString),
                         ('data_font', ogr.OFTString), ('cost_model', ogr.OFTInteger)], covers)
    legend = db.CreateLayer('llegenda_costos', geom_type=ogr.wkbNone)
    for field, datatype in [('classe', ogr.OFTInteger), ('categoria', ogr.OFTString), ('cost_model', ogr.OFTInteger)]:
        legend.CreateField(ogr.FieldDefn(field, datatype))
    for code, label in categories.items():
        feature = ogr.Feature(legend.GetLayerDefn())
        feature['classe'], feature['categoria'], feature['cost_model'] = code, label, costs[code]
        legend.CreateFeature(feature)

    rows, graph, network_info = icgc_network(full_bounds, municipality)
    origin, destination = network_info['origin'], network_info['destination']
    opened_length = network_info['opened_network_m']
    network_count = vector('xarxa', ogr.wkbLineString,
                           [('rtt_id', ogr.OFTInteger64), ('part_id', ogr.OFTInteger),
                            ('node_a', ogr.OFTString), ('node_b', ogr.OFTString),
                            ('tipus', ogr.OFTString), ('nom', ogr.OFTString), ('codivia', ogr.OFTString), ('v_kmh', ogr.OFTReal),
                            ('entorn', ogr.OFTString), ('estat', ogr.OFTString), ('terreny', ogr.OFTString),
                            ('xarxa', ogr.OFTString), ('dins_muni', ogr.OFTInteger)], rows)
    vector('origen', ogr.wkbPoint, [('nom', ogr.OFTString)], [(Point(origin), {'nom': 'O · Origen'})])
    vector('desti', ogr.wkbPoint, [('nom', ogr.OFTString)], [(Point(destination), {'nom': 'D · Destí'})])

    # Explicit polygons retained from the geometrically documented crossing
    # model. Widths/extensions are declared teaching choices, not road surveys.
    passes = []
    for filename, layername in [('pas-p2.gpkg', 'pas-p2'), ('altres-passos.gpkg', 'altres-passos')]:
        source = ogr.Open(str(OLD / 'dades' / filename), 0)
        for feature in source.GetLayerByName(layername):
            geometry = shapely.force_2d(shapely.from_wkb(bytes(feature.GetGeometryRef().ExportToWkb())))
            code = 2 if filename.startswith('pas-p2') else 1
            passes.append((geometry, {'pas_id': code, 'nom': 'P2 · pas principal' if code == 2 else 'P1 · pas alternatiu',
                                     'obert': 1, 'font': 'Corredor sobre eix RTT; amplada modelada20m, prolongació40m'}))
    vector('passos', ogr.wkbMultiPolygon,
           [('pas_id', ogr.OFTInteger), ('nom', ogr.OFTString), ('obert', ogr.OFTInteger), ('font', ogr.OFTString)], passes)
    principal = shapely.union_all([geometry for geometry, attributes in passes if attributes['pas_id'] == 2])
    closed_graph = graph.copy()
    removed = []
    for geometry, attributes in rows:
        if attributes['rtt_id'] == P2_RTT_ID:
            a, b = tuple(geometry.coords[0]), tuple(geometry.coords[-1])
            if closed_graph.has_edge(a, b, attributes['part_id']):
                closed_graph.remove_edge(a, b, attributes['part_id'])
                removed.append({'part_id': attributes['part_id'], 'rtt_id': attributes['rtt_id']})
    assert removed, 'The declared ICGC crossing is absent from the prepared network'
    closed_length = None
    if nx.has_path(closed_graph, origin, destination):
        closed_length = nx.shortest_path_length(closed_graph, origin, destination, weight='weight')
    source = ogr.Open(str(OUT / 'fonts/eixos-rtt-2024.gpkg'), 0)
    source.GetLayerByName('original').SetAttributeFilter("codivia = 'AP-7'")
    motorway = [shapely.force_2d(shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb()))) for f in source.GetLayerByName('original')]
    vector('autopista_eixos', ogr.wkbLineString, [('nom', ogr.OFTString)],
           [(geometry, {'nom': 'AP-7 · eix RTT'}) for geometry in motorway])
    band = shapely.union_all(motorway).buffer(35).intersection(box(*BOUNDS))
    road_cover = shapely.union_all([geometry for geometry, attributes in covers if attributes['classe'] == 351])
    barrier = band.intersection(road_cover)
    if barrier.geom_type == 'Polygon':
        barrier = shapely.MultiPolygon([barrier])
    db = None
    # Raster tables use the standard gridded-coverage extension; exact float
    # samples are checked after the append instead of using an RGB hillshade.
    for name, filename, options in [('mdt', 'mdt-5m.tif', ['TILE_FORMAT=TIFF']),
                                     ('ortofoto', 'ortofoto-2025.tif', ['TILE_FORMAT=PNG'])]:
        image = gdal.Translate(str(stage), str(OUT / 'fonts' / filename), format='GPKG',
                               creationOptions=['APPEND_SUBDATASET=YES', 'RASTER_TABLE=' + name, *options])
        assert image is not None
        image = None
    original_dem = gdal.Open(str(OUT / 'fonts/mdt-5m.tif'))
    embedded_dem = gdal.Open(f'GPKG:{stage}:mdt')
    assert embedded_dem.GetGeoTransform() == original_dem.GetGeoTransform()
    assert np.array_equal(embedded_dem.ReadAsArray(), original_dem.ReadAsArray())
    embedded_dem = original_dem = None
    final = OUT / 'alumnat/accessibilitat-vilaseca.gpkg'
    assert not final.exists()
    stage.rename(final)
    summary = {'bounds': BOUNDS, 'full_bounds': full_bounds, 'crs': 'EPSG:25831', 'resolution_m': RES,
               'origin': origin, 'destination': destination, 'original_endpoints': [OLD_O, OLD_D],
               'endpoint_shift_m': [math.dist(origin, OLD_O), math.dist(destination, OLD_D)],
               'network_source': 'ICGC RTT 2024', 'network_preparation': network_info,
               'network_parts': network_count, 'network_components': network_info['component_sizes'],
               'opened_network_m': opened_length, 'closed_network_m': closed_length, 'closed_edges': removed,
               'cover_polygons': cover_count,
               'municipal_cover_gap_m2': municipality.difference(coverage).area,
               'industrial_polygons_in_municipality': industrial, 'costs': costs,
               'student_gpkg_sha256_before_project': sha(final), 'embedded_dem_exact': True}
    record(OUT / 'controls/preparacio.json', summary)
    print(json.dumps({key: summary[key] for key in ['origin', 'destination', 'endpoint_shift_m', 'network_parts',
                                                  'opened_network_m', 'closed_network_m', 'cover_polygons',
                                                  'municipal_cover_gap_m2', 'embedded_dem_exact']}, indent=2), flush=True)


def style_start():
    from qgis.core import (QgsVectorLayer, QgsRasterLayer, QgsLineSymbol, QgsFillSymbol, QgsMarkerSymbol,
                          QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsPalLayerSettings, QgsTextFormat,
                          QgsTextBufferSettings, QgsVectorLayerSimpleLabeling, QgsRectangle, QgsReferencedRectangle, Qgis)
    from qgis.PyQt.QtGui import QColor, QFont
    setup()
    app, project, context = qgis_session()
    gpkg = OUT / 'alumnat/accessibilitat-vilaseca.gpkg'
    project.clear()
    from qgis.core import QgsCoordinateReferenceSystem
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    project.setEllipsoid('NONE')
    project.setTitle('Accessibilitat de Vila-seca · dades d’inici')
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    ortho = QgsRasterLayer(f'GPKG:{gpkg}:ortofoto', 'Ortofoto ICGC2025 · context2m')
    dem = QgsRasterLayer(f'GPKG:{gpkg}:mdt', 'MDT ICGC · altitud5m')
    assert ortho.isValid() and dem.isValid()
    project.addMapLayer(ortho)
    project.addMapLayer(dem)
    project.layerTreeRoot().findLayer(dem.id()).setItemVisibilityChecked(False)
    definitions = [
        ('municipi', 'Límit municipal de Vila-seca', 'polygon', '#475d70', False),
        ('cobertes', 'Cobertes del sòl2024 · classes', 'covers', '#6d9768', False),
        ('cobertura_sense_dades', 'Cobertura desconeguda · conservar NoData', 'polygon', '#ad6549', False),
        ('ambit_calcul', 'Àmbit de càlcul · cel·la5m', 'polygon', '#69757d', False),
        ('xarxa', 'Xarxa a peu · ICGC RTT 2024', 'line', '#69757d', True),
        ('autopista_eixos', 'AP-7 · eixos de referència', 'line', '#8a665a', False),
        ('passos', 'P2 principal i passos alternatius', 'passes', '#9e468c', True),
        ('origen', 'Origen O', 'point', '#00866f', True),
        ('desti', 'Destí D', 'point', '#ba3545', True),
    ]
    for table, name, kind, colour, visible in definitions:
        layer = QgsVectorLayer(str(gpkg) + '|layername=' + table, name, 'ogr')
        assert layer.isValid(), table
        if kind == 'line':
            layer.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color': colour, 'line_width': '.35'}))
        elif kind == 'point':
            layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name': 'circle' if table == 'origen' else 'diamond',
                                                                   'size': '4.5', 'color': colour,
                                                                   'outline_color': 'white', 'outline_width': '.6'}))
            labels = QgsPalLayerSettings()
            labels.fieldName = 'nom'
            text = QgsTextFormat()
            text.setFont(QFont('DejaVu Sans', 12))
            text.setSize(12)
            text.setColor(QColor('#202020'))
            halo = QgsTextBufferSettings()
            halo.setEnabled(True)
            halo.setColor(QColor('white'))
            halo.setSize(1.)
            text.setBuffer(halo)
            labels.setFormat(text)
            layer.setLabeling(QgsVectorLayerSimpleLabeling(labels))
            layer.setLabelsEnabled(True)
        elif kind == 'covers':
            categories = []
            for code in sorted({f['classe'] for f in layer.getFeatures()}):
                c = '#b6c89d' if code < 300 else '#d8c2b4'
                if code == 351:
                    c = '#fff3cf'
                if code >= 460:
                    c = '#95c6d9'
                symbol = QgsFillSymbol.createSimple({'color': c, 'outline_style': 'no'})
                categories.append(QgsRendererCategory(code, symbol, str(code)))
            layer.setRenderer(QgsCategorizedSymbolRenderer('classe', categories))
        else:
            layer.renderer().setSymbol(QgsFillSymbol.createSimple({'color': '255,255,255,0',
                                                                 'outline_color': colour, 'outline_width': '.6'}))
        project.addMapLayer(layer)
        project.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(visible)
        error = layer.saveStyleToDatabase('inici', 'Estil inicial de la pràctica; font i model documentats', True, '')
        assert not error, error
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*BOUNDS), project.crs()))
    uri = 'geopackage:' + str(gpkg) + '?projectName=inici'
    assert project.write(uri), uri
    project.clear()
    assert project.read(uri)
    assert all(layer.isValid() for layer in project.mapLayers().values())
    report = {'uri': uri, 'project': 'inici', 'layers': len(project.mapLayers()),
              'datasources': [layer.source() for layer in project.mapLayers().values()],
              'student_gpkg_sha256': sha(gpkg)}
    record(OUT / 'controls/projecte-inici.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


def build():
    """Execute the complete student chain with explicit layers and controls."""
    import heapq
    import numpy as np
    import shapely
    from osgeo import gdal
    from qgis.core import (QgsApplication, QgsVectorLayer, QgsRasterLayer, QgsVectorFileWriter,
                          QgsRectangle, QgsProcessingFeedback, QgsProcessingException)
    from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
    setup()
    app, project, context = qgis_session()
    import processing
    gpkg = OUT / 'alumnat/accessibilitat-vilaseca.gpkg'
    before = sha(gpkg)
    input_info = json.loads((OUT / 'controls/preparacio.json').read_text())
    origin, destination = input_info['origin'], input_info['destination']
    result_dir = OUT / 'docent/resultats'
    extent = f'{BOUNDS[0]},{BOUNDS[2]},{BOUNDS[1]},{BOUNDS[3]} [EPSG:25831]'
    width, height = (BOUNDS[2] - BOUNDS[0]) // RES, (BOUNDS[3] - BOUNDS[1]) // RES
    controls = {'origin': origin, 'destination': destination, 'bounds': BOUNDS, 'resolution_m': RES,
                'crs': 'EPSG:25831', 'network': {}, 'service': {}, 'cost': {}, 'walk': {}, 'expressions': {}}
    definitions = {}

    class Feedback(QgsProcessingFeedback):
        def __init__(self):
            super().__init__()
            self.messages = []
        def reportError(self, message, fatalError=False):
            self.messages.append(message)
        def pushConsoleInfo(self, message):
            self.messages.append(message)
        def pushCommandInfo(self, message):
            self.messages.append(message)

    def run(identifier, params):
        algorithm = QgsApplication.processingRegistry().algorithmById(identifier)
        assert algorithm is not None, identifier
        if identifier not in definitions:
            definitions[identifier] = [{
                'name': p.name(), 'description': p.description(), 'default': str(p.defaultValue()),
                'options': p.options() if hasattr(p, 'options') else None,
            } for p in algorithm.parameterDefinitions()]
            record(OUT / 'controls/algorismes-inici.json', definitions)
        feedback = Feedback()
        print('PROCESS', identifier, flush=True)
        try:
            return processing.run(identifier, params, context=context, feedback=feedback)
        finally:
            with (OUT / 'controls/processing-inici.log').open('a') as stream:
                stream.write(identifier + '\n' + '\n'.join(feedback.messages) + '\n')

    def layer(name):
        result = QgsVectorLayer(str(gpkg) + '|layername=' + name, name, 'ogr')
        assert result.isValid(), name
        return result

    vector_result = OUT / 'docent/resultats.gpkg'
    def save(value, name):
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = 'GPKG'
        options.layerName = name
        options.actionOnExistingFile = (QgsVectorFileWriter.CreateOrOverwriteLayer if vector_result.exists()
                                       else QgsVectorFileWriter.CreateOrOverwriteFile)
        status = QgsVectorFileWriter.writeAsVectorFormatV3(value, str(vector_result), project.transformContext(), options)
        assert status[0] == QgsVectorFileWriter.NoError, status
        return str(vector_result) + '|layername=' + name

    def calc(expression, inputs, name):
        entries = []
        raster_layers = []
        for reference, path in inputs.items():
            raster = QgsRasterLayer(str(path), reference)
            assert raster.isValid(), path
            raster_layers.append(raster)
            entry = QgsRasterCalculatorEntry()
            entry.ref, entry.raster, entry.bandNumber = reference + '@1', raster, 1
            entries.append(entry)
        path = result_dir / (name + '.tif')
        calculator = QgsRasterCalculator(expression, str(path), 'GTiff', QgsRectangle(*BOUNDS),
                                         width, height, entries, project.transformContext())
        assert calculator.processCalculation() == QgsRasterCalculator.Success, calculator.lastError()
        controls['expressions'][name] = expression
        return str(path)

    def rasterize(value, name, field=None, burn=1, datatype=5):
        return run('gdal:rasterize', {'INPUT': value, 'FIELD': field, 'BURN': burn,
                   'UNITS': 1, 'WIDTH': RES, 'HEIGHT': RES, 'EXTENT': extent,
                   'INIT': 0, 'NODATA': -9999, 'DATA_TYPE': datatype,
                   'OUTPUT': str(result_dir / (name + '.tif'))})['OUTPUT']

    origins, destinations, network, covers, passes = [layer(name) for name in ['origen', 'desti', 'xarxa', 'cobertes', 'passos']]
    straight = run('native:shortestline', {'SOURCE': origins, 'DESTINATION': destinations,
                                        'METHOD': 0, 'NEIGHBORS': 1, 'OUTPUT': 'memory:'})['OUTPUT']
    save(straight, 'euclidiana_vector')
    controls['euclidean_vector_m'] = next(straight.getFeatures()).geometry().length()
    assert abs(controls['euclidean_vector_m'] - math.dist(origin, destination)) < 1e-7
    origin_zero = rasterize(origins, 'origen_zero')
    origin_null = str(result_dir / 'origen_null.tif')
    image = gdal.Translate(origin_null, origin_zero, noData=0)
    image = None
    grass_distance = run('grass:r.grow.distance', {
        'input': origin_null, 'metric': 0, '-m': False,
        'distance': str(result_dir / 'distancia_grass.tif'), 'value': 'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': RES,
    })['distance']
    gdal_distance = run('gdal:proximity', {'INPUT': origin_zero, 'BAND': 1, 'VALUES': '1', 'UNITS': 0,
                           'DATA_TYPE': 5, 'NODATA': -9999, 'OUTPUT': str(result_dir / 'distancia_gdal.tif')})['OUTPUT']
    def cell(point):
        return int((BOUNDS[3] - point[1]) / RES), int((point[0] - BOUNDS[0]) / RES)
    o, d = cell(origin), cell(destination)
    def read(path):
        image = gdal.Open(str(path))
        assert image.GetGeoTransform() == (BOUNDS[0], RES, 0., BOUNDS[3], 0., -RES), path
        values = image.ReadAsArray().astype(float)
        nodata = image.GetRasterBand(1).GetNoDataValue()
        values[~np.isfinite(values) | (values == nodata)] = np.nan
        return values
    grass_array, gdal_array = read(grass_distance), read(gdal_distance)
    expected = math.dist((o[0], o[1]), (d[0], d[1])) * RES
    assert abs(grass_array[d] - expected) < .001 and abs(gdal_array[d] - expected) < .001
    assert np.nanmax(np.abs(grass_array - gdal_array)) < .002
    controls['euclidean_raster_m'] = float(grass_array[d])
    controls['grass_gdal_max_difference_m'] = float(np.nanmax(np.abs(grass_array - gdal_array)))

    principal = run('native:extractbyattribute', {'INPUT': passes, 'FIELD': 'pas_id', 'OPERATOR': 0,
                                               'VALUE': 2, 'OUTPUT': 'memory:'})['OUTPUT']
    # The RTT bridge is an identified axis. Removing every long cartographic
    # axis touching the raster corridor would also delete the approach to O.
    closed = run('native:extractbyattribute', {'INPUT': network, 'FIELD': 'rtt_id', 'OPERATOR': 1,
                                             'VALUE': P2_RTT_ID, 'OUTPUT': 'memory:'})['OUTPUT']
    controls['closed_rtt_axis'] = P2_RTT_ID
    closed_uri = save(closed, 'xarxa_tancada')
    common = {'START_POINT': f'{origin[0]},{origin[1]} [EPSG:25831]',
              'END_POINT': f'{destination[0]},{destination[1]} [EPSG:25831]',
              'DEFAULT_DIRECTION': 2, 'SPEED_FIELD': 'v_kmh', 'DEFAULT_SPEED': 5,
              'TOLERANCE': 0, 'POINT_TOLERANCE': .1, 'OUTPUT': 'memory:'}
    for state, value in [('obert', network), ('tancat', closed)]:
        reference = input_info['opened_network_m' if state == 'obert' else 'closed_network_m']
        try:
            route = run('native:shortestpathpointtopoint', {**common, 'INPUT': value, 'STRATEGY': 0})['OUTPUT']
        except QgsProcessingException as error:
            assert state == 'tancat' and reference is None and 'no route' in str(error).lower(), error
            route = QgsVectorLayer('LineString?crs=EPSG:25831', 'Sense ruta', 'memory')
            controls['network'][state] = {'reachable': False, 'length_m': None,
                                          'time_min': None, 'message': str(error)}
        else:
            length = next(route.getFeatures()).geometry().length()
            assert reference is not None and abs(length - reference) < .02, (state, length, reference)
            controls['network'][state] = {'reachable': True, 'length_m': length, 'time_min': length / 5000 * 60}
        save(route, 'ruta_' + state)
        controls['service'][state] = {}
        for minutes in [3, 6, 12]:
            service = run('native:serviceareafrompoint', {
                'INPUT': value, 'STRATEGY': 1, 'SPEED_FIELD': 'v_kmh', 'DEFAULT_SPEED': 5,
                'DEFAULT_DIRECTION': 2, 'TOLERANCE': 0, 'START_POINT': common['START_POINT'],
                'TRAVEL_COST2': minutes / 60, 'OUTPUT_LINES': 'memory:',
            })['OUTPUT_LINES']
            save(service, f'servei_{state}_{minutes:02d}')
            union = shapely.union_all([shapely.from_wkb(bytes(f.geometry().asWkb())) for f in service.getFeatures()])
            controls['service'][state][str(minutes)] = {'unique_line_m': union.length, 'parameter_hours': minutes / 60}
    buffer = run('native:buffer', {'INPUT': layer('autopista_eixos'), 'DISTANCE': 35, 'SEGMENTS': 8,
                                 'DISSOLVE': True, 'OUTPUT': 'memory:'})['OUTPUT']
    road_cover = run('native:extractbyattribute', {'INPUT': covers, 'FIELD': 'classe', 'OPERATOR': 0,
                                                'VALUE': 351, 'OUTPUT': 'memory:'})['OUTPUT']
    barrier = run('native:intersection', {'INPUT': road_cover, 'OVERLAY': buffer, 'OUTPUT': 'memory:'})['OUTPUT']
    save(barrier, 'barrera_autopista')
    classes = rasterize(covers, 'classes', field='classe')
    vector_base = rasterize(covers, 'base_vector', field='cost_model')
    table = [0, 0, 99]
    for code, weight in input_info['costs'].items():
        table.extend([int(code), int(code), weight])
    base = run('native:reclassifybytable', {'INPUT_RASTER': classes, 'RASTER_BAND': 1,
             'TABLE': table, 'NO_DATA': -9999, 'RANGE_BOUNDARIES': 2,
             'NODATA_FOR_MISSING': True, 'DATA_TYPE': 5, 'OUTPUT': str(result_dir / 'base.tif')})['OUTPUT']
    # Raster class→cost is equivalent to the independently rasterized vector
    # cost field, except uncovered background0, explicitly recoded to99.
    expected_base = read(vector_base)
    expected_base[expected_base == 0] = 99
    assert np.array_equal(read(base), expected_base), 'Reclassification differs from the declared class table.'
    road_raster = rasterize(network, 'vials')
    road_values = read(road_raster)
    assert set(np.unique(road_values)) <= {0., 1.}
    controls['roads'] = {'source': 'xarxa; admitted ICGC RTT axes', 'burn_value': 1,
                         'road_cells': int(np.count_nonzero(road_values == 1)),
                         'cells_without_weight_one_in_cover_base': int(np.count_nonzero(
                             (road_values == 1) & (read(base) != 1))),
                         'priority': 'open passages; excluded motorway/closed P2; admitted roads; covers'}
    barriers = rasterize(barrier, 'barrera')
    pass_raster = rasterize(passes, 'pas', field='pas_id')
    # The real GUI expressions are executed, including intermediate numeric99
    # and final NoData99. Branches never have to recover a prematurely null cell.
    for state, expression in [
        ('obert', 'if("pas@1" > 0, 1, if("barrera@1" > 0, 99, if("vials@1" = 1, 1, if("base@1" = 0, 99, "base@1"))))'),
        ('tancat', 'if("pas@1" = 1, 1, if(("pas@1" = 2) OR ("barrera@1" > 0), 99, if("vials@1" = 1, 1, if("base@1" = 0, 99, "base@1"))))'),
    ]:
        numeric = calc(expression, {'pas': pass_raster, 'barrera': barriers, 'vials': road_raster,
                                    'base': base}, 'friccio_numeric_' + state)
        final = str(result_dir / ('friccio_' + state + '.tif'))
        image = gdal.Translate(final, numeric, noData=99)
        image = None
        friction = read(final)
        assert np.isfinite(friction[o]) and np.isfinite(friction[d]), (state, 'Endpoint excluded')
        codes, p, b = read(base), read(pass_raster), read(barriers)
        reference = np.where(p > 0 if state == 'obert' else p == 1, 1,
                             np.where((b > 0) | ((p == 2) if state == 'tancat' else False), 99,
                                       np.where(road_values == 1, 1, np.where(codes == 0, 99, codes))))
        actual = gdal.Open(numeric).ReadAsArray()
        assert np.array_equal(actual, reference), 'GUI conditional differs from its independent cell model.'
        cell_cost = calc('"friccio@1" * 5', {'friccio': final}, 'cost_cella_' + state)
        accumulated = str(result_dir / ('cost_' + state + '.tif'))
        directions = str(result_dir / ('direccions_' + state + '.tif'))
        run('grass:r.cost', {'input': cell_cost, 'start_points': str(gpkg) + '|layername=origen',
             '-k': False, '-n': True, 'output': accumulated, 'outdir': directions,
             'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': RES})
        path = str(result_dir / ('ruta_cost_' + state + '.gpkg'))
        run('grass:r.path', {'input': directions, 'format': 1,
             'start_points': str(gpkg) + '|layername=desti', 'vector_path': path, 'raster_path': 'TEMPORARY_OUTPUT',
             'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': RES})
        route_layer = QgsVectorLayer(path, 'route', 'ogr')
        assert route_layer.isValid() and route_layer.featureCount() > 0
        controls['cost'][state] = {'cost_weighted_m': float(read(accumulated)[d]),
                                  'path_length_m': sum(f.geometry().length() for f in route_layer.getFeatures()),
                                  'excluded_cells': int(np.count_nonzero(~np.isfinite(friction)))}
        temporal = calc('("friccio@1" - 1) * 0.125', {'friccio': final}, 'friccio_temporal_' + state)
        assert np.nanmax(np.abs(read(temporal) - (friction - 1) * .125)) < 1e-7
    dem_path = str(result_dir / 'mdt_ambit.tif')
    image = gdal.Translate(dem_path, f'GPKG:{gpkg}:mdt', projWin=[BOUNDS[0], BOUNDS[3], BOUNDS[2], BOUNDS[1]])
    image = None
    z = read(dem_path)
    assert np.isfinite(z).all()
    flat = str(result_dir / 'mdt_pla.tif')
    source = gdal.Open(dem_path)
    image = gdal.GetDriverByName('GTiff').Create(flat, width, height, 1, gdal.GDT_Float32)
    image.SetGeoTransform(source.GetGeoTransform())
    image.SetProjection(source.GetProjection())
    image.GetRasterBand(1).WriteArray(np.zeros_like(z))
    image = source = None
    moves = [(dy, dx, RES * math.hypot(dy, dx)) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dy or dx]
    def independent(friction, start, end, elevation=None):
        distances = np.full(friction.shape, np.inf)
        distances[start] = 0
        queue = [(0., *start)]
        while queue:
            cost, y, x = heapq.heappop(queue)
            if cost != distances[y, x]:
                continue
            if (y, x) == end:
                return cost
            for dy, dx, distance in moves:
                yy, xx = y + dy, x + dx
                if not (0 <= yy < height and 0 <= xx < width) or not np.isfinite(friction[yy, xx]):
                    continue
                step = (friction[y, x] + friction[yy, xx]) / 2 * distance
                if elevation is not None:
                    dh = elevation[yy, xx] - elevation[y, x]
                    coefficient = 6 if dh > 0 else (-1.9998 if dh / distance < -.2125 else 1.9998)
                    step += .72 * distance + coefficient * dh
                candidate = cost + step
                if candidate < distances[yy, xx]:
                    distances[yy, xx] = candidate
                    heapq.heappush(queue, (candidate, yy, xx))
        return float('inf')
    for state in ['obert', 'tancat']:
        check = independent(read(result_dir / ('friccio_' + state + '.tif')), o, d)
        assert abs(check - controls['cost'][state]['cost_weighted_m']) < .03
        controls['cost'][state]['independent_cost'] = check
    walk_params = {'walk_coeff': '0.72,6.0,1.9998,-1.9998', 'lambda': 1., 'slope_factor': -.2125,
                   '-k': False, '-n': True, 'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': RES}
    for name, state, flat_model, start, end in [
        ('obert_anada', 'obert', False, 'origen', 'desti'),
        ('obert_tornada', 'obert', False, 'desti', 'origen'),
        ('tancat_anada', 'tancat', False, 'origen', 'desti'),
        ('pla_anada', 'obert', True, 'origen', 'desti'),
        ('pla_tornada', 'obert', True, 'desti', 'origen'),
    ]:
        seconds_path = str(result_dir / ('marxa_' + name + '_segons.tif'))
        direction = str(result_dir / ('marxa_' + name + '_direccions.tif'))
        run('grass:r.walk.points', {**walk_params, 'elevation': flat if flat_model else dem_path,
             'friction': str(result_dir / ('friccio_temporal_' + state + '.tif')),
             'start_points': str(gpkg) + '|layername=' + start, 'output': seconds_path, 'outdir': direction})
        seconds = read(seconds_path)
        start_cell, end_cell = (o, d) if start == 'origen' else (d, o)
        check = independent(read(result_dir / ('friccio_temporal_' + state + '.tif')),
                            start_cell, end_cell, np.zeros_like(z) if flat_model else z)
        assert abs(seconds[end_cell] - check) < .08, (name, seconds[end_cell], check)
        route_path = str(result_dir / ('marxa_' + name + '_ruta.gpkg'))
        run('grass:r.path', {'input': direction, 'format': 1, 'start_points': str(gpkg) + '|layername=' + end,
             'vector_path': route_path, 'raster_path': 'TEMPORARY_OUTPUT',
             'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': RES})
        minutes_path = calc('"segons@1" / 60', {'segons': seconds_path}, 'marxa_' + name + '_minuts')
        controls['walk'][name] = {'seconds': float(seconds[end_cell]), 'minutes': float(seconds[end_cell] / 60),
                                  'independent_seconds': check}
        if name not in ['obert_anada', 'tancat_anada']:
            continue
        contours = str(result_dir / ('isocrones_' + state + '.gpkg'))
        run('grass:r.contour', {'input': minutes_path, 'levels': '3,6,12', 'cut': 3, 'output': contours,
             'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': RES})
        classes_path = calc('if("minuts@1" <= 3, 1, if("minuts@1" <= 6, 2, if("minuts@1" <= 12, 3, 4)))',
                            {'minuts': minutes_path}, 'franges_' + state)
        minutes = read(minutes_path)
        controls['walk'][name]['isochrones_cells'] = [int(np.count_nonzero(np.isfinite(minutes) & (minutes <= t))) for t in [3, 6, 12]]
        edge = np.concatenate([minutes[0], minutes[-1], minutes[:, 0], minutes[:, -1]])
        controls['walk'][name]['touches_frame'] = [bool(np.any(np.isfinite(edge) & (edge <= t))) for t in [3, 6, 12]]
        assert not any(controls['walk'][name]['touches_frame']), 'Extend the region instead of publishing truncated isochrones.'
        assert np.array_equal(np.isnan(read(classes_path)), np.isnan(minutes))
    assert abs(controls['walk']['pla_anada']['seconds'] - controls['walk']['pla_tornada']['seconds']) < .03
    assert abs(controls['walk']['obert_anada']['seconds'] - controls['walk']['obert_tornada']['seconds']) > 1
    assert sha(gpkg) == before, 'A computation changed the initial student inputs.'
    controls['student_inputs_unchanged'] = True
    record(OUT / 'controls/resultats-inici.json', controls)
    print(json.dumps(controls, ensure_ascii=False, indent=2), flush=True)


def style_teacher():
    from qgis.core import (QgsVectorLayer, QgsRasterLayer, QgsLineSymbol, QgsSimpleLineSymbolLayer,
                          QgsRasterShader, QgsColorRampShader, QgsSingleBandPseudoColorRenderer,
                          QgsRectangle, QgsReferencedRectangle, Qgis)
    setup()
    app, project, context = qgis_session()
    gpkg = OUT / 'alumnat/accessibilitat-vilaseca.gpkg'
    results = OUT / 'docent/resultats'
    vector_results = OUT / 'docent/resultats.gpkg'
    controls = json.loads((OUT / 'controls/resultats-inici.json').read_text())
    definitions = {}

    def raster(key, filename, name, items, exact=False, opacity=1):
        definitions[key] = ('raster', str(results / filename), name, items, exact, opacity)

    def line(key, uri, name, colour, width=.9, dashed=False):
        definitions[key] = ('line', uri, name, colour, width, dashed)

    distance_colours = [(0, '#ffffe5', '0m'), (250, '#d9f0a3', '250m'),
                        (500, '#78c679', '500m'), (1000, '#238443', '1000m'), (2000, '#004529', '2000m')]
    raster('distance', 'distancia_grass.tif', 'Distància euclidiana GRASS · m', distance_colours, opacity=.75)
    straight_label = f'Recta O–D · {controls["euclidean_vector_m"]:.1f} m'.replace('.', ',')
    line('straight', str(vector_results) + '|layername=euclidiana_vector', straight_label, '#9742a0', .95, True)
    for state, colour in [('obert', '#006699'), ('tancat', '#d37838')]:
        route_label = 'Ruta de xarxa · ' + state
        if not controls['network'][state]['reachable']:
            route_label += ' · sense ruta'
        line('network_' + state, str(vector_results) + '|layername=ruta_' + state,
             route_label, colour, 1.15, state == 'tancat')
        for minutes, c, w in [(12, '#e89537', 1.8), (6, '#27a584', 1.4), (3, '#1565ad', 1.)]:
            line(f'service_{state}_{minutes}', str(vector_results) + f'|layername=servei_{state}_{minutes:02d}',
                 f'{minutes}min · pas {state}', c, w)
        raster('friction_' + state, f'friccio_{state}.tif', 'Fricció · ' + state,
               [(1, '#e9f6e9', '1 · vial/pas'), (2, '#c7dcae', '2 · espai obert'),
                (3, '#ded0b0', '3 · platja'), (4, '#d7bd83', '4 · conreu/urbà'),
                (6, '#a89268', '6 · bosc/industrial')], exact=True, opacity=.9)
        raster('cost_' + state, f'cost_{state}.tif', 'Cost acumulat · m ponderats · ' + state,
               [(0, '#ffffcc', '0'), (500, '#c7e9b4', '500'), (1500, '#7fcdbb', '1500'),
                (3000, '#41b6c4', '3000'), (6000, '#253494', '6000')], opacity=.85)
        line('cost_route_' + state, str(results / f'ruta_cost_{state}.gpkg'), 'Camí de cost · ' + state,
             colour, 1.1, state == 'tancat')
        raster('iso_' + state, f'franges_{state}.tif', 'Franges de temps · ' + state,
               [(1, '#2365a4', '0–3min'), (2, '#289d85', '>3–6min'),
                (3, '#e39d39', '>6–12min'), (4, '#e7e7e7', '>12min')], exact=True, opacity=.8)
        line('contours_' + state, str(results / f'isocrones_{state}.gpkg'), 'Contorns3/6/12min · ' + state,
             '#354652', .35)
    raster('minutes', 'marxa_obert_anada_minuts.tif', 'Temps de marxa · minuts',
           [(0, '#ffffcc', '0min'), (3, '#c7e9b4', '3min'), (6, '#7fcdbb', '6min'),
            (12, '#41b6c4', '12min'), (30, '#253494', '30min')], opacity=.85)
    line('walk_out', str(results / 'marxa_obert_anada_ruta.gpkg'), 'Anada · marxa amb MDT', '#54278f', 1.)
    line('walk_back', str(results / 'marxa_obert_tornada_ruta.gpkg'), 'Tornada · marxa amb MDT', '#c94743', .9, True)
    specifications = {
        '00-inici': [],
        '01-euclidiana': ['distance', 'straight'],
        '02-xarxa': ['network_tancat', 'network_obert', 'straight'],
        '03-servei-obert': ['service_obert_12', 'service_obert_6', 'service_obert_3'],
        '04-servei-tancat': ['service_tancat_12', 'service_tancat_6', 'service_tancat_3'],
        '05-friccio-oberta': ['friction_obert'],
        '06-friccio-tancada': ['friction_tancat'],
        '07-cost': ['cost_obert', 'cost_route_tancat', 'cost_route_obert'],
        '08-marxa': ['minutes', 'walk_back', 'walk_out'],
        '09-isocrones-obert': ['iso_obert', 'contours_obert'],
        '10-isocrones-tancat': ['iso_tancat', 'contours_tancat'],
    }
    reports = []
    for name, keys in specifications.items():
        assert project.read('geopackage:' + str(gpkg) + '?projectName=inici')
        project.setTitle('Accessibilitat · ' + name)
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for value in project.mapLayers().values():
            node = project.layerTreeRoot().findLayer(value.id())
            if '|layername=xarxa' in value.source():
                node.setItemVisibilityChecked(name in ['00-inici', '02-xarxa', '03-servei-obert', '04-servei-tancat'])
            if '|layername=origen' in value.source() or '|layername=desti' in value.source():
                node.setItemVisibilityChecked(False)
        for key in keys:
            kind, uri, label, *parameters = definitions[key]
            value = QgsRasterLayer(uri, label) if kind == 'raster' else QgsVectorLayer(uri, label, 'ogr')
            assert value.isValid(), (key, uri)
            if kind == 'raster':
                items, exact, opacity = parameters
                ramp = QgsColorRampShader()
                ramp.setColorRampType(QgsColorRampShader.Exact if exact else QgsColorRampShader.Interpolated)
                from qgis.PyQt.QtGui import QColor
                ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(v, QColor(c), text) for v, c, text in items])
                ramp.setMinimumValue(items[0][0])
                ramp.setMaximumValue(items[-1][0])
                shader = QgsRasterShader()
                shader.setRasterShaderFunction(ramp)
                renderer = QgsSingleBandPseudoColorRenderer(value.dataProvider(), 1, shader)
                renderer.setClassificationMin(items[0][0])
                renderer.setClassificationMax(items[-1][0])
                value.setRenderer(renderer)
                value.setOpacity(opacity)
                message, ok = value.saveNamedStyle(str(Path(uri).with_suffix('.qml')))
                assert ok, message
            else:
                colour, width, dashed = parameters
                symbol = QgsLineSymbol.createSimple({'line_color': 'white', 'line_width': str(width + .6)})
                symbol.appendSymbolLayer(QgsSimpleLineSymbolLayer.create({'line_color': colour,
                    'line_width': str(width), 'line_style': 'dash' if dashed else 'solid'}))
                value.renderer().setSymbol(symbol)
                error = value.saveStyleToDatabase('docent', 'Estil del moment docent verificat', True, '')
                assert not error, error
            project.addMapLayer(value)
        # Fresh endpoint instances render above rasters and maintain their
        # database style/labels without mutating the initial package.
        for table, label in [('origen', 'Origen O'), ('desti', 'Destí D')]:
            value = QgsVectorLayer(str(gpkg) + '|layername=' + table, label, 'ogr')
            project.addMapLayer(value)
        bounds = BOUNDS
        if name == '02-xarxa':
            route = QgsVectorLayer(str(vector_results) + '|layername=ruta_tancat', 'Route extent', 'ogr')
            if route.featureCount() == 0:
                route = QgsVectorLayer(str(vector_results) + '|layername=ruta_obert', 'Open route extent', 'ogr')
            rectangle = route.extent()
            bounds = (rectangle.xMinimum() - 180, rectangle.yMinimum() - 180,
                      rectangle.xMaximum() + 180, rectangle.yMaximum() + 180)
        if name.startswith(('05', '06', '07', '08')):
            bounds = (343600, 4553100, 345200, 4554400)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*bounds), project.crs()))
        path = OUT / 'docent/projectes' / (name + '.qgz')
        assert project.write(str(path))
        reports.append({'path': str(path.relative_to(OUT)), 'layers': len(project.mapLayers()),
                        'visible_results': keys, 'bounds': bounds})
        project.clear()
    record(OUT / 'controls/projectes-docent.json', reports)
    print(json.dumps({'projects': len(reports)}, indent=2), flush=True)


def documents(receipts_directory):
    import shutil
    setup()
    assert receipts_directory, 'Build with manual_practice_pdf_build and supply --pdf-receipts.'
    receipts = (ROOT / receipts_directory).resolve()
    assert receipts.is_relative_to(ROOT / 'sandbox/practiques' / PACKAGE_STEM)
    document_name = reading_name()
    reproduction = OUT / 'reproduccio'
    reproduction.mkdir(exist_ok=True)
    for source, name in [(Path(__file__), 'preparar.py'),
                         (ROOT / 'context/qgis/accessibilitat-inici.md', 'prompt.md'),
                         (ROOT / 'context/qgis/accessibilitat-inici.yml', 'recipe.yml')]:
        shutil.copyfile(source, reproduction / name)
    image = 'sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa'
    settings = {'image': image, 'producer': 'unaltraweb0.7.2 manual_practice_pdf_build', 'readings': {}}
    for recipient in ['alumnat', 'docent']:
        response = json.loads((receipts / (recipient + '-pdf.json')).read_text())
        built = response['structuredContent']
        assert not response['isError'] and built['ok'] and not built['publishes']
        assert built['version'] == VERSION and built['language'] == LANGUAGE and built['audience'] == recipient
        assert built['renderer']['observed_image_id'] == image
        source = PRACTICE / LANGUAGE / recipient / (document_name + '.md')
        assert built['source'] == str(source.relative_to(ROOT))
        pdf = (ROOT / built['pdf']).resolve()
        assert pdf.is_relative_to(ROOT / 'sandbox/practiques' / PACKAGE_STEM)
        assert sha(pdf) == built['pdf_sha256']
        target = OUT / recipient / (document_name + '.pdf')
        assert not target.exists(), 'Existing candidate PDF is retained; select a new destination.'
        shutil.copyfile(pdf, target)
        shutil.copyfile(source, OUT / recipient / (document_name + '.md'))
        settings['readings'][recipient] = {'job': built['job'], 'source_sha256': sha(source),
                                           'pdf_sha256': sha(target), 'fingerprint': built['fingerprint']}
    record(OUT / 'controls/handouts.json', settings)
    (OUT / 'COMENCA-AQUI.txt').write_text(
        'Accessibilitat de Vila-seca · preparació completa del professorat\n\n'
        'Per a l’alumnat: només alumnat/accessibilitat-vilaseca.gpkg i alumnat/LLEGIU-ME.pdf.\n'
        'Crear una connexió GeoPackage i obrir-ne el projecte inici.\n'
        'docent/: LLEGIU-ME.pdf, resultats i onze projectes per parades.\n'
        'fonts/: originals/còpies de font; controls/: paràmetres i verificacions.\n'
        'captures/: PNG/SVG/manifests; reproduccio/: fonts editables de preparació/captura.\n'
        'Els preparadors esperen les rutes del repositori geodisseny i el runtime fixat;\n'
        'no són un instal·lador autònom. La guia permet fer els passos directament amb QGIS.\n'
        'Autoria: Benito Zaragozí. Nova versió per a revisió humana, sense pujada a Moodle.\n')


def style_cell_cost():
    """Represent the unchanged cell-cost raster with explicit passage values."""
    from qgis.core import QgsRasterLayer, QgsRasterShader, QgsColorRampShader, QgsSingleBandPseudoColorRenderer
    from qgis.PyQt.QtGui import QColor
    setup()
    app, project, context = qgis_session()
    path = OUT / 'docent/resultats/cost_cella_obert.tif'
    layer = QgsRasterLayer(str(path), 'Cost per cel·la · passos oberts')
    assert layer.isValid()
    ramp = QgsColorRampShader()
    ramp.setColorRampType(QgsColorRampShader.Exact)
    ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(value, QColor(colour), label) for value, colour, label in [
        (5, '#e9f6e9', '5 · vial/pas'), (10, '#c7dcae', '10 · espai obert'),
        (15, '#ded0b0', '15 · platja'), (20, '#d7bd83', '20 · conreu/urbà'),
        (30, '#a89268', '30 · bosc/industrial')]])
    ramp.setMinimumValue(5)
    ramp.setMaximumValue(30)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(ramp)
    renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader)
    renderer.setClassificationMin(5)
    renderer.setClassificationMax(30)
    layer.setRenderer(renderer)
    message, ok = layer.saveNamedStyle(str(path.with_suffix('.qml')))
    assert ok, message


def package():
    import shutil
    import sqlite3
    import zipfile
    setup()
    qgis_report = json.loads((OUT / 'controls/verificacio-qgis.json').read_text())
    pdf_report = json.loads((OUT / 'controls/verificacio-pdf.json').read_text())
    assert qgis_report['ok'] and pdf_report['ok']
    assert qgis_report['student_gpkg_sha256'] == sha(OUT / 'alumnat/accessibilitat-vilaseca.gpkg')
    for name, digest in qgis_report['checked_hashes'].items():
        assert sha(OUT / name) == digest, ('Verified data changed', name)
    source_manifest = json.loads((OUT / 'fonts/fonts.json').read_text())
    for name, evidence in source_manifest.items():
        assert sha(OUT / 'fonts' / name) == evidence['sha256'], ('Original snapshot changed', name)
    shutil.copyfile(Path(__file__), OUT / 'reproduccio/preparar.py')
    document_name = reading_name()
    for key, recipient in [('GUIA', 'alumnat'), ('SOLUCIONS', 'docent')]:
        source = PRACTICE / LANGUAGE / recipient / (document_name + '.md')
        assert pdf_report[key]['source_sha256'] == sha(source)
        assert pdf_report[key]['sha256'] == sha(OUT / recipient / (document_name + '.pdf'))
    import yaml
    captures = [capture['id'] for capture in yaml.safe_load(
        (ROOT / 'context/qgis/accessibilitat-inici.yml').read_text())['captures']]
    for name in captures:
        evidence = json.loads((OUT / 'captures/icgc-final/rendered' / (name + '.manifest.yml')).read_text())
        assert evidence['ok'] and not evidence['warnings'], name
        assert evidence['image_digest'] == IMAGE
    for path in [OUT / 'alumnat/accessibilitat-vilaseca.gpkg', OUT / 'docent/resultats.gpkg']:
        connection = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
        assert connection.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        connection.close()
        assert not path.with_name(path.name + '-wal').exists()
        assert not path.with_name(path.name + '-shm').exists()
    import xml.etree.ElementTree as ET
    required = {OUT / 'alumnat/accessibilitat-vilaseca.gpkg', OUT / 'alumnat' / (document_name + '.pdf')}
    student_files = list(required)
    if MODULE:
        student_files += [OUT / 'alumnat' / (name + '.tif') for name in MODULE['initial_rasters']]
        required.update(student_files)
    projects = sorted((OUT / 'docent/projectes').glob('*.qgz'))
    assert len(projects) == 11
    if MODULE:
        projects = [path for path in projects if path.stem in MODULE['projects']]
        assert len(projects) == len(MODULE['projects'])
    required.update(projects)
    # Only classroom project dependencies and named worked-stage outputs enter
    # the teacher ZIP. Agent snapshots/caches/logs/scripts stay in sandbox.
    for project in projects:
        with zipfile.ZipFile(project) as archive:
            qgs = next(name for name in archive.namelist() if name.endswith('.qgs'))
            document = ET.fromstring(archive.read(qgs))
        for node in document.findall('.//projectlayers/maplayer/datasource'):
            uri = node.text or ''
            if uri.startswith('GPKG:'):
                uri = uri[5:].rsplit(':', 1)[0]
            else:
                uri = uri.split('|', 1)[0]
            assert not Path(uri).is_absolute(), (project, uri)
            dependency = (project.parent / uri).resolve()
            assert dependency.is_relative_to(OUT.resolve()) and dependency.is_file(), (project, uri)
            required.add(dependency)
    worked = [name + '.tif' for name in MODULE['worked_rasters']] if MODULE else [
                 'classes.tif', 'base.tif', 'vials.tif', 'pas.tif', 'barrera.tif', 'origen_zero.tif', 'origen_null.tif',
                 'friccio_obert.tif', 'friccio_tancat.tif', 'cost_cella_obert.tif', 'cost_cella_tancat.tif',
                 'direccions_obert.tif', 'direccions_tancat.tif', 'friccio_temporal_obert.tif',
                 'friccio_temporal_tancat.tif', 'mdt_ambit.tif', 'mdt_pla.tif']
    for name in worked:
        required.add(OUT / 'docent/resultats' / name)
    for path in list(required):
        qml = path.with_suffix('.qml')
        if qml.exists() and qml.is_relative_to(OUT / 'docent'):
            required.add(qml)
    teacher_pdf = OUT / 'docent' / (document_name + '.pdf')
    required.add(teacher_pdf)
    assert all(path.is_file() for path in required)
    assert all(path.is_relative_to(OUT / 'alumnat') or path.is_relative_to(OUT / 'docent') for path in required)
    candidates = OUT / 'lliuraments'
    candidates.mkdir(exist_ok=True)
    inventories, destinations = {}, {}
    assert not DIST.exists() or not any(DIST.iterdir()), 'A sealed dist version is never overwritten.'
    for kind in ['alumnat', 'docent']:
        destination = candidates / delivery_name(kind)
        assert not destination.exists(), 'An existing delivery is never overwritten.'
        if kind == 'alumnat':
            files = sorted(student_files)
            prefix = PACKAGE_STEM + '/'
        else:
            files = sorted(required)
            prefix = PACKAGE_STEM + '-docent/'
        inventory = []
        with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for path in files:
                relative = path.name if kind == 'alumnat' or path == teacher_pdf else str(path.relative_to(OUT))
                archive.write(path, prefix + relative)
                inventory.append({'path': relative, 'bytes': path.stat().st_size, 'sha256': sha(path)})
        with zipfile.ZipFile(destination) as archive:
            assert archive.testzip() is None and len(archive.namelist()) == len(inventory)
            for item in inventory:
                with archive.open(prefix + item['path']) as stream:
                    assert hashlib.file_digest(stream, 'sha256').hexdigest() == item['sha256']
        inventories[kind] = inventory
        final = DIST / delivery_name(kind)
        destinations[kind] = {'path': str(final.relative_to(ROOT)), 'bytes': destination.stat().st_size,
                              'sha256': sha(destination), 'files': len(inventory), 'zip_crc': 'ok', 'all_member_sha256': 'ok'}
        record(destination.with_suffix('.receipt.json'), destinations[kind])
    assert len(inventories['alumnat']) == 2 + (len(MODULE['initial_rasters']) if MODULE else 0)
    assert all(not item['path'].startswith(('fonts/', 'controls/', 'captures/', 'reproduccio/')) for item in inventories['docent'])
    DIST.mkdir(parents=True, exist_ok=True)
    for kind, evidence in destinations.items():
        candidate = candidates / delivery_name(kind)
        final = ROOT / evidence['path']
        with candidate.open('rb') as source, final.open('xb') as target:
            shutil.copyfileobj(source, target)
        assert sha(final) == evidence['sha256']
    record(DIST / 'manifest.json', {'schema_version': 1, 'practica': PACKAGE_STEM,
                                  'version': VERSION, 'language': LANGUAGE, 'status': 'local-moodle-packages',
                                  'human_approved': False, 'site_release': None, 'packages': destinations,
                                  'inventories': inventories, 'reconstruction': str(OUT.relative_to(ROOT))})
    record(OUT / 'MANIFEST.json', {'schema_version': 1, 'status': 'private-author-review',
                                  'human_approved': False, 'runtime': IMAGE, 'inventories': inventories,
                                  'packages': destinations})
    record(OUT / 'sealed.json', {'status': 'private-author-review', 'human_approved': False,
                                'manifest_sha256': sha(OUT / 'MANIFEST.json'), 'packages': destinations})
    print(json.dumps(destinations, ensure_ascii=False, indent=2), flush=True)


def seal_common():
    """Retain the common calculation for selecting the three classroom modules."""
    setup()
    assert MODULE is None
    assert json.loads((OUT / 'controls/verificacio-qgis.json').read_text())['ok']
    paths = [path for folder in ['alumnat', 'docent', 'fonts', 'captures', 'controls', 'reproduccio']
             for path in (OUT / folder).rglob('*') if path.is_file()]
    record(OUT / 'MANIFEST.json', {'kind': 'accessibilitat-common-classroom-calculation',
        'version': VERSION, 'runtime': IMAGE, 'human_approved': False,
        'files': [{'path': str(path.relative_to(OUT)), 'sha256': sha(path), 'bytes': path.stat().st_size}
                  for path in sorted(paths)]})
    record(OUT / 'sealed.json', {'manifest_sha256': sha(OUT / 'MANIFEST.json'),
                               'human_approved': False, 'status': 'private-common-calculation'})


def stage_module(source_run):
    """Separate existing projects/data; the common calculation is not repeated."""
    import shutil
    assert MODULE and not OUT.exists()
    previous = ROOT / 'sandbox/practiques/accessibilitat-vilaseca' / source_run
    seal = json.loads((previous / 'sealed.json').read_text())
    assert sha(previous / 'MANIFEST.json') == seal['manifest_sha256']
    manifest = json.loads((previous / 'MANIFEST.json').read_text())
    assert manifest['kind'] == 'accessibilitat-common-classroom-calculation'
    initialise()
    for item in manifest['files']:
        path = Path(item['path'])
        assert not path.is_absolute() and '..' not in path.parts
        assert sha(previous / path) == item['sha256']
        target = OUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with (previous / path).open('rb') as source, target.open('xb') as destination:
            shutil.copyfileobj(source, destination)
        assert sha(target) == item['sha256']
    for name in MODULE['initial_rasters']:
        shutil.copyfile(OUT / 'docent/resultats' / (name + '.tif'), OUT / 'alumnat' / (name + '.tif'))
    record(OUT / 'controls/module-source.json', {'source': str(previous.relative_to(ROOT)),
        'manifest_sha256': seal['manifest_sha256'], 'classroom_selection': MODULE,
        'gis_recalculated': False, 'human_approved': False})


def rename_deliverables(source_version):
    """Stage a new delivery version with the exact bytes of verified archives."""
    import shutil
    import zipfile
    source_dist = ROOT / 'dist/practiques' / PACKAGE_STEM / source_version / LANGUAGE
    assert source_dist != DIST, 'Select a new version; sealed deliveries are immutable.'
    assert not DIST.exists(), 'An existing delivery version is never overwritten.'
    source_path = source_dist / 'manifest.json'
    source_digest = sha(source_path)
    source = json.loads(source_path.read_text())
    assert source['practica'] == PACKAGE_STEM and source['language'] == LANGUAGE
    assert set(source['packages']) == {'alumnat', 'docent'}
    reconstruction = (ROOT / source['reconstruction']).resolve()
    assert reconstruction.is_relative_to(ROOT / 'sandbox/practiques' / PACKAGE_STEM)
    seal = json.loads((reconstruction / 'sealed.json').read_text())
    assert sha(reconstruction / 'MANIFEST.json') == seal['manifest_sha256']
    stage = ROOT / 'sandbox/practiques' / PACKAGE_STEM / ('lliurament-' + VERSION + '-' + str(time.time_ns()))
    stage.mkdir()
    record(stage / '.owner.json', {'owner': Path(__file__).name, 'operation': 'delivery-names',
                                  'source_manifest': str(source_path.relative_to(ROOT)),
                                  'source_manifest_sha256': source_digest})
    candidates = stage / 'lliuraments'
    candidates.mkdir()
    destinations = {}
    for recipient, evidence in source['packages'].items():
        for key in ['sha256', 'bytes', 'files']:
            assert evidence[key] == seal['packages'][recipient][key]
        original = (ROOT / evidence['path']).resolve()
        assert original.parent == source_dist.resolve()
        assert sha(original) == evidence['sha256'] and original.stat().st_size == evidence['bytes']
        inventory = source['inventories'][recipient]
        prefix = PACKAGE_STEM + ('-docent' if recipient == 'docent' else '') + '/'
        with zipfile.ZipFile(original) as archive:
            assert archive.testzip() is None
            assert set(archive.namelist()) == {prefix + item['path'] for item in inventory}
            assert len(archive.namelist()) == len(inventory) == evidence['files']
            for item in inventory:
                with archive.open(prefix + item['path']) as stream:
                    assert hashlib.file_digest(stream, 'sha256').hexdigest() == item['sha256']
        candidate = candidates / delivery_name(recipient)
        with original.open('rb') as stream, candidate.open('xb') as target:
            shutil.copyfileobj(stream, target)
        assert sha(candidate) == evidence['sha256']
        destinations[recipient] = dict(evidence, path=str((DIST / candidate.name).relative_to(ROOT)))
        record(candidate.with_suffix('.receipt.json'), destinations[recipient])
    assert sha(source_path) == source_digest
    updated = dict(source, version=VERSION, packages=destinations,
                   packaging_run=str(stage.relative_to(ROOT)),
                   renamed_from={'manifest': str(source_path.relative_to(ROOT)), 'sha256': source_digest,
                                 'content_unchanged': True})
    record(stage / 'MANIFEST.json', updated)
    record(stage / 'sealed.json', {'manifest_sha256': sha(stage / 'MANIFEST.json'), 'packages': destinations,
                                 'operation': 'delivery-names', 'content_unchanged': True})
    DIST.mkdir(parents=True)
    for recipient, evidence in destinations.items():
        with (candidates / delivery_name(recipient)).open('rb') as stream, (ROOT / evidence['path']).open('xb') as target:
            shutil.copyfileobj(stream, target)
        assert sha(ROOT / evidence['path']) == evidence['sha256']
    record(DIST / 'manifest.json', updated)
    print(json.dumps(destinations, ensure_ascii=False, indent=2), flush=True)


def verify_run():
    """Check this activity's new ICGC classroom states before packaging."""
    import subprocess
    setup()
    paths = [path for directory in ('alumnat', 'docent') for path in (OUT / directory).rglob('*')
             if path.is_file() and path.suffix in {'.gpkg', '.tif', '.tfw', '.qml', '.qgz', '.xml'}]
    checked = {str(path.relative_to(OUT)): sha(path) for path in paths}
    code = '''import json
from pathlib import Path
from qgis.core import QgsApplication,QgsProject,QgsVectorLayer
app=QgsApplication([],False);app.initQgis();p=QgsProject.instance();root=Path('/paquet')
gpkg=root/'alumnat/accessibilitat-vilaseca.gpkg'
assert p.read('geopackage:'+str(gpkg)+'?projectName=inici')
assert len(p.mapLayers())==11 and all(l.isValid() for l in p.mapLayers().values())
network=QgsVectorLayer(str(gpkg)+'|layername=xarxa','ICGC','ogr')
fields=network.fields().names();assert 'rtt_id' in fields and 'way_id' not in fields
assert network.featureCount()==7945
p.clear();projects=[]
for file in sorted((root/'docent/projectes').glob('*.qgz')):
    assert p.read(str(file))
    assert all(l.isValid() and '/paquet/' in l.source() for l in p.mapLayers().values())
    projects.append({'project':file.name,'all_valid':True,'layers':len(p.mapLayers())});p.clear()
assert len(projects)==11
closed=QgsVectorLayer(str(root/'docent/resultats.gpkg')+'|layername=ruta_tancat','Sense ruta','ogr')
assert closed.isValid() and closed.featureCount()==0
print(json.dumps({'ok':True,'initial_layers':11,'network_source':'ICGC RTT2024',
                  'network_parts':network.featureCount(),'projects':projects,'closed_route_empty':True}))
'''
    result = subprocess.run(['docker', 'run', '--rm', '--pull', 'never', '--user', f'{os.getuid()}:{os.getgid()}',
                             '--network', 'none', '--read-only', '--tmpfs', '/tmp',
                             '--env', 'HOME=/tmp', '--env', 'QT_QPA_PLATFORM=offscreen',
                             '--mount', f'type=bind,src={OUT},dst=/paquet,readonly',
                             '--entrypoint', 'python3', IMAGE, '-c', code],
                            capture_output=True, text=True, timeout=180)
    record(OUT / 'controls/verificacio-qgis-native.json', {'returncode': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr, 'image': IMAGE, 'readonly': True, 'network': 'none'})
    assert result.returncode == 0, result.stdout + result.stderr
    assert checked == {str(path.relative_to(OUT)): sha(path) for path in paths}
    report = json.loads(result.stdout)
    report.update({'student_gpkg_sha256': sha(OUT / 'alumnat/accessibilitat-vilaseca.gpkg'),
                   'checked_hashes': checked, 'readonly': True, 'network': 'none', 'runtime': IMAGE})
    record(OUT / 'controls/verificacio-qgis.json', report)
    print(json.dumps({key: report[key] for key in ('ok', 'initial_layers', 'network_parts', 'closed_route_empty')}))


def verify_deliverables():
    """Open the exact Moodle ZIPs in an isolated readonly QGIS environment."""
    import shutil
    import subprocess
    import zipfile
    evidence = json.loads((DIST / 'manifest.json').read_text())
    review = ROOT / 'sandbox/practiques/accessibilitat-vilaseca' / ('verificacio-' + str(time.time_ns()))
    review.mkdir(parents=True)
    before = {}
    for recipient, item in evidence['packages'].items():
        archive_path = ROOT / item['path']
        assert sha(archive_path) == item['sha256']
        target = review / recipient
        target.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            assert archive.testzip() is None
            for member in archive.infolist():
                path = Path(member.filename)
                assert not path.is_absolute() and '..' not in path.parts
                assert member.filename.endswith(('.pdf', '.gpkg', '.tif', '.qml', '.qgz'))
            archive.extractall(target)
        before.update({str(path.relative_to(review)): sha(path) for path in target.rglob('*') if path.is_file()})
    code = '''import json
from pathlib import Path
from qgis.core import QgsApplication,QgsProject
from osgeo import gdal
app=QgsApplication([],False);app.initQgis();p=QgsProject.instance()
root=Path('/paquet');initial=root/'alumnat/accessibilitat-vilaseca/accessibilitat-vilaseca.gpkg'
assert p.read('geopackage:'+str(initial)+'?projectName=inici')
assert len(p.mapLayers())==11 and all(l.isValid() for l in p.mapLayers().values())
p.clear();teacher=root/'docent/accessibilitat-vilaseca-docent';projects=[]
for file in sorted((teacher/'docent/projectes').glob('*.qgz')):
    assert p.read(str(file))
    assert all(l.isValid() and '/paquet/' in l.source() for l in p.mapLayers().values())
    projects.append(file.name);p.clear()
assert len(projects)==11
values={}
for name in ['cost_cella_obert.tif','cost_cella_tancat.tif']:
    image=gdal.Open(str(teacher/'docent/resultats'/name));a=image.ReadAsArray();nd=image.GetRasterBand(1).GetNoDataValue()
    p2=float(a[291,274]);alt=float(a[324,219]);assert alt==5
    if name=='cost_cella_obert.tif':assert p2==5
    else:assert p2==nd
    values[name]={'p2':'NoData' if p2==nd else p2,'alternatiu':alt}
print(json.dumps({'ok':True,'initial_layers':11,'projects':projects,'passages':values}))
'''
    if MODULE:
        code = code.replace('alumnat/accessibilitat-vilaseca/', 'alumnat/' + PACKAGE_STEM + '/')
        code = code.replace('accessibilitat-vilaseca-docent', PACKAGE_STEM + '-docent')
        code = code.replace('assert len(projects)==11', 'assert len(projects)==' + str(len(MODULE['projects'])))
        if MODULE['slug'] != 'accessibilitat-raster-vilaseca':
            code = code.replace("for name in ['cost_cella_obert.tif','cost_cella_tancat.tif']:", 'for name in []:')
    command = ['docker', 'run', '--rm', '--user', f'{os.getuid()}:{os.getgid()}', '--network', 'none',
               '--env', 'HOME=/tmp', '--env', 'QT_QPA_PLATFORM=offscreen',
               '--env', 'PYTHONPATH=/usr/share/qgis/python:/usr/share/qgis/python/plugins',
               '--mount', f'type=bind,src={review},dst=/paquet,readonly', '--workdir', '/paquet',
               '--entrypoint', 'python3', IMAGE, '-c', code]
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    record(review / 'qgis-receipt.json', {'returncode': result.returncode, 'stdout': result.stdout,
                                       'stderr': result.stderr, 'network': 'none', 'readonly': True})
    assert result.returncode == 0, result.stdout + result.stderr
    assert all(sha(review / path) == digest for path, digest in before.items())
    report = json.loads(result.stdout)
    report.update({'checked_files': len(before), 'unchanged': True,
                   'packages': evidence['packages'], 'review_path': str(review.relative_to(ROOT))})
    record(review / 'verified.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action='store_true')
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--recover-stage', action='store_true')
    parser.add_argument('--style-start', action='store_true')
    parser.add_argument('--renew-initial', action='store_true')
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--style-teacher', action='store_true')
    parser.add_argument('--docs', action='store_true')
    parser.add_argument('--pdf-receipts')
    parser.add_argument('--package', action='store_true')
    parser.add_argument('--organise', action='store_true')
    parser.add_argument('--stage-icgc', action='store_true')
    parser.add_argument('--reuse-icgc-from', metavar='RUN')
    parser.add_argument('--capture-config', action='store_true')
    parser.add_argument('--capture-pass')
    parser.add_argument('--verify-deliverables', action='store_true')
    parser.add_argument('--verify-run', action='store_true')
    parser.add_argument('--rename-deliverables-from', metavar='VERSION')
    parser.add_argument('--run-id')
    parser.add_argument('--version', default=VERSION)
    parser.add_argument('--language', choices=['ca', 'es', 'en'], default='ca')
    parser.add_argument('--style-cell-cost', action='store_true')
    parser.add_argument('--module', choices=MODULES)
    parser.add_argument('--stage-module-from', metavar='RUN')
    parser.add_argument('--seal-common', action='store_true')
    arguments = parser.parse_args()
    import re
    LANGUAGE = arguments.language
    VERSION = arguments.version
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', arguments.version)
    if arguments.module:
        MODULE = MODULES[arguments.module]
        PACKAGE_STEM = MODULE['slug']
        PRACTICE = ROOT / 'practiques' / PACKAGE_STEM
    DIST = ROOT / 'dist/practiques' / PACKAGE_STEM / arguments.version / LANGUAGE
    if arguments.run_id:
        assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', arguments.run_id)
        OUT = ROOT / 'sandbox/practiques' / PACKAGE_STEM / arguments.run_id
    if arguments.stage_module_from:
        assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', arguments.stage_module_from)
        assert arguments.module and arguments.run_id
        stage_module(arguments.stage_module_from)
    if arguments.reuse_icgc_from:
        assert arguments.run_id, 'Select an explicit new run for the reading revision.'
        assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', arguments.reuse_icgc_from)
        assert not any([arguments.init, arguments.organise, arguments.stage_icgc,
                        arguments.fetch, arguments.prepare, arguments.build, arguments.recover_stage,
                        arguments.renew_initial, arguments.style_start, arguments.style_teacher,
                        arguments.style_cell_cost, arguments.rename_deliverables_from])
        reuse_icgc(arguments.reuse_icgc_from)
    if arguments.rename_deliverables_from:
        assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', arguments.rename_deliverables_from)
        assert not any([arguments.init, arguments.organise, arguments.fetch, arguments.prepare,
                        arguments.build, arguments.docs, arguments.package, arguments.recover_stage,
                        arguments.renew_initial, arguments.style_start, arguments.style_teacher,
                         arguments.style_cell_cost, arguments.stage_icgc, arguments.capture_config]), 'Rename only already verified deliveries.'
        rename_deliverables(arguments.rename_deliverables_from)
    if arguments.organise:
        organise()
    if arguments.stage_icgc:
        stage_icgc()
    if arguments.init:
        initialise()
    if arguments.fetch:
        fetch()
    if arguments.recover_stage:
        import sqlite3
        setup()
        stage = OUT / 'alumnat/.initial-stage.gpkg'
        assert stage.is_file() and not (OUT / 'alumnat/accessibilitat-vilaseca.gpkg').exists()
        connection = sqlite3.connect(f'file:{stage}?mode=ro', uri=True)
        tables = {row[0] for row in connection.execute('SELECT table_name FROM gpkg_contents')}
        assert tables <= {'municipi', 'ambit_calcul', 'cobertura_sense_dades', 'cobertes', 'llegenda_costos',
                          'xarxa', 'origen', 'desti', 'passos', 'autopista_eixos', 'barrera_autopista', 'mdt', 'ortofoto'}
        connection.close()
        digest = sha(stage)
        archived = OUT / 'controls' / f'failed-stage-{time.time_ns()}.gpkg'
        stage.rename(archived)
        record(archived.with_suffix('.json'), {'sha256': digest, 'tables': sorted(tables),
                                              'reason': 'Own incomplete preparation; original bytes retained.'})
    if arguments.renew_initial:
        setup()
        initial = OUT / 'alumnat/accessibilitat-vilaseca.gpkg'
        expected = json.loads((OUT / 'controls/projecte-inici.json').read_text())['student_gpkg_sha256']
        assert sha(initial) == expected, 'Keep edited initial data; do not replace unfamiliar work.'
        archived = OUT / 'controls' / f'initial-before-source-revision-{time.time_ns()}.gpkg'
        initial.rename(archived)
        record(archived.with_suffix('.json'), {'sha256': expected, 'reason': 'Source-only regeneration of own unsealed inputs.'})
    if arguments.prepare:
        prepare()
    if arguments.style_start:
        style_start()
    if arguments.build:
        build()
    if arguments.style_teacher:
        style_teacher()
    if arguments.capture_config:
        capture_config(pass_id=arguments.capture_pass)
    if arguments.docs:
        documents(arguments.pdf_receipts)
    if arguments.style_cell_cost:
        style_cell_cost()
    if arguments.package:
        package()
    if arguments.verify_run:
        verify_run()
    if arguments.verify_deliverables:
        verify_deliverables()
    if arguments.seal_common:
        seal_common()
