"""Check the chapter's worked examples against the retained Constantí inputs.

--stage snapshots explicit inputs into a new ignored run. --check runs only
inside the pinned QGIS image; it writes numerical evidence, not teaching data
or generated chapter prose. Existing runs and checks are never overwritten.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil

ROOT = Path.cwd().resolve()
assert (ROOT / '.unaltraweb/computations.yml').is_file()
IMAGE = 'sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2'
HANDOUT = Path('sandbox/practiques/lliurament-geodisseny/2026-10-26-pdf-data-01/handouts/layout02/estadistica-constanti/alumnat/data/estadistica-constanti.gpkg')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def stage(out):
    assert not out.exists(), 'Select a new theory run.'
    out.mkdir(parents=True)
    inputs = out / 'inputs'
    inputs.mkdir()
    paths = {'punts-municipis.json': Path('context/inputs/punts-municipis.json'),
             'punts-escenaris.json': Path('context/inputs/punts-escenaris.json'),
             'constanti.gpkg': HANDOUT,
             'chapter-before.md': Path('_chapters/ca/04-estadistica-espacial.md'),
             'bibliography-before.bib': Path('_bibliography/manual.bib'),
             'comprovar-teoria.py': Path(__file__).resolve().relative_to(ROOT)}
    records = []
    for name, relative in paths.items():
        source = ROOT / relative
        digest = sha(source)
        shutil.copyfile(source, inputs / name)
        assert sha(inputs / name) == digest
        records.append({'source': str(relative), 'snapshot': 'inputs/' + name, 'sha256': digest})
    save(out / 'sources.json', {'kind': 'geodisseny-descriptive-theory-inputs', 'files': records,
         'qgis_image': IMAGE, 'human_approved': False,
         'coverage_reference': 'Wang, Shi and Miao (2015), doi:10.1371/journal.pone.0118537'})
    print(json.dumps({'ok': True, 'run': str(out.relative_to(ROOT)), 'snapshots': len(records)}), flush=True)


def check(out, pass_id):
    import numpy as np
    from osgeo import ogr
    from qgis.core import QgsApplication, QgsExpression, QgsGeometry, QgsPointXY, Qgis
    destination = out / pass_id
    assert not destination.exists(), 'Select a new theory check.'
    destination.mkdir()
    inputs = out / 'inputs'
    sources = json.loads((out / 'sources.json').read_text())
    assert all(sha(out / row['snapshot']) == row['sha256'] for row in sources['files'])
    application = QgsApplication([], False)
    application.initQgis()

    def statistics(xy):
        xy = np.asarray(xy, dtype=float)
        mean = xy.mean(axis=0)
        delta = xy - mean
        covariance = delta.T @ delta / len(xy)
        vx, vy, cxy = covariance[0, 0], covariance[1, 1], covariance[0, 1]
        radical = math.sqrt((vx - vy) ** 2 + 4 * cxy ** 2)
        eigenvalues = np.asarray([(vx + vy + radical) / 2, (vx + vy - radical) / 2])
        a, b = np.sqrt(eigenvalues)
        theta = math.atan2(2 * cxy, vx - vy) / 2
        u = delta[:, 0] * math.cos(theta) + delta[:, 1] * math.sin(theta)
        v = -delta[:, 0] * math.sin(theta) + delta[:, 1] * math.cos(theta)
        assert np.allclose([np.mean(u*u), np.mean(v*v)], eigenvalues, rtol=1e-12)
        assert np.allclose(eigenvalues, np.linalg.eigvalsh(covariance)[::-1], rtol=1e-12)
        d2 = np.sum(delta * delta, axis=1)
        radius = math.sqrt(float(np.mean(d2)))
        q = (u/a)**2 + (v/b)**2
        return {'n': len(xy), 'mean': mean.tolist(), 'covariance': covariance.tolist(),
                'eigenvalues': eigenvalues.tolist(), 'semiaxes': [float(a), float(b)],
                'radius': radius, 'theta_east_deg': math.degrees(theta),
                'azimuth_deg': (90 - math.degrees(theta)) % 180,
                'circle_inside': int(np.count_nonzero(d2 <= radius*radius + 1e-8)),
                'ellipse_inside': int(np.count_nonzero(q <= 1 + 1e-12)),
                'squared_distances': d2.tolist(), 'standardized_squared_distances': q.tolist()}

    toy = [[0, 0], [2, 4], [3, 3], [4, 2], [6, 6]]
    example = statistics(toy)
    assert np.allclose(example['mean'], [3, 3])
    assert np.allclose(example['covariance'], [[4, 3.2], [3.2, 4]])
    assert np.allclose(example['eigenvalues'], [7.2, .8])
    assert example['circle_inside'] == 3 and example['ellipse_inside'] == 1

    database = ogr.Open(str(inputs / 'constanti.gpkg'), 0)
    layer = database.GetLayerByName('punts')
    points = list(layer)
    xy = np.asarray([(f.GetGeometryRef().GetX(), f.GetGeometryRef().GetY()) for f in points])
    municipal = json.loads((inputs / 'punts-municipis.json').read_text())
    plotted = next(row for row in municipal['maps'] if str(row['code']) == '430477')
    assert np.allclose(sorted(map(tuple, xy)), sorted(map(tuple, plotted['points'])), atol=1e-8, rtol=0)
    reference = next(row for row in municipal['municipalities'] if str(row['code']) == '430477')['all']
    result = statistics(xy)
    assert result['n'] == 124
    assert np.allclose(result['mean'], reference['centre'], atol=1e-8, rtol=0)
    assert abs(result['radius'] - reference['sd_m']) < 1e-8
    assert np.allclose(result['semiaxes'], reference['semiaxes_m'], atol=1e-8, rtol=0)
    assert abs((result['theta_east_deg'] - reference['angle_east_deg'] + 90) % 180 - 90) < 1e-9

    bands = json.loads((inputs / 'punts-escenaris.json').read_text())
    scenarios = {}
    for index, name in enumerate(('w_inf', 'w_mid', 'w_sup')):
        weights = np.asarray([f['POT_KW'] if f['POT_KW'] is not None else bands['bands'][f['INTERVAL']][index]
                              for f in points], dtype=float)
        centre = np.average(xy, axis=0, weights=weights)
        scenarios[name] = {'sum_weights': float(weights.sum()), 'centre': centre.tolist(),
                           'delta': (centre - np.asarray(result['mean'])).tolist(),
                           'shift': float(np.linalg.norm(centre - np.asarray(result['mean'])))}
        if name == 'w_mid':
            assert np.allclose(weights, [f['w_mid'] for f in points])
            scenarios[name]['top_five_sum'] = float(np.sort(weights)[-5:].sum())
            scenarios[name]['top_five_percent'] = float(np.sort(weights)[-5:].sum()/weights.sum()*100)
    assert scenarios['w_mid']['sum_weights'] == 2970
    scenarios['extreme_centres_distance'] = float(np.linalg.norm(
        np.asarray(scenarios['w_sup']['centre']) - scenarios['w_inf']['centre']))

    geometries = {}
    x, y = result['mean']
    a, b = result['semiaxes']
    for name, expression in [('circle', f'make_circle(make_point({x:.15g},{y:.15g}),{result["radius"]:.15g},72)'),
                             ('ellipse', f'make_ellipse(make_point({x:.15g},{y:.15g}),{a:.15g},{b:.15g},{result["azimuth_deg"]:.15g},72)')]:
        parsed = QgsExpression(expression)
        geometry = parsed.evaluate()
        assert not parsed.hasEvalError(), parsed.evalErrorString()
        assert isinstance(geometry, QgsGeometry) and geometry.isGeosValid()
        ring = geometry.asPolygon()[0]
        assert len(ring) == 73
        vertices = np.asarray([(point.x(), point.y()) for point in ring[:-1]])
        if name == 'ellipse':
            assert np.allclose(2 * np.cov(vertices, rowvar=False, ddof=0), result['covariance'], atol=.01, rtol=0)
        count = sum(geometry.intersects(QgsGeometry.fromPointXY(QgsPointXY(float(px), float(py)))) for px, py in xy)
        geometries[name] = {'expression': expression, 'vertices_including_closure': len(ring), 'inside': count}
    assert geometries['circle']['inside'] == result['circle_inside']
    assert geometries['ellipse']['inside'] == result['ellipse_inside']

    coverages = [{'multiplier': k, 'normal_bivariate_fraction': 1 - math.exp(-k*k/2)}
                 for k in (1, math.sqrt(2), 2, 3)]
    for fraction in (.66, .95):
        k = math.sqrt(-2 * math.log(1 - fraction))
        assert abs(1 - math.exp(-k*k/2) - fraction) < 1e-14
        coverages.append({'multiplier': k, 'normal_bivariate_fraction': fraction})
    report = {'ok': True, 'qgis': Qgis.QGIS_VERSION, 'image': IMAGE, 'network': 'none',
              'verification_source_sha256': sha(Path(__file__)), 'sources_sha256': sha(out / 'sources.json'),
              'example': example, 'example_coordinates_km': toy, 'constanti': result,
              'scenarios': scenarios, 'qgis_geometries': geometries, 'normal_bivariate_coverage': coverages,
              'circle_72_max_chord_error_m': result['radius'] * (1 - math.cos(math.pi/72)),
              'inputs_unchanged': True}
    assert all(sha(out / row['snapshot']) == row['sha256'] for row in sources['files'])
    save(destination / 'verified.json', report)
    summary = {key: value for key, value in report.items() if key not in ('constanti',)}
    summary['constanti'] = {key: value for key, value in result.items()
                           if key not in ('squared_distances', 'standardized_squared_distances')}
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='2026-10-26-teoria-01')
    parser.add_argument('--pass-id', default='check01')
    parser.add_argument('--stage', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    assert Path(args.run).name == args.run and args.run not in ('.', '..')
    assert Path(args.pass_id).name == args.pass_id and args.pass_id not in ('.', '..')
    out = ROOT / 'sandbox/practiques/estadistica-constanti' / args.run
    if args.stage:
        stage(out)
    if args.check:
        check(out, args.pass_id)
