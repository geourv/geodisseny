"""XEMA: validated half-hour maxima for the common day 2025-08-15 (TU)."""
import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
from urllib.parse import urlencode

ROOT=Path(__file__).resolve().parents[2]
PRIVATE=ROOT/'tmp/dades-docents/temperatures-20260930'
DAY='2025-08-15'
BASE='https://analisi.transparenciacatalunya.cat'


def fetch():
    originals=PRIVATE/'originals';originals.mkdir(parents=True,exist_ok=True)
    receipt=PRIVATE/'fonts.json'
    manifest=json.loads(receipt.read_text()) if receipt.exists() else {}
    query={'$where':"codi_variable='40' AND data_lectura >= '2025-08-15T00:00:00' AND data_lectura < '2025-08-16T00:00:00'",
           '$order':'codi_estacio,data_lectura','$limit':20000}
    sources=[('observacions.json',BASE+'/resource/nzvn-apee.json?'+urlencode(query)),
             ('estacions.json',BASE+'/resource/yqwd-vj5e.json?$limit=1000'),
             ('variables.json',BASE+'/resource/4fb2-n3yi.json?$limit=200'),
             ('metadades-observacions.json',BASE+'/api/views/nzvn-apee.json'),
             ('metadades-estacions.json',BASE+'/api/views/yqwd-vj5e.json')]
    for name,url in sources:
        path=originals/name
        if path.exists():
            assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest[name]['sha256'],path
            continue
        with urllib.request.urlopen(url,timeout=120) as response:data=response.read(16_000_001)
        assert len(data)<=16_000_000
        parsed=json.loads(data)
        if name=='observacions.json':assert 5000<len(parsed)<20000
        path.write_bytes(data)
        manifest[name]={'url':url,'sha256':hashlib.sha256(data).hexdigest(),
                        'bytes':len(data),'retrieved':datetime.now(timezone.utc).isoformat()}
        receipt.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        print('FETCH',name,len(parsed),len(data),flush=True)


def prepare():
    from osgeo import ogr,osr
    ogr.UseExceptions()
    sources=PRIVATE/'originals'
    receipt=json.loads((PRIVATE/'fonts.json').read_text())
    for name,item in receipt.items():assert hashlib.sha256((sources/name).read_bytes()).hexdigest()==item['sha256']
    variables=json.loads((sources/'variables.json').read_text())
    variable=next(v for v in variables if v['codi_variable']=='40')
    assert variable['nom_variable']=='Temperatura màxima' and variable['unitat']=='°C'
    metadata={r['codi_estacio']:r for r in json.loads((sources/'estacions.json').read_text())}
    rows=json.loads((sources/'observacions.json').read_text())
    groups=defaultdict(list)
    for row in rows:groups[row['codi_estacio']].append(row)
    expected={datetime.fromisoformat(DAY)+timedelta(minutes=30*i) for i in range(48)}
    points=[];excluded={}
    source_crs=osr.SpatialReference();source_crs.ImportFromEPSG(4326)
    source_crs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    projected=osr.SpatialReference();projected.ImportFromEPSG(25831)
    transform=osr.CoordinateTransformation(source_crs,projected)
    for code,series in sorted(groups.items()):
        if code not in metadata:excluded[code]='metadata missing';continue
        m=metadata[code]
        valid=[r for r in series if r.get('codi_estat')=='V' and r.get('codi_base')=='SH' and r.get('valor_lectura') is not None]
        times=[datetime.fromisoformat(r['data_lectura']) for r in valid]
        if len(times)!=48 or set(times)!=expected:
            excluded[code]=f'not 48 unique validated half-hours ({len(times)})';continue
        if m['data_inici'][:10]>DAY or (m.get('data_fi') and m['data_fi'][:10]<=DAY):
            excluded[code]='metadata operational interval mismatch';continue
        values=[float(r['valor_lectura']) for r in valid]
        assert all(-40<=v<=60 for v in values),(code,values)
        x,y,_=transform.TransformPoint(float(m['longitud']),float(m['latitud']))
        points.append({'codi':code,'nom':m['nom_estacio'],'x_m':x,'y_m':y,'alt_m':float(m['altitud']),
                       'tx_c':max(values),'n':48,'dia_tu':DAY})
    assert len(points)>=100
    output=PRIVATE/'estacions.gpkg'
    if output.exists():raise RuntimeError('Existing observations retained; use a new preparation name')
    ds=ogr.GetDriverByName('GPKG').CreateDataSource(str(output))
    layer=ds.CreateLayer('temperatures',projected,ogr.wkbPoint)
    for name in ['codi','nom','dia_tu']:layer.CreateField(ogr.FieldDefn(name,ogr.OFTString))
    for name in ['tx_c','alt_m','x_m','y_m']:layer.CreateField(ogr.FieldDefn(name,ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn('n',ogr.OFTInteger))
    for p in points:
        f=ogr.Feature(layer.GetLayerDefn())
        for key,value in p.items():f.SetField(key,value)
        g=ogr.Geometry(ogr.wkbPoint);g.AddPoint_2D(p['x_m'],p['y_m']);f.SetGeometry(g);layer.CreateFeature(f)
    ds=None
    data={'day':DAY,'time_reference':'00:00–24:00 Temps Universal; initial interval labels',
          'variable':'maximum of 48 validated half-hour maxima, variable 40',
          'station_count':len(points),'excluded':excluded,'stations':points,'sources':receipt,
          'metadata_note':'Station coordinates and operating intervals from the metadata snapshot; not a history of every relocation.'}
    (PRIVATE/'dades.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'n':len(points),'excluded':excluded,'range_c':[min(p['tx_c'] for p in points),max(p['tx_c'] for p in points)]},ensure_ascii=False,indent=2))


def analyse():
    import os,sys
    import numpy as np
    from scipy.spatial.distance import pdist
    from osgeo import ogr,gdal
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsVectorLayer,QgsProject,QgsCoordinateReferenceSystem,
                           QgsProcessingContext,QgsProcessingFeedback)
    app=QgsApplication([],False);app.initQgis()
    lock=json.loads((ROOT/'context/qgis/plugins-lock.json').read_text())
    sys.path[:0]=['/usr/share/qgis/python/plugins',str(ROOT/lock['cache'])]
    from processing.core.Processing import Processing
    Processing.initialize()
    from processing_saga_nextgen.processing.provider import SagaNextGenAlgorithmProvider
    provider=SagaNextGenAlgorithmProvider();QgsApplication.processingRegistry().addProvider(provider)
    import processing
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    readonly=QgsVectorLayer.LayerOptions();readonly.forceReadOnly=True
    points=QgsVectorLayer(str(PRIVATE/'estacions.gpkg'),'XEMA 15-08-2025','ogr',readonly)
    assert points.isValid() and points.featureCount()==182
    project.addMapLayer(points)
    sample_path=PRIVATE/'variograma.dbf'
    if not sample_path.exists():
        processing.run('sagang:variogram',{'POINTS':points,'FIELD':'tx_c','DISTCOUNT':12,
            'DISTMAX':150000,'NSKIP':1,'RESULT':str(sample_path)},context=context)
    sample=QgsVectorLayer(str(sample_path),'Semivariograma','ogr',readonly)
    assert sample.isValid() and sample.featureCount()>0
    print('VARIOGRAM',sample.featureCount(),sample.fields().names(),flush=True)
    data=json.loads((PRIVATE/'dades.json').read_text())
    coordinates=np.array([[p['x_m'],p['y_m']] for p in data['stations']]);values=np.array([p['tx_c'] for p in data['stations']])
    distances=pdist(coordinates);gamma=.5*pdist(values[:,None])**2
    bins=np.linspace(0,150000,13);experimental=[]
    for lo,hi in zip(bins[:-1],bins[1:]):
        selected=(distances>lo)&(distances<=hi)
        experimental.append({'lower_m':lo,'upper_m':hi,'distance_m':float(distances[selected].mean()),
                             'gamma_c2':float(gamma[selected].mean()),'pairs':int(selected.sum())})
    extent=[260000,530000,4486000,4752000];extent_text=','.join(map(str,extent))+' [EPSG:25831]'
    idw=PRIVATE/'idw.tif'
    interpolation=f'{points.source()}::~::0::~::{points.fields().indexFromName("tx_c")}::~::0'
    if not idw.exists():
        processing.run('qgis:idwinterpolation',{'INTERPOLATION_DATA':interpolation,'DISTANCE_COEFFICIENT':2,
            'EXTENT':extent_text,'PIXEL_SIZE':2000,'OUTPUT':str(idw)},context=context)
    class Feedback(QgsProcessingFeedback):
        def __init__(self):super().__init__();self.lines=[]
        def pushInfo(self,s):self.lines.append(s)
        def pushConsoleInfo(self,s):self.lines.append(s)
        def reportError(self,s,fatalError=False):self.lines.append(s);print('SAGA',s,flush=True)
    feedback=Feedback()
    parameters={'POINTS':points,'FIELD':'tx_c',
                'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX':extent_text,
                'TARGET_USER_SIZE':2000,'TARGET_USER_FITS':1,'VAR_MAXDIST':150000,'VAR_NCLASSES':12,
                 'VAR_NSKIP':1,'VAR_MODEL':'a + b*x/100000','LOG':False,'BLOCK':False,
                'CV_METHOD':0,'SEARCH_RANGE':1,'SEARCH_POINTS_ALL':1,'TQUALITY':1,
                'CV_SUMMARY':str(PRIVATE/'cv-no-utilitzada.dbf'),'CV_RESIDUALS':str(PRIVATE/'cv-no-utilitzada.shp'),
                 'PREDICTION':str(PRIVATE/'kriging-ajustat.sdat'),'VARIANCE':str(PRIVATE/'variancia-ajustada.sdat')}
    if not (PRIVATE/'kriging-ajustat.sdat').exists() or not (PRIVATE/'saga-ajustat-log.txt').exists():
        try:processing.run('sagang:ordinarykriging',parameters,context=context,feedback=feedback)
        finally:(PRIVATE/'saga-ajustat-log.txt').write_text('\n'.join(feedback.lines)+'\n')
    import re
    fitted={name:float(value) for name,value in re.findall(r'^([ab]) = ([-+\d.eE]+)',(PRIVATE/'saga-ajustat-log.txt').read_text(),re.M)}
    assert fitted.keys()=={'a','b'} and fitted['a']>=0 and fitted['b']>0,fitted
    gdal.UseExceptions();ogr.UseExceptions()
    first=gdal.Open(str(idw));second=gdal.Open(str(PRIVATE/'kriging-ajustat.sdat'))
    assert second is not None
    assert np.allclose(first.GetGeoTransform(),second.GetGeoTransform()),(first.GetGeoTransform(),second.GetGeoTransform())
    admin=ogr.Open(str(ROOT/'tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg'))
    layer=admin.GetLayerByName('_21_catalunya-5000')
    mask=gdal.GetDriverByName('MEM').Create('',first.RasterXSize,first.RasterYSize,1,gdal.GDT_Byte)
    mask.SetProjection(first.GetProjection());mask.SetGeoTransform(first.GetGeoTransform())
    gdal.RasterizeLayer(mask,[1],layer,burn_values=[1]);inside=mask.ReadAsArray().astype(bool)
    fields={}
    for name,source in [('idw',first),('kriging',second)]:
        a=source.ReadAsArray();assert np.isfinite(a[inside]).all()
        assert np.min(a[inside])>-20 and np.max(a[inside])<65,(name,np.min(a[inside]),np.max(a[inside]))
        fields[name]=np.where(inside,np.round(a,3),-9999).tolist()
        target=PRIVATE/(name+('-ajustat' if name=='kriging' else '')+'-catalunya.tif')
        if not target.exists():
            out=gdal.GetDriverByName('GTiff').CreateCopy(str(target),source,options=['COMPRESS=DEFLATE'])
            out.GetRasterBand(1).SetNoDataValue(-9999);out.GetRasterBand(1).WriteArray(np.where(inside,a,-9999));out=None
    layer.ResetReading();country=next(iter(layer))
    boundary=json.loads(country.GetGeometryRef().SimplifyPreserveTopology(300).ExportToJson())
    # The provider fits the variogram; retain its exact fit report for interpreting parameters.
    result={**data,'experimental_variogram':experimental,'extent':extent,'pixel_m':2000,'fields':fields,
            'boundary':boundary,'qgis_algorithm':'sagang:ordinarykriging','variogram_formula':parameters['VAR_MODEL'],
            'idw_power':2,'parameters':{k:v for k,v in parameters.items() if k!='POINTS'},
             'saga_log':(PRIVATE/'saga-ajustat-log.txt').read_text()}
    variance=gdal.Open(str(PRIVATE/'variancia-ajustada.sdat')).ReadAsArray()
    assert np.min(variance[inside])>=-1e-6
    (ROOT/'context/inputs/temperatures-catalunya.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    print('MODEL',len(values),first.RasterXSize,first.RasterYSize,flush=True)
    print('\n'.join(line for line in result['saga_log'].splitlines() if any(k in line.lower() for k in ['model','formula','nugget','sill','range','r2','a =','b =','c ='])),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fetch',action='store_true');parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--analyse',action='store_true')
    args=parser.parse_args()
    if args.fetch:fetch()
    if args.prepare:prepare()
    if args.analyse:analyse()
