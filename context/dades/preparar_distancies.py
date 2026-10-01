"""Local, reproducible workshop on Euclidean distance, networks and raster cost.

Use the pinned QGIS 3.44 runtime. Only this new private destination is writable;
all source inventories stay read-only. --fetch needs the official ICGC services;
the calculation and classroom projects work offline afterwards.
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
import zipfile

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'tmp/dades-docents/qgis/distancies-vilaseca-20261001'
RTT=ROOT/'tmp/dades-docents/practiques/rtt-original.gpkg'
BOUNDS=(343600,4553000,345300,4554700)
RES=5
MDT_URL='https://datacloud.icgc.cat/datacloud/model-elevacions-terreny/tif_unzip/model-elevacions-terreny-lidar-catalunya-5m-2021-2023.tif'
RTT_SHA='5233ff1fa85cb2fee92ca484e5d5ab5232a321fd1dfaf59df93aa8ca87c8f151'
ORIGIN=(344407.0,4553668.36)
DESTINATION=(344473.01,4554030.72)
PASS_ID=1354754
CAPTURES=['distancies-dades','distancies-vector-parametres','distancies-vector-resultat',
          'distancies-raster-parametres','distancies-raster-resultat','distancies-xarxa-parametres',
          'distancies-xarxa-resultat','distancies-isocrones-parametres','distancies-isocrones-resultat',
          'distancies-friccio','distancies-cost-parametres','distancies-path-parametres',
          'distancies-cost-resultat','distancies-pineda-friccio','distancies-pineda-cost']

def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def setup():
    marker=OUT/'.preparacio.json'
    if OUT.exists():
        assert marker.exists() and json.loads(marker.read_text())['owner']=='preparar_distancies.py',OUT
    else:
        OUT.mkdir()
        marker.write_text(json.dumps({'owner':'preparar_distancies.py','created':'2026-10-01'})+'\n')
    for name in ['fonts','dades','resultats','projectes','controls']:(OUT/name).mkdir(exist_ok=True)
    assert sha(RTT)==RTT_SHA,'Original RTT alterat'

def fetch():
    from osgeo import gdal,osr
    gdal.UseExceptions();setup()
    manifest_path=OUT/'fonts/fonts.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    def record(path,**info):
        manifest[path.name]={'sha256':sha(path),'bytes':path.stat().st_size,'consulta':'2026-10-01',**info}
        manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    def ready(path):
        if not path.exists():return False
        assert path.name in manifest and sha(path)==manifest[path.name]['sha256'],path
        return True
    x0,y0,x1,y1=BOUNDS
    ortho=OUT/'fonts/ortofoto-2025.tif'
    if not ready(ortho):
        params={'SERVICE':'WMS','VERSION':'1.3.0','REQUEST':'GetMap','LAYERS':'ortofoto_25cm_color_2025',
                'STYLES':'','CRS':'EPSG:25831','BBOX':','.join(map(str,BOUNDS)),
                'WIDTH':1700,'HEIGHT':1700,'FORMAT':'image/png'}
        url='https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?'+urlencode(params)
        for attempt in range(3):
            try:
                request=urllib.request.Request(url,headers={'User-Agent':'Geodisseny teaching workshop'})
                with urllib.request.urlopen(request,timeout=120) as response:content=response.read(25_000_001)
                break
            except urllib.error.HTTPError as error:
                if error.code<500 or attempt==2:raise
                time.sleep(2+attempt*3)
        assert len(content)<=25_000_000 and content.startswith(b'\x89PNG\r\n\x1a\n')
        gdal.FileFromMemBuffer('/vsimem/orto-vilaseca.png',content)
        image=gdal.Translate(str(ortho),'/vsimem/orto-vilaseca.png',format='GTiff',outputSRS='EPSG:25831',
            outputBounds=[x0,y1,x1,y0],creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        assert image.RasterXSize==1700;image=None;gdal.Unlink('/vsimem/orto-vilaseca.png')
        record(ortho,producer='ICGC',url=url,edition=2025,bounds=BOUNDS,resolution_m=1,
               derivation='WMS 25 cm source rendered at 1 m per output pixel; RGB GeoTIFF')
    dem=OUT/'fonts/mdt-5m.tif'
    if not ready(dem):
        gdal.SetConfigOption('GDAL_DISABLE_READDIR_ON_OPEN','EMPTY_DIR')
        gdal.SetConfigOption('GDAL_HTTP_TIMEOUT','90')
        image=gdal.Translate(str(dem),'/vsicurl/'+MDT_URL,format='GTiff',projWin=[x0,y1,x1,y0],
            xRes=RES,yRes=RES,resampleAlg='nearest',creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        assert image.GetGeoTransform()==(x0,RES,0.,y1,0.,-RES)
        assert image.RasterXSize==340 and image.RasterYSize==340
        image=None
        record(dem,producer='ICGC',url=MDT_URL,edition='LiDAR 2021–2023',bounds=BOUNDS,resolution_m=5,
               derivation='Native 5 m bounded crop; no interpolation to finer resolution')
    manifest['rtt-original.gpkg']={'source':str(RTT.relative_to(ROOT)),'sha256':RTT_SHA,'edition':2024,
        'producer':'ICGC','url':'https://datacloud.icgc.cat/datacloud/topografia-territorial/gpkg_unzip/topografia-territorial-v1r0-2024.gpkg',
        'note':'Previously retained original features; local subset is made without moving their vertices.'}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

def build():
    """Calculate with QGIS/GDAL/GRASS and independently check raster distances."""
    import sys,heapq
    import numpy as np
    import shapely
    from shapely.geometry import Point,LineString,box
    from osgeo import gdal,ogr,osr
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsProcessingContext,
        QgsVectorLayer,QgsVectorFileWriter,QgsGeometry,QgsFeature,QgsField,QgsRasterLayer,QgsProcessingException)
    from qgis.PyQt.QtCore import QVariant
    setup();gdal.UseExceptions();ogr.UseExceptions()
    app=QgsApplication([],False);app.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    def run(algorithm,params):
        print('PROCESS',algorithm,flush=True)
        return processing.run(algorithm,params,context=context)
    def save(layer,relative):
        path=OUT/relative
        assert path.resolve().is_relative_to(OUT.resolve())
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='GPKG';options.layerName=path.stem
        options.fileEncoding='UTF-8';options.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteFile
        status=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(path),project.transformContext(),options)
        assert status[0]==QgsVectorFileWriter.NoError,status
        return str(path)
    def vector(kind,fields,rows):
        layer=QgsVectorLayer(kind+'?crs=EPSG:25831','Preparació','memory')
        layer.dataProvider().addAttributes([QgsField(n,t) for n,t in fields]);layer.updateFields()
        features=[]
        for geometry,attributes in rows:
            f=QgsFeature(layer.fields());g=QgsGeometry();g.fromWkb(shapely.force_2d(geometry).wkb)
            if kind.startswith('Multi'):g.convertToMultiType()
            f.setGeometry(g);f.setAttributes(attributes);features.append(f)
        assert layer.dataProvider().addFeatures(features)[0];layer.updateExtents()
        return layer
    original=ogr.Open(str(RTT),0);source=original.GetLayerByName('_35_transports_l');source.SetSpatialFilterRect(*BOUNDS)
    features=list(source)
    extract=OUT/'fonts/rtt-vilaseca.gpkg'
    if not extract.exists():
        target=ogr.GetDriverByName('GPKG').CreateDataSource(str(extract));source.ResetReading()
        target.CopyLayer(source,'eixos',options=['FID=rtt_id'])
        for name in ['transports_tipus','transports_terreny','transports_xarxa']:
            target.CopyLayer(original.GetLayerByName(name),name)
        target=None
    allowed={'vca','vnc','vcu','vpu','vpd','vcd','cor','bir','bin'}
    boundary=box(*BOUNDS);network=[];highways=[];crossings=[]
    for f in features:
        geom=shapely.force_2d(shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())))
        if f['codivia']=='AP-7':highways.append(geom.intersection(boundary))
        if f['tipus'] not in allowed:continue
        clipped=geom.intersection(boundary)
        for line in clipped.geoms if clipped.geom_type in ('MultiLineString','GeometryCollection') else [clipped]:
            if line.geom_type!='LineString' or line.length==0:continue
            network.append((line,[f.GetFID(),f['tipus'],f['nom'],'B',5.0]))
    # RTT axes are cartography, not a pre-noded navigation graph. Split only
    # endpoint-to-interior contacts (<= 5 mm) between generic ground-level
    # axes. Do NOT split arbitrary line crossings or connect motorway axes.
    from shapely.ops import substring
    terrain={f.GetFID():f['terreny'] for f in features}
    geometries=[g for g,attrs in network];tree=shapely.STRtree(geometries)
    cuts={i:[] for i in range(len(network))};junctions=[]
    for i,(line,attrs) in enumerate(network):
        if terrain[attrs[0]]!='gen':continue
        for xy in [line.coords[0],line.coords[-1]]:
            point=Point(xy)
            for j in tree.query(point.buffer(.005)):
                j=int(j)
                if j==i or terrain[network[j][1][0]]!='gen':continue
                other=geometries[j];position=other.project(point)
                if .005<position<other.length-.005 and point.distance(other)<=.005:
                    cuts[j].append(position)
                    junctions.append({'endpoint_axis':attrs[0],'split_axis':network[j][1][0],'xy':list(xy),
                                      'distance_m':point.distance(other)})
    noded=[]
    for i,(line,attrs) in enumerate(network):
        positions=[0,*sorted(set(cuts[i])),line.length]
        for first,last in zip(positions,positions[1:]):
            if last-first<.001:continue
            part=substring(line,first,last)
            rounded=LineString(np.round(shapely.get_coordinates(part),3))
            if rounded.length>0:noded.append((rounded,attrs))
    print('ENDPOINT JUNCTIONS',json.dumps(junctions,ensure_ascii=False),flush=True)
    network=noded
    fields=[('rtt_id',QVariant.LongLong),('tipus',QVariant.String),('nom',QVariant.String),
            ('sentit',QVariant.String),('v_kmh',QVariant.Double)]
    opened=vector('MultiLineString',fields,network)
    closed_rows=[(g,a) for g,a in network if a[0]!=PASS_ID]
    assert len(network)-len(closed_rows)>=1
    closed=vector('MultiLineString',fields,closed_rows)
    save(opened,'dades/xarxa-oberta.gpkg');save(closed,'dades/xarxa-tancada.gpkg')
    vertices={tuple(p) for g,a in network for p in shapely.get_coordinates(g)}
    assert ORIGIN in vertices and DESTINATION in vertices
    points=vector('Point',[('nom',QVariant.String),('paper',QVariant.String)],
        [(Point(ORIGIN),['O · Origen','origen']),(Point(DESTINATION),['D · Destí','desti'])])
    save(points,'dades/extrems.gpkg')
    starts=vector('Point',[('nom',QVariant.String)],[(Point(ORIGIN),['O · Origen'])])
    ends=vector('Point',[('nom',QVariant.String)],[(Point(DESTINATION),['D · Destí'])])
    origin_path=save(starts,'dades/origen.gpkg');destination_path=save(ends,'dades/desti.gpkg')
    highway=shapely.union_all(highways);barrier=highway.buffer(25).intersection(boundary)
    save(vector('MultiPolygon',[('nom',QVariant.String)],[(barrier,['AP-7 · barrera del model'])]),'dades/barrera-ap7.gpkg')
    # A corridor crosses the band only where a non-motorway axis crosses the
    # motorway axes. Width 20 m and 40 m extensions are declared model choices.
    for line,attributes in network:
        if not line.intersects(highway):continue
        xy=shapely.get_coordinates(line);first=xy[0]-40*(xy[1]-xy[0])/np.linalg.norm(xy[1]-xy[0])
        last=xy[-1]+40*(xy[-1]-xy[-2])/np.linalg.norm(xy[-1]-xy[-2])
        corridor=LineString(np.vstack([first,xy,last])).buffer(10,cap_style='flat')
        crossings.append((corridor,attributes[0]))
    target_corridors=[g for g,fid in crossings if fid==PASS_ID]
    assert len(target_corridors)==1
    other_corridors=[g for g,fid in crossings if fid!=PASS_ID]
    assert other_corridors,'Need another represented crossing for the detour'
    save(vector('MultiPolygon',[('nom',QVariant.String)],[(target_corridors[0],['P2 · pas que tanquem o obrim'])]),'dades/pas-p2.gpkg')
    save(vector('MultiPolygon',[('nom',QVariant.String),('rtt_id',QVariant.LongLong)],
                [(g,['Altres passos',fid]) for g,fid in crossings if fid!=PASS_ID]),'dades/altres-passos.gpkg')
    save(vector('Polygon',[('nom',QVariant.String)],[(boundary,['Àmbit comú · cel·la de 5 m'])]),'dades/ambit.gpkg')
    building_zip=ROOT/'tmp/dades-docents/seccions/originals/cadastre-dgc-43173.zip'
    with zipfile.ZipFile(building_zip) as archive:
        building_member=next(n for n in archive.namelist() if n.endswith('.building.gml'))
    building_source=ogr.Open('/vsizip/'+str(building_zip)+'/'+building_member)
    building_layer=building_source.GetLayerByName('Building');building_layer.SetSpatialFilterRect(*BOUNDS)
    reference=osr.SpatialReference();reference.ImportFromEPSG(25831)
    assert building_layer.GetSpatialRef().IsSame(reference)
    buildings=[]
    for f in building_layer:
        geometry=shapely.force_2d(shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())))
        if not geometry.is_valid:geometry=shapely.make_valid(geometry)
        geometry=geometry.intersection(boundary)
        if geometry.geom_type in ('Polygon','MultiPolygon') and not geometry.is_empty:
            buildings.append((geometry,[f['gml_id']]))
    assert buildings
    save(vector('MultiPolygon',[('id_font',QVariant.String)],buildings),'fonts/edificis.gpkg')
    provenance_path=OUT/'fonts/fonts.json';provenance=json.loads(provenance_path.read_text())
    provenance['edificis.gpkg']={'producer':'Dirección General del Catastro','municipality':'Vila-seca',
        'source':str(building_zip.relative_to(ROOT)),'source_sha256':sha(building_zip),
        'catalogue':'https://www.catastro.hacienda.gob.es/INSPIRE/Buildings/43/ES.SDGC.BU.atom_43.xml',
        'derivation':'Building footprints intersecting the study extent; clipped, validified when necessary, original identifier retained.',
        'features':len(buildings),'sha256':sha(OUT/'fonts/edificis.gpkg')}
    provenance_path.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
    straight=run('native:shortestline',{'SOURCE':starts,'DESTINATION':ends,'METHOD':0,'NEIGHBORS':1,'OUTPUT':'memory:'})['OUTPUT']
    save(straight,'resultats/linia-euclidiana.gpkg')
    euclidean=next(straight.getFeatures()).geometry().length()
    assert abs(euclidean-math.dist(ORIGIN,DESTINATION))<1e-8
    extent=f'{BOUNDS[0]},{BOUNDS[2]},{BOUNDS[1]},{BOUNDS[3]} [EPSG:25831]'
    origin_raster=str(OUT/'dades/origen-5m.tif')
    run('gdal:rasterize',{'INPUT':starts,'BURN':1,'UNITS':1,'WIDTH':RES,'HEIGHT':RES,'EXTENT':extent,
        'INIT':0,'DATA_TYPE':0,'OUTPUT':origin_raster})
    proximity=str(OUT/'resultats/distancia-euclidiana.tif')
    run('gdal:proximity',{'INPUT':origin_raster,'BAND':1,'VALUES':'1','UNITS':0,'DATA_TYPE':5,
                         'NODATA':-9999,'OUTPUT':proximity})
    dem=gdal.Open(str(OUT/'fonts/mdt-5m.tif'));gt=dem.GetGeoTransform();shape=(dem.RasterYSize,dem.RasterXSize)
    assert gt==(BOUNDS[0],RES,0.,BOUNDS[3],0.,-RES)
    assert np.all(dem.ReadAsArray()!=dem.GetRasterBand(1).GetNoDataValue())
    def cell(p):return int((p[1]-gt[3])/gt[5]),int((p[0]-gt[0])/gt[1])
    a,b=cell(ORIGIN),cell(DESTINATION)
    def centre(ij):return gt[0]+(ij[1]+.5)*RES,gt[3]-(ij[0]+.5)*RES
    origin_image=gdal.Open(origin_raster)
    assert origin_image.GetGeoTransform()==gt and np.count_nonzero(origin_image.ReadAsArray()==1)==1
    assert origin_image.ReadAsArray()[a]==1
    dist_image=gdal.Open(proximity);assert dist_image.GetGeoTransform()==gt
    raster_distance=float(dist_image.ReadAsArray()[b])
    assert abs(raster_distance-math.dist(centre(a),centre(b)))<1e-3
    assert abs(raster_distance-euclidean)<=RES*math.sqrt(2)
    save(vector('Point',[('nom',QVariant.String)],[(Point(centre(a)),['O · centre de cel·la']),
        (Point(centre(b)),['D · centre de cel·la'])]),'dades/centres-cella.gpkg')
    params={'STRATEGY':0,'START_POINT':f'{ORIGIN[0]},{ORIGIN[1]} [EPSG:25831]',
            'END_POINT':f'{DESTINATION[0]},{DESTINATION[1]} [EPSG:25831]',
            'DIRECTION_FIELD':'sentit','VALUE_FORWARD':'F','VALUE_BACKWARD':'R','VALUE_BOTH':'B',
            'DEFAULT_DIRECTION':2,'SPEED_FIELD':'v_kmh','DEFAULT_SPEED':5,'TOLERANCE':0,'POINT_TOLERANCE':.1,'OUTPUT':'memory:'}
    controls={'origin':ORIGIN,'destination':DESTINATION,'bounds':BOUNDS,'resolution_m':RES,'crs':'EPSG:25831',
              'ellipsoid':'NONE','euclidean_vector_m':euclidean,'euclidean_raster_m':raster_distance,
              'origin_cell_centre':centre(a),'destination_cell_centre':centre(b),
              'network_types':sorted(allowed),'network_count':len(network),'closed_edge_id':PASS_ID,
              'endpoint_junctions':junctions,'coordinate_rounding_m':.001,
              'crossing_ids':[fid for g,fid in crossings],'network':{},'service_areas':{},'raster_cost':{}}
    for name,layer in [('obert',opened),('tancat',closed)]:
        try:
            route=run('native:shortestpathpointtopoint',{**params,'INPUT':layer})['OUTPUT']
        except QgsProcessingException as error:
            if name!='tancat' or 'no route' not in str(error).lower():raise
            controls['network'][name]={'reachable':False,'length_m':None,'time_h':None,'time_min':None,
                                       'message':'No route in this selected cartographic network after closing the pass.'}
            save(vector('MultiLineString',[('nom',QVariant.String)],[]),f'resultats/ruta-xarxa-{name}.gpkg')
            continue
        f=next(route.getFeatures());length=f.geometry().length()
        assert length>=euclidean-.01
        save(route,f'resultats/ruta-xarxa-{name}.gpkg')
        fast=run('native:shortestpathpointtopoint',{**params,'INPUT':layer,'STRATEGY':1})['OUTPUT']
        hours=float(next(fast.getFeatures())['cost'])
        assert abs(hours-length/5000)<1e-8
        controls['network'][name]={'reachable':True,'length_m':length,'time_h':hours,'time_min':hours*60}
    assert controls['network']['obert']['reachable']
    if controls['network']['tancat']['reachable']:
        assert controls['network']['tancat']['length_m']>controls['network']['obert']['length_m']
    # Empirical check of the public algorithm's time parameter: the new
    # TRAVEL_COST2 parameter is exercised on a 1000 m line at 6 km/h.
    toy=vector('MultiLineString',[('v_kmh',QVariant.Double)],[(LineString([(350000,4550000),(351000,4550000)]),[6.])])
    def service(layer,point,cost):
        return run('native:serviceareafrompoint',{'INPUT':layer,'STRATEGY':1,'SPEED_FIELD':'v_kmh','DEFAULT_SPEED':5,
            'DEFAULT_DIRECTION':2,'TOLERANCE':0,'START_POINT':point,'TRAVEL_COST2':cost,'OUTPUT_LINES':'memory:'})['OUTPUT_LINES']
    trial=service(toy,'350000,4550000 [EPSG:25831]',5)
    trial_length=sum(f.geometry().length() for f in trial.getFeatures())
    service_unit='minutes' if abs(trial_length-500)<.1 else 'hours'
    if service_unit=='hours':
        trial=service(toy,'350000,4550000 [EPSG:25831]',5/60)
        assert abs(sum(f.geometry().length() for f in trial.getFeatures())-500)<.1,trial_length
    controls['service_time_parameter']={'name':'TRAVEL_COST2','unit':service_unit,'toy_check_m':500,'toy_speed_kmh':6}
    def unique_length(layer):
        return shapely.union_all([shapely.from_wkb(bytes(f.geometry().asWkb())) for f in layer.getFeatures()]).length
    for minutes in [3,6,12]:
        cost=minutes if service_unit=='minutes' else minutes/60
        layer=service(opened,params['START_POINT'],cost)
        assert layer.featureCount()>0
        save(layer,f'resultats/servei-{minutes:02d}-min.gpkg')
        controls['service_areas'][str(minutes)]={'features':layer.featureCount(),'parameter':cost,
            'raw_sum_of_segments_m':sum(f.geometry().length() for f in layer.getFeatures()),
            'unique_reachable_line_m':unique_length(layer)}
    closed_service=service(closed,params['START_POINT'],6 if service_unit=='minutes' else 6/60)
    save(closed_service,'resultats/servei-tancat-06-min.gpkg')
    controls['closed_service_6_min_m']=unique_length(closed_service)
    sr=osr.SpatialReference();sr.ImportFromEPSG(25831)
    def burn(geometries):
        memory=ogr.GetDriverByName('Memory').CreateDataSource('');vl=memory.CreateLayer('polygons',sr,ogr.wkbMultiPolygon)
        for geom in geometries:
            f=ogr.Feature(vl.GetLayerDefn());f.SetGeometry(ogr.CreateGeometryFromWkb(geom.wkb));vl.CreateFeature(f)
        image=gdal.GetDriverByName('MEM').Create('',shape[1],shape[0],1,gdal.GDT_Byte)
        image.SetGeoTransform(gt);image.SetProjection(dem.GetProjection())
        gdal.RasterizeLayer(image,[1],vl,burn_values=[1]);return image.ReadAsArray().astype(bool)
    def raster(relative,array,nodata=-9999):
        path=OUT/relative
        image=gdal.GetDriverByName('GTiff').Create(str(path),shape[1],shape[0],1,gdal.GDT_Float32,['COMPRESS=DEFLATE','TILED=YES'])
        image.SetGeoTransform(gt);image.SetProjection(dem.GetProjection())
        image.GetRasterBand(1).SetNoDataValue(nodata);image.GetRasterBand(1).WriteArray(array);image=None
        return str(path)
    road_mask=burn([g.buffer(5) for g,attrs in network]);barrier_mask=burn([barrier])
    others_mask=burn(other_corridors);p2_mask=burn(target_corridors);building_mask=burn([g for g,a in buildings])
    raster('dades/mascara-camins.tif',road_mask.astype(float));raster('dades/mascara-ap7.tif',barrier_mask.astype(float))
    raster('dades/mascara-altres-passos.tif',others_mask.astype(float));raster('dades/mascara-p2.tif',p2_mask.astype(float))
    raster('dades/mascara-edificis.tif',building_mask.astype(float))
    neighbours=[(dy,dx) for dy in [-1,0,1] for dx in [-1,0,1] if dy or dx]
    for name,gate in [('tancat',others_mask),('obert',others_mask|p2_mask)]:
        friction=np.where(road_mask,1.,4.)
        friction[barrier_mask]=-9999;friction[gate]=1.;friction[building_mask]=-9999
        assert friction[a]>0 and friction[b]>0
        friction_path=raster(f'dades/friccio-{name}.tif',friction)
        cellcost=np.where(friction>0,friction*RES,-9999)
        input_path=raster(f'dades/cost-cella-{name}.tif',cellcost)
        accum=str(OUT/f'resultats/cost-acumulat-{name}.tif');direction=str(OUT/f'resultats/direccions-{name}.tif')
        run('grass:r.cost',{'input':input_path,'start_points':origin_path,'-k':False,'-n':True,
            'output':accum,'outdir':direction,'GRASS_REGION_PARAMETER':extent,'GRASS_REGION_CELLSIZE_PARAMETER':RES})
        raster_path=str(OUT/f'resultats/cami-raster-{name}.tif');vector_path=str(OUT/f'resultats/ruta-cost-{name}.gpkg')
        if Path(vector_path).exists():Path(vector_path).unlink()
        run('grass:r.path',{'input':direction,'format':1,'start_points':destination_path,'raster_path':raster_path,
            'vector_path':vector_path,'GRASS_REGION_PARAMETER':extent,'GRASS_REGION_CELLSIZE_PARAMETER':RES})
        accumulated=gdal.Open(accum);assert accumulated.GetGeoTransform()==gt
        actual=float(accumulated.ReadAsArray()[b]);assert actual>0
        distance=np.full(shape,np.inf);distance[a]=0.;queue=[(0.,a)]
        while queue:
            cost,(y,x)=heapq.heappop(queue)
            if cost!=distance[y,x]:continue
            if (y,x)==b:break
            for dy,dx in neighbours:
                yy,xx=y+dy,x+dx
                if not (0<=yy<shape[0] and 0<=xx<shape[1]) or friction[yy,xx]<=0:continue
                candidate=cost+(friction[y,x]+friction[yy,xx])*.5*RES*math.hypot(dy,dx)
                if candidate<distance[yy,xx]:distance[yy,xx]=candidate;heapq.heappush(queue,(candidate,(yy,xx)))
        assert abs(actual-distance[b])<.02,(name,actual,distance[b])
        route_layer=QgsVectorLayer(vector_path,'Camí de cost','ogr');assert route_layer.isValid()
        route_length=sum(f.geometry().length() for f in route_layer.getFeatures())
        assert route_length>=raster_distance-.02
        array=accumulated.ReadAsArray();valid=np.isfinite(array)&(array!=accumulated.GetRasterBand(1).GetNoDataValue())
        assert np.count_nonzero(valid)<array.size
        controls['raster_cost'][name]={'cost_weighted_m':actual,'path_length_m':route_length,
            'independent_check':float(distance[b]),'reachable_cells':int(np.count_nonzero(valid)),
            'excluded_cells':int(np.count_nonzero(friction<0))}
    assert controls['raster_cost']['obert']['cost_weighted_m']<controls['raster_cost']['tancat']['cost_weighted_m']
    run('gdal:slope',{'INPUT':str(OUT/'fonts/mdt-5m.tif'),'BAND':1,'SCALE':1,'AS_PERCENT':False,'COMPUTE_EDGES':True,
                      'OUTPUT':str(OUT/'dades/pendent-graus.tif')})
    controls['assumptions']={'speed_kmh':5,'directions':'both','road_buffer_m':5,'motorway_buffer_m':25,
        'crossing_corridor_width_m':20,'crossing_extension_m':40,'friction':{'roads':1,'other':4,'motorway':'NoData except retained crossings','buildings':'NoData'},
        'cost_unit':'weighted metres, not minutes','dem_role':'grid reference and optional slope exercise; not added to the main cost'}
    (OUT/'controls/resultats.json').write_text(json.dumps(controls,ensure_ascii=False,indent=2)+'\n')
    (OUT/'controls/algorismes.json').write_text(json.dumps({name:[{'name':p.name(),'description':p.description(),
        'default':str(p.defaultValue())} for p in QgsApplication.processingRegistry().algorithmById(name).parameterDefinitions()]
        for name in ['native:shortestline','gdal:rasterize','gdal:proximity','native:shortestpathpointtopoint',
                     'native:serviceareafrompoint','grass:r.cost','grass:r.path']},ensure_ascii=False,indent=2)+'\n')
    assert sha(RTT)==RTT_SHA
    print(json.dumps(controls,ensure_ascii=False,indent=2),flush=True)

def style():
    """Prepare labelled layers and portable, task-sized QGIS projects."""
    import sys,shutil
    import numpy as np
    from osgeo import gdal
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsVectorLayer,QgsRasterLayer,
        QgsLineSymbol,QgsSimpleLineSymbolLayer,QgsFillSymbol,QgsMarkerSymbol,QgsCategorizedSymbolRenderer,
        QgsRendererCategory,QgsPalLayerSettings,QgsTextFormat,QgsTextBufferSettings,QgsVectorLayerSimpleLabeling,
        QgsRasterShader,QgsColorRampShader,QgsSingleBandPseudoColorRenderer,QgsRectangle,QgsReferencedRectangle,
        QgsGeometry,QgsFeature,QgsField,QgsVectorFileWriter,Qgis)
    from qgis.PyQt.QtGui import QColor,QFont
    from qgis.PyQt.QtCore import QVariant
    setup();gdal.UseExceptions()
    app=QgsApplication([],False);app.initQgis()
    project=QgsProject.instance();crs=QgsCoordinateReferenceSystem('EPSG:25831')
    project.setCrs(crs);project.setEllipsoid('NONE')
    controls=json.loads((OUT/'controls/resultats.json').read_text())
    pineda=ROOT/'tmp/dades-docents/practiques'
    # Copies of the earlier calculation, never edited in its original folder.
    copies={'models/solar-pineda.gpkg':'dades/pineda-parcella.gpkg',
            'models/extrems-pineda.gpkg':'dades/pineda-extrems.gpkg',
            'models/friccio-penalitzat.tif':'dades/pineda-friccio.tif',
            'models/cost-penalitzat.tif':'resultats/pineda-cost.tif',
            'models/ruta-pineda-penalitzat.gpkg':'resultats/pineda-ruta-penalitzada.gpkg',
            'models/ruta-pineda-obert.gpkg':'resultats/pineda-ruta-uniforme.gpkg',
            'mdt-solar-pineda-5m.tif':'fonts/pineda-mdt-5m.tif'}
    for original,relative in copies.items():
        if not (OUT/relative).exists():shutil.copyfile(pineda/original,OUT/relative)
    if not (OUT/'fonts/pineda-ortofoto-2025.tif').exists():
        ds=gdal.Translate(str(OUT/'fonts/pineda-ortofoto-2025.tif'),str(pineda/'orto-pineda-2025.png'),
            format='GTiff',outputSRS='EPSG:25831',outputBounds=[347200,4551420,348050,4550750],
            creationOptions=['COMPRESS=DEFLATE','TILED=YES']);ds=None
    controls['pineda_sources']={name:{'source':str((pineda/source).relative_to(ROOT)),'source_sha256':sha(pineda/source)}
        for source,name in copies.items()}
    previous=json.loads((pineda/'models/controls.json').read_text())
    controls['pineda']=previous['walking']
    layers={}
    def register(relative,name):
        path=OUT/relative
        layer=QgsRasterLayer(str(path),name) if path.suffix=='.tif' else QgsVectorLayer(str(path),name,'ogr')
        assert layer.isValid(),relative
        layers[relative]=layer
        return layer
    def persist(relative,layer):
        message,ok=layer.saveNamedStyle(str((OUT/relative).with_suffix('.qml')));assert ok,message
        if isinstance(layer,QgsVectorLayer):
            error=layer.saveStyleToDatabase('docencia','Estil del paquet de distàncies; dades i supòsits documentats',True,'')
            assert not error,error
    def line(relative,name,color,width=.8,dash=False,casing=False):
        layer=register(relative,name)
        options={'line_color':color,'line_width':str(width),'line_style':'dash' if dash else 'solid'}
        symbol=QgsLineSymbol.createSimple({'line_color':'white','line_width':str(width+.7)}) if casing else QgsLineSymbol.createSimple(options)
        if casing:symbol.appendSymbolLayer(QgsSimpleLineSymbolLayer.create(options))
        layer.renderer().setSymbol(symbol);persist(relative,layer);return layer
    def polygon(relative,name,fill,outline,width=.3):
        layer=register(relative,name)
        layer.renderer().setSymbol(QgsFillSymbol.createSimple({'color':fill,'outline_color':outline,'outline_width':str(width)}))
        persist(relative,layer);return layer
    def point(relative,name,color,shape='circle'):
        layer=register(relative,name)
        layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':shape,'size':'4.2','color':color,
                                    'outline_color':'white','outline_width':'.65'}))
        labels=QgsPalLayerSettings();labels.fieldName='nom'
        text=QgsTextFormat();font=QFont('DejaVu Sans');font.setBold(True);text.setFont(font);text.setSize(18)
        text.setColor(QColor('#202020'));halo=QgsTextBufferSettings();halo.setEnabled(True);halo.setSize(1.1)
        halo.setColor(QColor('white'));text.setBuffer(halo);labels.setFormat(text)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(labels));layer.setLabelsEnabled(True)
        persist(relative,layer);return layer
    def raster(relative,name,items,exact=False):
        layer=register(relative,name)
        function=QgsColorRampShader();function.setColorRampType(QgsColorRampShader.Exact if exact else QgsColorRampShader.Interpolated)
        function.setColorRampItemList([QgsColorRampShader.ColorRampItem(v,QColor(c),label) for v,c,label in items])
        function.setMinimumValue(items[0][0]);function.setMaximumValue(items[-1][0])
        shader=QgsRasterShader();shader.setRasterShaderFunction(function)
        renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,shader)
        renderer.setClassificationMin(items[0][0]);renderer.setClassificationMax(items[-1][0])
        layer.setRenderer(renderer);persist(relative,layer);return layer
    register('fonts/ortofoto-2025.tif','Ortofoto ICGC 2025 · píxel 1 m')
    line('dades/xarxa-oberta.gpkg','Xarxa · pas obert','#626c77',.25)
    line('dades/xarxa-tancada.gpkg','Xarxa · pas tancat','#626c77',.25)
    polygon('dades/barrera-ap7.gpkg','AP-7 · barrera del model','80,80,80,180','#3d4347',.25)
    polygon('fonts/edificis.gpkg','Edificis · barrera','155,155,155,210','#676767',.18)
    polygon('dades/pas-p2.gpkg','Pas P2 · Camí del Mas de la Plana','255,255,255,0','#9b398f',.8)
    polygon('dades/altres-passos.gpkg','Altres passos del model','255,255,255,0','#00866f',.6)
    point('dades/origen.gpkg','Origen O','#00866f')
    point('dades/desti.gpkg','Destí D','#ba3545','diamond')
    point('dades/extrems.gpkg','Extrems O i D','#ba3545')
    point('dades/centres-cella.gpkg','Centres de les cel·les O i D','#6a4c93','cross2')
    polygon('dades/ambit.gpkg','Àmbit comú · 5 m','255,255,255,0','#444444',.3)
    line('resultats/linia-euclidiana.gpkg',f'Línia recta · {controls["euclidean_vector_m"]:.1f} m'.replace('.',','),
         '#9742a0',.95,True,True)
    line('resultats/ruta-xarxa-obert.gpkg',f'Ruta de xarxa · {controls["network"]["obert"]["length_m"]:.1f} m'.replace('.',','),
         '#006699',1.15,False,True)
    line('resultats/ruta-xarxa-tancat.gpkg','Pas tancat · sense ruta','#ba3545',1.)
    for minutes,color,width in [(12,'#e89537',1.8),(6,'#27a584',1.4),(3,'#1565ad',1.0)]:
        line(f'resultats/servei-{minutes:02d}-min.gpkg',f'Accessible en {minutes} min',color,width)
    line('resultats/servei-tancat-06-min.gpkg','6 min amb el pas tancat','#ba3545',1.4,True,True)
    distance_colors=[(0,'#ffffe5','0 m'),(250,'#d9f0a3','250 m'),(500,'#78c679','500 m'),
                     (1000,'#238443','1000 m'),(1800,'#004529','1800 m')]
    raster('resultats/distancia-euclidiana.tif','Distància euclidiana · m',distance_colors)
    raster('dades/origen-5m.tif','Origen rasteritzat · 0/1',[(0,'#00ffffff','0 · fons'),(1,'#00866f','1 · origen')],True)
    for name in ['obert','tancat']:
        raster(f'dades/friccio-{name}.tif',f'Fricció · pas {name}',[(1,'#e9f6e9','1 · camins'),(4,'#e2c792','4 · resta')],True)
        raster(f'dades/cost-cella-{name}.tif',f'Cost per cel·la · pas {name}',[(5,'#e9f6e9','5 · cost de travessa'),(20,'#e2c792','20 · cost de travessa')],True)
        raster(f'resultats/cost-acumulat-{name}.tif',f'Cost acumulat · pas {name} (m ponderats)',
               [(0,'#ffffcc','0'),(250,'#c7e9b4','250'),(500,'#7fcdbb','500'),(1000,'#41b6c4','1000'),
                (2000,'#2c7fb8','2000'),(4000,'#253494','4000')])
        register(f'resultats/direccions-{name}.tif',f'Direccions de retorn · {name}')
        register(f'resultats/cami-raster-{name}.tif',f'Camí en cel·les · {name}')
        cost=controls['raster_cost'][name]['cost_weighted_m']
        line(f'resultats/ruta-cost-{name}.gpkg',f'Ruta de cost {name} · {cost:.1f} m ponderats'.replace('.',','),
             '#006699' if name=='obert' else '#cc552b',1.05,name=='tancat',True)
    raster('fonts/mdt-5m.tif','MDT LiDAR · altitud (m)',[(0,'#e7f0d7','0 m'),(25,'#c2b58b','25 m'),(50,'#92744f','50 m'),(80,'#63462c','80 m')])
    raster('dades/pendent-graus.tif','Pendent · graus',[(0,'#ffffe5','0°'),(5,'#fee391','5°'),(15,'#fec44f','15°'),(30,'#d95f0e','30°'),(60,'#993404','60°')])
    for name in ['camins','ap7','altres-passos','p2','edificis']:
        raster(f'dades/mascara-{name}.tif','Màscara · '+name,[(0,'#00ffffff','0 · fora'),(1,'#a85630','1 · dins')],True)
    register('fonts/pineda-ortofoto-2025.tif','Pineda · ortofoto ICGC 2025')
    register('fonts/pineda-mdt-5m.tif','Pineda · MDT (no usat en la fricció)')
    polygon('dades/pineda-parcella.gpkg','Parcel·la de la Pineda','255,255,255,0','#893d91',.7)
    point('dades/pineda-extrems.gpkg','Pineda · O i D','#b63449')
    raster('dades/pineda-friccio.tif','Pineda · fricció 1/20',[(1,'#e9f6e9','1 · exterior'),(20,'#e6a153','20 · parcel·la')],True)
    raster('resultats/pineda-cost.tif','Pineda · cost acumulat (m ponderats)',[(0,'#ffffcc','0'),(250,'#c7e9b4','250'),
           (500,'#7fcdbb','500'),(750,'#41b6c4','750'),(1500,'#2c7fb8','1500'),(3000,'#253494','3000')])
    line('resultats/pineda-ruta-penalitzada.gpkg','Vorejar · 724,3 m','#006699',1.15,False,True)
    line('resultats/pineda-ruta-uniforme.gpkg','Travessar · 608,3 m','#bd334c',.85,True,True)
    # One local project per teaching view keeps origin, destination and the
    # relevant raster/legend visible without layers left over from earlier shots.
    detail=(343960,4553360,344820,4554160)
    endpoints=['dades/origen.gpkg','dades/desti.gpkg']
    context_layers=['fonts/ortofoto-2025.tif','dades/xarxa-oberta.gpkg','dades/pas-p2.gpkg',*endpoints]
    views={
        '00-inici':(context_layers,detail),
        '01-dades':(context_layers,detail),
        '02-vector':(context_layers[:-2]+['resultats/linia-euclidiana.gpkg',*endpoints],detail),
        '03-raster':(['fonts/ortofoto-2025.tif','resultats/distancia-euclidiana.tif','dades/pas-p2.gpkg',*endpoints],detail),
        '04-xarxa':(context_layers[:-2]+['resultats/linia-euclidiana.gpkg','resultats/ruta-xarxa-obert.gpkg',*endpoints],detail),
        '05-isocrones':(['fonts/ortofoto-2025.tif','dades/xarxa-oberta.gpkg','resultats/servei-12-min.gpkg',
                         'resultats/servei-06-min.gpkg','resultats/servei-03-min.gpkg','resultats/servei-tancat-06-min.gpkg',
                         'dades/pas-p2.gpkg',*endpoints],BOUNDS),
        '06-friccio':(['fonts/ortofoto-2025.tif','dades/barrera-ap7.gpkg','fonts/edificis.gpkg','dades/friccio-tancat.tif',
                       'dades/altres-passos.gpkg','dades/pas-p2.gpkg',*endpoints],detail),
        '07-cost':(['fonts/ortofoto-2025.tif','dades/barrera-ap7.gpkg','fonts/edificis.gpkg','resultats/cost-acumulat-obert.tif',
                    'resultats/ruta-cost-tancat.gpkg','resultats/ruta-cost-obert.gpkg','dades/pas-p2.gpkg',*endpoints],
                   (343800,4553300,344850,4554250)),
        '08-pineda-friccio':(['fonts/pineda-ortofoto-2025.tif','dades/pineda-friccio.tif','dades/pineda-parcella.gpkg',
                            'resultats/pineda-ruta-uniforme.gpkg','resultats/pineda-ruta-penalitzada.gpkg','dades/pineda-extrems.gpkg'],
                           (347200,4550750,348050,4551420)),
        '09-pineda-cost':(['fonts/pineda-ortofoto-2025.tif','resultats/pineda-cost.tif','dades/pineda-parcella.gpkg',
                          'resultats/pineda-ruta-penalitzada.gpkg','dades/pineda-extrems.gpkg'],
                         (347200,4550750,348050,4551420))}
    inventory={key:layer.name() for key,layer in layers.items()}
    # Loading fresh copies lets each project own and safely delete its layers.
    for name,(visible,bounds) in views.items():
        project.clear();project.setCrs(crs);project.setEllipsoid('NONE');project.setTitle('Distàncies · '+name)
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for relative in visible:
            path=OUT/relative
            layer=QgsRasterLayer(str(path),inventory[relative]) if path.suffix=='.tif' else QgsVectorLayer(str(path),inventory[relative],'ogr')
            assert layer.isValid(),relative
            project.addMapLayer(layer)
        hidden=project.layerTreeRoot().addGroup('Altres dades del paquet')
        for relative in inventory:
            if relative in visible:continue
            if name.startswith(('08','09')) and 'pineda' not in relative:continue
            if not name.startswith(('08','09')) and 'pineda' in relative:continue
            path=OUT/relative
            layer=QgsRasterLayer(str(path),inventory[relative]) if path.suffix=='.tif' else QgsVectorLayer(str(path),inventory[relative],'ogr')
            project.addMapLayer(layer,False);node=hidden.addLayer(layer);node.setItemVisibilityChecked(False)
        hidden.setExpanded(False)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*bounds),crs))
        assert project.write(str(OUT/'projectes'/f'{name}.qgz'))
    (OUT/'controls/capes.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
    (OUT/'controls/vistes.json').write_text(json.dumps({k:{'visible':v,'bounds':b} for k,(v,b) in views.items()},ensure_ascii=False,indent=2)+'\n')
    (OUT/'controls/resultats.json').write_text(json.dumps(controls,ensure_ascii=False,indent=2)+'\n')
    provenance_path=OUT/'fonts/fonts.json';provenance=json.loads(provenance_path.read_text())
    provenance['edificis.gpkg']['sha256']=sha(OUT/'fonts/edificis.gpkg')
    provenance_path.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
    print('Styled',len(layers),'layers and wrote',len(views),'relative-path QGIS projects',flush=True)

def stage():
    """Curate a portable handout tree; do not include exploratory/obsolete files."""
    import shutil,sqlite3
    import xml.etree.ElementTree as ET
    setup();target=OUT/'lliurament';marker=target/'.stage-owner.json'
    if target.exists():assert marker.exists() and json.loads(marker.read_text())['owner']=='preparar_distancies.py'
    else:
        target.mkdir();marker.write_text(json.dumps({'owner':'preparar_distancies.py'})+'\n')
    source_inventory=json.loads((OUT/'controls/capes.json').read_text())
    files={name:OUT/name for name in source_inventory}
    for name in list(files):
        qml=(OUT/name).with_suffix('.qml')
        if qml.exists():files[str(Path(name).with_suffix('.qml'))]=qml
    for name in ['fonts/rtt-vilaseca.gpkg','fonts/fonts.json','controls/resultats.json',
                 'controls/capes.json','controls/vistes.json','controls/algorismes.json']:
        files[name]=OUT/name
    views=json.loads((OUT/'controls/vistes.json').read_text())
    for name in views:files[f'projectes/{name}.qgz']=OUT/'projectes'/f'{name}.qgz'
    files['GUIA.md']=ROOT/'context/practiques/distancies-vilaseca.md'
    files['SOLUCIONS.md']=ROOT/'context/practiques/distancies-vilaseca-docent.md'
    files['reproduccio/preparar_distancies.py']=Path(__file__)
    files['reproduccio/prompt-captures.md']=ROOT/'context/qgis/distancies.md'
    for name in ['distancies','distancies-raster','distancies-xarxa','distancies-cost','distancies-pineda']:
        files[f'reproduccio/{name}.yml']=ROOT/'context/qgis'/f'{name}.yml'
    for name in CAPTURES:
        for suffix in ['.png','.annotations.svg']:
            files[f'captures/{name}{suffix}']=ROOT/'assets/captures'/f'{name}{suffix}'
        files[f'reproduccio/manifests/{name}.yml']=ROOT/'context/qgis/manifests'/f'{name}.yml'
    for name,source in sorted(files.items()):
        assert source.is_file(),source
        destination=target/name;destination.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix=='.gpkg':
            if destination.exists():destination.unlink()
            original=sqlite3.connect(f'file:{source}?mode=ro',uri=True)
            copy=sqlite3.connect(destination);original.backup(copy)
            assert copy.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
            copy.execute('PRAGMA journal_mode=DELETE');copy.close();original.close()
        else:shutil.copyfile(source,destination)
    provenance_path=target/'fonts/fonts.json';provenance=json.loads(provenance_path.read_text())
    if 'edificis.gpkg' in provenance:
        record=provenance['edificis.gpkg'];record['preparation_sha256']=record['sha256']
        record['sha256']=sha(target/'fonts/edificis.gpkg')
        record['delivery']='Standalone SQLite backup; delivery hashes are also in MANIFEST.json.'
    provenance_path.write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
    project_checks=[]
    for path in sorted((target/'projectes').glob('*.qgz')):
        with zipfile.ZipFile(path) as archive:
            qgs=next(n for n in archive.namelist() if n.endswith('.qgs'))
            document=ET.fromstring(archive.read(qgs))
        sources=[]
        for node in document.findall('.//projectlayers/maplayer/datasource'):
            text=node.text or '';relative=text.split('|',1)[0]
            assert not Path(relative).is_absolute(),(path.name,text)
            resolved=(path.parent/relative).resolve()
            assert resolved.is_relative_to(target.resolve()) and resolved.is_file(),(path.name,text)
            sources.append(str(resolved.relative_to(target)))
        assert sources
        project_checks.append({'project':path.name,'layers':len(sources),'sources':sources})
    (target/'controls/portabilitat.json').write_text(json.dumps(project_checks,ensure_ascii=False,indent=2)+'\n')
    summary=json.loads((target/'controls/resultats.json').read_text())
    csv=['model;escenari;longitud_m;cost;unitat_cost']
    csv.append(f'euclidiana_vector;independent_del_pas;{summary["euclidean_vector_m"]:.6f};{summary["euclidean_vector_m"]:.6f};m')
    csv.append(f'euclidiana_raster;independent_del_pas;{summary["euclidean_raster_m"]:.6f};{summary["euclidean_raster_m"]:.6f};m')
    for name,value in summary['network'].items():
        if value['reachable']:csv.append(f'xarxa;{name};{value["length_m"]:.6f};{value["time_min"]:.6f};minuts_a_5_kmh')
        else:csv.append(f'xarxa;{name};;;sense_ruta')
    for name,value in summary['raster_cost'].items():
        csv.append(f'cost_raster;{name};{value["path_length_m"]:.6f};{value["cost_weighted_m"]:.6f};m_ponderats')
    (target/'controls/resultats.csv').write_text('\n'.join(csv)+'\n')
    (target/'COMENCA-AQUI.txt').write_text(
        'Distàncies i recorreguts a Vila-seca\n\n'
        '1. Descomprimeix tota la carpeta.\n2. Llegeix GUIA.pdf o GUIA.md.\n'
        '3. Obre projectes/00-inici.qgz amb QGIS 3.44 i crea la teva carpeta treball.\n'
        '4. Conserva les carpetes juntes. Les dades són locals i els projectes tenen rutes relatives.\n'
        '5. resultats/ i SOLUCIONS.pdf contenen referències per comprovar la feina.\n\n'
        'Els models de velocitat i fricció són supòsits docents.\n'
        'Autor: Benito Zaragozí. Preparació: 2026-10-01.\n')
    print('Staged',len(files),'files and checked',len(project_checks),'relative-path projects at',target,flush=True)

def refresh_docs():
    """Refresh narrative sources without changing the already checked datasets."""
    import shutil
    target=OUT/'lliurament'
    assert (target/'.stage-owner.json').exists()
    for source,name in [('distancies-vilaseca.md','GUIA.md'),('distancies-vilaseca-docent.md','SOLUCIONS.md')]:
        shutil.copyfile(ROOT/'context/practiques'/source,target/name)
    shutil.copyfile(Path(__file__),target/'reproduccio/preparar_distancies.py')
    settings={'image':'ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:9e0b3a45753c170b795e9a9d6df61580085c113436beac5bf6c8de69b6562097',
        'pandoc':'3.1.11.1','engine':'xelatex','SOURCE_DATE_EPOCH':0,
        'variables':{'fontfamily':'fontspec','mainfont':'DejaVu Sans','monofont':'DejaVu Sans Mono','fontsize':'11pt','colorlinks':True},
        'GUIA':{'geometry':'a4paper,landscape,left=18mm,right=18mm,top=15mm,bottom=15mm','toc_depth':2},
        'SOLUCIONS':{'geometry':'a4paper,margin=18mm'}}
    (target/'controls/handouts.json').write_text(json.dumps(settings,ensure_ascii=False,indent=2)+'\n')

def package():
    """Seal only after the handouts and relocated QGIS projects are checked."""
    import sqlite3
    setup();target=OUT/'lliurament'
    for name in ['GUIA.pdf','SOLUCIONS.pdf','controls/verificacio-qgis.json']:
        assert (target/name).is_file(),name
    report=json.loads((target/'controls/verificacio-qgis.json').read_text());assert report['ok'],report
    output=ROOT/'tmp/dades-docents/practica-distancies-vilaseca-20261001.zip'
    assert not output.exists(),'An existing delivery is never replaced.'
    inventory=[]
    for path in sorted(target.rglob('*')):
        if not path.is_file() or path.name in ('.stage-owner.json','MANIFEST.json'):continue
        assert path.suffix not in ('.wal','.shm') and not path.name.endswith(('-wal','-shm')),path
        if path.suffix=='.gpkg':
            connection=sqlite3.connect(f'file:{path}?mode=ro',uri=True)
            assert connection.execute('PRAGMA integrity_check').fetchone()[0]=='ok';connection.close()
        inventory.append({'path':str(path.relative_to(target)),'bytes':path.stat().st_size,'sha256':sha(path)})
    manifest={'schema_version':1,'title':'Pràctica de distàncies, xarxa i costos a Vila-seca',
        'author':'Benito Zaragozí','prepared':'2026-10-01','crs':'EPSG:25831',
        'runtime':{'qgis':'3.44.11','gdal':'3.10.3','grass':'8.4.1',
                   'image':'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'},
        'file_count':len(inventory),'files':inventory}
    (target/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for record in inventory:archive.write(target/record['path'],'distancies-vilaseca/'+record['path'])
        archive.write(target/'MANIFEST.json','distancies-vilaseca/MANIFEST.json')
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist())==len(inventory)+1
        for record in inventory:
            data=archive.read('distancies-vilaseca/'+record['path'])
            assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256']
    receipt={'path':str(output.relative_to(ROOT)),'sha256':sha(output),'bytes':output.stat().st_size,
             'files':len(inventory)+1,'qgis_validation':report,'zip_crc':'ok','all_member_sha256':'ok'}
    (output.with_suffix('.receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2),flush=True)

def inspect():
    from osgeo import gdal,ogr
    import shapely
    from shapely.geometry import Point
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    setup();gdal.UseExceptions();ogr.UseExceptions()
    ds=ogr.Open(str(RTT),0);layer=ds.GetLayerByName('_35_transports_l');layer.SetSpatialFilterRect(*BOUNDS)
    features=list(layer);focus=Point(344366,4553740)
    rows=[]
    fig,ax=plt.subplots(figsize=(12,11))
    ortho=gdal.Open(str(OUT/'fonts/ortofoto-2025.tif'))
    ax.imshow(ortho.ReadAsArray()[:3].transpose(1,2,0),extent=[BOUNDS[0],BOUNDS[2],BOUNDS[1],BOUNDS[3]])
    for f in features:
        geom=shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb()))
        near=geom.distance(focus)<220
        for line in geom.geoms if geom.geom_type=='MultiLineString' else [geom]:
            xy=shapely.get_coordinates(line)
            ax.plot(xy[:,0],xy[:,1],color='#ff6600' if f['tipus']=='aut' else '#00ffff',lw=1.2 if near else .25)
        if near:
            c=geom.centroid;ax.text(c.x,c.y,str(f.GetFID()),fontsize=7,color='black',bbox={'facecolor':'white','alpha':.8,'edgecolor':'none','pad':.6})
            rows.append({'id':f.GetFID(),**f.items(),'length_m':geom.length,'bounds':geom.bounds,
                         'ends':[shapely.get_coordinates(geom)[0].tolist(),shapely.get_coordinates(geom)[-1].tolist()]})
    ax.set(xlim=(344000,344750),ylim=(4553400,4554100),aspect='equal')
    ax.ticklabel_format(style='plain',useOffset=False)
    fig.savefig(OUT/'controls/pas-inspeccio.png',dpi=150);plt.close(fig)
    (OUT/'controls/pas-inspeccio.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(rows,ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--fetch',action='store_true');parser.add_argument('--inspect',action='store_true')
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--style',action='store_true')
    parser.add_argument('--stage',action='store_true');parser.add_argument('--package',action='store_true')
    parser.add_argument('--refresh-docs',action='store_true')
    args=parser.parse_args()
    if args.build and args.style:parser.error('Execute --build and --style in separate QGIS processes.')
    if args.fetch:fetch()
    if args.inspect:inspect()
    if args.build:build()
    if args.style:style()
    if args.stage:stage()
    if args.refresh_docs:refresh_docs()
    if args.package:package()
