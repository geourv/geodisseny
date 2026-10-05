"""Visibility workshop: an industrial flare, TV-3148 and land-cover polygons.

Private originals/results and immutable Moodle deliveries stay under tmp/.
Only --fetch uses the network. Run GIS stages in the pinned QGIS image.
"""
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import time
from urllib.parse import urlencode
import urllib.request
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'tmp/dades-docents/qgis/visibilitat-costa-20261002-r3'
BOUNDS = (342000,4549000,352000,4559000)
RES = 5
DATE = '2026-10-02'
IMAGE = 'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'
BASE = 'https://datacloud.icgc.cat/datacloud/'
MDT_URL = BASE+'model-elevacions-terreny/tif_unzip/model-elevacions-terreny-lidar-catalunya-5m-2021-2023.tif'
MDS_URL = BASE+'model-superficies/tif_unzip/model-superficies-lidar-catalunya-1m-2021-2023.tif'
COVER_URL = BASE+'cobertes-sol/gpkg_unzip/cobertes-sol-v1r0-2024.gpkg'
RTT_URL = BASE+'topografia-territorial/gpkg_unzip/topografia-territorial-v1r0-2024.gpkg'
RTT = ROOT/'tmp/dades-docents/practiques/rtt-original.gpkg'
RTT_SHA = '5233ff1fa85cb2fee92ca484e5d5ab5232a321fd1dfaf59df93aa8ca87c8f151'
CURVATURE = .85714
EYE_HEIGHT = 1.7
TORCH_OSM_ID = 7682543312
TORCH_XY = (346894.82449881244,4552508.353399318)
INDUSTRIAL_ID = 1459998
BUFFER_DISTANCE = 150
BUFFER_SEGMENTS = 32
CLOSING_DISTANCES = [25,50,75,100,125,150,200,250,300,400]
CAPTURES = ['visibilitat-costa-'+name for name in ['dades','mds','torxa','punt','intervisibilitat',
    'cota-minima','carretera','acumulada','buffer-positiu','perimetre','area','poligon']]
CAPTURES += ['visibilitat-acces-'+name for name in ['menu','barra','caixa-viewshed','menu-buffer','caixa-buffer']]
FIGURES = ['visibilitat-mostreig','visibilitat-mdt-mds','visibilitat-matriu-real','visibilitat-perfils','visibilitat-perimetre']
DELIVERY = ROOT/'tmp/dades-docents/practica-visibilitat-costa-20261002-r3.zip'
PREVIOUS_DELIVERY = ROOT/'tmp/dades-docents/practica-visibilitat-costa-20261002-r2.zip'
PREVIOUS_SHA = 'afbce1dfcf05f300bb39e442c79a18da08bbcbe003765fa4ba5bb919bf165501'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write_json(path,data):
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str)+'\n')


def initialise():
    marker = OUT/'.visibilitat.json'
    if OUT.exists():
        assert marker.is_file() and json.loads(marker.read_text())['owner']==Path(__file__).name
    else:
        OUT.mkdir()
        write_json(marker,{'owner':Path(__file__).name,'created':DATE})
    for name in ['fonts','dades','resultats','projectes','controls','captures','figures','reproduccio']:
        (OUT/name).mkdir(exist_ok=True)


def clone_sources():
    """Reuse exact retained sources, without opening the previous QGIS files."""
    initialise();assert sha(PREVIOUS_DELIVERY)==PREVIOUS_SHA
    copied=[]
    with zipfile.ZipFile(PREVIOUS_DELIVERY) as archive:
        manifest=json.loads(archive.read('visibilitat-costa/MANIFEST.json'))
        for record in manifest['files']:
            relative=Path(record['path'])
            if relative.parts[0]!='fonts':continue
            assert not relative.is_absolute() and '..' not in relative.parts
            data=archive.read('visibilitat-costa/'+record['path'])
            assert hashlib.sha256(data).hexdigest()==record['sha256']
            target=OUT/relative
            if target.exists():assert sha(target)==record['sha256'],relative
            else:target.write_bytes(data)
            copied.append(record)
    write_json(OUT/'controls/source-delivery.json',{'path':str(PREVIOUS_DELIVERY.relative_to(ROOT)),
        'sha256':PREVIOUS_SHA,'copied_sources':copied})
    print('Verified and copied',len(copied),'source files from the immutable previous ZIP',flush=True)


def fetch():
    import numpy as np
    from osgeo import gdal,ogr
    import xml.etree.ElementTree as ET
    initialise(); gdal.UseExceptions(); ogr.UseExceptions()
    for key,value in {'GDAL_DISABLE_READDIR_ON_OPEN':'EMPTY_DIR','GDAL_HTTP_TIMEOUT':'120',
                      'GDAL_HTTP_MAX_RETRY':'3','CPL_VSIL_CURL_ALLOWED_EXTENSIONS':'.tif,.gpkg'}.items():
        gdal.SetConfigOption(key,value)
    manifest_path = OUT/'fonts/fonts.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    def ready(name):
        path = OUT/'fonts'/name
        if not path.exists(): return False
        assert name in manifest and sha(path)==manifest[name]['sha256'],name
        return True
    def record(name,**metadata):
        path = OUT/'fonts'/name
        manifest[name] = {'sha256':sha(path),'bytes':path.stat().st_size,'prepared':DATE,
            'producer':'ICGC','licence_url':'https://www.icgc.cat/condicions',**metadata}
        write_json(manifest_path,manifest)
        print('RETAINED',name,manifest[name]['bytes'],flush=True)
    for name,url,layername,where in [
        ('cobertes-industrials-2024.gpkg',COVER_URL,'cobertes_sol','nivell_2 = 347'),
        ('rtt-xemeneies-2024.gpkg',RTT_URL,'_20_construccions_n',"tipus = 'xem'")]:
        if ready(name): continue
        source = ogr.Open('/vsicurl/'+url,0)
        layer = source.GetLayerByName(layername)
        layer.SetSpatialFilterRect(344000,4550500,350000,4554000)
        layer.SetAttributeFilter(where)
        target = ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT/'fonts'/name))
        copy = target.CopyLayer(layer,'original',options=['FID=icgc_id'])
        count = copy.GetFeatureCount(); assert count>0
        copy=None; target=None; source=None
        record(name,url=url,edition=2024,layer=layername,selection=where,
               spatial_filter=[344000,4550500,350000,4554000],features=count,
               derivation='Whole original features intersecting the rectangle; original feature IDs retained as icgc_id.')
    if not ready('rtt-tv3148.gpkg'):
        assert sha(RTT)==RTT_SHA
        source=ogr.Open(str(RTT),0); layer=source.GetLayerByName('_35_transports_l')
        layer.SetAttributeFilter("codivia = 'TV-3148'")
        target=ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT/'fonts/rtt-tv3148.gpkg'))
        copy=target.CopyLayer(layer,'original',options=['FID=rtt_id']); count=copy.GetFeatureCount()
        assert count==63
        for name in ['transports_tipus','transports_terreny','transports_entorn']:
            target.CopyLayer(source.GetLayerByName(name),name)
        copy=None; target=None; source=None
        record('rtt-tv3148.gpkg',url=RTT_URL,edition=2024,features=count,
               source=str(RTT.relative_to(ROOT)),source_sha256=RTT_SHA,
               selection="codivia = 'TV-3148'",derivation='Original cartographic axes; both carriageways and roundabouts retained.')
    if not ready('tv3148-completa-2024.gpkg'):
        source=ogr.Open('/vsicurl/'+RTT_URL,0);layer=source.GetLayerByName('_35_transports_l')
        layer.SetSpatialFilterRect(343500,4547500,348500,4554000)
        layer.SetAttributeFilter("codivia = 'TV-3148'")
        target=ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT/'fonts/tv3148-completa-2024.gpkg'))
        copy=target.CopyLayer(layer,'original',options=['FID=rtt_id']);count=copy.GetFeatureCount()
        extent=copy.GetExtent();assert count>=63
        for name in ['transports_tipus','transports_terreny','transports_entorn']:
            target.CopyLayer(source.GetLayerByName(name),name)
        copy=None;target=None;source=None
        record('tv3148-completa-2024.gpkg',url=RTT_URL,edition=2024,features=count,
               selection="codivia = 'TV-3148'",extent=extent,
               spatial_filter=[343500,4547500,348500,4554000],
               derivation='Complete original axes tagged TV-3148, ending at the TV-3146 junction on the approach to la Pineda; IDs retained.')
    # Metadata correction after checking the complete road-code selection:
    # the southern urban continuation has code TV-3146, not TV-3148.
    manifest['tv3148-completa-2024.gpkg']['derivation']='Complete original axes tagged TV-3148, ending at the TV-3146 junction on the approach to la Pineda; IDs retained.'
    write_json(manifest_path,manifest)
    if not ready('mar-rtt-2024.gpkg'):
        import shapely
        from shapely.geometry import box
        source=ogr.Open('/vsicurl/'+RTT_URL,0);layer=source.GetLayerByName('_50_hidrografia_p')
        layer.SetSpatialFilterRect(*BOUNDS);layer.SetAttributeFilter("tipus = 'mar'")
        target=ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT/'fonts/mar-rtt-2024.gpkg'))
        copy=target.CreateLayer('mar',layer.GetSpatialRef(),ogr.wkbMultiPolygon)
        copy.CreateField(ogr.FieldDefn('icgc_id',ogr.OFTInteger64));ids=[]
        for f in layer:
            g=shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())).intersection(box(*BOUNDS))
            if g.is_empty:continue
            item=ogr.Feature(copy.GetLayerDefn());item.SetField('icgc_id',f.GetFID())
            item.SetGeometry(ogr.ForceToMultiPolygon(ogr.CreateGeometryFromWkb(g.wkb)))
            assert copy.CreateFeature(item)==0;ids.append(f.GetFID())
        assert ids;copy=None;target=None;source=None
        record('mar-rtt-2024.gpkg',url=RTT_URL,edition=2024,layer='_50_hidrografia_p',
               selection="tipus = 'mar'",source_ids=ids,derivation='Sea polygons clipped to the calculation rectangle.')
    if not ready('mar-cobertes-2024.gpkg'):
        import shapely
        from shapely.geometry import box
        source=ogr.Open('/vsicurl/'+COVER_URL,0);layer=source.GetLayerByName('cobertes_sol')
        layer.SetSpatialFilterRect(*BOUNDS);layer.SetAttributeFilter('nivell_2 = 466')
        target=ogr.GetDriverByName('GPKG').CreateDataSource(str(OUT/'fonts/mar-cobertes-2024.gpkg'))
        copy=target.CreateLayer('mar',layer.GetSpatialRef(),ogr.wkbMultiPolygon)
        copy.CreateField(ogr.FieldDefn('icgc_id',ogr.OFTInteger64));ids=[]
        for f in layer:
            g=shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())).intersection(box(*BOUNDS))
            if g.is_empty:continue
            item=ogr.Feature(copy.GetLayerDefn());item.SetField('icgc_id',f.GetFID())
            item.SetGeometry(ogr.ForceToMultiPolygon(ogr.CreateGeometryFromWkb(g.wkb)))
            assert copy.CreateFeature(item)==0;ids.append(f.GetFID())
        assert ids;copy=None;target=None;source=None
        record('mar-cobertes-2024.gpkg',url=COVER_URL,edition=2024,selection='nivell_2 = 466',
               source_ids=ids,derivation='Original sea category clipped to the calculation rectangle.')
    if not ready('torxa-osm-v1.json'):
        url=f'https://www.openstreetmap.org/api/0.6/node/{TORCH_OSM_ID}/1'
        with urllib.request.urlopen(url,timeout=90) as response:xml=response.read(20000)
        node=ET.fromstring(xml).find('node');tags={t.attrib['k']:t.attrib['v'] for t in node.findall('tag')}
        assert node.attrib['id']==str(TORCH_OSM_ID) and tags['man_made']=='flare'
        write_json(OUT/'fonts/torxa-osm-v1.json',{'id':TORCH_OSM_ID,'version':1,
            'latitude':float(node.attrib['lat']),'longitude':float(node.attrib['lon']),
            'timestamp':node.attrib['timestamp'],'tags':tags,'source_url':url})
        record('torxa-osm-v1.json',producer='OpenStreetMap contributors',url=url,
               edition='Node version 1, 2020-07-04',licence_url='https://www.openstreetmap.org/copyright',
               derivation='Selected public node and descriptive tags; location checked against ICGC orthoimage.')
    x0,y0,x1,y1=BOUNDS
    for name,url,method in [('mdt-5m.tif',MDT_URL,'Native 5 m crop; overviews disabled'),
        ('mds-max-5m.tif',MDS_URL,'Maximum of native 1 m samples per 5 m cell; overviews disabled')]:
        if ready(name): continue
        path=OUT/'fonts'/('partial-'+name)
        if path.exists(): path.unlink()
        if name.startswith('mdt'):
            ds=gdal.Translate(str(path),'/vsicurl/'+url,format='GTiff',projWin=[x0,y1,x1,y0],
                xRes=RES,yRes=RES,resampleAlg='nearest',overviewLevel='NONE',
                creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        else:
            ds=gdal.Warp(str(path),'/vsicurl/'+url,format='GTiff',outputBounds=BOUNDS,
                dstSRS='EPSG:25831',xRes=RES,yRes=RES,targetAlignedPixels=True,resampleAlg='max',
                overviewLevel='NONE',outputType=gdal.GDT_Float32,dstNodata=-9999,warpMemoryLimit=256,
                creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        assert ds.GetGeoTransform()==(x0,RES,0.,y1,0.,-RES)
        array=ds.ReadAsArray(); nodata=ds.GetRasterBand(1).GetNoDataValue()
        valid=np.isfinite(array)&(array!=nodata)
        stats={'shape':list(array.shape),'nodata':nodata,'invalid_cells':int((~valid).sum()),
               'min':float(array[valid].min()),'max':float(array[valid].max())}
        ds=None; path.rename(OUT/'fonts'/name)
        record(name,url=url,edition='LiDAR 2021–2023',crs='EPSG:25831',bounds=BOUNDS,
               resolution_m=RES,derivation=method,statistics=stats)
    if not ready('mds-torxa-1m.tif'):
        bounds=[346850,4552460,346940,4552560]
        ds=gdal.Translate(str(OUT/'fonts/mds-torxa-1m.tif'),'/vsicurl/'+MDS_URL,format='GTiff',
            projWin=[bounds[0],bounds[3],bounds[2],bounds[1]],overviewLevel='NONE',
            creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        assert ds.GetGeoTransform()[1]==1;ds=None
        record('mds-torxa-1m.tif',url=MDS_URL,edition='LiDAR 2021–2023',bounds=bounds,
               resolution_m=1,derivation='Native 1 m crop around the identified flare; no overview or interpolation.')
    for name,bounds,res in [('ortofoto-context-2025.tif',BOUNDS,10),
        ('ortofoto-industria-2025.tif',(345000,4550500,349500,4553250),2.5),
        ('ortofoto-torxa-2025.tif',(346650,4552300,347150,4552750),.5)]:
        if ready(name): continue
        a,b,c,d=bounds
        params={'SERVICE':'WMS','VERSION':'1.3.0','REQUEST':'GetMap','LAYERS':'ortofoto_25cm_color_2025',
            'STYLES':'','CRS':'EPSG:25831','BBOX':','.join(map(str,bounds)),
            'WIDTH':int((c-a)/res),'HEIGHT':int((d-b)/res),'FORMAT':'image/png'}
        url='https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?'+urlencode(params)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url,timeout=120) as response: content=response.read(30_000_001)
                assert content.startswith(b'\x89PNG\r\n\x1a\n') and len(content)<=30_000_000
                break
            except Exception:
                if attempt==2: raise
                time.sleep(3)
        gdal.FileFromMemBuffer('/vsimem/costa.png',content)
        ds=gdal.Translate(str(OUT/'fonts'/name),'/vsimem/costa.png',format='GTiff',
            outputSRS='EPSG:25831',outputBounds=[a,d,c,b],creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        ds=None; gdal.Unlink('/vsimem/costa.png')
        record(name,url=url,edition=2025,bounds=bounds,resolution_m=res,
               derivation=f'WMS 25 cm source rendered at {res} m/pixel for cartographic context.')
    print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True)


def geometry():
    """Compare native QGIS closings and retain a compact study precinct."""
    import sys
    import shapely
    from shapely.geometry import Polygon,mapping
    from osgeo import ogr
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsProcessingContext,
        QgsVectorLayer,QgsFeature,QgsField,QgsGeometry,QgsVectorFileWriter)
    from qgis.PyQt.QtCore import QVariant
    initialise();ogr.UseExceptions();app=QgsApplication([],False);app.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    source=ogr.Open(str(OUT/'fonts/cobertes-industrials-2024.gpkg'),0)
    feature=source.GetLayerByName('original').GetFeature(INDUSTRIAL_ID)
    original=shapely.from_wkb(bytes(feature.GetGeometryRef().ExportToWkb()));source=None
    assert original.is_valid and original.geom_type=='Polygon'
    solid=Polygon(original.exterior)
    def memory(rows):
        layer=QgsVectorLayer('MultiPolygon?crs=EPSG:25831','Geometria docent','memory')
        layer.dataProvider().addAttributes([QgsField('id_font',QVariant.LongLong),QgsField('metode',QVariant.String),
            QgsField('area_ha',QVariant.Double),QgsField('forats',QVariant.Int),QgsField('afegit_ext_ha',QVariant.Double)])
        layer.updateFields();features=[]
        for g,method in rows:
            parts=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
            f=QgsFeature(layer.fields());q=QgsGeometry();q.fromWkb(g.wkb);q.convertToMultiType();f.setGeometry(q)
            f.setAttributes([INDUSTRIAL_ID,method,g.area/10000,sum(len(p.interiors) for p in parts),g.difference(solid).area/10000])
            features.append(f)
        assert layer.dataProvider().addFeatures(features)[0];layer.updateExtents();return layer
    def save(layer,relative):
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='GPKG';options.layerName=Path(relative).stem
        options.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteFile
        result=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(OUT/relative),project.transformContext(),options)
        assert result[0]==QgsVectorFileWriter.NoError,result
    def run(ident,params):return processing.run(ident,params,context=context)['OUTPUT']
    def one(layer):
        assert layer.featureCount()==1
        value=shapely.from_wkb(bytes(next(layer.getFeatures()).geometry().asWkb()))
        return value.geoms[0] if value.geom_type=='MultiPolygon' and len(value.geoms)==1 else value
    initial=memory([(original,'original')]);save(initial,'dades/coberta-original.gpkg')
    cleaned=run('native:deleteholes',{'INPUT':initial,'MIN_AREA':0,'OUTPUT':'memory:'})
    convex=run('native:convexhull',{'INPUT':initial,'OUTPUT':'memory:'})
    vertices=run('native:extractvertices',{'INPUT':cleaned,'OUTPUT':'memory:'})
    concave=run('native:concavehull',{'INPUT':vertices,'ALPHA':.3,'HOLES':False,'NO_MULTIGEOMETRY':False,'OUTPUT':'memory:'})
    buffer_options={'SEGMENTS':BUFFER_SEGMENTS,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':True,'OUTPUT':'memory:'}
    rows=[(original,'original'),(one(cleaned),'sense-forats'),(one(convex),'convex'),
          (one(concave),'concau-03')]
    for distance in CLOSING_DISTANCES:
        expanded=run('native:buffer',{'INPUT':initial,'DISTANCE':distance,**buffer_options})
        closed=run('native:buffer',{'INPUT':expanded,'DISTANCE':-distance,**buffer_options})
        rows.append((one(closed),f'tancament-{distance}m'))
        if distance==BUFFER_DISTANCE:
            save(memory([(one(expanded),f'buffer-positiu-{distance}m')]),'dades/buffer-positiu.gpkg')
    assert rows[1][0].equals(solid) and original.difference(rows[1][0]).area<1e-6
    chosen=f'tancament-{BUFFER_DISTANCE}m'
    selected=next(g for g,method in rows if method==chosen)
    assert selected.is_valid and selected.geom_type=='Polygon' and not selected.interiors
    save(memory([(selected,chosen)]),'dades/poligon.gpkg');save(memory(rows),'dades/alternatives-perimetre.gpkg')
    alternatives=[]
    for g,method in rows:
        parts=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
        alternatives.append({'id':method,'area_m2':g.area,'perimeter_m':g.length,'parts':len(parts),
            'holes':sum(len(p.interiors) for p in parts),'source_lost_m2':original.difference(g).area,
            'added_outside_original_perimeter_m2':g.difference(solid).area,'geometry':mapping(g)})
    ids=['native:deleteholes','native:convexhull','native:extractvertices','native:concavehull','native:buffer']
    report={'source_id':INDUSTRIAL_ID,'source_sha256':sha(OUT/'fonts/cobertes-industrials-2024.gpkg'),
        'source_area_m2':original.area,'study_area_m2':selected.area,'net_added_area_m2':selected.area-original.area,
        'source_holes':len(original.interiors),'chosen':chosen,'exterior_preserved':False,
        'added_outside_original_perimeter_m2':selected.difference(solid).area,
        'source_lost_m2':original.difference(selected).area,
        'derivation':'Morphological closing of the original MCSC polygon: positive buffer, dissolve, then negative buffer of the same magnitude. Rounded joins; finite arc segmentation causes a small measured source loss.',
        'parameters':{'deleteholes':{'MIN_AREA':0},'concavehull':{'ALPHA':.3,'HOLES':False,'input':'exterior vertices'},
            'closing':{'distances_m':[BUFFER_DISTANCE,-BUFFER_DISTANCE],'segments':BUFFER_SEGMENTS,'join_style':'round',
                'dissolve':True,'tested_distances_m':CLOSING_DISTANCES}},'alternatives':alternatives,
        'algorithm_schema':{ident:[{'name':p.name(),'description':p.description(),'default':str(p.defaultValue())}
            for p in QgsApplication.processingRegistry().algorithmById(ident).parameterDefinitions()] for ident in ids}}
    write_json(OUT/'controls/geometria.json',report)
    print(json.dumps([{k:v for k,v in row.items() if k!='geometry'} for row in alternatives],ensure_ascii=False,indent=2),flush=True)


def build():
    import csv
    import heapq
    import numpy as np
    import shapely
    from shapely.geometry import Point,LineString,box,mapping
    from osgeo import gdal,ogr,osr
    initialise();gdal.UseExceptions();ogr.UseExceptions()
    manifest=json.loads((OUT/'fonts/fonts.json').read_text())
    for name,record in manifest.items():assert sha(OUT/'fonts'/name)==record['sha256'],name
    terrain=gdal.Open(str(OUT/'fonts/mdt-5m.tif'));surface=gdal.Open(str(OUT/'fonts/mds-max-5m.tif'))
    dtm=terrain.ReadAsArray().astype(float);dsm=surface.ReadAsArray().astype(float);gt=terrain.GetGeoTransform()
    assert gt==surface.GetGeoTransform() and dtm.shape==dsm.shape==(2000,2000)
    sr=osr.SpatialReference();sr.ImportFromEPSG(25831)
    def vector(relative,kind,fields,rows):
        path=OUT/relative;assert path.resolve().is_relative_to(OUT)
        driver=ogr.GetDriverByName('GPKG')
        if path.exists():driver.DeleteDataSource(str(path))
        ds=driver.CreateDataSource(str(path));layer=ds.CreateLayer(path.stem,sr,kind)
        for name,t in fields:layer.CreateField(ogr.FieldDefn(name,t))
        for geometry,attrs in rows:
            f=ogr.Feature(layer.GetLayerDefn())
            for name,value in attrs.items():
                if value is not None:f.SetField(name,value)
            g=ogr.CreateGeometryFromWkb(shapely.force_2d(geometry).wkb)
            if kind==ogr.wkbMultiPolygon:g=ogr.ForceToMultiPolygon(g)
            f.SetGeometry(g);assert layer.CreateFeature(f)==0
        layer=None;ds=None
    def raster(relative,array,nodata=-9999):
        kind=gdal.GDT_Byte if array.dtype==np.uint8 else (gdal.GDT_Float64 if 'cota-minima' in relative else gdal.GDT_Float32)
        ds=gdal.GetDriverByName('GTiff').Create(str(OUT/relative),array.shape[1],array.shape[0],1,kind,
            ['COMPRESS=DEFLATE','TILED=YES'])
        ds.SetGeoTransform(gt);ds.SetProjection(terrain.GetProjection());ds.GetRasterBand(1).SetNoDataValue(nodata)
        ds.GetRasterBand(1).WriteArray(array);ds=None
    def display_map(values,mask):
        # Compact figure input, not a duplicate of the GIS rasters in Git.
        # Display-only rounding to 0.01%; analytical outputs stay unrounded.
        sampled=values[::5,::5];sample_mask=mask[::5,::5]
        codes=np.where(sample_mask,np.rint(sampled*100),65535).astype('<u2')
        return {'shape':list(codes.shape),'encoding':'zlib-base64-uint16-le','scale':100,
                'nodata':65535,'data':base64.b64encode(zlib.compress(codes.tobytes(),9)).decode('ascii')}
    def cell(p):return int((p.y-gt[3])/gt[5]),int((p.x-gt[0])/gt[1])
    def centre(p):
        r,c=cell(p);return Point(gt[0]+(c+.5)*RES,gt[3]-(r+.5)*RES)
    def geometries(path,layername):
        ds=ogr.Open(str(OUT/path),0);layer=ds.GetLayerByName(layername)
        rows=[(f.GetFID(),shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())),f.items()) for f in layer]
        ds=None;return rows
    def burn(geometry):
        ds=ogr.GetDriverByName('Memory').CreateDataSource('');layer=ds.CreateLayer('mask',sr,ogr.wkbMultiPolygon)
        f=ogr.Feature(layer.GetLayerDefn());f.SetGeometry(ogr.ForceToMultiPolygon(ogr.CreateGeometryFromWkb(geometry.wkb)));layer.CreateFeature(f)
        image=gdal.GetDriverByName('MEM').Create('',dtm.shape[1],dtm.shape[0],1,gdal.GDT_Byte)
        image.SetGeoTransform(gt);image.SetProjection(terrain.GetProjection());gdal.RasterizeLayer(image,[1],layer,burn_values=[1])
        return image.ReadAsArray().astype(bool)
    sea=shapely.union_all([g for _,g,_ in geometries('fonts/mar-rtt-2024.gpkg','mar')])
    sea_mask=burn(sea)
    missing=~np.isfinite(dtm)|~np.isfinite(dsm)|(dtm==-9999)|(dsm==-9999)
    unknown_land=missing&~sea_mask
    print('NODATA',{'total':int(missing.sum()),'outside_mapped_sea':int(unknown_land.sum())},flush=True)
    valid=~missing&~sea_mask
    # Mapped marine voids have a documented 0 m boundary condition. Other
    # voids are scratch zeros ONLY: every ray crossing them is excluded by
    # the common coverage mask below, before any physical visibility is used.
    dtm[missing]=0;dsm[missing]=0
    assert np.all(dsm>=dtm)
    raster('dades/mdt-calcul.tif',dtm);raster('dades/mds-calcul.tif',dsm)
    raster('dades/buits-no-resolts.tif',unknown_land.astype(np.uint8),255)
    raster('dades/altura-obstacles.tif',np.where(valid,dsm-dtm,-9999))
    terrain=gdal.Open(str(OUT/'dades/mdt-calcul.tif'));surface=gdal.Open(str(OUT/'dades/mds-calcul.tif'))
    industrial=next((g,attrs) for fid,g,attrs in geometries('fonts/cobertes-industrials-2024.gpkg','original') if fid==INDUSTRIAL_ID)
    original_polygon,attributes=industrial
    geometry_report=json.loads((OUT/'controls/geometria.json').read_text())
    prepared=geometries('dades/poligon.gpkg','poligon');assert len(prepared)==1
    polygon=prepared[0][1]
    if polygon.geom_type=='MultiPolygon':
        assert len(polygon.geoms)==1;polygon=polygon.geoms[0]
    selected_geometry=next(row['geometry'] for row in geometry_report['alternatives'] if row['id']==geometry_report['chosen'])
    assert polygon.is_valid and polygon.symmetric_difference(shapely.geometry.shape(selected_geometry)).area<1e-6
    assert polygon.covers(Point(TORCH_XY))
    vector('dades/ambit.gpkg',ogr.wkbPolygon,[('nom',ogr.OFTString)],[(box(*BOUNDS),{'nom':'Àmbit de càlcul de 10 × 10 km'})])
    # A single cartographic itinerary avoids double-counting both carriageways.
    # Native QGIS shortest path is checked independently during package QA.
    edges=geometries('fonts/tv3148-completa-2024.gpkg','original')
    graph={};edge_data={}
    for fid,line,attrs in edges:
        xy=list(line.coords)
        for segment,(first,last) in enumerate(zip(xy,xy[1:])):
            a=tuple(round(v,3) for v in first);b=tuple(round(v,3) for v in last)
            if a==b:continue
            part=LineString([first,last]);key=(fid,segment)
            graph.setdefault(a,[]).append((part.length,b,key,False));graph.setdefault(b,[]).append((part.length,a,key,True))
            edge_data[key]=(part,attrs)
    start=(344634.192,4552407.204);end=(347279.010,4550113.250)
    assert start in graph and end in graph
    distances={start:0};previous={};queue=[(0,start)]
    while queue:
        cost,node=heapq.heappop(queue)
        if cost!=distances[node]:continue
        if node==end:break
        for length,other,fid,reverse in graph[node]:
            candidate=cost+length
            if candidate<distances.get(other,float('inf')):
                distances[other]=candidate;previous[other]=(node,fid,reverse);heapq.heappush(queue,(candidate,other))
    assert end in previous
    chosen=[];node=end
    while node!=start:
        node,fid,reverse=previous[node];chosen.append((fid,reverse))
    chosen.reverse();coordinates=[]
    for fid,reverse in chosen:
        xy=list(edge_data[fid][0].coords)
        if reverse:xy.reverse()
        if coordinates:assert math.dist(coordinates[-1],xy[0])<.005
        coordinates.extend(xy if not coordinates else xy[1:])
    road=LineString(coordinates);assert abs(road.length-distances[end])<.01
    vector('dades/carretera.gpkg',ogr.wkbLineString,[('nom',ogr.OFTString),('long_m',ogr.OFTReal)],
        [(road,{'nom':'TV-3148 · Vila-seca–enllaç de la Pineda','long_m':road.length})])
    vector('dades/eixos-recorregut.gpkg',ogr.wkbLineString,[('ordre',ogr.OFTInteger),('rtt_id',ogr.OFTInteger64),('segment',ogr.OFTInteger),('terreny',ogr.OFTString)],
        [(edge_data[fid][0],{'ordre':i,'rtt_id':fid[0],'segment':fid[1],'terreny':edge_data[fid][1]['terreny']}) for i,(fid,_) in enumerate(chosen,1)])
    sources=[];tiles=[]
    def add_source(sid,group,p,weight,pk=None):
        used=centre(p);r,c=cell(used);assert valid[r,c],sid
        z_abs=float(dtm[r,c]+EYE_HEIGHT if group=='carretera' else dsm[r,c]+1.)
        # A road sample whose eye level is under the opaque MDS is explicitly
        # unavailable in the controlled two-model road comparison.
        calculable=int(z_abs>dsm[r,c])
        sources.append({'id':sid,'grup':group,'x_original':p.x,'y_original':p.y,'x':used.x,'y':used.y,
            'desplac_m':p.distance(used),'pes':float(weight),'pk_m':pk,'z_abs_m':z_abs,
            'h_mdt_m':z_abs-float(dtm[r,c]),'h_mds_m':z_abs-float(dsm[r,c]),'calculable':calculable})
    add_source('T','punt',Point(TORCH_XY),1.)
    number=math.ceil(road.length/100);step=road.length/number
    for i in range(number):add_source(f'C{i+1:02d}','carretera',road.interpolate((i+.5)*step),step,(i+.5)*step)
    x0,y0,x1,y1=polygon.bounds
    for y in np.arange(math.floor(y0/250)*250,y1,250):
        for x in np.arange(math.floor(x0/250)*250,x1,250):
            cut=polygon.intersection(box(x,y,x+250,y+250))
            if cut.area<=1e-6:continue
            sid=f'A{len(tiles)+1:02d}';tiles.append((cut,{'id':sid,'area_m2':cut.area}))
            add_source(sid,'area',cut.representative_point(),cut.area)
    assert abs(sum(s['pes'] for s in sources if s['grup']=='carretera')-road.length)<1e-6
    assert abs(sum(s['pes'] for s in sources if s['grup']=='area')-polygon.area)<.001
    fields=[('id',ogr.OFTString),('grup',ogr.OFTString),('calculable',ogr.OFTInteger)]+[(k,ogr.OFTReal) for k in
        ['x_original','y_original','x','y','desplac_m','pes','pk_m','z_abs_m','h_mdt_m','h_mds_m']]
    for group,name in [('punt','torxa'),('carretera','mostres-carretera'),('area','mostres-area')]:
        vector(f'dades/{name}.gpkg',ogr.wkbPoint,fields,[(Point(s['x'],s['y']),s) for s in sources if s['grup']==group])
    vector('dades/fragments-area.gpkg',ogr.wkbMultiPolygon,[('id',ogr.OFTString),('area_m2',ogr.OFTReal)],tiles)
    receivers=[]
    # Illustrative road positions deliberately show a clear view, a terrain
    # obstruction, a surface obstruction and the southern end. They are not
    # a representative sample of viewers. R5 is an out-of-domain control.
    road_sources=[s for s in sources if s['grup']=='carretera']
    for i,sid in enumerate(['C05','C11','C13','C37'],1):
        s=next(s for s in road_sources if s['id']==sid)
        receivers.append({'id':f'R{i}','nom':f'TV-3148 · {s["id"]}','mostra':s['id'],
            'x':s['x'],'y':s['y'],'z_abs_m':float(dtm[cell(Point(s['x'],s['y']))]+EYE_HEIGHT),
            'calculable':s['calculable'],'pk_m':s['pk_m']})
    receivers.append({'id':'R5','nom':'Control fora del retall','mostra':'fora','x':352100.,'y':4552000.,
        'z_abs_m':None,'calculable':0,'pk_m':None})
    rf=[('id',ogr.OFTString),('nom',ogr.OFTString),('mostra',ogr.OFTString),('calculable',ogr.OFTInteger)]+[
        (k,ogr.OFTReal) for k in ['x','y','z_abs_m','pk_m']]
    vector('dades/receptors.gpkg',ogr.wkbPoint,rf,[(Point(r['x'],r['y']),r) for r in receivers])
    controls={'runtime':{'qgis':'3.44.11','gdal':gdal.VersionInfo(),'image':IMAGE},'bounds':BOUNDS,
        'resolution_m':RES,'valid_receiver_cells':int(valid.sum()),'marine_cells':int(sea_mask.sum()),
        'input_nodata_union_cells':int(missing.sum()),'unexplained_inland_nodata_cells':int(unknown_land.sum()),
        'nodata_preparation':'Mapped sea voids: 0 m boundary condition in calculation copies. Other voids: rays through them excluded for every source by a flat binary-obstacle coverage run; original voids and sea are not receivers.',
        'industrial_id':INDUSTRIAL_ID,'source_industrial_class':347,'industrial_area_m2':polygon.area,
        'source_industrial_area_m2':original_polygon.area,
        'geometry_preparation':{k:v for k,v in geometry_report.items() if k not in ['alternatives','algorithm_schema']},
        'industrial_holes':len(polygon.interiors),'industrial_hole_area_m2':sum(shapely.Polygon(r).area for r in polygon.interiors),
        'industrial_geometry':f'Study petrochemical precinct: native:buffer +{BUFFER_DISTANCE} m then -{BUFFER_DISTANCE} m, {BUFFER_SEGMENTS} segments, rounded joins, dissolve. Original MCSC and positive-buffer intermediate retained separately; not an official boundary or the entire southern complex.',
        'road_length_m':road.length,'road_edges':list(dict.fromkeys(fid[0] for fid,_ in chosen)),
        'road_start':coordinates[0],'road_end':coordinates[-1],
        'road_route_method':'Undirected shortest cartographic path on all original TV-3148 vertices; vertex key tolerance 1 mm; one itinerary, not a traffic-routing model.',
        'road_step_m':step,'road_total_samples':number,'area_grid_m':250,
        'receiver_selection':'Illustrative C05, C11, C13 and C37: contrasting visibility responses, not a representative population sample; R5 outside the crop.',
        'torch':sources[0],'torch_osm_id':TORCH_OSM_ID,'receiver_height_m':EYE_HEIGHT,
        'target_definition':'T and A: 1 m above retained MDS surface; road observers: MDT + 1.7 m. Absolute endpoint elevations retained for both models.',
        'curvature_coefficient':CURVATURE,'sources':sources,'receivers':receivers,'groups':{},'single_sources':{}}
    native=gdal.Open(str(OUT/'fonts/mds-torxa-1m.tif'));native_array=native.ReadAsArray()
    controls['torch']['native_mds_peak_m']=float(native_array.max())
    assert abs(native_array.max()-(sources[0]['z_abs_m']-1))<.01
    fixture=gdal.GetDriverByName('MEM').Create('',21,3,1,gdal.GDT_Float32)
    fixture.SetGeoTransform((346000,5,0,4555000,0,-5));fixture.SetProjection(terrain.GetProjection())
    toy=np.full((3,21),100.);toy[:,10]=115.;fixture.GetRasterBand(1).WriteArray(toy)
    minimum=gdal.ViewshedGenerate(fixture.GetRasterBand(1),'MEM','',[],346002.5,4554992.5,2,0,1,0,255,-9999,
        0,gdal.GVM_Edge,0,heightMode=gdal.GVOT_MIN_TARGET_HEIGHT_FROM_DEM).ReadAsArray()
    assert abs(float(minimum[1,20])-128)<1e-6
    controls['wall_check']={'observer_z':102,'wall_z':115,'distance_m':100,'wall_distance_m':50,'required_z':float(minimum[1,20])}
    toy.fill(0);fixture.GetRasterBand(1).WriteArray(toy)
    flat=gdal.ViewshedGenerate(fixture.GetRasterBand(1),'MEM','',[],346002.5,4554992.5,0,0,
        1,0,255,255,0,gdal.GVM_Edge,0).ReadAsArray()
    assert np.all(flat==1)
    toy[:,10]=1;fixture.GetRasterBand(1).WriteArray(toy)
    blocked=gdal.ViewshedGenerate(fixture.GetRasterBand(1),'MEM','',[],346002.5,4554992.5,0,0,
        1,0,255,255,0,gdal.GVM_Edge,0).ReadAsArray()
    assert blocked[1,5]==1 and blocked[1,20]==0
    controls['unknown_coverage_fixture']='Flat 0 m plane all visible; 1 m unknown stripe blocks known cells behind it, with zero curvature.'
    groups={g:[s for s in sources if s['grup']==g and s['calculable']] for g in ['punt','carretera','area']}
    matrices={name:{r['id']:{} for r in receivers} for name in ['mdt','mds']};maps={};torch_maps={}
    initial_valid=int(valid.sum())
    if unknown_land.any():
        coverage=gdal.GetDriverByName('MEM').Create('',dtm.shape[1],dtm.shape[0],1,gdal.GDT_Float32)
        coverage.SetGeoTransform(gt);coverage.SetProjection(terrain.GetProjection())
        coverage.GetRasterBand(1).WriteArray(unknown_land.astype(np.float32))
        for s in sources:
            image=gdal.ViewshedGenerate(coverage.GetRasterBand(1),'MEM','',[],s['x'],s['y'],0,0,
                1,0,255,255,0,gdal.GVM_Edge,0)
            assert image.GetGeoTransform()==gt
            valid &= image.ReadAsArray().astype(bool)
        coverage=None
    for s in sources:
        if s['calculable']:assert valid[cell(Point(s['x'],s['y']))],s['id']
    controls['valid_receiver_cells']=int(valid.sum())
    controls['cells_excluded_by_unknown_elevation_rays']=initial_valid-int(valid.sum())
    raster('dades/domini-valid.tif',np.where(valid,1,-9999).astype(float))
    print('COMMON DOMAIN',controls['valid_receiver_cells'],'EXCLUDED RAYS',controls['cells_excluded_by_unknown_elevation_rays'],flush=True)
    # The elementary road exercise uses all 37 MDT observers. The controlled
    # MDT/MDS comparison below additionally uses the common valid-eye subset.
    road_count=np.zeros(dtm.shape,np.uint8)
    (OUT/'resultats/conques-carretera-mdt').mkdir(exist_ok=True)
    for s in road_sources:
        image=gdal.ViewshedGenerate(terrain.GetRasterBand(1),'MEM','',[],s['x'],s['y'],EYE_HEIGHT,EYE_HEIGHT,
            1,0,255,255,CURVATURE,gdal.GVM_Edge,0)
        visible=image.ReadAsArray().astype(bool)&valid;road_count+=visible
        raster(f'resultats/conques-carretera-mdt/{s["id"]}.tif',np.where(valid,visible,255).astype(np.uint8),255)
    raster('resultats/carretera-mdt-totes-nombre.tif',np.where(valid,road_count,255).astype(np.uint8),255)
    raster('resultats/carretera-mdt-totes-percent.tif',np.where(valid,100*road_count.astype(float)/number,-9999))
    controls['road_mdt_all']={'n':number,'visible_any_cells':int((road_count>0).sum()),
        'max_count':int(road_count[valid].max()),'weight_sum_m':road.length,
        'mean_weighted_percent':float((100*road_count[valid].astype(float)/number).mean())}
    maps['carretera-mdt-totes']=display_map(100*road_count.astype(float)/number,valid)
    for group,items in groups.items():
        assert items,group
        assert len(items)<255,'Use a wider count raster before increasing the sampling beyond Byte capacity.'
        counts={n:np.zeros(dtm.shape,np.uint8) for n in ['mdt','mds']};weighted={n:np.zeros(dtm.shape,float) for n in ['mdt','mds']}
        for index,s in enumerate(items,1):
            if index==1 or index%10==0 or index==len(items):print('VIEWSHED',group,index,'/',len(items),s['id'],flush=True)
            views={}
            for name,ds in [('mdt',terrain),('mds',surface)]:
                image=gdal.ViewshedGenerate(ds.GetRasterBand(1),'MEM','',[],s['x'],s['y'],s[f'h_{name}_m'],0,
                    1,0,255,-9999,CURVATURE,gdal.GVM_Edge,0,heightMode=gdal.GVOT_MIN_TARGET_HEIGHT_FROM_DEM)
                assert image.GetGeoTransform()==gt
                z_min=image.ReadAsArray();assert np.isfinite(z_min).all()
                visible=(dtm+EYE_HEIGHT>=z_min)&valid
                if s['id']=='T':
                    raster(f'resultats/cota-minima-{name}.tif',z_min)
                    torch_maps[name]=visible
                    raster(f'resultats/torxa-{name}.tif',np.where(valid,visible,255).astype(np.uint8),255)
                    if name=='mdt':
                        normal=gdal.ViewshedGenerate(ds.GetRasterBand(1),'MEM','',[],s['x'],s['y'],s['h_mdt_m'],EYE_HEIGHT,
                            1,0,255,255,CURVATURE,gdal.GVM_Edge,0).ReadAsArray().astype(bool)&valid
                        assert np.array_equal(normal,visible)
                counts[name]+=visible;weighted[name]+=visible*s['pes'];views[name]=visible
                for r in receivers:matrices[name][r['id']][s['id']]=int(visible[cell(Point(r['x'],r['y']))]) if r['calculable'] else None
                image=None
            assert not np.any(views['mds']&~views['mdt']),s['id']
            controls['single_sources'][s['id']]={n:int(v.sum()) for n,v in views.items()}
        total=sum(s['pes'] for s in items);all_items=[s for s in sources if s['grup']==group]
        controls['groups'][group]={'n':len(items),'total_n':len(all_items),'weight_sum':total,
            'total_weight':sum(s['pes'] for s in all_items),'excluded_ids':[s['id'] for s in all_items if not s['calculable']],
            'unit':{'punt':'one point','carretera':'metres of sampled road','area':'square metres of represented polygon'}[group]}
        for name in ['mdt','mds']:
            fraction=100*weighted[name]/total
            assert fraction.min()>=0 and fraction.max()<=100+1e-8
            raster(f'resultats/{group}-{name}-nombre.tif',np.where(valid,counts[name],255).astype(np.uint8),255)
            raster(f'resultats/{group}-{name}-percent.tif',np.where(valid,fraction,-9999))
            if group=='area':
                any_part=(counts[name]>0)|torch_maps[name]
                raster(f'resultats/poligon-{name}-alguna.tif',np.where(valid,any_part,255).astype(np.uint8),255)
                controls.setdefault('polygon_any',{})[name]={'visible_cells':int(any_part.sum()),
                    'definition':f'Any of {len(items)} area samples OR the separately inventoried flare T; T has no invented area weight.'}
                maps['poligon-'+name+'-alguna']=display_map(any_part.astype(float)*100,valid)
            controls['groups'][group][name]={'visible_any_cells':int((counts[name]>0).sum()),
                'visible_all_cells':int(((counts[name]==len(items))&valid).sum()),'mean_weighted_percent':float(fraction[valid].mean())}
            maps[group+'-'+name]=display_map(fraction,valid)
    for s in road_sources:
        for n in ['mdt','mds']:s['T_'+n]=int(torch_maps[n][cell(Point(s['x'],s['y']))]) if n=='mdt' or s['calculable'] else None
    vector('resultats/carretera-torxa.gpkg',ogr.wkbPoint,fields+[(f'T_{n}',ogr.OFTInteger) for n in ['mdt','mds']],
        [(Point(s['x'],s['y']),s) for s in road_sources])
    controls['road_torch_exposure']={n:sum(s['pes']*s['T_'+n] for s in road_sources if s['calculable']) for n in ['mdt','mds']}
    controls['road_torch_exposure_mdt_all_m']=sum(s['pes']*s['T_mdt'] for s in road_sources)
    for r in receivers:
        for n in ['mdt','mds']:
            r['T_'+n]=matrices[n][r['id']]['T']
            r['G_'+n]=int(bool(r['T_'+n]) or any(matrices[n][r['id']][s['id']] for s in groups['area'])) if r['calculable'] else None
            for group,key in [('carretera','C'),('area','A')]:
                r[f'{key}_{n}_pct']=100*sum(s['pes']*matrices[n][r['id']][s['id']] for s in groups[group])/sum(s['pes'] for s in groups[group]) if r['calculable'] else None
    final_fields=rf+[(f'{key}_{n}',ogr.OFTInteger) for key in ['T','G'] for n in ['mdt','mds']]+[(f'{g}_{n}_pct',ogr.OFTReal) for g in ['C','A'] for n in ['mdt','mds']]
    vector('resultats/receptors-resultats.gpkg',ogr.wkbPoint,final_fields,[(Point(r['x'],r['y']),r) for r in receivers])
    torch=sources[0];links=[];profiles=[];R=6378137.
    for r in receivers:
        links.append((LineString([(torch['x'],torch['y']),(r['x'],r['y'])]),{'receptor':r['id'],'mdt':r['T_mdt'],'mds':r['T_mds']}))
        if not r['calculable']:continue
        length=math.hypot(r['x']-torch['x'],r['y']-torch['y']);t=np.linspace(0,1,math.ceil(length/2.5)+1)
        x=torch['x']+(r['x']-torch['x'])*t;y=torch['y']+(r['y']-torch['y'])*t
        row=((y-gt[3])/gt[5]).astype(int);col=((x-gt[0])/gt[1]).astype(int)
        d=t*length;line=torch['z_abs_m']+(r['z_abs_m']-torch['z_abs_m'])*t;bulge=CURVATURE*d*(length-d)/(2*R)
        p={'receiver':r['id'],'name':r['nom'],'distance_m':d.tolist(),'line_z':line.tolist(),
            'mdt_z':(dtm[row,col]+bulge).tolist(),'mds_z':(dsm[row,col]+bulge).tolist(),
            'mdt_visible':r['T_mdt'],'mds_visible':r['T_mds']}
        for n,arr in [('mdt',dtm),('mds',dsm)]:p[n+'_minimum_clearance_m']=float((line[1:-1]-arr[row[1:-1],col[1:-1]]-bulge[1:-1]).min())
        profiles.append(p)
    vector('resultats/intervisibilitat.gpkg',ogr.wkbLineString,[('receptor',ogr.OFTString),('mdt',ogr.OFTInteger),('mds',ogr.OFTInteger)],links)
    controls['profiles']=[{k:v for k,v in p.items() if not isinstance(v,list)} for p in profiles]
    for name,rows in [('receptors',receivers),('carretera',road_sources)]:
        with (OUT/'controls'/f'{name}.csv').open('w') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    write_json(OUT/'controls/resultats.json',controls);write_json(OUT/'controls/matrius.json',matrices);write_json(OUT/'controls/perfils.json',profiles)
    figure={'controls':controls,'sector':mapping(polygon),'original_sector':mapping(original_polygon),
        'geometry_alternatives':geometry_report['alternatives'],'tiles':[mapping(g) for g,a in tiles],
        'road':mapping(road),'sources':sources,'receivers':receivers,'maps':maps,'profiles':profiles,
        'display_sampling':'One 5 m cell per 25 m display spacing; display-only values rounded to 0.01 percent and losslessly compressed as uint16, 65535 means NoData.'}
    (ROOT/'context/inputs/visibilitat-costa.json').write_text(json.dumps(figure,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps({'torch':controls['torch'],'road_length_m':road.length,'groups':controls['groups'],
        'receivers':receivers,'profiles':controls['profiles']},ensure_ascii=False,indent=2),flush=True)


def style():
    import sys
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsVectorLayer,QgsRasterLayer,
        QgsFillSymbol,QgsLineSymbol,QgsMarkerSymbol,QgsRasterShader,QgsColorRampShader,QgsSingleBandPseudoColorRenderer,
        QgsRendererCategory,QgsCategorizedSymbolRenderer,QgsPalLayerSettings,QgsTextFormat,QgsTextBufferSettings,
        QgsVectorLayerSimpleLabeling,QgsRectangle,QgsReferencedRectangle,Qgis)
    from qgis.PyQt.QtGui import QColor,QFont
    initialise();app=QgsApplication([],False);app.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    controls=json.loads((OUT/'controls/resultats.json').read_text())
    project=QgsProject.instance();crs=QgsCoordinateReferenceSystem('EPSG:25831');inventory={}
    project.setCrs(crs);project.setEllipsoid('NONE')
    def register(relative,name):
        path=OUT/relative
        layer=QgsRasterLayer(str(path),name) if path.suffix=='.tif' else QgsVectorLayer(str(path),name,'ogr')
        assert layer.isValid(),relative;inventory[relative]=name;return layer
    def persist(relative,layer):
        message,ok=layer.saveNamedStyle(str((OUT/relative).with_suffix('.qml')));assert ok,message
        if isinstance(layer,QgsVectorLayer) and not relative.startswith('fonts/'):
            assert not layer.saveStyleToDatabase('docencia','Visibilitat: torxa, carretera i polígon',True,'')
    def polygon(relative,name,colour,fill='255,255,255,0',width=.7):
        layer=register(relative,name);layer.renderer().setSymbol(QgsFillSymbol.createSimple({
            'color':fill,'outline_color':colour,'outline_width':str(width)}));persist(relative,layer)
    def point(relative,name,colour,size=3,labels=False):
        layer=register(relative,name);layer.renderer().setSymbol(QgsMarkerSymbol.createSimple({
            'name':'circle','color':colour,'size':str(size),'outline_color':'white','outline_width':'.45'}))
        if labels:
            pal=QgsPalLayerSettings();pal.fieldName='id';text=QgsTextFormat();font=QFont('DejaVu Sans');font.setBold(True)
            text.setFont(font);text.setSize(20);text.setColor(QColor('#252525'))
            halo=QgsTextBufferSettings();halo.setEnabled(True);halo.setColor(QColor('white'));halo.setSize(1)
            text.setBuffer(halo);pal.setFormat(text);layer.setLabeling(QgsVectorLayerSimpleLabeling(pal));layer.setLabelsEnabled(True)
        persist(relative,layer)
    def raster(relative,name,items,kind='interpolated',opacity=1):
        layer=register(relative,name);function=QgsColorRampShader()
        function.setColorRampType({'exact':QgsColorRampShader.Exact,'discrete':QgsColorRampShader.Discrete,
            'interpolated':QgsColorRampShader.Interpolated}[kind])
        function.setColorRampItemList([QgsColorRampShader.ColorRampItem(v,QColor(c),label) for v,c,label in items])
        function.setMinimumValue(items[0][0]);function.setMaximumValue(items[-1][0])
        shader=QgsRasterShader();shader.setRasterShaderFunction(function)
        renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,shader)
        renderer.setClassificationMin(items[0][0]);renderer.setClassificationMax(items[-1][0])
        layer.setRenderer(renderer);layer.setOpacity(opacity);persist(relative,layer)
    for name,title in [('context','context'),('industria','àrea industrial'),('torxa','torxa')]:
        register(f'fonts/ortofoto-{name}-2025.tif','Ortofoto ICGC 2025 · '+title)
    heights=[(0,'#f7f4e8','0 m'),(25,'#d9dcb3','25 m'),(75,'#a4a874','75 m'),(150,'#61584b','150 m')]
    raster('dades/mdt-calcul.tif','MDT · càlcul 5 m',heights)
    raster('dades/mds-calcul.tif','MDS · càlcul 5 m',heights)
    raster('dades/domini-valid.tif','Domini comú calculable',[(1,'#f0f0f0','1 · calculable')],'exact',.3)
    raster('dades/altura-obstacles.tif','MDS − MDT · metres',[(0,'#f7f7f7','0 m'),(10,'#fed976','10 m'),
        (30,'#fd8d3c','30 m'),(80,'#bd0026','80 m'),(140,'#67001f','140 m')])
    polygon('dades/coberta-original.gpkg','Coberta original MCSC · 162,59 ha','#707070','220,220,220,65',.4)
    area_label=f"{controls['industrial_area_m2']/10000:.2f}".replace('.',',')
    n_area=controls['groups']['area']['n']
    polygon('dades/poligon.gpkg',f'Recinte petroquímic d’estudi · {area_label} ha','#d67a17')
    polygon('dades/buffer-positiu.gpkg',f'Buffer intermedi · +{BUFFER_DISTANCE} m','#287d85','65,150,160,35',.5)
    alternatives=register('dades/alternatives-perimetre.gpkg','Alternatives de recinte')
    alternatives.setRenderer(QgsCategorizedSymbolRenderer('metode',[
        QgsRendererCategory(key,QgsFillSymbol.createSimple({'color':'255,255,255,0','outline_color':colour,'outline_width':'.6'}),label)
        for key,colour,label in [('original','#777777','MCSC original'),('sense-forats','#9b8670','Només patis interiors'),
            ('convex','#ac3b4e','Convexa'),('concau-03','#6f51a6','Còncava · 0,3')]+
            [(f'tancament-{distance}m','#d67a17' if distance==BUFFER_DISTANCE else '#176e78',f'Tancament · ±{distance} m')
             for distance in CLOSING_DISTANCES]]))
    persist('dades/alternatives-perimetre.gpkg',alternatives)
    polygon('dades/fragments-area.gpkg',f'A · {n_area} fragments de graella','#6f51a6','209,193,232,55',.3)
    polygon('dades/ambit.gpkg','Àmbit calculat · 10 × 10 km','#4f5966',width=.45)
    road=register('dades/carretera.gpkg','TV-3148 · recorregut de 3.652,27 m')
    road.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':'#086b7a','line_width':'1'}));persist('dades/carretera.gpkg',road)
    point('dades/torxa.gpkg','T · torxa de la Canonja','#a23557',4.5,True)
    point('dades/mostres-carretera.gpkg','C · 37 mostres del recorregut','#086b7a',2.8)
    point('dades/mostres-area.gpkg',f'A · {n_area} mostres interiors','#6f51a6',2.8)
    point('dades/receptors.gpkg','R1–R5 · punts de consulta','#752f86',4,True)
    point('resultats/receptors-resultats.gpkg','Receptors · respostes MDT/MDS','#752f86',4,True)
    layer=register('resultats/carretera-torxa.gpkg','Torxa des de la carretera · MDS')
    layer.setRenderer(QgsCategorizedSymbolRenderer('T_mds',[
        QgsRendererCategory(0,QgsMarkerSymbol.createSimple({'name':'circle','color':'#b9543d','size':'3','outline_color':'white'}),'0 · oculta'),
        QgsRendererCategory(1,QgsMarkerSymbol.createSimple({'name':'circle','color':'#168164','size':'3','outline_color':'white'}),'1 · visible'),
        QgsRendererCategory(None,QgsMarkerSymbol.createSimple({'name':'cross2','color':'#565656','size':'3','outline_color':'white'}),'No calculat en MDS')]))
    persist('resultats/carretera-torxa.gpkg',layer)
    layer=register('resultats/intervisibilitat.gpkg','Intervisibilitat amb T · MDS')
    layer.setRenderer(QgsCategorizedSymbolRenderer('mds',[
        QgsRendererCategory(0,QgsLineSymbol.createSimple({'line_color':'#b9543d','line_width':'.7','line_style':'dash'}),'0 · oculta'),
        QgsRendererCategory(1,QgsLineSymbol.createSimple({'line_color':'#168164','line_width':'.85'}),'1 · visible'),
        QgsRendererCategory(None,QgsLineSymbol.createSimple({'line_color':'#8b8b8b','line_width':'.5','line_style':'dot'}),'No calculat')]))
    persist('resultats/intervisibilitat.gpkg',layer)
    binary=[(0,'#e4e4e4','0 · ocult'),(1,'#188568','1 · visible')]
    fractions=[(0,'#eeeeee','0%'),(5,'#d1e5f0','>0–5%'),(25,'#92c5de','>5–25%'),(50,'#4393c3','>25–50%'),(100,'#08519c','>50–100%')]
    for name in ['mdt','mds']:
        raster(f'resultats/cota-minima-{name}.tif',f'Cota mínima {name.upper()} · m absoluts',
            [(0,'#ffffcc','0 m'),(50,'#c7e9b4','50 m'),(100,'#41b6c4','100 m'),(160,'#253494','160 m')])
        raster(f'resultats/torxa-{name}.tif',f'T · conca {name.upper()}',binary,'exact',.8)
        raster(f'resultats/poligon-{name}-alguna.tif',f'Polígon · alguna part · {name.upper()}',binary,'exact',.8)
        for group,title in [('carretera','C · 28 mostres comparables'),('area',f'A · {n_area} mostres interiors')]:
            n=controls['groups'][group]['n']
            raster(f'resultats/{group}-{name}-nombre.tif',f'{title} · nombre · {name.upper()}',
                [(0,'#f5f5f5','0'),(n/2,'#70aacf',str(n/2)),(n,'#084594',str(n))])
            raster(f'resultats/{group}-{name}-percent.tif',f'{title} · % ponderat · {name.upper()}',fractions,'discrete')
    raster('resultats/carretera-mdt-totes-nombre.tif','Carretera · suma de 37 conques MDT',
        [(0,'#efefef','0'),(5,'#c6dbef','5'),(15,'#6baed6','15'),(25,'#2171b5','25'),(37,'#08306b','37')])
    raster('resultats/carretera-mdt-totes-percent.tif','Carretera · fracció de 37 posicions MDT',fractions,'discrete')
    base=['fonts/ortofoto-context-2025.tif'];wide=(342000,4549000,352500,4559000)
    detail=(344300,4549750,349900,4553500)
    views={
        '00-inici':(base+['dades/poligon.gpkg','dades/carretera.gpkg','dades/torxa.gpkg'],detail),
        '01-torxa':(['fonts/ortofoto-torxa-2025.tif','dades/torxa.gpkg'],(346650,4552300,347150,4552750)),
        '02-intervisibilitat':(base+['dades/poligon.gpkg','dades/carretera.gpkg','resultats/intervisibilitat.gpkg','dades/torxa.gpkg','dades/receptors.gpkg'],wide),
        '03-conca-mdt':(base+['resultats/torxa-mdt.tif','dades/ambit.gpkg','dades/poligon.gpkg','dades/carretera.gpkg','dades/torxa.gpkg','dades/receptors.gpkg'],wide),
        '04-conca-mds':(base+['resultats/torxa-mds.tif','dades/ambit.gpkg','dades/poligon.gpkg','dades/carretera.gpkg','dades/torxa.gpkg','dades/receptors.gpkg'],wide),
        '05-carretera':(base+['dades/poligon.gpkg','dades/carretera.gpkg','resultats/carretera-torxa.gpkg','dades/torxa.gpkg'],detail),
        '06-acumulada':(base+['resultats/carretera-mdt-totes-nombre.tif','dades/ambit.gpkg','dades/carretera.gpkg','dades/mostres-carretera.gpkg','dades/torxa.gpkg'],wide),
        '07-poligon':(base+['resultats/poligon-mds-alguna.tif','dades/ambit.gpkg','dades/poligon.gpkg','dades/mostres-area.gpkg','dades/carretera.gpkg','dades/torxa.gpkg'],wide),
        '08-area-ponderada':(['fonts/ortofoto-industria-2025.tif','dades/poligon.gpkg','dades/fragments-area.gpkg','dades/mostres-area.gpkg','dades/torxa.gpkg'],(345200,4551700,350000,4553000)),
        '09-perimetre':(['fonts/ortofoto-industria-2025.tif','dades/coberta-original.gpkg','dades/poligon.gpkg','dades/torxa.gpkg'],(345200,4551700,350000,4553000))}
    for name,(visible,extent) in views.items():
        project.clear();project.setCrs(crs);project.setEllipsoid('NONE');project.setTitle('Visibilitat costa · '+name)
        project.setFilePathStorage(Qgis.FilePathType.Relative)
        for relative in visible:project.addMapLayer(register(relative,inventory[relative]))
        hidden=project.layerTreeRoot().addGroup('Altres dades del paquet')
        for relative in list(inventory):
            if relative in visible:continue
            layer=register(relative,inventory[relative]);project.addMapLayer(layer,False);hidden.addLayer(layer).setItemVisibilityChecked(False)
        hidden.setExpanded(False)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*extent),crs))
        assert project.write(str(OUT/'projectes'/f'{name}.qgz'))
    write_json(OUT/'controls/capes.json',inventory);write_json(OUT/'controls/vistes.json',{k:{'visible':v,'bounds':b} for k,(v,b) in views.items()})
    ids=['gdal:viewshed','native:pointsalonglines','native:creategrid','native:clip','native:pointonsurface',
        'native:rastersampling','native:shortestpathpointtopoint','native:cellstatistics','native:rastercalc',
        'native:deleteholes','native:convexhull','native:concavehull','native:buffer']
    schema={ident:[{'name':p.name(),'description':p.description(),'default':str(p.defaultValue()),
        'options':p.options() if hasattr(p,'options') else None} for p in QgsApplication.processingRegistry().algorithmById(ident).parameterDefinitions()] for ident in ids}
    write_json(OUT/'controls/algorismes.json',schema)
    print('Styled',len(inventory),'layers and',len(views),'portable projects',flush=True)


def standalone_sqlite():
    import sqlite3
    initialise()
    for path in sorted(OUT.rglob('*.gpkg')):
        original=sqlite3.connect(path)
        original.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        original.execute('PRAGMA journal_mode=DELETE')
        assert original.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        temporary=path.with_name(path.stem+'.standalone.gpkg');assert not temporary.exists()
        copy=sqlite3.connect(temporary);original.backup(copy)
        assert copy.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        copy.execute('PRAGMA journal_mode=DELETE');copy.close();original.close()
        assert not path.with_name(path.name+'-wal').exists(),path
        temporary.replace(path)
    manifest=json.loads((OUT/'fonts/fonts.json').read_text())
    for name,record in manifest.items():
        record['preparation_sha256']=record.get('preparation_sha256',record['sha256'])
        record['sha256']=sha(OUT/'fonts'/name)
    write_json(OUT/'fonts/fonts.json',manifest)


def verify_package(root,report_path):
    """Run with /paquet readonly, no source repository mount and no network."""
    import socket,sys,tempfile
    import numpy as np
    from osgeo import gdal
    from qgis.core import (QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsProcessingContext,
        QgsRasterLayer,QgsVectorLayer,QgsVariantUtils,QgsExpression,QgsExpressionContext,Qgis)
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen');gdal.UseExceptions()
    gdal.SetConfigOption('GDAL_PAM_ENABLED','NO')
    assert [name for _,name in socket.if_nameindex()]==['lo']
    assert not Path('/workspace').exists()
    app=QgsApplication([],False);app.initQgis();sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize()
    import processing
    controls=json.loads((root/'controls/resultats.json').read_text())
    inventory=json.loads((root/'controls/capes.json').read_text());project=QgsProject.instance();projects=[]
    for path in sorted((root/'projectes').glob('*.qgz')):
        project.clear();assert project.read(str(path)),path
        layers=list(project.mapLayers().values());assert len(layers)==len(inventory)
        assert project.crs().authid()=='EPSG:25831' and project.ellipsoid()=='NONE'
        for layer in layers:
            assert layer.isValid(),(path.name,layer.source())
            assert Path(layer.source().split('|',1)[0]).resolve().is_relative_to(root),layer.source()
        projects.append({'project':path.name,'layers':len(layers),'invalid':[]})
    assert len(projects)==len(json.loads((root/'controls/vistes.json').read_text()))==10
    project.clear();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    def run(ident,params):
        print('VERIFY',ident,flush=True);return processing.run(ident,params,context=context)
    buffer_options={'SEGMENTS':BUFFER_SEGMENTS,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':True,'OUTPUT':'memory:'}
    expanded=run('native:buffer',{'INPUT':str(root/'dades/coberta-original.gpkg'),'DISTANCE':BUFFER_DISTANCE,**buffer_options})['OUTPUT']
    intermediate=QgsVectorLayer(str(root/'dades/buffer-positiu.gpkg'),'Buffer positiu','ogr')
    assert next(expanded.getFeatures()).geometry().symDifference(next(intermediate.getFeatures()).geometry()).area()<1e-6
    closed=run('native:buffer',{'INPUT':expanded,'DISTANCE':-BUFFER_DISTANCE,**buffer_options})['OUTPUT']
    retained=QgsVectorLayer(str(root/'dades/poligon.gpkg'),'Recinte petroquímic','ogr')
    closed_geometry=next(closed.getFeatures()).geometry();retained_geometry=next(retained.getFeatures()).geometry()
    assert closed_geometry.symDifference(retained_geometry).area()<1e-6
    import shapely
    original_layer=QgsVectorLayer(str(root/'dades/coberta-original.gpkg'),'Original','ogr')
    source_geometry=shapely.from_wkb(bytes(next(original_layer.getFeatures()).geometry().asWkb()))
    if source_geometry.geom_type=='MultiPolygon':source_geometry=source_geometry.geoms[0]
    retained_shape=shapely.from_wkb(bytes(retained_geometry.asWkb()))
    independent=source_geometry.buffer(BUFFER_DISTANCE,quad_segs=BUFFER_SEGMENTS).buffer(-BUFFER_DISTANCE,quad_segs=BUFFER_SEGMENTS)
    assert len(source_geometry.interiors)==19 and retained_shape.symmetric_difference(independent).area<.001
    assert retained_shape.is_valid and all(not part.interiors for part in (retained_shape.geoms if retained_shape.geom_type=='MultiPolygon' else [retained_shape]))
    assert abs(retained_shape.area-controls['industrial_area_m2'])<.001
    xy=lambda p:f'{p[0]},{p[1]} [EPSG:25831]'
    route=run('native:shortestpathpointtopoint',{'INPUT':str(root/'fonts/tv3148-completa-2024.gpkg')+'|layername=original',
        'STRATEGY':0,'DEFAULT_DIRECTION':2,'TOLERANCE':.001,'POINT_TOLERANCE':.1,
        'START_POINT':xy(controls['road_start']),'END_POINT':xy(controls['road_end']),'OUTPUT':'memory:'})['OUTPUT']
    route_length=sum(f.geometry().length() for f in route.getFeatures())
    assert abs(route_length-controls['road_length_m'])<.02,(route_length,controls['road_length_m'])
    samples=run('native:pointsalonglines',{'INPUT':str(root/'dades/carretera.gpkg'),'DISTANCE':controls['road_step_m'],
        'START_OFFSET':controls['road_step_m']/2,'END_OFFSET':0,'OUTPUT':'memory:'})['OUTPUT']
    expected=[s for s in controls['sources'] if s['grup']=='carretera'];assert samples.featureCount()==len(expected)==37
    for f,s in zip(samples.getFeatures(),expected):
        p=f.geometry().asPoint();assert math.hypot(p.x()-s['x_original'],p.y()-s['y_original'])<1e-5
    grid=run('native:creategrid',{'TYPE':2,'EXTENT':'345250,350000,4551750,4552750 [EPSG:25831]',
        'HSPACING':250,'VSPACING':250,'HOVERLAY':0,'VOVERLAY':0,'CRS':'EPSG:25831','OUTPUT':'memory:'})['OUTPUT']
    clipped=run('native:clip',{'INPUT':grid,'OVERLAY':str(root/'dades/poligon.gpkg'),'OUTPUT':'memory:'})['OUTPUT']
    assert clipped.featureCount()==controls['groups']['area']['n']
    assert abs(sum(f.geometry().area() for f in clipped.getFeatures())-controls['industrial_area_m2'])<.01
    points=run('native:pointonsurface',{'INPUT':str(root/'dades/fragments-area.gpkg'),'ALL_PARTS':False,'OUTPUT':'memory:'})['OUTPUT']
    expected={s['id']:s for s in controls['sources'] if s['grup']=='area'}
    for f in points.getFeatures():
        s=expected[f['id']];p=f.geometry().asPoint()
        assert math.hypot(p.x()-s['x_original'],p.y()-s['y_original'])<1e-5
    terrain=QgsRasterLayer(str(root/'dades/mdt-calcul.tif'),'MDT')
    minimum=QgsRasterLayer(str(root/'resultats/cota-minima-mds.tif'),'Cota mínima MDS')
    domain=QgsRasterLayer(str(root/'dades/domini-valid.tif'),'Domini')
    for layer in [terrain,minimum,domain]:project.addMapLayer(layer)
    valid=gdal.Open(str(root/'dades/domini-valid.tif')).ReadAsArray()==1
    assert int(valid.sum())==controls['valid_receiver_cells']
    target=controls['torch']
    with tempfile.TemporaryDirectory() as temporary:
        temporary=Path(temporary)
        output=run('gdal:viewshed',{'INPUT':str(root/'dades/mds-calcul.tif'),'BAND':1,
            'OBSERVER':xy([target['x'],target['y']]),'OBSERVER_HEIGHT':target['h_mds_m'],
            'TARGET_HEIGHT':0,'MAX_DISTANCE':0,'EXTRA':'-om DEM -cc 0.85714 -a_nodata -9999',
            'OUTPUT':str(temporary/'minimum.tif')})['OUTPUT']
        a=gdal.Open(output).ReadAsArray();b=gdal.Open(str(root/'resultats/cota-minima-mds.tif')).ReadAsArray()
        assert np.max(np.abs(a-b))<1e-5
        output=run('native:rastercalc',{'LAYERS':[terrain,minimum,domain],
            'EXPRESSION':'"Domini@1" * (("MDT@1" + 1.7) >= "Cota mínima MDS@1")',
            'EXTENT':'342000,352000,4549000,4559000 [EPSG:25831]','CELL_SIZE':5,'CRS':'EPSG:25831',
            'OUTPUT':str(temporary/'binary.tif')})['OUTPUT']
        ds=gdal.Open(output);values=ds.ReadAsArray();nd=ds.GetRasterBand(1).GetNoDataValue()
        expected=gdal.Open(str(root/'resultats/torxa-mds.tif')).ReadAsArray()
        assert np.array_equal(values[valid],expected[valid]) and np.all(values[~valid]==nd)
        files=sorted((root/'resultats/conques-carretera-mdt').glob('C*.tif'));assert len(files)==37
        output=run('native:cellstatistics',{'INPUT':[str(p) for p in files],'STATISTIC':0,'IGNORE_NODATA':False,
            'REFERENCE_LAYER':str(files[0]),'OUTPUT_NODATA_VALUE':255,'OUTPUT':str(temporary/'sum.tif')})['OUTPUT']
        values=gdal.Open(output).ReadAsArray();expected=gdal.Open(str(root/'resultats/carretera-mdt-totes-nombre.tif')).ReadAsArray()
        assert np.array_equal(values,expected)
        for name in ['mdt','mds']:
            a=gdal.Open(str(root/f'resultats/area-{name}-nombre.tif')).ReadAsArray()
            t=gdal.Open(str(root/f'resultats/torxa-{name}.tif')).ReadAsArray()
            union=gdal.Open(str(root/f'resultats/poligon-{name}-alguna.tif')).ReadAsArray()
            assert np.array_equal(union[valid],((a>0)|(t==1))[valid])
            assert not np.any((t==1)&(union!=1))
        for field,path in [('T_mds','torxa-mds.tif'),('G_mds','poligon-mds-alguna.tif'),('A_mds_pct','area-mds-percent.tif')]:
            sampled=run('native:rastersampling',{'INPUT':str(root/'dades/receptors.gpkg'),
                'RASTERCOPY':str(root/'resultats'/path),'COLUMN_PREFIX':'control_', 'OUTPUT':'memory:'})['OUTPUT']
            lookup={r['id']:r for r in controls['receivers']}
            for f in sampled.getFeatures():
                expected=lookup[f['id']][field];value=f['control_1']
                if expected is None:assert QgsVariantUtils.isNull(value),value
                else:assert abs(float(value)-expected)<1e-5
        road_samples=run('native:rastersampling',{'INPUT':str(root/'dades/mostres-carretera.gpkg'),
            'RASTERCOPY':str(root/'resultats/torxa-mds.tif'),'COLUMN_PREFIX':'T_mds_', 'OUTPUT':'memory:'})['OUTPUT']
        expression=QgsExpression('CASE WHEN "calculable" = 1 THEN "T_mds_1" ELSE NULL END')
        ec=QgsExpressionContext();ec.setFields(road_samples.fields())
        expected={s['id']:s['T_mds'] for s in controls['sources'] if s['grup']=='carretera'}
        road_states={'visible':0,'hidden':0,'unavailable':0}
        for f in road_samples.getFeatures():
            ec.setFeature(f);value=expression.evaluate(ec);assert not expression.hasEvalError()
            if expected[f['id']] is None:
                assert QgsVariantUtils.isNull(value);road_states['unavailable']+=1
            else:
                assert int(value)==expected[f['id']]
                road_states['visible' if int(value) else 'hidden']+=1
        assert road_states=={'visible':7,'hidden':21,'unavailable':9}
    ds=gdal.Open(str(root/'dades/mdt-calcul.tif'));dtm=ds.ReadAsArray();gt=ds.GetGeoTransform()
    dsm=gdal.Open(str(root/'dades/mds-calcul.tif')).ReadAsArray();profiles=[]
    for r in controls['receivers']:
        if not r['calculable']:continue
        length=math.hypot(r['x']-target['x'],r['y']-target['y'])
        t=np.linspace(0,1,math.ceil(length/.5)+1)
        xx=target['x']+(r['x']-target['x'])*t;yy=target['y']+(r['y']-target['y'])*t
        rows=((yy-gt[3])/gt[5]).astype(int);cols=((xx-gt[0])/gt[1]).astype(int)
        sight=target['z_abs_m']+(r['z_abs_m']-target['z_abs_m'])*t
        bulge=CURVATURE*(t*length)*(length-t*length)/(2*6378137.)
        result={'receiver':r['id']}
        for n,arr in [('mdt',dtm),('mds',dsm)]:
            clearance=float((sight-arr[rows,cols]-bulge)[1:-1].min())
            assert int(clearance>=0)==r['T_'+n],(r['id'],n,clearance)
            result[n+'_minimum_clearance_m']=clearance
        profiles.append(result)
    hashes={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and p.suffix in ['.gpkg','.tif','.qml','.qgz']}
    report={'ok':True,'qgis':Qgis.QGIS_VERSION,'gdal':gdal.VersionInfo(),'projects':projects,
        'network_interfaces':['lo'],'source_repository_mounted':False,'package_mount':'read-only',
        'native_closing':f'+{BUFFER_DISTANCE}/-{BUFFER_DISTANCE} m with {BUFFER_SEGMENTS} segments: intermediate and final geometries match QGIS; independent GEOS/Shapely comparison matches',
        'native_route_length_m':route_length,'native_road_sampling':'37 matching positions',
        'native_area_sampling':f'{clipped.featureCount()} fragments, area and point-on-surface positions match',
        'native_minimum_height':'matches GDAL C API','native_raster_calculator':'all valid cells and NoData mask match',
        'native_road_sum':'all cells of 37-raster sum match','polygon_any':f'{controls["groups"]["area"]["n"]} A OR T; includes entire T viewshed',
        'native_sampling':'matches T, polygon union, A percentage, including null R5',
        'native_road_point_validity_expression':road_states,
        'independent_profiles_05m':profiles,'checked_hashes':hashes}
    write_json(report_path,report);print(json.dumps({k:v for k,v in report.items() if k!='checked_hashes'},ensure_ascii=False,indent=2),flush=True)


def refresh_docs():
    import csv
    initialise()
    for source,name in [('visibilitat-costa.md','GUIA.md'),('visibilitat-costa-docent.md','SOLUCIONS.md')]:
        shutil.copyfile(ROOT/'context/practiques'/source,OUT/name)
    shutil.copyfile(Path(__file__),OUT/'reproduccio/preparar_visibilitat_costa.py')
    shutil.copyfile(ROOT/'context/dades/lots_visibilitat.py',OUT/'reproduccio/lots_visibilitat.py')
    for suffix in ['.md','.yml']:
        shutil.copyfile(ROOT/'context/qgis'/('visibilitat-costa'+suffix),OUT/'reproduccio'/('captura'+suffix))
        shutil.copyfile(ROOT/'context/qgis'/('visibilitat-acces'+suffix),OUT/'reproduccio'/('captura-acces'+suffix))
    (OUT/'reproduccio/manifests').mkdir(exist_ok=True)
    for name in CAPTURES:
        manifest=json.loads((ROOT/'context/qgis/manifests'/f'{name}.yml').read_text())
        assert manifest['ok'] and manifest['capture_id']==name and manifest['image_digest']==IMAGE
        assert not manifest.get('warnings'),(name,manifest.get('warnings'))
        for suffix in ['.png','.annotations.svg']:
            shutil.copyfile(ROOT/'assets/captures'/f'{name}{suffix}',OUT/'captures'/f'{name}{suffix}')
        shutil.copyfile(ROOT/'context/qgis/manifests'/f'{name}.yml',OUT/'reproduccio/manifests'/f'{name}.yml')
    for name in FIGURES:
        shutil.copyfile(ROOT/'assets/img/generated'/f'{name}.svg',OUT/'figures'/f'{name}.svg')
        shutil.copyfile(ROOT/'assets/quarto/figures'/f'{name}.qmd',OUT/'reproduccio'/f'{name}.qmd')
    shutil.copyfile(ROOT/'context/inputs/visibilitat-costa.json',OUT/'reproduccio/visibilitat-costa.json')
    for p in json.loads((OUT/'controls/perfils.json').read_text()):
        with (OUT/'controls'/f'perfil-T-{p["receiver"]}.csv').open('w') as stream:
            writer=csv.writer(stream,delimiter=';');writer.writerow(['distancia_m','linia_m','mdt_corregit_m','mds_corregit_m'])
            writer.writerows(zip(p['distance_m'],p['line_z'],p['mdt_z'],p['mds_z']))
    write_json(OUT/'controls/handouts.json',{
        'image':'ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:9e0b3a45753c170b795e9a9d6df61580085c113436beac5bf6c8de69b6562097',
        'engine':'xelatex','SOURCE_DATE_EPOCH':0,'fontfamily':'fontspec','mainfont':'DejaVu Sans','monofont':'DejaVu Sans Mono',
        'fontsize':'11pt','geometry':'a4paper,margin=18mm','guide_toc_depth':2})
    (OUT/'COMENCA-AQUI.txt').write_text(
        'Visibilitat: torxa de la Canonja, TV-3148 i àrea industrial\n\n'
        '1. Descomprimeix tot el paquet de Moodle i llegeix GUIA.pdf.\n'
        '2. Obre projectes/00-inici.qgz amb QGIS 3.44. Crea treball/ per a les teves sortides.\n'
        '3. Conserva les carpetes juntes: les dades són locals i les rutes, relatives.\n'
        '4. SOLUCIONS.pdf i resultats/ contenen controls docents.\n\n'
        'La guia avança de punt a carretera i a polígon. Les altures, el mostreig i la cobertura\n'
        'són part del model; no és una mesura de flames, població o impacte paisatgístic.\n'
        'Les fonts de reproduccio/ documenten la preparació i les captures. La preparació\n'
        'completa espera el repositori font; el treball QGIS del guió funciona amb aquest paquet.\n'
        "El guió lots_visibilitat.py reexecuta els lots amb les dades del paquet des de QGIS; vegeu GUIA.pdf.\n"
        'Fonts i llicències ICGC/OpenStreetMap: fonts/fonts.json.\n'
        'Autor: Benito Zaragozí. Preparació: 2026-10-02.\n')


def retain_batch_report(path):
    report=json.loads(path.read_text())
    assert report['ok'] and report['gui_coordinate_rows']==37
    assert report['script_sha256']==sha(ROOT/'context/dades/lots_visibilitat.py')
    for relative,digest in report['checked_hashes'].items():
        assert (OUT/relative).resolve().is_relative_to(OUT) and sha(OUT/relative)==digest,relative
    shutil.copyfile(path,OUT/'controls/verificacio-lots.json')


def package():
    initialise()
    assert not DELIVERY.exists(),'Never overwrite an existing Moodle delivery.'
    validation=json.loads((OUT/'controls/verificacio-qgis.json').read_text())
    batches=json.loads((OUT/'controls/verificacio-lots.json').read_text())
    assert batches['ok'] and batches['script_sha256']==sha(OUT/'reproduccio/lots_visibilitat.py')
    for relative,digest in batches['checked_hashes'].items():assert sha(OUT/relative)==digest,relative
    pdfs=json.loads((OUT/'controls/verificacio-pdf.json').read_text())
    assert validation['ok'] and len(validation['projects'])==10
    for relative,digest in validation['checked_hashes'].items():assert sha(OUT/relative)==digest,relative
    for name in ['GUIA','SOLUCIONS']:
        assert not pdfs[name]['overflow'] and sha(OUT/(name+'.pdf'))==pdfs[name]['sha256']
        assert sha(OUT/(name+'.md'))==pdfs[name]['source_sha256']
    inventory=[]
    for path in sorted(OUT.rglob('*')):
        if not path.is_file() or path.name in ['.visibilitat.json','MANIFEST.json']:continue
        assert not path.is_symlink() and not path.name.startswith('partial-')
        assert not path.name.endswith(('-wal','-shm','.standalone.gpkg')),path
        inventory.append({'path':str(path.relative_to(OUT)),'bytes':path.stat().st_size,'sha256':sha(path)})
    write_json(OUT/'MANIFEST.json',{'schema_version':1,'title':'Visibilitat: torxa, carretera i polígon',
        'author':'Benito Zaragozí','prepared':DATE,'runtime':IMAGE,'crs':'EPSG:25831',
        'file_count':len(inventory),'files':inventory})
    with zipfile.ZipFile(DELIVERY,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for record in inventory:archive.write(OUT/record['path'],'visibilitat-costa/'+record['path'])
        archive.write(OUT/'MANIFEST.json','visibilitat-costa/MANIFEST.json')
    with zipfile.ZipFile(DELIVERY) as archive:
        assert archive.testzip() is None and len(archive.namelist())==len(inventory)+1
        for record in inventory:
            data=archive.read('visibilitat-costa/'+record['path'])
            assert len(data)==record['bytes'] and hashlib.sha256(data).hexdigest()==record['sha256']
    receipt={'path':str(DELIVERY.relative_to(ROOT)),'sha256':sha(DELIVERY),'bytes':DELIVERY.stat().st_size,
        'files':len(inventory)+1,'projects':len(validation['projects']),
        'layers':len(json.loads((OUT/'controls/capes.json').read_text())),
        'captures':len(CAPTURES),'figures':len(FIGURES),
        'guide_pages':pdfs['GUIA']['pages'],'solutions_pages':pdfs['SOLUCIONS']['pages'],
        'zip_crc':'ok','all_member_sha256':'ok','qgis_validation':'passed','distribution':'Moodle; outside Git and website'}
    write_json(DELIVERY.with_suffix('.receipt.json'),receipt);print(json.dumps(receipt,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--init',action='store_true')
    parser.add_argument('--clone-sources',action='store_true')
    parser.add_argument('--fetch',action='store_true')
    parser.add_argument('--geometry',action='store_true')
    parser.add_argument('--build',action='store_true')
    parser.add_argument('--style',action='store_true')
    parser.add_argument('--sqlite',action='store_true')
    parser.add_argument('--docs',action='store_true')
    parser.add_argument('--package',action='store_true')
    parser.add_argument('--batch-report',type=Path)
    parser.add_argument('--verify-package',type=Path)
    parser.add_argument('--verify-report',type=Path)
    args=parser.parse_args()
    if sum([args.geometry,args.build,args.style])>1:parser.error('Use separate processes for geometry, calculation and styling.')
    if DELIVERY.exists() and any([args.init,args.clone_sources,args.fetch,args.geometry,args.build,args.style,args.sqlite,args.docs,args.package,args.batch_report]):
        parser.error('This delivery is sealed. Prepare a new version instead of modifying it.')
    if args.init: initialise()
    if args.clone_sources: clone_sources()
    if args.fetch: fetch()
    if args.geometry: geometry()
    if args.build: build()
    if args.style: style()
    if args.sqlite: standalone_sqlite()
    if args.docs: refresh_docs()
    if args.batch_report:retain_batch_report(args.batch_report)
    if args.package: package()
    if args.verify_package:
        if not args.verify_report:parser.error('--verify-report is required with --verify-package')
        verify_package(args.verify_package.resolve(),args.verify_report)
