"""Reproduce real ICAEN mean centres and prepare styled local capture inputs."""
import hashlib
import json
import os
from pathlib import Path
import sys

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from qgis.core import (QgsApplication, QgsVectorLayer, QgsVectorFileWriter, QgsProject,
                       QgsCoordinateReferenceSystem, QgsGeometry, QgsFeature,
                       QgsField, QgsMarkerSymbol, QgsFillSymbol,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory)
from qgis.PyQt.QtCore import QVariant
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'tmp/dades-docents/qgis'
app = QgsApplication([], False); app.initQgis()
sys.path.insert(0, '/usr/share/qgis/python/plugins')
import processing
from processing.core.Processing import Processing
Processing.initialize()
project = QgsProject.instance()
project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
source = ROOT/'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'
points = QgsVectorLayer(str(source)+'|layername=autoconsum_tarragones', 'ICAEN', 'ogr')
assert points.isValid() and points.featureCount() == 5102
points.setSubsetString('"POT_KW" > 0')
assert points.featureCount() == 3762
rows = [(f.geometry().asMultiPoint()[0], f['POT_KW']) for f in points.getFeatures()]
xy = np.array([[p.x(), p.y()] for p,w in rows]); weights=np.array([w for p,w in rows])
assert weights.sum() == 36633
centres = QgsVectorLayer('Point?crs=EPSG:25831', 'Centres comparats', 'memory')
centres.dataProvider().addAttributes([QgsField('nom', QVariant.String),
                                    QgsField('x_m', QVariant.Double), QgsField('y_m', QVariant.Double)])
centres.updateFields()
checks = {}
for name, weight, expected in [('Sense pes', None, xy.mean(axis=0)),
                               ('Ponderat kW', 'POT_KW', np.average(xy, axis=0, weights=weights))]:
    result = processing.run('native:meancoordinates',
                             {'INPUT':points, 'WEIGHT':weight, 'UID':None, 'OUTPUT':'memory:'})['OUTPUT']
    f = next(result.getFeatures()); p = f.geometry().asPoint()
    assert np.allclose([p.x(),p.y()], expected, atol=.00001, rtol=0)
    item = QgsFeature(centres.fields()); item.setGeometry(f.geometry())
    item.setAttributes([name, p.x(), p.y()]); centres.dataProvider().addFeatures([item])
    checks[name] = [p.x(), p.y()]
admin = ROOT/'tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg'
county_source = QgsVectorLayer(str(admin)+'|layername=_51_comarques-5000', 'Comarques', 'ogr')
county = QgsVectorLayer('MultiPolygon?crs=EPSG:25831', 'Tarragonès', 'memory')
county.dataProvider().addAttributes(county_source.fields()); county.updateFields()
selected = [f for f in county_source.getFeatures() if f['NOMCOMAR'] == 'Tarragonès']
county.dataProvider().addFeatures(selected); county.updateExtents()
assert county.featureCount() == 1
centroid = next(county.getFeatures()).geometry().centroid()
p = centroid.asPoint(); item = QgsFeature(centres.fields()); item.setGeometry(centroid)
item.setAttributes(['Centroide comarcal',p.x(),p.y()]); centres.dataProvider().addFeatures([item])
checks['Centroide comarcal'] = [p.x(),p.y()]

def save(layer, name):
    target = OUT/(name+'.gpkg')
    if target.exists() and '--replace-generated' not in sys.argv:
        raise RuntimeError(f'Output already exists: {target}; use --replace-generated for these owned inputs')
    options = QgsVectorFileWriter.SaveVectorOptions(); options.driverName='GPKG'; options.layerName=name
    result = QgsVectorFileWriter.writeAsVectorFormatV3(layer, str(target), project.transformContext(), options)
    assert result[0] == QgsVectorFileWriter.NoError, result
    return QgsVectorLayer(str(target), name, 'ogr')

OUT.mkdir(parents=True, exist_ok=True)
known = save(points, 'icaen-coneguda')
known.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'circle','color':'#56788f',
                           'outline_style':'no','size':'1.2'}))
known.saveStyleToDatabase('ICAEN coneguda', '3762 registres amb potència positiva coneguda', True, '')
boundary = save(county, 'icaen-ambit')
boundary.renderer().setSymbol(QgsFillSymbol.createSimple({'color':'#f3f5f7','outline_color':'#647582',
                                                         'outline_width':'.3'}))
boundary.saveStyleToDatabase('Tarragonès', 'ICGC 20260120', True, '')
centres.updateExtents(); output = save(centres, 'icaen-centres')
categories = []
for name, symbol, colour in [('Sense pes','diamond','#006699'),
                             ('Ponderat kW','triangle','#d35621'),
                             ('Centroide comarcal','cross2','#20252a')]:
    marker = QgsMarkerSymbol.createSimple({'name':symbol,'color':colour,'outline_color':colour,
                                          'outline_width':'.4','size':'5'})
    categories.append(QgsRendererCategory(name,marker,name))
output.setRenderer(QgsCategorizedSymbolRenderer('nom',categories))
output.saveStyleToDatabase('Centres comparats', 'Mateixos 3762 registres als dos centres estadístics', True, '')
report = {'algorithm':'native:meancoordinates', 'n':len(rows),'known_kw':float(weights.sum()),
          'crs':'EPSG:25831','centres':checks,'weight_shift_m':float(np.linalg.norm(
              np.array(checks['Sense pes'])-np.array(checks['Ponderat kW'])))}
(OUT/'icaen-controls.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
# QGIS objects live to process exit; explicit exitQgis while they are alive can
# destroy provider-owned objects prematurely in standalone headless processes.
