"""Run the authored field-calculator recipe on real and controlled point sets.

Use the pinned QGIS engine with readonly /dades, /inputs and /guide; only
/proof is writable. This is activity evidence, not a generic MCP verifier.
"""
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import numpy as np
sys.path.append('/usr/share/qgis/python/plugins')
from qgis.core import (QgsApplication,QgsProject,QgsVectorLayer,QgsFeature,QgsGeometry,QgsPointXY,
                       QgsCoordinateReferenceSystem,QgsProcessingContext,QgsProcessingFeedback,Qgis)
from processing.core.Processing import Processing
import processing

FIELDS=('n_punts','vx_m2','vy_m2','cxy_m2','D_m','delta_m2','a_m','b_m','azimut')
app=QgsApplication([],False)
app.initQgis()
Processing.initialize()
project=QgsProject.instance()
project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))


def authored(path):
    text=path.read_text()
    entries=re.findall(r'\*\*`([^`]+)`\*\*[^\n]*\n\n```text\n(.*?)\n```',text,re.S)
    fields={name:body.strip() for name,body in entries if name in FIELDS}
    assert set(fields)==set(FIELDS),(str(path),fields.keys())
    return fields


expressions=authored(Path('/guide/student.md'))
manual=authored(Path('/guide/manual.md'))
assert all(re.sub(r'\s+','',expressions[name])==re.sub(r'\s+','',manual[name]) for name in FIELDS)
calculator=QgsApplication.processingRegistry().algorithmById('native:fieldcalculator')
assert calculator
types=calculator.parameterDefinition('FIELD_TYPE').options()
assert 'double' in types[0].lower() and 'integer' in types[1].lower(),types
geometry_algorithm=QgsApplication.processingRegistry().algorithmById('native:geometrybyexpression')
assert geometry_algorithm


def resolved(value):
    layer=value if isinstance(value,QgsVectorLayer) else QgsVectorLayer(value,'Resultat','ogr')
    assert layer.isValid()
    return layer


def run(algorithm,parameters):
    context=QgsProcessingContext()
    context.setProject(project)
    feedback=QgsProcessingFeedback()
    result=processing.run(algorithm,parameters,context=context,feedback=feedback)
    return resolved(result['OUTPUT'])


def memory_points(xy):
    layer=QgsVectorLayer('Point?crs=EPSG:25831','P','memory')
    features=[]
    for x,y in xy:
        feature=QgsFeature(layer.fields())
        feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(x),float(y))))
        features.append(feature)
    assert layer.dataProvider().addFeatures(features)[0]
    layer.updateExtents()
    return layer


def check_case(name,layer,reference=None):
    project.clear()
    layer.setName('P')
    project.addMapLayer(layer)
    assert layer.crs().authid()=='EPSG:25831'
    original=list(layer.getFeatures())
    xy=np.asarray([(feature.geometry().asPoint().x(),feature.geometry().asPoint().y()) for feature in original],dtype=float)
    assert len(xy)>0 and np.isfinite(xy).all()
    mean=xy.mean(axis=0)
    centered=xy-mean
    covariance=centered.T@centered/len(xy)
    eigenvalues=np.linalg.eigvalsh(covariance)[::-1]
    expected_a,expected_b=np.sqrt(np.maximum(eigenvalues,0))
    expected_d=math.sqrt(float(np.trace(covariance)))
    theta=math.atan2(2*covariance[0,1],covariance[0,0]-covariance[1,1])/2
    expected_azimuth=(90-math.degrees(theta))%180
    parameters={'INPUT':layer,'WEIGHT':'','OUTPUT':'TEMPORARY_OUTPUT'}
    mean_algorithm=QgsApplication.processingRegistry().algorithmById('native:meancoordinates')
    names={item.name() for item in mean_algorithm.parameterDefinitions()}
    if 'UID' in names:parameters['UID']=''
    result=run(mean_algorithm,parameters)
    assert result.featureCount()==1
    native_calls=[]
    for field in FIELDS:
        result=run(calculator,{'INPUT':result,'FIELD_NAME':field,'FIELD_TYPE':1 if field=='n_punts' else 0,
            'FIELD_LENGTH':20,'FIELD_PRECISION':10,'FORMULA':expressions[field],'OUTPUT':'TEMPORARY_OUTPUT'})
        assert result.featureCount()==1
        native_calls.append({'algorithm':'native:fieldcalculator','field':field,'formula':expressions[field]})
    feature=next(result.getFeatures())
    point=feature.geometry().asPoint()
    assert np.allclose([point.x(),point.y()],mean,rtol=0,atol=1e-7)
    assert int(feature['n_punts'])==len(xy)
    assert np.allclose([feature['vx_m2'],feature['vy_m2'],feature['cxy_m2']],
        [covariance[0,0],covariance[1,1],covariance[0,1]],rtol=1e-11,atol=1e-7),name
    assert np.allclose([feature['D_m'],feature['a_m'],feature['b_m']],
                       [expected_d,expected_a,expected_b],rtol=1e-10,atol=1e-7),name
    assert math.isclose(float(feature['D_m'])**2,float(feature['a_m'])**2+float(feature['b_m'])**2,rel_tol=1e-11,abs_tol=1e-8)
    isotropic=float(feature['delta_m2'])==0
    if not isotropic:
        assert abs((float(feature['azimut'])-expected_azimuth+90)%180-90)<1e-7,(name,feature['azimut'],expected_azimuth)
    else:assert feature['azimut']==0
    if reference:
        assert abs(float(feature['D_m'])-reference['sd_m'])<1e-7
        assert np.allclose([feature['a_m'],feature['b_m']],reference['semiaxes_m'],rtol=0,atol=1e-7)
    geometries={}
    if expected_b>1e-7:
        for shape,formula in (('circle','make_circle($geometry, "D_m", 72)'),
                              ('ellipse','make_ellipse($geometry, "a_m", "b_m", "azimut", 72)')):
            drawn=run(geometry_algorithm,{'INPUT':result,'OUTPUT_GEOMETRY':0,'WITH_Z':False,'WITH_M':False,
                                         'EXPRESSION':formula,'OUTPUT':'TEMPORARY_OUTPUT'})
            geometry=next(drawn.getFeatures()).geometry()
            assert not geometry.isEmpty() and geometry.isGeosValid()
            ring=geometry.asPolygon()[0]
            assert len(ring)==73
            if shape=='ellipse':
                vertices=np.asarray([(vertex.x(),vertex.y()) for vertex in ring[:-1]])
                assert np.allclose(2*np.cov(vertices,rowvar=False,ddof=0),covariance,rtol=1e-10,atol=1e-6),name
            geometries[shape]={'valid':True,'vertices':len(ring),
                'inside':sum(geometry.intersects(feature.geometry()) for feature in original)}
    else:
        assert abs(float(feature['b_m']))<1e-7
    return {'name':name,'count':len(xy),'centre':mean.tolist(),'covariance':covariance.tolist(),
        'fields':{field:int(feature[field]) if field=='n_punts' else float(feature[field]) for field in FIELDS},
        'isotropic':isotropic,'polygon_ellipse_supported':bool(expected_b>1e-7),'geometries':geometries,
        'native_calculator_calls':native_calls}


source=Path('/dades/estadistica-constanti.gpkg')
before=hashlib.sha256(source.read_bytes()).hexdigest()
cases=[]
cases.append(check_case('Constantí',QgsVectorLayer(str(source)+'|layername=punts','P','ogr')))
assert cases[0]['count']==124 and cases[0]['geometries']['circle']['inside']==86 and cases[0]['geometries']['ellipse']['inside']==68
municipal=json.loads(Path('/inputs/municipis.json').read_text())
for row in municipal['maps']:
    if str(row['code'])=='430477':continue
    reference=next(item for item in municipal['municipalities'] if str(item['code'])==str(row['code']))
    cases.append(check_case(reference.get('name',str(row['code'])),memory_points(row['points']),reference['all']))
toy=np.asarray([[0,0],[2,4],[3,3],[4,2],[6,6]],dtype=float)*1000
example=check_case('Cinc punts construïts, metres',memory_points(toy))
assert example['geometries']['circle']['inside']==3 and example['geometries']['ellipse']['inside']==1
cases.append(example)
for angle in (-70,125):
    radians=math.radians(angle)
    rotation=np.array([[math.cos(radians),-math.sin(radians)],[math.sin(radians),math.cos(radians)]])
    cases.append(check_case('Construït girat '+str(angle),memory_points(toy@rotation.T+[340000,4550000])))
cases.append(check_case('Isòtrop construït',memory_points([[1,0],[-1,0],[0,1],[0,-1]])))
cases.append(check_case('Alineats construïts',memory_points([[0,0],[1,0],[2,0]])))
cases.append(check_case('Coincidents construïts',memory_points([[2,3]]*4)))
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
report={'ok':True,'qgis':Qgis.QGIS_VERSION,'network':'none','inputs_readonly':True,
    'input_gpkg_sha256':before,'inputs_unchanged':True,'actual_authored_expressions_equal':True,
    'field_type_options':types,'cases':cases,'case_count':len(cases),
    'verification_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with Path('/proof/verified.json').open('x') as stream:json.dump(report,stream,ensure_ascii=False,indent=2)
print(json.dumps({'ok':True,'cases':len(cases),'municipal_counts':[case['count'] for case in cases[:3]],
                  'constanti_fields':cases[0]['fields']},ensure_ascii=False),flush=True)
