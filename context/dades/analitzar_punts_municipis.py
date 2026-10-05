"""Audit original ICAEN XML and compare descriptive municipal distributions.

Compute offline in the pinned QGIS image with inputs readonly. --record retains
the reviewed compact figure input; originals and the sealed workshop stay intact.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
GML = ROOT/'tmp/dades-docents/originals/icaen-2026-09-28/GML/ENERGIA_INSTALAUTOCONFV.gml'
GPKG = ROOT/'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'
ADMIN = ROOT/'tmp/dades-docents/moodle/ambits-tarragona-20260120.gpkg'
_APP = None


def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')


def analyse(output, selected):
    global _APP
    import numpy as np
    from osgeo import ogr
    from qgis.core import QgsApplication, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    _APP = QgsApplication([], False); _APP.initQgis()
    sys.path.insert(0, '/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing
    ogr.UseExceptions()
    assert sha(GPKG) == '1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'
    assert sha(ADMIN) == '444411b1418625ca24d03487b9c55a62cad4541c246b882bc11969d7b3c6e124'
    ds = ogr.Open(str(GPKG), 0); layer = ds.GetLayerByName('autoconsum_tarragones')
    records = {}; groups = defaultdict(list)
    for feature in layer:
        geometry = feature.GetGeometryRef(); assert geometry.GetGeometryCount() == 1
        point = geometry.GetGeometryRef(0)
        row = {'id': feature['gml_id'], 'municipi': feature['MUNICIPI'],
               'code': str(feature['CODI_MUN']).zfill(6), 'power': feature['POT_KW'],
               'interval': feature['INTERVAL'], 'xy': [point.GetX(), point.GetY()]}
        assert row['id'] not in records
        records[row['id']] = row; groups[row['code']].append(row)
    ds = None; assert len(records) == 5102
    audit = Counter(); intervals = Counter(); examples = []
    gml_ns = '{http://www.opengis.net/gml}'
    for _, element in ET.iterparse(GML, events=['end']):
        if element.tag != '{http://www.safe.com/gml/fme}ENERGIA_INSTALAUTOCONFV': continue
        audit['gml_total'] += 1
        fields = {child.tag.rsplit('}', 1)[-1]: child.text for child in element}
        if fields.get('COMARCA') == 'Tarragonès':
            audit['county_records'] += 1
            ident = element.attrib[gml_ns+'id']; row = records[ident]
            text = (fields.get('POT_KW') or '').strip()
            power = float(text) if text else None
            assert power == row['power'], (ident, text, row['power'])
            position = element.find('.//'+gml_ns+'pos')
            assert position is not None
            xy = list(map(float, position.text.split()))
            assert np.allclose(xy, row['xy'], atol=1e-7, rtol=0)
            audit['valid_geometry'] += 1
            if power is None:
                audit['power_empty'] += 1
                audit['power_element_present'] += 'POT_KW' in fields
                intervals[fields.get('INTERVAL') or '(buit)'] += 1
                if len(examples) < 3:
                    examples.append({'municipi': fields['MUNICIPI'], 'power_xml': text,
                                     'interval': fields.get('INTERVAL')})
            else:
                audit['power_known'] += 1; audit['power_sum_kw'] += power
        element.clear()
    assert audit['county_records'] == audit['valid_geometry'] == 5102
    assert audit['power_known'] == 3762 and audit['power_empty'] == 1340
    assert audit['power_sum_kw'] == 36633

    def summary(rows, weighted=False):
        xy = np.array([row['xy'] for row in rows]); w = np.array([row['power'] if weighted else 1 for row in rows], dtype=float)
        mean = np.average(xy, axis=0, weights=w)
        centred = xy-mean; covariance = (centred.T*w)@centred/w.sum()
        eigen, vectors = np.linalg.eigh(covariance)
        angle = float(np.degrees(np.arctan2(vectors[1,-1], vectors[0,-1]))%180)
        return {'n': len(rows), 'centre': mean.tolist(), 'sd_m': float(np.sqrt(np.trace(covariance))),
                'semiaxes_m': np.sqrt(np.maximum(eigen[::-1], 0)).tolist(), 'angle_east_deg': angle}

    project = QgsProject.instance(); project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831')); project.setEllipsoid('NONE')
    options = QgsVectorLayer.LayerOptions(); options.forceReadOnly = True
    source = QgsVectorLayer(str(GPKG)+'|layername=autoconsum_tarragones', 'ICAEN', 'ogr', options)
    assert source.isValid()
    native = {}
    for mode, subset, weight in [('all', '', None), ('known', '"POT_KW" > 0', None), ('weighted', '"POT_KW" > 0', 'POT_KW')]:
        assert source.setSubsetString(subset)
        result = processing.run('native:meancoordinates', {'INPUT': source, 'WEIGHT': weight, 'UID': 'CODI_MUN', 'OUTPUT': 'memory:'})['OUTPUT']
        native[mode] = {str(f['CODI_MUN']).zfill(6): [f.geometry().asPoint().x(), f.geometry().asPoint().y()] for f in result.getFeatures()}
        assert len(native[mode]) == len(groups)
    municipalities = []
    for code, rows in sorted(groups.items()):
        known = [r for r in rows if r['power'] is not None and r['power'] > 0]
        power = sum(r['power'] for r in known)
        record = {'code': code, 'name': rows[0]['municipi'], 'n_all': len(rows), 'n_known': len(known),
                  'power_kw': power, 'null_power': len(rows)-len(known),
                  'record_share_known_pct': 100*len(known)/3762, 'power_share_known_pct': 100*power/36633,
                  'all': summary(rows), 'known': summary(known), 'weighted': summary(known, True)}
        for mode in native: assert np.allclose(record[mode]['centre'], native[mode][code], atol=1e-6, rtol=0)
        record['weight_shift_m'] = float(np.linalg.norm(np.array(record['weighted']['centre'])-record['known']['centre']))
        municipalities.append(record)
    county = {'all': summary(list(records.values())),
              'known': summary([r for r in records.values() if r['power'] is not None]),
              'weighted': summary([r for r in records.values() if r['power'] is not None], True)}
    county['selection_shift_m'] = float(np.linalg.norm(np.array(county['all']['centre'])-county['known']['centre']))
    shapes = {}; admin_layers = []; admin = ogr.Open(str(ADMIN), 0)
    for layer in admin:
        fields = [f.GetName() for f in layer.schema]
        admin_layers.append({'name': layer.GetName(), 'fields': fields, 'count': layer.GetFeatureCount()})
        if 'CODIMUNI' not in fields: continue
        for feature in layer:
            code = str(feature['CODIMUNI']).zfill(6)
            if code in groups:
                shapes[code] = json.loads(feature.GetGeometryRef().SimplifyPreserveTopology(5).ExportToJson())
    admin = None
    maps = []
    for code in selected:
        assert code in shapes and code in groups, (code, list(shapes))
        maps.append({'code': code, 'boundary': shapes[code], 'points': [r['xy'] for r in groups[code]]})
    report = {'sources': {str(p.relative_to(ROOT)): sha(p) for p in [GML, GPKG, ADMIN]},
              'audit': dict(audit), 'null_power_intervals': dict(intervals), 'null_power_examples': examples,
              'county': county, 'municipalities': municipalities, 'native_grouped_centres_verified': True,
              'crs': 'EPSG:25831', 'geometry_simplification_for_drawing_m': 5, 'admin_layers': admin_layers, 'maps': maps}
    write(output, report)
    print(json.dumps({k: report[k] for k in ['audit','null_power_intervals','null_power_examples','county','admin_layers']},ensure_ascii=False,indent=2),flush=True)
    for row in municipalities:
        print(f"{row['code']} {row['name']}: n={row['n_all']}; coneguts={row['n_known']}; kW={row['power_kw']}; quota n/potència={row['record_share_known_pct']:.2f}/{row['power_share_known_pct']:.2f}%; D={row['all']['sd_m']:.1f}m; desplaçament={row['weight_shift_m']:.1f}m",flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output'); parser.add_argument('--municipis', nargs='*', default=[]); parser.add_argument('--record')
    args = parser.parse_args()
    if args.record:
        data = json.loads(Path(args.record).read_text()); assert data['native_grouped_centres_verified'] and data['maps']
        write(ROOT/'context/inputs/punts-municipis.json', data)
    else:
        assert args.output; analyse(args.output, args.municipis)
    if _APP is not None:
        from qgis.core import QgsProject
        import gc
        QgsProject.instance().clear(); gc.collect(); _APP.exitQgis()
