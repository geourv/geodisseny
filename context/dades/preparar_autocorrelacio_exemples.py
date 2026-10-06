"""Reproducible C5 exploration; originals and earlier teaching bundles stay read-only.

--fetch: retain official income data/methodology on the host, with SHA-256.
--inspect: inspect retained inputs using the pinned QGIS/GDAL/PySAL runtime.
Analysis writes only to the new, unsealed autocorrelacio-20261005 destination.
"""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request
import urllib.parse
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'tmp/dades-docents/qgis/autocorrelacio-20261005'
SECTIONS = ROOT / 'tmp/dades-docents/seccions/seccions-analisi.gpkg'
PV = ROOT / 'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'
IMAGE = 'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'
SOURCES = {
    'ine-31223.csv': 'https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/31223.csv',
    'ine-31231.csv': 'https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/31231.csv',
    'ine-adrh-metodologia.pdf': 'https://www.ine.es/metodologia/metodologia_adrh.pdf',
    'ine-adrh-metadades.html': 'https://www.ine.es/dynt3/metadatos/es/RespuestaDatos.html?oe=30325',
}
SOURCE_SHA256 = {
    'ine-31223.csv': '894f8d0bd143347b7b0ad677db31d7a04c56ce26e231a85379db00304938bbf2',
    'ine-31231.csv': 'c9aaa295b835447422468a35ab316623cc917516d79b6bfe50557b23592bef38',
    'ine-adrh-metodologia.pdf': '96d2cfcddc73c3d76c232e23a1dc37ddf46fbc100de03f426043c04771ed291d',
}
SHOTS = ['eines', 'renda-parametres', 'renda-resultat', 'renda-veins', 'constanti-dades',
         'constanti-parametres', 'constanti-resultat', 'gi-parametres', 'gi-resultat']
SEED = 20261005
PERMUTATIONS = 9999


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def dump(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def fetch():
    folder = OUT / 'originals'
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / 'downloads.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for name, url in SOURCES.items():
        path = folder / name
        if path.exists():
            assert name in manifest and sha(path) == manifest[name]['sha256'], name
            if name in SOURCE_SHA256:
                assert sha(path) == SOURCE_SHA256[name]
            continue
        request = urllib.request.Request(url, headers={'User-Agent': 'Geodisseny educational preparation'})
        with urllib.request.urlopen(request, timeout=120) as response:
            assert urllib.parse.urlparse(response.url).hostname == 'www.ine.es'
            content = response.read(30_000_001)
            assert len(content) < 30_000_000
            content_type = response.headers.get('Content-Type')
        if name.endswith('.pdf'):
            assert content.startswith(b'%PDF')
        elif name.endswith('.csv'):
            assert b';' in content[:1000] and b'<html' not in content[:1000].lower()
        if name in SOURCE_SHA256:
            assert hashlib.sha256(content).hexdigest() == SOURCE_SHA256[name], f'Official snapshot changed: {name}; review a new version.'
        path.write_bytes(content)
        manifest[name] = {'url': url, 'sha256': sha(path), 'bytes': len(content),
                          'content_type': content_type, 'retrieved': '2026-10-05'}
        dump(manifest_path, manifest)
        print(name, manifest[name], flush=True)


def income_rows(name='ine-31223.csv'):
    path = OUT / 'originals' / name
    manifest = json.loads((OUT / 'downloads.json').read_text())
    assert sha(path) == manifest[path.name]['sha256']
    content = path.read_bytes()
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        text = content.decode('iso-8859-15')
    return list(csv.DictReader(io.StringIO(text), delimiter=';'))


def inspect():
    from osgeo import ogr
    import numpy
    import scipy
    import libpysal
    import esda
    ogr.UseExceptions()
    assert sha(SECTIONS) == '84d7a33bfa8dab8089bb852e447947c92a95da3bf733161663e24a2be98523af'
    for path in [SECTIONS, PV]:
        ds = ogr.Open(str(path), 0)
        for layer in ds:
            print(path.name, layer.GetName(), layer.GetFeatureCount(),
                  [f.GetName() for f in layer.schema], flush=True)
            feature = layer.GetNextFeature()
            print(dict(feature.items()), flush=True)
    rows = income_rows()
    print('Income header / first:', rows[0], 'rows:', len(rows))
    for name in rows[0]:
        values = sorted({r[name] for r in rows})
        print(name, len(values), values[:12])
    print('Versions:', {m.__name__: m.__version__ for m in [numpy, scipy, libpysal, esda]})


def analyse():
    """Use full 2024 section boundaries; never infer contiguity from display geometry."""
    from osgeo import ogr, osr, gdal
    import numpy as np
    import scipy
    from scipy.spatial.distance import cdist
    import shapely
    import libpysal
    import esda
    from libpysal.weights import Queen, Rook, KNN, DistanceBand, W
    from esda import Moran, Moran_Local, Moran_BV
    from preparar_seccions import INE_TO_CADASTRE

    assert not (OUT / 'sealed.json').exists(), 'Sealed teaching bundles are immutable.'
    ogr.UseExceptions()
    assert sha(SECTIONS) == '84d7a33bfa8dab8089bb852e447947c92a95da3bf733161663e24a2be98523af'
    assert sha(PV) == '1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'
    ds = ogr.Open(str(SECTIONS), 0)
    sections = sorted([dict(f.items()) for f in ds.GetLayerByName('seccions')], key=lambda s: s['cusec'])
    bycode = {s['cusec']: s for s in sections}
    originals = ROOT / 'tmp/dades-docents/seccions/originals'
    previous_manifest = json.loads((originals.parent / 'downloads.json').read_text())
    for name, spec in previous_manifest.items():
        assert sha(originals / name) == spec['sha256'], name
    ds = ogr.Open('/vsizip/' + str(originals / 'seccions-20240101.zip'))
    reference = osr.SpatialReference(); reference.ImportFromEPSG(25831)
    layer = ds.GetLayer(0)
    assert layer.GetSpatialRef().IsSame(reference)
    for f in layer:
        code = f['MUNICIPI'][:5] + f['DISTRICTE'].zfill(2) + f['SECCIO'].zfill(3)
        if code in bycode:
            bycode[code]['geometry'] = shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb()))
    assert len(sections) == 151 and all(s['geometry'].is_valid for s in sections)

    # INE: one selected indicator/year/section, no municipality or district totals.
    selected_income = [r for r in income_rows() if r['Periodo'] == '2023'
        and r['Indicadores de renta media y mediana'] == 'Renta neta media por persona'
        and r['Secciones'] and r['Secciones'][:5] in INE_TO_CADASTRE]
    income = {}
    for r in selected_income:
        code = r['Secciones'].split(' ', 1)[0]
        assert code not in income
        raw = r['Total'].strip()
        value = None if raw in ('', '.', '..') else float(raw.replace('.', '').replace(',', '.'))
        income[code] = {'value': value, 'raw': raw, 'name': r['Municipios'][6:]}
    missing_codes = sorted(set(bycode) - set(income))
    extra_codes = sorted(set(income) - set(bycode))
    # The time-series CSV retains historic section codes with blank 2023 rows.
    assert not missing_codes and all(income[c]['value'] is None for c in extra_codes), (missing_codes, extra_codes)
    for s in sections:
        inc = income[s['cusec']]
        s.update(renda=inc['value'], renda_raw=inc['raw'], municipi=inc['name'],
                 footprint_m2=0., area_buildings_n=0)
    population = {}
    for r in income_rows('ine-31231.csv'):
        if r['Periodo'] == '2023' and r['Indicadores demográficos'] == 'Población' and r['Secciones']:
            code = r['Secciones'].split(' ', 1)[0]
            if code in bycode:
                assert code not in population
                raw = r['Total'].strip()
                population[code] = None if raw in ('', '.', '..') else int(raw.replace('.', ''))
    assert set(population) == set(bycode)
    for s in sections:
        s['population_2024'] = population[s['cusec']]

    # Whole Building footprint assigned by a point guaranteed inside it, matching
    # the existing count denominator. This is plan area, not floor/roof area.
    geoms = [s['geometry'] for s in sections]
    tree = shapely.STRtree(geoms)
    audit = Counter()
    previous = {}
    for municipality, (dgc, _) in INE_TO_CADASTRE.items():
        archive = originals / f'cadastre-dgc-{dgc}.zip'
        with zipfile.ZipFile(archive) as z:
            name = next(n for n in z.namelist() if n.endswith('.building.gml'))
        ds = ogr.Open('/vsizip/' + str(archive) + '/' + name)
        layer = ds.GetLayerByName('Building')
        assert layer.GetSpatialRef().IsSame(reference)
        for f in layer:
            audit['input_buildings'] += 1
            raw = f.GetGeometryRef()
            if raw is None:
                audit['missing_geometry'] += 1; continue
            g = shapely.from_wkb(bytes(raw.ExportToWkb()))
            key = f['gml_id']
            signature = tuple(f[k] for k in ['beginning', 'end', 'conditionOfConstruction', 'currentUse', 'numberOfDwellings'])
            if key in previous:
                old_g, old_sig, old_m = previous[key]
                if g.equals(old_g) and signature == old_sig:
                    audit['duplicate_buildings'] += 1; continue
                assert old_m != municipality and not g.intersects(old_g), key
                audit['reused_id_distinct_municipal_objects'] += 1
            previous[key] = (g, signature, municipality)
            if not g.is_valid:
                audit['invalid_geometry'] += 1; g = shapely.make_valid(g)
            if g.is_empty:
                audit['empty_geometry'] += 1; continue
            matches = tree.query(g.representative_point(), predicate='intersects')
            if len(matches) != 1:
                audit['unmatched' if len(matches) == 0 else 'ambiguous'] += 1; continue
            if f['conditionOfConstruction'] != 'functional':
                continue
            s = sections[int(matches[0])]
            assert g.area > 0
            s['footprint_m2'] += float(g.area)
            s['area_buildings_n'] += 1
            audit['functional_assigned'] += 1
            if not s['geometry'].covers(g):
                audit['functional_crossing_section_boundary'] += 1
    assert audit['functional_assigned'] == 38689, audit
    assert all(s['area_buildings_n'] == s['functional_n'] for s in sections)
    for s in sections:
        s['kw_1000m2'] = 1000 * s['pv_edifici_kw'] / s['footprint_m2'] if s['moran_sample'] else None
        s['log_count'] = float(np.log1p(s['kw_per_100_buildings'])) if s['moran_sample'] else None
        s['log_area'] = float(np.log1p(s['kw_1000m2'])) if s['moran_sample'] else None
        s['age'] = s['age_median_exact'] if s['age_exact_n'] >= 10 else None
        s['mean_area'] = s['footprint_m2'] / s['functional_n']

    trials = []
    retained = {}

    def weights(sample, kind):
        geometry = [r['geometry'] for r in sample]
        xy = np.array([[g.centroid.x, g.centroid.y] for g in geometry])
        if kind in ('queen', 'rook'):
            w = (Queen if kind == 'queen' else Rook).from_iterable(geometry)
        elif kind == 'ties8':
            distances = cdist(xy, xy)
            np.fill_diagonal(distances, np.inf)
            cutoffs = np.sort(distances, axis=1)[:, 7]
            w = W({i: np.flatnonzero(distances[i] <= cutoffs[i] + 1e-8).tolist() for i in range(len(xy))})
        elif kind.startswith('knn'):
            w = KNN.from_array(xy, k=int(kind[3:]))
        elif kind.startswith('radius'):
            w = DistanceBand(xy, threshold=float(kind[6:]), binary=True)
        else:
            raise ValueError(kind)
        w.transform = 'r'
        matrix, _ = w.full()
        assert np.allclose(np.diag(matrix), 0)
        distances = cdist(xy, xy)
        diagnostic = {'islands': [sample[i]['key'] for i in w.islands],
            'components': int(w.n_components), 'degree_min': int(w.min_neighbors),
            'degree_max': int(w.max_neighbors), 'links': int(np.count_nonzero(matrix)),
            'longest_link_m': float(distances[matrix > 0].max()),
            'asymmetric_pairs': len(w.asymmetry(intrinsic=False))}
        if kind.startswith('knn'):
            np.fill_diagonal(distances, np.inf)
            kth = np.sort(distances, axis=1)[:, int(kind[3:]) - 1]
            diagnostic['cutoff_tie_rows'] = int(sum(np.count_nonzero(np.isclose(row, d, rtol=0, atol=1e-8)) > 1
                for row, d in zip(distances, kth)))
            diagnostic['coincident_extra_records'] = len(xy) - len(np.unique(xy, axis=0))
        return w, diagnostic

    def test(sample, field, kind, ident, keep_local=False):
        y = np.array([r[field] for r in sample], dtype=float)
        assert np.all(np.isfinite(y)) and np.var(y) > 0
        w, diagnostic = weights(sample, kind)
        result = {'id': ident, 'field': field, 'weights': kind, 'n': len(sample), **diagnostic}
        if w.islands:
            result['not_calculated'] = 'Isolated units retained as a diagnostic; this trial has no inferential result.'
            trials.append(result); return
        z = y - y.mean()
        matrix, _ = w.full()
        direct = len(y) / matrix.sum() * z @ matrix @ z / (z @ z)
        np.random.seed(SEED)
        statistic = Moran(y, w, permutations=PERMUTATIONS)
        assert np.isclose(statistic.I, direct, atol=1e-12)
        # Direction fixed in advance: positive association. Do not select the
        # smaller tail after seeing the observed sign.
        p_positive = (1 + np.count_nonzero(statistic.sim >= statistic.I)) / (PERMUTATIONS + 1)
        result.update(I=float(statistic.I), expected_I=float(statistic.EI),
            p_positive=float(p_positive), esda_p_sim=float(statistic.p_sim),
            mean=float(y.mean()), min=float(y.min()), max=float(y.max()))
        if keep_local:
            local = Moran_Local(y, w, permutations=PERMUTATIONS, seed=SEED,
                                n_jobs=1, keep_simulations=False)
            p = np.asarray(local.p_sim)
            order = np.argsort(p)
            accepted = p[order] <= .05 * np.arange(1, len(p) + 1) / len(p)
            cutoff = float(p[order][np.where(accepted)[0][-1]]) if np.any(accepted) else -1.
            labels = {1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'}
            lag = libpysal.weights.lag_spatial(w, y)
            standardized = z / y.std(ddof=0)
            lag_z = libpysal.weights.lag_spatial(w, standardized)
            items = []
            for i, row in enumerate(sample):
                items.append({'key': row['key'], 'value': float(y[i]), 'z': float(standardized[i]),
                    'lag': float(lag[i]), 'lag_z': float(lag_z[i]), 'I_local': float(local.Is[i]),
                    'p_sim': float(p[i]), 'quadrant': labels[int(local.q[i])],
                    'fdr': bool(p[i] <= cutoff), 'neighbors': [sample[j]['key'] for j in w.neighbors[i]]})
            result['local_nominal'] = dict(Counter(x['quadrant'] for x in items if x['p_sim'] < .05))
            result['local_fdr'] = dict(Counter(x['quadrant'] for x in items if x['fdr']))
            result['fdr_cutoff'] = cutoff
            retained[ident] = items
        trials.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return w

    for s in sections:
        s['key'] = s['cusec']
    fields = ['renda', 'age', 'log_count', 'log_area', 'mean_area']
    for field in fields:
        sample = [s for s in sections if s[field] is not None]
        for kind in ['queen', 'rook', 'knn4', 'knn8']:
            test(sample, field, kind, f'{field}-{kind}', keep_local=kind == 'queen')
    common = [s for s in sections if s['association_sample'] and s['renda'] is not None]
    w, _ = weights(common, 'queen')
    assert not w.islands
    association = []
    association_rows = []
    normalized_common = {}
    for field in ['age', 'renda', 'log_count', 'log_area', 'mean_area']:
        values = np.array([s[field] for s in common])
        normalized_common[field] = (values - values.mean()) / values.std(ddof=0)
    for i, row in enumerate(common):
        association_rows.append({'key': row['key'], **{f: float(values[i]) for f, values in normalized_common.items()},
            'lag_log_count': float(libpysal.weights.lag_spatial(w, normalized_common['log_count'])[i])})
    for x, y in [('age', 'log_count'), ('age', 'log_area'), ('renda', 'log_count'), ('renda', 'log_area'),
                 ('mean_area', 'log_count'), ('mean_area', 'log_area')]:
        xv, yv = [np.array([s[f] for s in common]) for f in (x, y)]
        np.random.seed(SEED)
        biv = Moran_BV(xv, yv, w, permutations=PERMUTATIONS)
        b, a = np.polyfit(xv, yv, 1)
        residual = yv - (a + b * xv)
        np.random.seed(SEED)
        res = Moran(residual, w, permutations=PERMUTATIONS)
        association.append({'x': x, 'y': y, 'n': len(common),
            'pearson_r': float(np.corrcoef(xv, yv)[0, 1]),
            'spearman_r': float(scipy.stats.spearmanr(xv, yv).statistic),
            'bivariate_I_x_lag_y': float(biv.I),
            'residual_I': float(res.I), 'residual_p_sim': float(res.p_sim)})
    print('Associations:', json.dumps(association, ensure_ascii=False), flush=True)

    points = []
    ds = ogr.Open(str(PV), 0)
    layer = ds.GetLayerByName('autoconsum_tarragones')
    layer.SetAttributeFilter('CODI_MUN = 430477')
    intervals = {'Pot <= 5kW': (0, 2.5, 5), '5 < Pot <= 25 kW': (5, 15, 25),
                 '25 < Pot <= 100 kW': (25, 62.5, 100)}
    for f in layer:
        g = shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb()))
        if g.geom_type == 'MultiPoint':
            assert len(g.geoms) == 1; g = g.geoms[0]
        p = f['POT_KW']
        row = {'key': f['gml_id'], 'pot_kw': p, 'interval': f['INTERVAL'], 'geometry': g}
        values = (p, p, p) if p is not None else intervals[f['INTERVAL']]
        for name, value in zip(('inf', 'mid', 'sup'), values):
            row[name] = float(np.log1p(p if p is not None else value))
        row['log_kw'] = float(np.log1p(p)) if p is not None else None
        points.append(row)
    points.sort(key=lambda p: p['key'])
    known = [p for p in points if p['pot_kw'] is not None]
    assert len(points) == 124 and len(known) == 98
    for kind in ['knn4', 'knn8', 'knn12', 'radius500', 'radius1000']:
        test(known, 'log_kw', kind, f'constanti-known-{kind}', keep_local=kind == 'knn8')
    for field in ['inf', 'mid', 'sup']:
        test(points, field, 'knn8', f'constanti-{field}-knn8', keep_local=field == 'mid')
    test(known, 'log_kw', 'ties8', 'constanti-known-all-cutoff-ties')
    test(list(reversed(known)), 'log_kw', 'knn8', 'constanti-known-reverse-order')
    test(known, 'pot_kw', 'knn8', 'constanti-known-raw-kw')

    report = {'seed': SEED, 'permutations': PERMUTATIONS,
        'global_p_convention': 'Positive-association upper tail chosen in advance; (1 + sum(sim >= I))/(B + 1). esda_p_sim also retained for comparison.',
        'local_p_convention': 'esda.Moran_Local.p_sim; BH alpha .05 as an exploratory sensitivity, not a universal guarantee under dependence.',
        'runtime': {'image': IMAGE, 'gdal': gdal.VersionInfo(), 'numpy': np.__version__,
                    'scipy': scipy.__version__, 'libpysal': libpysal.__version__, 'esda': esda.__version__},
        'sources': json.loads((OUT / 'downloads.json').read_text()),
        'inherited_sources': previous_manifest,
        'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in [SECTIONS, PV]},
        'income_join': {'n': len(sections), 'missing_codes': missing_codes, 'unused_blank_codes': extra_codes,
                       'null_values': [s['cusec'] for s in sections if s['renda'] is None],
                       'population_under_100_or_missing': [s['cusec'] for s in sections if s['population_2024'] is None or s['population_2024'] < 100]},
        'building_audit': dict(audit), 'footprint_total_m2': sum(s['footprint_m2'] for s in sections),
        'trials': trials, 'association': association, 'association_rows': association_rows, 'local': retained,
        'sections': [{k: v for k, v in s.items() if k != 'geometry'} for s in sections],
        'points': [{**{k: v for k, v in p.items() if k != 'geometry'},
                    'xy': [p['geometry'].x, p['geometry'].y]} for p in points]}
    dump(OUT / 'analysis.json', report)
    # Full geometry for QGIS; simplified display geometry remains separate.
    for name, rows in [('seccions', sections), ('constanti', points)]:
        dump(OUT / f'{name}.geojson', {'type': 'FeatureCollection',
             'crs': {'type': 'name', 'properties': {'name': 'EPSG:25831'}},
             'features': [{'type': 'Feature', 'properties': {k: v for k, v in r.items() if k != 'geometry'},
                           'geometry': shapely.geometry.mapping(r['geometry'])} for r in rows]})
    print('Income join:', report['income_join'], 'Building audit:', dict(audit), flush=True)


def prepare_qgis():
    """Execute the installed Processing provider, retain outputs and portable projects."""
    global _APP
    import numpy as np
    from qgis.core import (QgsApplication, QgsProject, QgsCoordinateReferenceSystem,
        QgsVectorLayer, QgsVectorFileWriter, QgsField, QgsFeature, QgsGeometry, QgsPointXY,
        QgsMarkerSymbol, QgsFillSymbol, QgsLineSymbol, QgsCategorizedSymbolRenderer,
        QgsRendererCategory, QgsGraduatedSymbolRenderer, QgsRendererRange, QgsRasterLayer,
        QgsPalLayerSettings, QgsVectorLayerSimpleLabeling, QgsTextFormat, QgsTextBufferSettings,
        QgsReferencedRectangle, QgsProcessingContext, QgsProcessingFeedback, Qgis)
    from qgis.PyQt.QtCore import QVariant
    from qgis.PyQt.QtGui import QColor
    import libpysal
    import esda
    from osgeo import gdal

    assert not (OUT / 'sealed.json').exists()
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _APP = QgsApplication([], False); _APP.initQgis()
    sys.path.insert(0, '/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing
    lock = json.loads((ROOT / 'context/qgis/plugins-lock.json').read_text())
    cache = ROOT / 'tmp/qgis/cache/plugins/sha256-950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc-139383569f94'
    sys.path.insert(0, str(cache))
    from HotSpotAnalysis_v3.processing.provider import HotspotProvider
    provider = HotspotProvider(); QgsApplication.processingRegistry().addProvider(provider)
    report = json.loads((OUT / 'analysis.json').read_text())
    controls = {'image': IMAGE, 'qgis': Qgis.QGIS_VERSION, 'analysis_sha256': sha(OUT / 'analysis.json'),
        'algorithms': [], 'outputs': {}, 'manual_click_by_click': False,
        'global_moran_algorithms': [a.id() for a in QgsApplication.processingRegistry().algorithms()
                                    if 'moran' in (a.id() + a.displayName()).lower()]}
    project = QgsProject.instance()
    project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    target = OUT / 'autocorrelacio.gpkg'
    first = True

    def save(layer, name, title):
        nonlocal first
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = 'GPKG'; options.layerName = name
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile if first else QgsVectorFileWriter.CreateOrOverwriteLayer
        result = QgsVectorFileWriter.writeAsVectorFormatV3(layer, str(target), project.transformContext(), options)
        assert result[0] == QgsVectorFileWriter.NoError, result
        first = False
        output = QgsVectorLayer(str(target) + '|layername=' + name, title, 'ogr')
        assert output.isValid() and output.featureCount() == layer.featureCount()
        return output

    def memory(geometry, fields, rows):
        layer = QgsVectorLayer(f'{geometry}?crs=EPSG:25831', 'Preparació', 'memory')
        layer.dataProvider().addAttributes([QgsField(n, t) for n, t in fields]); layer.updateFields()
        features = []
        for geometry, attributes in rows:
            f = QgsFeature(layer.fields()); f.setGeometry(geometry); f.setAttributes(attributes); features.append(f)
        assert layer.dataProvider().addFeatures(features)[0]
        layer.updateExtents(); return layer

    section_source = QgsVectorLayer(str(OUT / 'seccions.geojson'), 'S', 'ogr')
    assert section_source.isValid()
    section_geoms = {f['cusec']: f.geometry() for f in section_source.getFeatures()}
    reference = {r['key']: r for r in report['local']['renda-queen']}
    cases = {'4314807013': 'A', '4314808012': 'B', '4304701002': 'C'}
    names = [('cusec', QVariant.String), ('municipi', QVariant.String), ('renda', QVariant.Double),
        ('pop2024', QVariant.Int), ('edat', QVariant.Double), ('n_edif', QVariant.Int), ('n_exact', QVariant.Int),
        ('petjada', QVariant.Double), ('kw_pub', QVariant.Double), ('kw100ed', QVariant.Double),
        ('kw1000m', QVariant.Double), ('log_pot', QVariant.Double), ('log_area', QVariant.Double),
        ('area_mitj', QVariant.Double), ('mostra', QVariant.Int), ('p_ref', QVariant.Double),
        ('q_ref', QVariant.String), ('fdr_ref', QVariant.Int), ('cas', QVariant.String)]
    rows = []
    for s in report['sections']:
        r = reference[s['key']]
        rows.append((section_geoms[s['key']], [s['key'], s['municipi'], s['renda'], s['population_2024'],
            s['age'], s['functional_n'], s['age_exact_n'], s['footprint_m2'], s['pv_edifici_kw'],
            s['kw_per_100_buildings'] if s['moran_sample'] else None, s['kw_1000m2'], s['log_count'],
            s['log_area'], s['mean_area'], int(s['association_sample']), r['p_sim'], r['quadrant'],
            int(r['fdr']), cases.get(s['key'], '')]))
    base = save(memory('MultiPolygon', names, rows), 'seccions', 'Renda 2023 · 151 seccions')
    shape_options = QgsVectorFileWriter.SaveVectorOptions()
    shape_options.driverName = 'ESRI Shapefile'; shape_options.fileEncoding = 'UTF-8'
    shape_path = OUT / 'renda.shp'
    result = QgsVectorFileWriter.writeAsVectorFormatV3(base, str(shape_path), project.transformContext(), shape_options)
    assert result[0] == QgsVectorFileWriter.NoError, result
    shape = QgsVectorLayer(str(shape_path), 'Renda 2023 · 151 seccions', 'ogr'); assert shape.isValid()
    shape_ids = [f['cusec'] for f in shape.getFeatures()]
    assert shape_ids == [s['key'] for s in report['sections']]
    w = libpysal.weights.Queen.from_shapefile(str(shape_path)); w.transform = 'r'
    assert all({shape_ids[j] for j in w.neighbors[i]} == set(reference[key]['neighbors']) for i, key in enumerate(shape_ids))
    y = np.array([f['renda'] for f in shape.getFeatures()])
    np.random.seed(SEED)
    global_result = esda.Moran(y, w, permutations=PERMUTATIONS)
    expected = next(r for r in report['trials'] if r['id'] == 'renda-queen')
    assert np.isclose(global_result.I, expected['I'], atol=1e-12)
    controls['shapefile_queen_global_I'] = float(global_result.I)
    controls['shapefile_contacts_equal_full_originals'] = True

    known = [p for p in report['points'] if p['pot_kw'] is not None]
    point_names = [('gml_id', QVariant.String), ('pot_kw', QVariant.Double), ('log_kw', QVariant.Double), ('cas', QVariant.String)]
    point_rows = [(QgsGeometry.fromPointXY(QgsPointXY(*p['xy'])), [p['key'], p['pot_kw'], p['log_kw'], 'A' if p['pot_kw'] == 450 else '']) for p in known]
    points = save(memory('Point', point_names, point_rows), 'constanti', 'Constantí · 98 potències publicades')

    params = {'WEIGHTS_TYPE': 2, 'OPTIMIZE': False, 'BINARY_WEIGHTS': True, 'DISTANCE_METRIC': 0,
              'ROW_STANDARDIZE': True, 'PERMUTATIONS': PERMUTATIONS, 'TWO_TAILED': False}

    def run(ident, source, field, name, title, overrides=None):
        parameters = {**params, **(overrides or {}), 'INPUT': source, 'FIELD': field, 'OUTPUT': 'memory:'}
        algorithm = QgsApplication.processingRegistry().algorithmById(ident)
        assert algorithm and set(parameters) <= {p.name() for p in algorithm.parameterDefinitions()}
        context = QgsProcessingContext(); context.setProject(project)
        feedback = QgsProcessingFeedback()
        output = processing.run(ident, parameters, context=context, feedback=feedback)['OUTPUT']
        assert output.featureCount() == source.featureCount()
        result = save(output, name, title)
        records = []
        for f in result.getFeatures():
            assert np.isfinite(float(f['Z_score'])) and 0 <= f['p_value'] <= 1
            key = f['cusec'] if 'cusec' in f.fields().names() else f['gml_id']
            q = int(f['q_value']) if 'q_value' in f.fields().names() else None
            records.append({'key': key, 'Z_score': float(f['Z_score']), 'p_value': float(f['p_value']), 'q_value': q})
        controls['algorithms'].append({'id': ident, 'parameters': {k: source.name() if k == 'INPUT' else v for k, v in parameters.items()},
            'feedback': feedback.textLog(), 'layer': name, 'n': len(records)})
        controls['outputs'][name] = records
        return result

    lisa = run('hotspotanalysis:moranlocal', shape, 'renda', 'renda_lisa', 'Renda · Moran local nominal')
    point_lisa = run('hotspotanalysis:moranlocal', points, 'log_kw', 'constanti_lisa', 'Constantí · Moran local nominal',
                     {'WEIGHTS_TYPE': 1, 'KNN_K': 8})
    gi = run('hotspotanalysis:getisordgistar', shape, 'renda', 'renda_gi', 'Renda · Getis–Ord Gi*',
             {'ROW_STANDARDIZE': False, 'TWO_TAILED': True})
    labels = {1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'}
    for name, source_ref in [('renda_lisa', report['local']['renda-queen']),
                              ('constanti_lisa', report['local']['constanti-known-knn8'])]:
        ref = {x['key']: x for x in source_ref}
        assert all(labels[x['q_value']] == ref[x['key']]['quadrant'] for x in controls['outputs'][name])
        controls[name + '_nominal_counts'] = dict(Counter(labels[x['q_value']] if x['p_value'] < .05 else 'NS' for x in controls['outputs'][name]))
        controls[name + '_p_max_difference_reference'] = max(abs(x['p_value'] - ref[x['key']]['p_sim']) for x in controls['outputs'][name])
    controls['gi_nominal_counts'] = dict(Counter(('Alt' if x['Z_score'] > 0 else 'Baix') if x['p_value'] < .05 else 'NS' for x in controls['outputs']['renda_gi']))

    palette = {'HH': '#b52e45', 'LL': '#276a98', 'HL': '#e5a275', 'LH': '#9bc9de', 'NS': '#dedfe0'}
    def symbol(layer, color):
        if layer.geometryType() == Qgis.GeometryType.Point:
            return QgsMarkerSymbol.createSimple({'color': color, 'outline_color': 'white', 'outline_width': '.15', 'size': '3.4'})
        return QgsFillSymbol.createSimple({'color': color, 'outline_color': 'white', 'outline_width': '.16'})
    def category_style(layer, expression, entries):
        layer.setRenderer(QgsCategorizedSymbolRenderer(expression,
            [QgsRendererCategory(key, symbol(layer, color), label) for key, color, label in entries]))
        layer.saveStyleToDatabase('docent', 'Estil docent explícit; llindar nominal, no FDR.', True, '')
    expression = "CASE WHEN \"p_value\" >= 0.05 THEN 'NS' WHEN \"q_value\" = 1 THEN 'HH' WHEN \"q_value\" = 2 THEN 'LH' WHEN \"q_value\" = 3 THEN 'LL' ELSE 'HL' END"
    entries = [(k, palette[k], t) for k, t in [('HH', 'Alt–alt (HH)'), ('LL', 'Baix–baix (LL)'),
               ('HL', 'Alt–baix (HL)'), ('LH', 'Baix–alt (LH)'), ('NS', 'No destacat (p ≥ 0,05)')]]
    for layer in [lisa, point_lisa]:
        category_style(layer, expression, entries)
    category_style(gi, "CASE WHEN \"p_value\" >= 0.05 THEN 'NS' WHEN \"Z_score\" > 0 THEN 'HH' ELSE 'LL' END",
                   [('HH', palette['HH'], 'Concentració alta'), ('LL', palette['LL'], 'Concentració baixa'), ('NS', palette['NS'], 'No destacat (p ≥ 0,05)')])

    def graduated(layer, field, cuts, colors, units):
        ranges = [QgsRendererRange(lo, hi, symbol(layer, color), f'{lo:g}–{hi:g} {units}')
                  for lo, hi, color in zip(cuts[:-1], cuts[1:], colors)]
        layer.setRenderer(QgsGraduatedSymbolRenderer(field, ranges))
        layer.saveStyleToDatabase('docent', 'Intervals fixos i unitats explícites.', True, '')
    graduated(base, 'renda', [7000, 11000, 15000, 19000, 23000, 28000],
              ['#fff0ba', '#f8cf6b', '#ec9853', '#cd5a41', '#8d2040'], '€/persona')
    graduated(points, 'pot_kw', [0, 5, 25, 100, 500], ['#78c7d0', '#259caf', '#14608a', '#542b74'], 'kW')

    def label(layer, field='cas', size=12):
        settings = QgsPalLayerSettings(); settings.fieldName = field
        fmt = QgsTextFormat(); fmt.setSize(size); fmt.setColor(QColor('#122c3a'))
        buffer = QgsTextBufferSettings(); buffer.setEnabled(True); buffer.setColor(QColor('white')); buffer.setSize(1)
        fmt.setBuffer(buffer); settings.setFormat(fmt)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(settings)); layer.setLabelsEnabled(True)
    for layer in [base, lisa, points, point_lisa]:
        label(layer); layer.saveStyleToDatabase('docent', 'Estil docent amb casos A/B/C.', True, '')
    base.saveNamedStyle(str(OUT / 'renda.qml'))
    shape.loadNamedStyle(str(OUT / 'renda.qml'))

    neighbor_codes = reference['4314807013']['neighbors']
    neighbor_rows = []
    for key, text in [('4314807013', 'A'), *zip(neighbor_codes, ['1', '2', '3'])]:
        r = reference[key]
        neighbor_rows.append((section_geoms[key], [key, text, r['value'], 'A' if text == 'A' else 'Veí']))
    neighbors = save(memory('MultiPolygon', [('cusec', QVariant.String), ('etiqueta', QVariant.String),
        ('renda', QVariant.Double), ('grup', QVariant.String)], neighbor_rows), 'renda_veins', 'A i els tres veïns queen')
    category_style(neighbors, 'grup', [('A', '#003366', 'A · secció estudiada'), ('Veí', '#91bdd5', 'Tres veïns queen')])
    label(neighbors, 'etiqueta', 14); neighbors.saveStyleToDatabase('docent', 'A i els seus contactes.', True, '')
    point_ref = {r['key']: r for r in report['local']['constanti-known-knn8']}
    point_byid = {p['key']: p for p in known}
    a = next(p for p in known if p['pot_kw'] == 450)
    lines = [(QgsGeometry.fromPolylineXY([QgsPointXY(*a['xy']), QgsPointXY(*point_byid[k]['xy'])]), [i + 1])
             for i, k in enumerate(point_ref[a['key']]['neighbors'])]
    links = save(memory('LineString', [('ordre', QVariant.Int)], lines), 'veins_punt_a', 'Vuit veïns del punt A')
    links.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color': '#b52e45', 'line_width': '.6'}))
    links.saveStyleToDatabase('docent', 'Veïnatge kNN8 del registre de 450 kW.', True, '')

    ortho_source = ROOT / 'tmp/dades-docents/qgis/punts-municipals-20261004/ortofoto.tif'
    shutil.copyfile(ortho_source, OUT / 'ortofoto.tif')
    ortho = QgsRasterLayer(str(OUT / 'ortofoto.tif'), 'Ortofoto ICGC 2025')
    assert ortho.isValid(); ortho.renderer().setOpacity(.55)
    ortho.saveNamedStyle(str(OUT / 'ortofoto.qml'))
    limits_source = QgsVectorLayer(str(ROOT / 'tmp/dades-docents/qgis/punts-municipals-20261004/municipis.gpkg') + '|layername=limits', 'Límits', 'ogr')
    limits_source.setSubsetString("\"CODIMUNI\" = '430477'")
    limits = save(limits_source, 'limit_constanti', 'Límit de Constantí')
    limits.renderer().setSymbol(QgsFillSymbol.createSimple({'color': '0,0,0,0', 'outline_color': '#5c6267', 'outline_width': '.4'}))
    limits.saveStyleToDatabase('docent', 'Context municipal.', True, '')

    def project_file(filename, layers, visible, extent):
        project.clear(); project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for layer in reversed(layers):
            project.addMapLayer(layer.clone())
        for node in project.layerTreeRoot().findLayers():
            node.setItemVisibilityChecked(node.layer().name() in visible)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(extent, project.crs()))
        project.setFileName(str(OUT / filename)); assert project.write()
    project_file('01-renda.qgz', [neighbors, lisa, gi, shape], [shape.name()], shape.extent())
    project_file('02-constanti.qgz', [point_lisa, points, links, limits, ortho],
                 [point_lisa.name(), limits.name(), ortho.name()], limits.extent())
    project.clear()
    dump(OUT / 'qgis-controls.json', controls)
    print(json.dumps({k: v for k, v in controls.items() if k != 'outputs'}, ensure_ascii=False, indent=2), flush=True)


def record_figures():
    """Small section-level inputs only; individual ICAEN records remain private."""
    report = json.loads((OUT / 'analysis.json').read_text())
    result = {k: report[k] for k in ['seed', 'permutations', 'global_p_convention', 'local_p_convention',
        'runtime', 'sources', 'source_sha256', 'income_join', 'building_audit', 'footprint_total_m2',
        'trials', 'association', 'association_rows', 'sections']}
    result['local'] = {k: v for k, v in report['local'].items() if not k.startswith('constanti')}
    for trial in result['trials']:
        if trial['id'].startswith('constanti'):
            trial['island_count'] = len(trial.pop('islands'))
    qgis = json.loads((OUT / 'qgis-controls.json').read_text())
    result['qgis'] = {k: v for k, v in qgis.items() if k != 'outputs'}
    final = json.loads((OUT / 'verification.json').read_text())
    for row in result['sections']:
        row['label_xy'] = final['label_xy'][row['key']]
    result['analysis_sha256'] = sha(OUT / 'analysis.json')
    result['attribution'] = 'INE ADRH 2023; ICGC/Idescat seccions 2024; Dirección General del Catastro 2026; ICAEN. Elaboració i càlcul propis.'
    dump(ROOT / 'context/inputs/autocorrelacio-exemples.json', result)


def finalise():
    """Inspect saved outputs and save presentation metadata without rerunning inference."""
    global _APP
    import numpy as np
    from qgis.core import QgsApplication, QgsVectorLayer, QgsProject, QgsDataProvider
    import libpysal
    from libpysal.weights import Queen
    from esda import Moran
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _APP = QgsApplication.instance() or QgsApplication([], False); _APP.initQgis()
    report = json.loads((OUT / 'analysis.json').read_text())
    controls = json.loads((OUT / 'qgis-controls.json').read_text())
    assert controls['analysis_sha256'] == sha(OUT / 'analysis.json')
    target = OUT / 'autocorrelacio.gpkg'
    options = QgsVectorLayer.LayerOptions(); options.forceReadOnly = True
    layer = QgsVectorLayer(str(target) + '|layername=seccions', 'S', 'ogr', options)
    assert layer.isValid() and layer.featureCount() == 151
    saved = {f['cusec']: f for f in layer.getFeatures()}
    assert set(saved) == {r['key'] for r in report['sections']}
    for r in report['sections']:
        assert np.isclose(saved[r['key']]['petjada'], r['footprint_m2'], atol=1e-8)
        assert saved[r['key']]['renda'] == r['renda']
    label_xy = {key: [f.geometry().pointOnSurface().asPoint().x(), f.geometry().pointOnSurface().asPoint().y()]
                for key, f in saved.items()}
    layer.saveNamedStyle(str(OUT / 'renda.qml'))
    refs = report['local']['renda-queen']; bycode = {r['key']: r for r in refs}
    y = np.array([r['value'] for r in refs]); n = len(y)
    gi = {r['key']: r for r in controls['outputs']['renda_gi']}
    errors = []
    for row in refs:
        values = [row['value'], *[bycode[k]['value'] for k in row['neighbors']]]
        k = len(values)
        direct_z = (sum(values) - y.mean() * k) / (y.std(ddof=0) * np.sqrt((n*k-k*k)/(n-1)))
        errors.append(abs(direct_z - gi[row['key']]['Z_score']))
    assert max(errors) < 1e-10, max(errors)
    smoke = Moran([1, 1, 4, 4], libpysal.weights.lat2W(1, 4), permutations=0)
    assert np.isclose(smoke.I, .5)
    projects = []
    project = QgsProject.instance()
    for name in ['01-renda.qgz', '02-constanti.qgz']:
        assert project.read(str(OUT / name))
        layers = list(project.mapLayers().values())
        assert layers and all(l.isValid() for l in layers)
        if name == '01-renda.qgz':
            for item in layers:
                if item.name() == 'Renda 2023 · 151 seccions':
                    item.setDataSource(str(OUT / 'renda.shp'), item.name(), 'ogr', QgsDataProvider.ProviderOptions())
                    item.loadNamedStyle(str(OUT / 'renda.qml'))
                    assert item.isValid()
            assert project.write()
        projects.append({'file': name, 'layers': len(layers), 'valid': True})
        project.clear()
    result = {'analysis_sha256': sha(OUT / 'analysis.json'), 'qgis_controls_sha256': sha(OUT / 'qgis-controls.json'),
        'label_xy': label_xy, 'gi_star_direct_max_abs_error': max(errors), 'dependency_smoke_I': float(smoke.I),
        'projects': projects, 'input_hashes_unchanged': {str(p.relative_to(ROOT)): sha(p) for p in [SECTIONS, PV]}}
    assert result['input_hashes_unchanged'] == report['source_sha256']
    dump(OUT / 'verification.json', result)
    print({k: v for k, v in result.items() if k != 'label_xy'}, flush=True)


def verify(directory, report_path):
    """Open a relocated bundle readonly/offline; no access to the original workspace is needed."""
    global _APP
    import sqlite3
    import numpy as np
    from qgis.core import QgsApplication, QgsProject, QgsVectorLayer
    directory = Path(directory)
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _APP = QgsApplication([], False); _APP.initQgis()
    hashes = {p.name: sha(p) for p in directory.iterdir() if p.suffix in ('.gpkg', '.tif', '.qgz', '.shp', '.shx', '.dbf', '.prj', '.cpg', '.qml')}
    project = QgsProject.instance(); results = []
    for filename, expected_count in [('01-renda.qgz', 4), ('02-constanti.qgz', 5)]:
        assert project.read(str(directory / filename))
        layers = list(project.mapLayers().values())
        assert len(layers) == expected_count and all(layer.isValid() for layer in layers)
        for layer in layers:
            source = Path(layer.source().split('|')[0]).resolve()
            assert source.is_relative_to(directory.resolve()), (filename, source)
        results.append({'project': filename, 'valid_layers': len(layers), 'relative_local_sources': True})
        project.clear()
    db = sqlite3.connect(f'file:{directory / "autocorrelacio.gpkg"}?mode=ro', uri=True)
    assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert db.execute('SELECT COUNT(*), COUNT(DISTINCT cusec), COUNT(renda) FROM seccions').fetchone() == (151, 151, 151)
    assert db.execute('SELECT COUNT(*), SUM(pot_kw) FROM constanti').fetchone() == (98, 2770.)
    for layer, count in [('renda_lisa', 151), ('renda_gi', 151), ('constanti_lisa', 98)]:
        assert db.execute(f'SELECT COUNT(*) FROM {layer}').fetchone()[0] == count
        assert db.execute(f'SELECT COUNT(*) FROM {layer} WHERE p_value IS NULL OR p_value < 0 OR p_value > 1').fetchone()[0] == 0
    db.close()
    assert all(sha(directory / name) == digest for name, digest in hashes.items())
    result = {'ok': True, 'offline': True, 'readonly': True, 'mounted_at': str(directory),
              'projects': results, 'hashes': hashes}
    dump(report_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


def docs():
    """Build standalone private handouts through the pinned public Pandoc image."""
    assert not (OUT / 'sealed.json').exists()
    for name in ['captures', 'reproduccio']:
        (OUT / name).mkdir(exist_ok=True)
    for shot in SHOTS:
        receipt_path = ROOT / f'context/qgis/manifests/c5-{shot}.yml'
        receipt = json.loads(receipt_path.read_text())
        assert receipt['ok'] and not receipt['warnings'] and receipt['image_digest'] == IMAGE
        assert receipt['backend'] == 'x11' and receipt['device_pixel_ratio'] == 1
        for suffix in ['.png', '.annotations.svg']:
            shutil.copyfile(ROOT / f'assets/captures/c5-{shot}{suffix}', OUT / f'captures/c5-{shot}{suffix}')
        shutil.copyfile(receipt_path, OUT / 'captures' / receipt_path.name)
    for source, name in [('context/practiques/autocorrelacio-exemples.md', 'GUIA'),
                         ('context/practiques/autocorrelacio-exemples-docent.md', 'SOLUCIONS')]:
        shutil.copyfile(ROOT / source, OUT / f'{name}.md')
    for source in [Path(__file__), ROOT / 'context/qgis/autocorrelacio-exemples.yml',
                   ROOT / 'context/qgis/autocorrelacio-exemples.md', ROOT / 'context/dades/preparar_seccions.py']:
        shutil.copyfile(source, OUT / 'reproduccio' / source.name)
    (OUT / 'COMENCA-AQUI.txt').write_text(
        'Autocorrelació espacial — Benito Zaragozí\n\n'
        'Llegeix GUIA.pdf. Obre 01-renda.qgz o 02-constanti.qgz i desa una còpia a treball/.\n'
        'Els camins són relatius: conserva el paquet complet. Crea la connexió GeoPackage al teu perfil.\n'
        'Els resultats conservats no substitueixen les teves execucions: desa-les amb altres noms.\n'
        'SOLUCIONS.pdf i els JSON documenten dades, estadístics, matrius i proves descartades.\n'
        'La renda és de 2023, les seccions de 2024, el Cadastre de 2026.\n'
        'ICAEN: extracció 28/09/2026; data efectiva no verificada.\n'
        'Els scripts de reproduccio/ necessiten el repositori i els originals privats descrits.\n')
    image = 'ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:9e0b3a45753c170b795e9a9d6df61580085c113436beac5bf6c8de69b6562097'
    for name in ['GUIA', 'SOLUCIONS']:
        command = ['docker', 'run', '--rm', '--pull=never', '--network', 'none',
            '--user', f'{os.getuid()}:{os.getgid()}', '--env', 'HOME=/tmp', '--env', 'SOURCE_DATE_EPOCH=0',
            '--mount', f'type=bind,src={OUT},dst=/data', '--workdir', '/data', '--entrypoint', 'pandoc', image,
            name + '.md', '-o', name + '.pdf', '--pdf-engine=xelatex', '-V', 'fontfamily=fontspec',
            '-V', 'mainfont=DejaVu Sans', '-V', 'monofont=DejaVu Sans Mono', '-V', 'fontsize=11pt',
            '-V', 'geometry=a4paper,margin=18mm']
        if name == 'GUIA':
            command += ['--toc', '--toc-depth=2']
        subprocess.run(command, check=True)


def stage_revision():
    """New documentary revision: reuse sealed data/inference/captures byte for byte."""
    previous = ROOT / 'tmp/dades-docents/qgis/autocorrelacio-20261005'
    archive = ROOT / 'tmp/dades-docents/practica-autocorrelacio-20261005.zip'
    assert sha(archive) == '86f6bcbb5443bbd9586b5a62ca27dff94b27150365e9c345c4c6176c5f4098f3'
    assert OUT.name == 'autocorrelacio-20261005-r2' and not OUT.exists()
    manifest = json.loads((previous / 'sealed.json').read_text())
    assert all(sha(previous / f['path']) == f['sha256'] for f in manifest['files'])
    shutil.copytree(previous, OUT, ignore=shutil.ignore_patterns('sealed.json', 'GUIA.*', 'SOLUCIONS.*',
        'reproduccio', 'captures', 'portabilitat.json', 'verificacio-pdf.json', 'COMENCA-AQUI.txt', '*~'))
    dump(OUT / 'lineage.json', {'parent_zip': str(archive.relative_to(ROOT)), 'parent_sha256': sha(archive),
        'reason': 'Handout page breaks and copyable SQL labels; numerical data and capture sources unchanged.',
        'reused_data_sha256': {name: sha(OUT / name) for name in ['analysis.json', 'qgis-controls.json', 'autocorrelacio.gpkg', 'renda.shp']}})


def package():
    """Seal a new private review ZIP only after portability and PDF checks."""
    assert not (OUT / 'sealed.json').exists()
    portable = json.loads((OUT / 'portabilitat.json').read_text()); assert portable['ok']
    assert all(sha(OUT / name) == digest for name, digest in portable['hashes'].items())
    pdfs = json.loads((OUT / 'verificacio-pdf.json').read_text())
    for name in ['GUIA', 'SOLUCIONS']:
        assert not pdfs[name]['overflow'] and sha(OUT / f'{name}.pdf') == pdfs[name]['sha256']
        assert sha(OUT / f'{name}.md') == pdfs[name]['source_sha256']
        source = (OUT / f'{name}.md').read_text()
        assert pdfs[name]['complete_body_headings'] == len(re.findall(r'^#{1,2} (.+)$', source, re.M))
        assert len(pdfs[name]['images_inside_page']) == len(re.findall(r'^!\[', source, re.M))
        lines = [line for block in re.findall(r'```(?:python|sql)\n(.*?)```', source, re.S) for line in block.splitlines() if line.strip()]
        assert pdfs[name]['exact_code_lines'] == len(lines)
    for shot in SHOTS:
        for suffix in ['.png', '.annotations.svg']:
            assert sha(ROOT / f'assets/captures/c5-{shot}{suffix}') == sha(OUT / f'captures/c5-{shot}{suffix}')
    shutil.copyfile(Path(__file__), OUT / 'reproduccio' / Path(__file__).name)
    files = []
    for path in sorted(OUT.rglob('*')):
        assert not path.is_symlink() and not path.name.endswith(('-wal', '-shm')), path
        if path.is_file() and path.name != 'sealed.json':
            files.append({'path': str(path.relative_to(OUT)), 'bytes': path.stat().st_size, 'sha256': sha(path)})
    dump(OUT / 'sealed.json', {'files': files, 'image': IMAGE, 'status': 'private-author-review', 'human_approved': False})
    target = ROOT / 'tmp/dades-docents' / f'practica-{OUT.name}.zip'
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(OUT.rglob('*')):
            if path.is_file():
                archive.write(path, 'autocorrelacio/' + str(path.relative_to(OUT)))
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for f in files:
            assert hashlib.sha256(archive.read('autocorrelacio/' + f['path'])).hexdigest() == f['sha256']
    dump(target.with_suffix('.receipt.json'), {'path': str(target.relative_to(ROOT)), 'sha256': sha(target),
        'bytes': target.stat().st_size, 'files': len(files) + 1, 'status': 'private-author-review'})
    print(target, sha(target), target.stat().st_size, flush=True)

def recover_package():
    """Recover the exact sealed r2 directory after a disk-full ZIP attempt."""
    assert OUT.name=='autocorrelacio-20261005-r2'
    seal=json.loads((OUT/'sealed.json').read_text())
    assert all(sha(OUT/f['path'])==f['sha256'] for f in seal['files'])
    target=ROOT/'tmp/dades-docents/practica-autocorrelacio-20261005-r2.zip'
    def valid(path):
        try:
            with zipfile.ZipFile(path) as archive:
                return archive.testzip() is None and all(hashlib.sha256(archive.read('autocorrelacio/'+f['path'])).hexdigest()==f['sha256'] for f in seal['files'])
        except (zipfile.BadZipFile,KeyError):return False
    if target.exists() and not valid(target):
        with target.open('rb') as stream:
            header=stream.read(30);assert header[:4]==b'PK\x03\x04'
            length=int.from_bytes(header[26:28],'little');assert stream.read(length).startswith(b'autocorrelacio/')
        failed=target.with_name(target.stem+'.failed-disk-full.zip');assert not failed.exists()
        failure={'path':str(failed.relative_to(ROOT)),'sha256':sha(target),'bytes':target.stat().st_size,'status':'incomplete-disk-full-attempt'}
        target.rename(failed);dump(failed.with_suffix('.receipt.json'),failure)
    if not target.exists():
        temporary=target.with_suffix('.zip.partial');assert not temporary.exists()
        with zipfile.ZipFile(temporary,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
            for path in sorted(OUT.rglob('*')):
                if path.is_file():archive.write(path,'autocorrelacio/'+str(path.relative_to(OUT)))
        assert valid(temporary);temporary.rename(target)
    assert valid(target)
    receipt={'path':str(target.relative_to(ROOT)),'sha256':sha(target),'bytes':target.stat().st_size,
        'files':len(seal['files'])+1,'status':'historical-private-author-review-r2','recovered_after':'disk-full'}
    dump(target.with_suffix('.receipt.json'),receipt);print(json.dumps(receipt,indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--inspect', action='store_true')
    parser.add_argument('--analyse', action='store_true')
    parser.add_argument('--qgis', action='store_true')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--finalise', action='store_true')
    parser.add_argument('--verify')
    parser.add_argument('--report')
    parser.add_argument('--docs', action='store_true')
    parser.add_argument('--package', action='store_true')
    parser.add_argument('--stage-revision', action='store_true')
    parser.add_argument('--revision', action='store_true', help='Use the r2 documentary bundle; analytical/capture sources stay on the retained original.')
    parser.add_argument('--recover-package',action='store_true')
    args = parser.parse_args()
    if args.revision or args.stage_revision:
        assert not any((args.fetch, args.analyse, args.qgis, args.finalise, args.record))
        OUT = OUT.with_name('autocorrelacio-20261005-r2')
    if (OUT / 'sealed.json').exists() and any((args.fetch, args.analyse, args.qgis, args.finalise, args.docs, args.package, args.stage_revision)):
        raise SystemExit('Paquet segellat: només es permet inspeccionar, verificar o llegir-ne els inputs. Prepara una versió nova.')
    if args.stage_revision:
        stage_revision()
    if args.fetch:
        fetch()
    if args.inspect:
        inspect()
    if args.analyse:
        analyse()
    if args.qgis:
        prepare_qgis()
    if args.finalise:
        finalise()
    if args.record:
        record_figures()
    if args.verify:
        assert args.report
        verify(args.verify, args.report)
    if args.docs:
        docs()
    if args.package:
        package()
    if args.recover_package:
        recover_package()
