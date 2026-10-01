"""Extend the sealed distance workshop with checked walking-time models.

The original ZIP is read-only. All new files belong to a separately marked
destination. Run --build and --style in separate pinned QGIS processes.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'tmp/dades-docents/practica-distancies-vilaseca-20261001.zip'
BASE_SHA='0a7ac7c331212ada3d1a0f2d2f728cb9c0513d4ca6e9ff6bedc87471f72bf2d5'
OUT=ROOT/'tmp/dades-docents/qgis/distancies-vilaseca-20261001-ampliada'
BOUNDS=(343600,4553000,345300,4554700)
O=(344407.,4553668.36)
D=(344473.01,4554030.72)
RES=5
COEFFICIENTS='0.72,6.0,1.9998,-1.9998'
QGIS_IMAGE='sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'
NEW_CAPTURES=['rwalk-parametres','rwalk-resultat','rwalk-contorns',
              'rwalk-isocrones-obert','rwalk-isocrones-tancat','xarxa-girs-parametres']
FIGURES=['anisotropia-pendent','restriccions-gir','isocrones-xarxa','isocrones-rwalk']

def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def write_json(path,data):
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def setup():
    marker=OUT/'.ampliacio.json'
    assert marker.is_file() and json.loads(marker.read_text())['owner']=='preparar_accessibilitat.py'
    assert sha(BASE)==BASE_SHA,'The original sealed workshop must stay unchanged.'

def initialise():
    assert sha(BASE)==BASE_SHA
    marker=OUT/'.ampliacio.json'
    if marker.exists():
        setup()
        if json.loads(marker.read_text()).get('initialised'):return
    else:
        assert not OUT.exists(),'Refuse an unowned destination.'
        OUT.mkdir()
        write_json(marker,{'owner':'preparar_accessibilitat.py','initialised':False})
    with zipfile.ZipFile(BASE) as archive:
        manifest=json.loads(archive.read('distancies-vilaseca/MANIFEST.json'))
        for record in manifest['files']:
            relative=Path(record['path']);destination=OUT/relative
            assert not relative.is_absolute() and destination.resolve().is_relative_to(OUT.resolve())
            content=archive.read('distancies-vilaseca/'+str(relative))
            assert hashlib.sha256(content).hexdigest()==record['sha256']
            destination.parent.mkdir(parents=True,exist_ok=True)
            if destination.exists():assert sha(destination)==record['sha256']
            else:destination.write_bytes(content)
        write_json(OUT/'controls/base-manifest.json',manifest)
    write_json(OUT/'controls/paquet-base.json',{'path':str(BASE.relative_to(ROOT)),'sha256':BASE_SHA})
    write_json(marker,{'owner':'preparar_accessibilitat.py','initialised':True})
    print('Initialised a separate copy of',manifest['file_count'],'verified source members',flush=True)

def qgis_session():
    import sys
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsProcessingContext
    app=QgsApplication([],False);app.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    return app,project,context

def build():
    import heapq
    import numpy as np
    import shapely
    from shapely.geometry import mapping
    from osgeo import gdal
    from qgis.core import QgsApplication,QgsVectorLayer,QgsFeature,QgsField,QgsGeometry,QgsVectorFileWriter,QgsProcessingFeedback
    from qgis.PyQt.QtCore import QVariant
    setup();gdal.UseExceptions()
    app,project,context=qgis_session()
    import processing
    class Feedback(QgsProcessingFeedback):
        def __init__(self):super().__init__();self.messages=[]
        def reportError(self,message,fatalError=False):self.messages.append('DIAGNOSTIC: '+message)
        def pushConsoleInfo(self,message):self.messages.append(message)
    log=OUT/'controls/processing-ampliacio.log';log.write_text('')
    def run(algorithm,params):
        print('PROCESS',algorithm,flush=True)
        feedback=Feedback()
        try:return processing.run(algorithm,params,context=context,feedback=feedback)
        finally:
            with log.open('a') as stream:stream.write(algorithm+'\n'+'\n'.join(feedback.messages)+'\n')
    dem=gdal.Open(str(OUT/'fonts/mdt-5m.tif'));gt=dem.GetGeoTransform();z=dem.ReadAsArray().astype(float)
    shape=z.shape;assert shape==(340,340) and gt==(343600.,5.,0.,4554700.,0.,-5.)
    assert np.isfinite(z).all() and np.min(z)>0
    extent='343600,345300,4553000,4554700 [EPSG:25831]'
    def raster(relative,array,nodata=-9999,transform=gt):
        path=OUT/relative
        image=gdal.GetDriverByName('GTiff').Create(str(path),array.shape[1],array.shape[0],1,gdal.GDT_Float32,
                                                 ['COMPRESS=DEFLATE','TILED=YES'])
        image.SetGeoTransform(transform);image.SetProjection(dem.GetProjection())
        image.GetRasterBand(1).SetNoDataValue(nodata);image.GetRasterBand(1).WriteArray(array);image=None
        return str(path)
    def array(relative):
        ds=gdal.Open(str(OUT/relative));assert ds.GetGeoTransform()==gt
        values=ds.ReadAsArray().astype(float);nd=ds.GetRasterBand(1).GetNoDataValue()
        values[~np.isfinite(values)|(values==nd)]=np.nan
        return values
    def cell(point):return int((point[1]-gt[3])/gt[5]),int((point[0]-gt[0])/gt[1])
    o,d=cell(O),cell(D)
    params={'walk_coeff':COEFFICIENTS,'lambda':1.,'slope_factor':-.2125,'max_cost':0,
            '-k':False,'-n':True,'GRASS_REGION_CELLSIZE_PARAMETER':RES}
    controls={'qgis':'3.44.11','grass':'8.4.1','crs':'EPSG:25831','resolution_m':RES,
              'bounds':BOUNDS,'walk_coeff':[.72,6.,1.9998,-1.9998],'lambda':1.,'slope_factor':-.2125,
              'friction_s_per_m':{'paths':0.,'other':.5,'barriers':'NoData'},
              'origin_elevation_m':float(z[o]),'destination_elevation_m':float(z[d]),'models':{}}
    # An isolated 100 m, +10 m profile tests direction and units in GRASS itself.
    toy_z=np.tile(np.arange(21)*.5,(3,1));toy_f=np.full((3,21),-9999.);toy_f[1,:]=0
    toy_dem=raster('controls/prova-rampa-mdt.tif',toy_z)
    toy_friction=raster('controls/prova-rampa-friccio.tif',toy_f)
    toy_extent='343600,343705,4554685,4554700 [EPSG:25831]'
    controls['ramp_check']={}
    for name,start,target,expected in [('up','343602.5,4554692.5',(1,20),132.),
                                      ('down','343702.5,4554692.5',(1,0),52.002)]:
        result=str(OUT/f'controls/prova-rampa-{name}.tif')
        run('grass:r.walk.coords',{**params,'elevation':toy_dem,'friction':toy_friction,
            'start_coordinates':start,'output':result,'outdir':str(OUT/f'controls/prova-rampa-{name}-direccions.tif'),
            'GRASS_REGION_PARAMETER':toy_extent})
        value=float(gdal.Open(result).ReadAsArray()[target]);assert abs(value-expected)<.01,(name,value,expected)
        controls['ramp_check'][name]={'seconds':value,'expected':expected}
    raster('dades/mdt-pla-control.tif',np.zeros(shape))
    for state in ['obert','tancat']:
        original=array(f'dades/friccio-{state}.tif')
        raster(f'dades/friccio-marxa-{state}.tif',np.where(np.isfinite(original),np.where(original==1,0.,.5),-9999))
    neighbours=[(dy,dx,RES*math.hypot(dy,dx)) for dy in [-1,0,1] for dx in [-1,0,1] if dy or dx]
    def independent(elev,friction,source,target):
        dist=np.full(shape,np.inf);dist[source]=0.;queue=[(0.,*source)]
        while queue:
            cost,y,x=heapq.heappop(queue)
            if cost!=dist[y,x]:continue
            if (y,x)==target:return cost
            for dy,dx,ds in neighbours:
                yy,xx=y+dy,x+dx
                if not (0<=yy<shape[0] and 0<=xx<shape[1]) or not np.isfinite(friction[yy,xx]):continue
                dh=float(elev[yy,xx]-elev[y,x]);coefficient=6. if dh>0 else (-1.9998 if dh/ds<-.2125 else 1.9998)
                step=.72*ds+coefficient*dh+.5*(friction[y,x]+friction[yy,xx])*ds
                assert step>=0
                candidate=cost+step
                if candidate<dist[yy,xx]:dist[yy,xx]=candidate;heapq.heappush(queue,(candidate,yy,xx))
        return float('inf')
    definitions=[('obert-anada','obert',False,'origen','desti'),('obert-tornada','obert',False,'desti','origen'),
                 ('tancat-anada','tancat',False,'origen','desti'),('pla-anada','obert',True,'origen','desti'),
                 ('pla-tornada','obert',True,'desti','origen')]
    for name,state,flat,start,end in definitions:
        result=f'resultats/rwalk-{name}-segons.tif';direction=f'resultats/rwalk-{name}-direccions.tif'
        elevation='dades/mdt-pla-control.tif' if flat else 'fonts/mdt-5m.tif'
        run('grass:r.walk.points',{**params,'elevation':str(OUT/elevation),
            'friction':str(OUT/f'dades/friccio-marxa-{state}.tif'),
            'start_points':str(OUT/f'dades/{start}.gpkg')+'|layername='+start,
            'output':str(OUT/result),'outdir':str(OUT/direction),'GRASS_REGION_PARAMETER':extent})
        seconds=array(result);source,target=(o,d) if start=='origen' else (d,o)
        actual=float(seconds[target]);friction=array(f'dades/friccio-marxa-{state}.tif')
        check=independent(np.zeros(shape) if flat else z,friction,source,target)
        assert abs(actual-check)<.05,(name,actual,check)
        assert np.isnan(seconds[~np.isfinite(friction)]).all()
        minutes=seconds/60.;raster(f'resultats/rwalk-{name}-minuts.tif',np.where(np.isfinite(minutes),minutes,-9999))
        route=f'resultats/rwalk-{name}-ruta.gpkg'
        if (OUT/route).exists():(OUT/route).unlink()
        run('grass:r.path',{'input':str(OUT/direction),'format':1,
            'start_points':str(OUT/f'dades/{end}.gpkg')+'|layername='+end,
            'vector_path':str(OUT/route),'raster_path':'TEMPORARY_OUTPUT',
            'GRASS_REGION_PARAMETER':extent,'GRASS_REGION_CELLSIZE_PARAMETER':RES})
        layer=QgsVectorLayer(str(OUT/route),name,'ogr');assert layer.isValid()
        length=sum(f.geometry().length() for f in layer.getFeatures())
        controls['models'][name]={'seconds':actual,'minutes':actual/60.,'length_m':length,'independent_seconds':check}
        if name not in ['obert-anada','tancat-anada']:continue
        classes=np.where(np.isfinite(minutes),np.select([minutes<=3,minutes<=6,minutes<=12],[1,2,3],default=4),0)
        raster(f'resultats/isocrones-marxa-{state}.tif',classes,0)
        contour=f'resultats/isocrones-contorns-{state}.gpkg'
        if (OUT/contour).exists():(OUT/contour).unlink()
        run('grass:r.contour',{'input':str(OUT/f'resultats/rwalk-{name}-minuts.tif'),'levels':'3,6,12','cut':3,
            'output':str(OUT/contour),'GRASS_REGION_PARAMETER':extent,'GRASS_REGION_CELLSIZE_PARAMETER':RES})
        contours=QgsVectorLayer(str(OUT/contour),'Contorns','ogr');assert contours.isValid()
        assert set(float(f['level']) for f in contours.getFeatures())=={3.,6.,12.}
        accessible=[int(np.count_nonzero(np.isfinite(minutes)&(minutes<=t))) for t in [3,6,12]]
        assert accessible==sorted(accessible)
        edge=np.concatenate([minutes[0],minutes[-1],minutes[:,0],minutes[:,-1]])
        controls['models'][name]['isochrones']={'limits_min':[3,6,12],'cells_cumulative':accessible,
            'hectares_cumulative':[n*25/10000 for n in accessible],
            'touches_frame':[bool(np.any(np.isfinite(edge)&(edge<=t))) for t in [3,6,12]]}
    assert abs(controls['models']['pla-anada']['seconds']-controls['models']['pla-tornada']['seconds'])<.01
    assert abs(controls['models']['obert-anada']['seconds']-controls['models']['obert-tornada']['seconds'])>1.
    # Network time bands are disjoint line portions, not polygon envelopes.
    def geom(layer):return shapely.union_all([shapely.from_wkb(bytes(f.geometry().asWkb())) for f in layer.getFeatures()])
    controls['network_bands']={}
    for state in ['obert','tancat']:
        bands=QgsVectorLayer('MultiLineString?crs=EPSG:25831','Franges','memory')
        bands.dataProvider().addAttributes([QgsField('classe',QVariant.Int),QgsField('minuts',QVariant.Int)]);bands.updateFields()
        previous=shapely.MultiLineString([]);lengths=[]
        for category,t in enumerate([3,6,12],1):
            network='xarxa-oberta.gpkg' if state=='obert' else 'xarxa-tancada.gpkg'
            current=run('native:serviceareafrompoint',{'INPUT':str(OUT/'dades'/network),
                'STRATEGY':1,'SPEED_FIELD':'v_kmh','DEFAULT_SPEED':5,'DEFAULT_DIRECTION':2,'TOLERANCE':0,
                'START_POINT':f'{O[0]},{O[1]} [EPSG:25831]','TRAVEL_COST2':t/60.,'OUTPUT_LINES':'memory:'})['OUTPUT_LINES']
            union=geom(current);part=union.difference(previous)
            lines=[g for g in shapely.get_parts(part) if g.geom_type=='LineString' and g.length>1e-7]
            if lines:
                geometry=shapely.MultiLineString(lines);feature=QgsFeature(bands.fields());q=QgsGeometry();q.fromWkb(geometry.wkb)
                feature.setGeometry(q);feature.setAttributes([category,t]);assert bands.dataProvider().addFeatures([feature])[0]
            lengths.append(float(union.length));previous=union
        path=OUT/f'resultats/franges-xarxa-{state}.gpkg'
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='GPKG';options.layerName=path.stem
        status=QgsVectorFileWriter.writeAsVectorFormatV3(bands,str(path),project.transformContext(),options)
        assert status[0]==QgsVectorFileWriter.NoError,status
        controls['network_bands'][state]={'limits_min':[3,6,12],'unique_length_m':lengths}
    identifiers=['grass:r.walk.points','grass:r.walk.coords','grass:r.path','grass:r.contour','native:shortestpathpointtopoint']
    schema={name:[{'name':p.name(),'description':p.description(),'default':str(p.defaultValue())}
        for p in QgsApplication.processingRegistry().algorithmById(name).parameterDefinitions()] for name in identifiers}
    assert not any('turn' in p['name'].lower() for p in schema['native:shortestpathpointtopoint'])
    write_json(OUT/'controls/algorismes-ampliacio.json',schema)
    write_json(OUT/'controls/ampliacio.json',controls)
    print(json.dumps(controls,ensure_ascii=False,indent=2),flush=True)

def style():
    from qgis.core import (QgsVectorLayer,QgsRasterLayer,QgsLineSymbol,QgsSimpleLineSymbolLayer,
        QgsRasterShader,QgsColorRampShader,QgsSingleBandPseudoColorRenderer,QgsCategorizedSymbolRenderer,
        QgsRendererCategory,QgsPalLayerSettings,QgsTextFormat,QgsTextBufferSettings,QgsVectorLayerSimpleLabeling,
        QgsRectangle,QgsReferencedRectangle,Qgis)
    from qgis.PyQt.QtGui import QColor,QFont
    setup();app,project,context=qgis_session();crs=project.crs()
    inventory=json.loads((OUT/'controls/capes.json').read_text())
    # A raster and vector must not share a .qml basename. Migrate only these
    # known outputs of this owned, still-unsealed preparation.
    for state in ['obert','tancat']:
        old=f'resultats/isocrones-marxa-{state}.gpkg';new=f'resultats/isocrones-contorns-{state}.gpkg'
        if (OUT/old).exists():
            assert not (OUT/new).exists()
            (OUT/old).rename(OUT/new)
        inventory.pop(old,None)
    controls=json.loads((OUT/'controls/ampliacio.json').read_text())
    colours=['#2365a4','#289d85','#e39d39']
    def load(relative,name):
        path=OUT/relative;layer=QgsRasterLayer(str(path),name) if path.suffix=='.tif' else QgsVectorLayer(str(path),name,'ogr')
        assert layer.isValid(),relative
        inventory[relative]=name;return layer
    def persist(relative,layer):
        message,ok=layer.saveNamedStyle(str((OUT/relative).with_suffix('.qml')));assert ok,message
        if isinstance(layer,QgsVectorLayer):
            assert not layer.saveStyleToDatabase('docencia','Model de marxa i isòcrones; supòsits documentats',True,'')
    def raster(relative,name,items,exact=False):
        layer=load(relative,name);ramp=QgsColorRampShader()
        ramp.setColorRampType(QgsColorRampShader.Exact if exact else QgsColorRampShader.Interpolated)
        ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(v,QColor(c),label) for v,c,label in items])
        ramp.setMinimumValue(items[0][0]);ramp.setMaximumValue(items[-1][0])
        shader=QgsRasterShader();shader.setRasterShaderFunction(ramp)
        renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,shader)
        renderer.setClassificationMin(items[0][0]);renderer.setClassificationMax(items[-1][0])
        layer.setRenderer(renderer);persist(relative,layer)
    timecolours=[(0,'#ffffcc','0 min'),(3,'#c7e9b4','3 min'),(6,'#7fcdbb','6 min'),
                 (12,'#41b6c4','12 min'),(20,'#253494','20 min')]
    for state in ['obert','tancat']:
        raster(f'dades/friccio-marxa-{state}.tif',f'Fricció de marxa {state} · s/m',
               [(0,'#e9f6e9','0 s/m · camins'),(.5,'#e2c792','0,5 s/m · resta')],True)
        raster(f'resultats/isocrones-marxa-{state}.tif',f'Franges de marxa · {state}',
               [(1,colours[0],'0–3 min'),(2,colours[1],'>3–6 min'),(3,colours[2],'>6–12 min'),(4,'#eeeeee','Més de 12 min')],True)
        relative=f'resultats/isocrones-contorns-{state}.gpkg';layer=load(relative,f'Isòcrones 3, 6, 12 min · {state}')
        layer.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':'#354652','line_width':'.35'}))
        labels=QgsPalLayerSettings();labels.fieldName='to_string(to_int("level")) || \' min\'';labels.isExpression=True
        text=QgsTextFormat();text.setFont(QFont('DejaVu Sans',12));text.setSize(12)
        halo=QgsTextBufferSettings();halo.setEnabled(True);halo.setSize(1.);halo.setColor(QColor('white'));text.setBuffer(halo)
        labels.setFormat(text);layer.setLabeling(QgsVectorLayerSimpleLabeling(labels));layer.setLabelsEnabled(True);persist(relative,layer)
        relative=f'resultats/franges-xarxa-{state}.gpkg';layer=load(relative,f'Trams 0–3, 3–6, 6–12 min · {state}')
        layer.setRenderer(QgsCategorizedSymbolRenderer('classe',[QgsRendererCategory(i,
            QgsLineSymbol.createSimple({'line_color':c,'line_width':'1.1'}),label)
            for i,c,label in zip([1,2,3],colours,['0–3 min','>3–6 min','>6–12 min'])]));persist(relative,layer)
    raster('dades/mdt-pla-control.tif','Altitud constant · control',[(0,'#efefe0','0 m')],True)
    for name,result in controls['models'].items():
        raster(f'resultats/rwalk-{name}-minuts.tif',f'Temps {name} · min',timecolours)
        load(f'resultats/rwalk-{name}-segons.tif',f'Temps {name} · segons')
        load(f'resultats/rwalk-{name}-direccions.tif',f'Direccions · {name}')
        relative=f'resultats/rwalk-{name}-ruta.gpkg'
        layer=load(relative,f'{name} · {result["minutes"]:.2f} min'.replace('.',','))
        symbol=QgsLineSymbol.createSimple({'line_color':'white','line_width':'1.7'})
        symbol.appendSymbolLayer(QgsSimpleLineSymbolLayer.create({'line_color':'#b74724' if 'tornada' in name else '#54278f',
            'line_width':'1.','line_style':'dash' if 'tornada' in name else 'solid'}))
        layer.renderer().setSymbol(symbol);persist(relative,layer)
    endpoints=['dades/origen.gpkg','dades/desti.gpkg']
    base=['fonts/ortofoto-2025.tif','dades/barrera-ap7.gpkg','fonts/edificis.gpkg']
    detail=(343930,4553320,344900,4554230)
    views={
        '10-marxa':(base+['resultats/rwalk-obert-anada-minuts.tif','resultats/rwalk-obert-anada-ruta.gpkg',
                        'resultats/rwalk-obert-tornada-ruta.gpkg','dades/pas-p2.gpkg',*endpoints],detail),
        '11-marxa-relleu':(['fonts/mdt-5m.tif','resultats/rwalk-obert-anada-ruta.gpkg','dades/pas-p2.gpkg',*endpoints],detail),
        '12-isocrones-obert':(base+['resultats/isocrones-marxa-obert.tif','resultats/isocrones-contorns-obert.gpkg',
                                 'dades/pas-p2.gpkg',*endpoints],BOUNDS),
        '13-isocrones-tancat':(base+['resultats/isocrones-marxa-tancat.tif','resultats/isocrones-contorns-tancat.gpkg',
                                  'dades/pas-p2.gpkg',*endpoints],BOUNDS),
        '14-franges-xarxa':(['fonts/ortofoto-2025.tif','dades/xarxa-oberta.gpkg','resultats/franges-xarxa-obert.gpkg',
                            'dades/pas-p2.gpkg',*endpoints],BOUNDS)}
    for name,(visible,bounds) in views.items():
        project.clear();project.setCrs(crs);project.setEllipsoid('NONE');project.setTitle('Accessibilitat · '+name)
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for relative in visible:project.addMapLayer(load(relative,inventory[relative]))
        hidden=project.layerTreeRoot().addGroup('Altres dades de marxa')
        for relative in list(inventory):
            if relative in visible or not any(x in relative for x in ['rwalk','marxa','isocrones-contorns','mdt-','franges-xarxa']):continue
            layer=load(relative,inventory[relative]);project.addMapLayer(layer,False);hidden.addLayer(layer).setItemVisibilityChecked(False)
        hidden.setExpanded(False)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*bounds),crs))
        assert project.write(str(OUT/'projectes'/f'{name}.qgz'))
    write_json(OUT/'controls/capes.json',inventory)
    write_json(OUT/'controls/vistes-ampliacio.json',{k:{'visible':v,'bounds':b} for k,(v,b) in views.items()})
    print('Styled',len(inventory),'layers in total; added',len(views),'relative-path projects',flush=True)

def figure_inputs():
    import numpy as np
    import shapely
    from shapely.geometry import mapping
    from osgeo import ogr,gdal
    setup();ogr.UseExceptions();gdal.UseExceptions()
    def geometries(relative):
        ds=ogr.Open(str(OUT/relative),0)
        layer=next(l for l in ds if l.GetGeomType()!=ogr.wkbNone)
        return [{'geometry':mapping(shapely.force_2d(shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())))),
                 'attributes':f.items()} for f in layer if f.GetGeometryRef() is not None]
    controls=json.loads((OUT/'controls/ampliacio.json').read_text())
    data={'bounds':BOUNDS,'origin':O,'destination':D,'controls':controls,
          'network':geometries('dades/xarxa-oberta.gpkg'),'motorway':geometries('dades/barrera-ap7.gpkg'),
          'buildings':geometries('fonts/edificis.gpkg'),'pass':geometries('dades/pas-p2.gpkg'),'states':{}}
    for state in ['obert','tancat']:
        image=gdal.Open(str(OUT/f'resultats/isocrones-marxa-{state}.tif'))
        data['states'][state]={'network_bands':geometries(f'resultats/franges-xarxa-{state}.gpkg'),
            'walking_classes':image.ReadAsArray().astype(int).tolist(),
            'contours':geometries(f'resultats/isocrones-contorns-{state}.gpkg'),
            'route':geometries(f'resultats/rwalk-{state}-anada-ruta.gpkg')}
    up=geometries('resultats/rwalk-obert-anada-ruta.gpkg')[0]['geometry']
    back=geometries('resultats/rwalk-obert-tornada-ruta.gpkg')[0]['geometry']
    data['controls']['same_route_out_and_back']=bool(shapely.equals(shapely.geometry.shape(up),shapely.geometry.shape(back)))
    write_json(OUT/'controls/ampliacio.json',data['controls'])
    write_json(ROOT/'context/inputs/accessibilitat-ampliada.json',data)
    print('Retained figure input; same route out/back:',data['controls']['same_route_out_and_back'])

def refresh_docs():
    setup()
    for source,name in [('distancies-vilaseca.md','GUIA.md'),('distancies-vilaseca-docent.md','SOLUCIONS.md')]:
        shutil.copyfile(ROOT/'context/practiques'/source,OUT/name)
    shutil.copyfile(Path(__file__),OUT/'reproduccio/preparar_accessibilitat.py')
    shutil.copyfile(ROOT/'context/inputs/accessibilitat-ampliada.json',OUT/'reproduccio/accessibilitat-ampliada.json')
    for name in ['rwalk','girs']:
        shutil.copyfile(ROOT/'context/qgis'/f'{name}.yml',OUT/'reproduccio'/f'{name}.yml')
    shutil.copyfile(ROOT/'context/qgis/accessibilitat-ampliada.md',OUT/'reproduccio/prompt-ampliacio.md')
    for name in NEW_CAPTURES:
        for suffix in ['.png','.annotations.svg']:
            shutil.copyfile(ROOT/'assets/captures'/f'{name}{suffix}',OUT/'captures'/f'{name}{suffix}')
        shutil.copyfile(ROOT/'context/qgis/manifests'/f'{name}.yml',OUT/'reproduccio/manifests'/f'{name}.yml')
    (OUT/'figures').mkdir(exist_ok=True)
    for name in FIGURES:
        shutil.copyfile(ROOT/'assets/img/generated'/f'{name}.svg',OUT/'figures'/f'{name}.svg')
        shutil.copyfile(ROOT/'assets/quarto/figures'/f'{name}.qmd',OUT/'reproduccio'/f'{name}.qmd')
    (OUT/'COMENCA-AQUI.txt').write_text(
        'Distàncies i recorreguts a Vila-seca · ampliació de marxa i isòcrones\n\n'
        '1. Descomprimeix tot el paquet i llegeix GUIA.pdf.\n'
        '2. Obre projectes/00-inici.qgz amb QGIS 3.44. Desa la teva feina a treball/.\n'
        '3. A–B: distàncies euclidianes. C–D: xarxa i cost. E–F: r.walk i isòcrones.\n'
        '4. Projectes 10–14: marxa, relleu i mapes temporals. Totes les dades són locals.\n'
        '5. SOLUCIONS.pdf i resultats/ contenen controls de referència.\n\n'
        'Autor: Benito Zaragozí. Preparació: 2026-10-01.\n')

def standalone_sqlite():
    import sqlite3
    setup()
    for path in sorted(OUT.rglob('*.gpkg')):
        temporary=path.with_name(path.stem+'.standalone.gpkg');assert not temporary.exists()
        original=sqlite3.connect(f'file:{path}?mode=ro',uri=True);copy=sqlite3.connect(temporary)
        original.backup(copy);assert copy.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        copy.execute('PRAGMA journal_mode=DELETE');copy.close();original.close()
        assert not path.with_name(path.name+'-wal').exists(),'QGIS must be closed before preparing standalone databases.'
        temporary.replace(path)
    fonts=json.loads((OUT/'fonts/fonts.json').read_text())
    for name,record in fonts.items():
        path=OUT/'fonts'/name
        if path.is_file():record['delivery_sha256']=sha(path)
    write_json(OUT/'fonts/fonts.json',fonts)
    print('Prepared standalone GeoPackages',flush=True)

def package():
    setup()
    validation=json.loads((OUT/'controls/verificacio-qgis.json').read_text())
    pdfs=json.loads((OUT/'controls/verificacio-pdf.json').read_text())
    assert validation['ok'] and len(validation['projects'])==15
    for name,digest in validation['checked_hashes'].items():assert sha(OUT/name)==digest,name
    for name in ['GUIA','SOLUCIONS']:
        assert not pdfs[name]['overflow'] and sha(OUT/(name+'.pdf'))==pdfs[name]['sha256']
        assert sha(OUT/(name+'.md'))==pdfs[name]['source_sha256']
    output=ROOT/'tmp/dades-docents/practica-distancies-vilaseca-20261001-ampliada.zip'
    assert not output.exists(),'Never replace an existing sealed package.'
    inventory=[]
    for path in sorted(OUT.rglob('*')):
        if not path.is_file() or path.name in ['.ampliacio.json','MANIFEST.json']:continue
        assert not path.name.endswith(('-wal','-shm','.standalone.gpkg')),path
        inventory.append({'path':str(path.relative_to(OUT)),'bytes':path.stat().st_size,'sha256':sha(path)})
    write_json(OUT/'MANIFEST.json',{'schema_version':1,'title':'Distàncies, marxa anisòtropa i isòcrones',
        'author':'Benito Zaragozí','prepared':'2026-10-01','crs':'EPSG:25831','base_sha256':BASE_SHA,
        'runtime':QGIS_IMAGE,'file_count':len(inventory),'files':inventory})
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for item in inventory:archive.write(OUT/item['path'],'distancies-vilaseca/'+item['path'])
        archive.write(OUT/'MANIFEST.json','distancies-vilaseca/MANIFEST.json')
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None and len(archive.namelist())==len(inventory)+1
        for item in inventory:
            data=archive.read('distancies-vilaseca/'+item['path'])
            assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    receipt={'path':str(output.relative_to(ROOT)),'sha256':sha(output),'bytes':output.stat().st_size,
             'files':len(inventory)+1,'projects':15,'layers':77,'captures':21,
             'zip_crc':'ok','all_member_sha256':'ok','qgis_validation':'passed',
             'guide_pages':pdfs['GUIA']['pages'],'solutions_pages':pdfs['SOLUCIONS']['pages']}
    write_json(output.with_suffix('.receipt.json'),receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--init',action='store_true');parser.add_argument('--build',action='store_true')
    parser.add_argument('--style',action='store_true');parser.add_argument('--figure-inputs',action='store_true')
    parser.add_argument('--docs',action='store_true');parser.add_argument('--sqlite',action='store_true')
    parser.add_argument('--package',action='store_true')
    args=parser.parse_args()
    if args.build and args.style:parser.error('Run --build and --style in separate QGIS processes.')
    if args.init:initialise()
    if args.build:build()
    if args.style:style()
    if args.figure_inputs:figure_inputs()
    if args.docs:refresh_docs()
    if args.sqlite:standalone_sqlite()
    if args.package:package()
