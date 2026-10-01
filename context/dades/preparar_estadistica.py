"""Reproducible QGIS descriptive summaries and the classic PySAL Columbus example."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
PRIVATE=ROOT/'tmp/dades-docents/estadistica-20260930'
CAPTURE=ROOT/'tmp/dades-docents/qgis'


def initialise():
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import QgsApplication
    app=QgsApplication([],False);app.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    lock=json.loads((ROOT/'context/qgis/plugins-lock.json').read_text())
    sys.path.insert(0,str(ROOT/lock['cache']))
    from processing.core.Processing import Processing
    Processing.initialize()
    PRIVATE.mkdir(parents=True,exist_ok=True)
    return app


def descriptive():
    import numpy as np
    from osgeo import gdal
    from qgis.core import (QgsVectorLayer,QgsProject,QgsCoordinateReferenceSystem,QgsFeature,QgsField,
                           QgsGeometry,QgsPointXY,QgsVectorFileWriter,QgsExpression,QgsExpressionContext,
                           QgsExpressionContextUtils,QgsFillSymbol,QgsMarkerSymbol,QgsCategorizedSymbolRenderer,
                           QgsRendererCategory)
    from qgis.PyQt.QtCore import QVariant
    app=initialise()
    import processing
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'))
    readonly=QgsVectorLayer.LayerOptions();readonly.forceReadOnly=True
    original_path=ROOT/'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'
    assert hashlib.sha256(original_path.read_bytes()).hexdigest()=='1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'
    original=QgsVectorLayer(str(original_path)+'|layername=autoconsum_tarragones','ICAEN','ogr',readonly)
    assert original.isValid()
    original.setSubsetString('"POT_KW" > 0')
    points=processing.run('native:multiparttosingleparts',{'INPUT':original,'OUTPUT':'memory:'})['OUTPUT']
    points.setName('ICAEN punts');project.addMapLayer(points)
    assert points.featureCount()==3762
    xy=np.array([[f.geometry().asPoint().x(),f.geometry().asPoint().y()] for f in points.getFeatures()])
    p=np.array([float(f['POT_KW']) for f in points.getFeatures()])
    def save(layer,path,name):
        if path.exists():
            old=QgsVectorLayer(str(path),name,'ogr')
            expected=list(layer.getFeatures());actual=list(old.getFeatures())
            assert len(expected)==len(actual) and all(a.geometry().equals(b.geometry()) for a,b in zip(expected,actual)),path
            return old
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='GPKG';options.layerName=name
        status=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(path),project.transformContext(),options)
        assert status[0]==QgsVectorFileWriter.NoError,status
        return QgsVectorLayer(str(path),name,'ogr')
    points_out=save(points,CAPTURE/'icaen-punts-simples.gpkg','ICAEN punts')
    points_out.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'circle','color':'#59798b','size':'1.2','outline_style':'no'}))
    points_out.saveStyleToDatabase('ICAEN','Selecció amb potència coneguda',True,'')
    centres=processing.run('native:meancoordinates',{'INPUT':points,'WEIGHT':None,'OUTPUT':'memory:'})['OUTPUT']
    centre=next(centres.getFeatures());mx,my=centre.geometry().asPoint().x(),centre.geometry().asPoint().y()
    assert np.allclose([mx,my],xy.mean(axis=0))
    expressions={
      'circle':"with_variable('cx',x($geometry),with_variable('cy',y($geometry),make_circle($geometry,sqrt(aggregate('ICAEN punts','mean',(x($geometry)-@cx)^2+(y($geometry)-@cy)^2)),72)))",
      'ellipse':"with_variable('cx',x($geometry),with_variable('cy',y($geometry),with_variable('xx',aggregate('ICAEN punts','mean',(x($geometry)-@cx)^2),with_variable('yy',aggregate('ICAEN punts','mean',(y($geometry)-@cy)^2),with_variable('xy',aggregate('ICAEN punts','mean',(x($geometry)-@cx)*(y($geometry)-@cy)),with_variable('d',sqrt((@xx-@yy)^2+4*@xy^2),make_ellipse($geometry,sqrt((@xx+@yy+@d)/2),sqrt((@xx+@yy-@d)/2),90-degrees(atan2(2*@xy,@xx-@yy))/2,72)))))))"}
    summary={}
    geometries={}
    for key,expression in expressions.items():
        context=QgsExpressionContext();context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(centres));context.setFeature(centre)
        expr=QgsExpression(expression);assert not expr.hasParserError(),expr.parserErrorString()
        geometry=expr.evaluate(context)
        assert not expr.hasEvalError(),expr.evalErrorString()
        assert isinstance(geometry,QgsGeometry) and not geometry.isEmpty(),key
        result=processing.run('native:geometrybyexpression',{'INPUT':centres,'EXPRESSION':expression,
            'OUTPUT_GEOMETRY':0,'WITH_Z':False,'WITH_M':False,'OUTPUT':'memory:'})['OUTPUT']
        actual=next(result.getFeatures()).geometry();assert actual.equals(geometry)
        out=save(result,CAPTURE/f'icaen-{key}.gpkg',key)
        out.renderer().setSymbol(QgsFillSymbol.createSimple({'style':'no','outline_color':'#b87924' if key=='circle' else '#006699',
                                                             'outline_width':'.8','outline_style':'dash' if key=='circle' else 'solid'}))
        out.saveStyleToDatabase(key,'Dispersió de la mateixa selecció',True,'')
        geometries[key]=json.loads(geometry.asJson())
    covariance=np.cov(xy,rowvar=False,ddof=0);eigen,vec=np.linalg.eigh(covariance)
    distance=float(np.sqrt(np.trace(covariance)))
    circle=np.array(geometries['circle']['coordinates'][0])[:,:2]
    assert np.allclose(np.linalg.norm(circle-[mx,my],axis=1),distance,rtol=1e-8)
    ellipse=np.array(geometries['ellipse']['coordinates'][0])[:-1,:2]
    assert np.allclose(2*np.cov(ellipse,rowvar=False,ddof=0),covariance,rtol=1e-6,atol=.01)
    angle=np.degrees(np.arctan2(vec[1,-1],vec[0,-1]))%180
    summary={'n':len(xy),'centre':[mx,my],'standard_distance_m':distance,
             'ellipse_semiaxes_m':np.sqrt(eigen[::-1]).tolist(),'angle_from_east_deg':float(angle),
             'expressions':expressions,'covariance':covariance.tolist()}
    # Keep the geometry expression as a normal QGIS expression for students.
    (PRIVATE/'ellipse-expression.txt').write_text(expressions['ellipse']+'\n')
    bounds=points.extent();extent=[float(np.floor(bounds.xMinimum()/1000)*1000),float(np.ceil(bounds.xMaximum()/1000)*1000),
                                 float(np.floor(bounds.yMinimum()/1000)*1000),float(np.ceil(bounds.yMaximum()/1000)*1000)]
    extent_text=','.join(map(str,extent))+' [EPSG:25831]'
    grid=processing.run('native:creategrid',{'TYPE':2,'EXTENT':extent_text,'HSPACING':1000,'VSPACING':1000,
             'HOVERLAY':0,'VOVERLAY':0,'CRS':project.crs(),'OUTPUT':'memory:'})['OUTPUT']
    counted=processing.run('native:countpointsinpolygon',{'POLYGONS':grid,'POINTS':points,'FIELD':'n_punts','OUTPUT':'memory:'})['OUTPUT']
    assert sum(f['n_punts'] for f in counted.getFeatures())==len(xy)
    save(grid,CAPTURE/'icaen-grid.gpkg','Graella 1 km')
    save(counted,CAPTURE/'icaen-recompte.gpkg','Recompte')
    cells=[{'geometry':json.loads(f.geometry().asJson()),'count':int(f['n_punts'])} for f in counted.getFeatures()]
    rasters=[]
    for radius in [500,1500]:
        name=f'icaen-kernel-{radius}'
        target=CAPTURE/(name+'.tif');assert not target.exists(),target
        result=processing.run('qgis:heatmapkerneldensityestimation',{'INPUT':points,'RADIUS':radius,
            'PIXEL_SIZE':100,'KERNEL':0,'DECAY':0,'OUTPUT_VALUE':0,'OUTPUT':str(target)})
        source=gdal.Open(str(target));a=source.ReadAsArray();gt=source.GetGeoTransform()
        a=np.where(a==source.GetRasterBand(1).GetNoDataValue(),0,a)
        # Quartic raw kernel (1-u²)² integrates to pi*r²/3 over the plane.
        normalized=a*(3/(np.pi*radius**2))*1e6
        assert abs(float(normalized.sum())*.01-len(xy))/len(xy)<.03
        rasters.append({'radius_m':radius,'pixel_m':100,'values':np.round(normalized,3).tolist(),
                        'extent':[gt[0],gt[0]+source.RasterXSize*gt[1],gt[3]+source.RasterYSize*gt[5],gt[3]],
                        'unit':'points per square kilometre; analytical quartic normalization of raw QGIS output'})
    boundary=QgsVectorLayer(str(ROOT/'tmp/dades-docents/qgis/icaen-ambit.gpkg'),'Tarragonès','ogr',readonly)
    data={'summary':summary,'points':xy.tolist(),'geometries':geometries,'cells':cells,'kernels':rasters,
          'county':json.loads(next(boundary.getFeatures()).geometry().asJson())}
    (ROOT/'context/inputs/icaen-estadistica.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')
    (PRIVATE/'controls.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)


def columbus():
    import numpy as np
    import libpysal
    from esda import Moran,Moran_Local
    from libpysal.weights import Queen,lag_spatial
    from osgeo import ogr
    ogr.UseExceptions();PRIVATE.mkdir(parents=True,exist_ok=True)
    path=Path(libpysal.examples.get_path('columbus.shp'))
    readme=path.parent/'README.md'
    if readme.exists():(PRIVATE/'columbus-readme.md').write_bytes(readme.read_bytes())
    (PRIVATE/'columbus-metadata.html').write_bytes((path.parent/'columbus.html').read_bytes())
    ds=ogr.Open(str(path));layer=ds.GetLayer(0)
    values=[];features=[]
    for f in layer:
        values.append(float(f['CRIME']))
        centroid=f.GetGeometryRef().Centroid()
        features.append({'type':'Feature','geometry':json.loads(f.GetGeometryRef().ExportToJson()),
                         'properties':{'id':int(f['POLYID']),'crime':float(f['CRIME']),
                                       'centre':[centroid.GetX(),centroid.GetY()]}})
    w=Queen.from_shapefile(str(path));w.transform='r'
    y=np.array(values);z=(y-y.mean())/y.std()
    np.random.seed(20260930);global_stat=Moran(y,w,permutations=9999)
    local=Moran_Local(y,w,permutations=9999,seed=20260930,n_jobs=1,keep_simulations=False)
    lag=lag_spatial(w,z)
    for i,f in enumerate(features):
        f['properties'].update(z=float(z[i]),lag=float(lag[i]),local_i=float(local.Is[i]),
                               p_sim=float(local.p_sim[i]),quadrant=int(local.q[i]),
                               neighbors=[int(features[j]['properties']['id']) for j in w.neighbors[i]])
    assert len(features)==49 and np.isclose(global_stat.I,.5001885571828611)
    geo={'type':'FeatureCollection','features':features,
         'coordinate_note':'Original digitised example coordinates, no claimed metric CRS or scale bar'}
    meta={'source':'libpysal.examples columbus','url':'https://pysal.org/libpysal/generated/libpysal.examples.available.html',
          'n':49,'variable':'CRIME: residential burglaries and vehicle thefts per thousand households, 1980',
          'I':float(global_stat.I),'p_sim':float(global_stat.p_sim),'permutations':9999,'seed':20260930,
          'weights':'Queen, row standardised','local_threshold':.05,
          'source_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in path.parent.iterdir() if p.is_file()}}
    (ROOT/'context/inputs/columbus.geojson').write_text(json.dumps(geo,ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'context/inputs/columbus-resultats.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(meta,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--descriptive',action='store_true');parser.add_argument('--columbus',action='store_true')
    args=parser.parse_args()
    if args.descriptive:descriptive()
    if args.columbus:columbus()
