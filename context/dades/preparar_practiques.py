"""Official-source extracts for the access and visibility practicals.

Run --fetch in the pinned QGIS image with network access. Originals are cached
below tmp/dades-docents/practiques; existing files must match their receipts.
Spatial extracts preserve source geometries/attributes. Raster reductions are
explicit derived products, not claimed to be the original resolution.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import urllib.request
from urllib.parse import quote
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / 'tmp/dades-docents/practiques'
RTT = 'https://datacloud.icgc.cat/datacloud/topografia-territorial/gpkg_unzip/topografia-territorial-v1r0-2024.gpkg'
MDT = 'https://datacloud.icgc.cat/datacloud/model-elevacions-terreny/tif_unzip/model-elevacions-terreny-lidar-catalunya-5m-2021-2023.tif'
MDS = 'https://datacloud.icgc.cat/datacloud/model-superficies/tif_unzip/model-superficies-lidar-catalunya-1m-2021-2023.tif'
ADMIN = ROOT / 'tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg'
ROADS_BBOX = (342500, 4550000, 356000, 4558500)
PINEDA_BBOX = (344500, 4546700, 347500, 4550000)


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def initialise():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    path = PRIVATE / 'manifest.json'
    return json.loads(path.read_text()) if path.exists() else {}


def cached(name, manifest):
    path = PRIVATE / name
    if path.exists():
        if name not in manifest or sha(path) != manifest[name]['sha256']:
            raise RuntimeError(f'Unmanaged or changed file: {path}')
        return True
    return False


def record(name, manifest, **metadata):
    path = PRIVATE / name
    manifest[name] = {'sha256':sha(path), 'bytes':path.stat().st_size,
                      'retrieved':'2026-09-29', **metadata}
    (PRIVATE/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(name, manifest[name], flush=True)


def fetch_zip(url, name, manifest):
    if cached(name, manifest): return
    assert url.startswith('https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/43/')
    request = urllib.request.Request(quote(url, safe=':/'), headers={'User-Agent':'Geodisseny teaching data preparation'})
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read(80_000_001)
    assert len(data) <= 80_000_000
    target = PRIVATE/name
    target.write_bytes(data)
    with zipfile.ZipFile(target) as archive: assert archive.testzip() is None
    record(name, manifest, url=url)


def fetch(only=None):
    from osgeo import gdal, ogr
    gdal.UseExceptions(); ogr.UseExceptions()
    for key, value in {'SQLITE_USE_OGR_VFS':'YES', 'GDAL_DISABLE_READDIR_ON_OPEN':'EMPTY_DIR',
                       'GDAL_HTTP_TIMEOUT':'90', 'GDAL_HTTP_MAX_RETRY':'3',
                       'CPL_VSIL_CURL_ALLOWED_EXTENSIONS':'.gpkg,.tif'}.items():
        gdal.SetConfigOption(key, value)
    manifest = initialise()
    admin = ogr.Open(str(ADMIN))
    layer = admin.GetLayerByName('_51_comarques-5000')
    layer.SetAttributeFilter("NOMCOMAR IN ('Tarragonès','Baix Camp')")
    assert layer.GetFeatureCount() == 2
    envelopes = [f.GetGeometryRef().GetEnvelope() for f in layer]
    regional = (math.floor(min(e[0] for e in envelopes)/1000)*1000-1000,
                math.floor(min(e[2] for e in envelopes)/1000)*1000-1000,
                math.ceil(max(e[1] for e in envelopes)/1000)*1000+1000,
                math.ceil(max(e[3] for e in envelopes)/1000)*1000+1000)
    if not cached('ambits.gpkg', manifest):
        out = ogr.GetDriverByName('GPKG').CreateDataSource(str(PRIVATE/'ambits.gpkg'))
        layer.ResetReading(); out.CopyLayer(layer, 'comarques')
        mun = admin.GetLayerByName('_61_municipis-5000'); mun.SetSpatialFilterRect(*regional)
        out.CopyLayer(mun, 'municipis')
        out.CopyLayer(admin.GetLayerByName('_21_catalunya-5000'), 'terra_catalunya')
        out = None
        record('ambits.gpkg', manifest, source=str(ADMIN.relative_to(ROOT)), source_sha256=sha(ADMIN),
               filter="NOMCOMAR IN ('Tarragonès','Baix Camp')", epsg=25831, bbox=regional)
    if only in (None, 'roads') and not cached('rtt-original.gpkg', manifest):
        source = ogr.Open('/vsicurl/'+RTT)
        out = ogr.GetDriverByName('GPKG').CreateDataSource(str(PRIVATE/'rtt-original.gpkg'))
        counts = {}
        for name in ['_35_transports_l', 'transports_tipus', 'transports_entorn',
                     'transports_estat', 'transports_terreny', 'transports_xarxa']:
            layer = source.GetLayerByName(name)
            if name == '_35_transports_l':
                layer.SetSpatialFilterRect(*ROADS_BBOX)
                layer.SetAttributeFilter("tipus IN ('cor','vca','vcu','vpu','aut','vpd','vnc','bir','bin','vcd')")
            copy = out.CopyLayer(layer, name, options=['FID=id'])
            counts[name] = copy.GetFeatureCount()
            print('Copied', name, counts[name], flush=True)
        out = None; source = None
        record('rtt-original.gpkg', manifest, url=RTT, bbox=ROADS_BBOX, counts=counts,
               geometry='whole source road-axis features intersecting bbox; no topology repair', epsg=25831,
               types=['cor','vca','vcu','vpu','aut','vpd','vnc','bir','bin','vcd'])
    if only == 'roads': return
    for code, place in [('43173','VILA SECA'),('43111','LA POBLA DE MAFUMET')]:
        url = f'https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/43/{code}-{place}/A.ES.SDGC.CP.{code}.zip'
        fetch_zip(url, f'parceles-dgc-{code}.zip', manifest)
    for name, url, bounds, resolution in [
            ('mdt-regional-25m.tif', MDT, regional, 25),
            ('mds-regional-25m.tif', MDS, regional, 25),
            ('mdt-pineda-5m.tif', MDT, PINEDA_BBOX, 5)]:
        if cached(name, manifest): continue
        source = gdal.Open('/vsicurl/'+url)
        assert source.GetSpatialRef().GetAuthorityCode(None) == '25831'
        x0,y0,x1,y1 = bounds
        output = gdal.Translate(str(PRIVATE/name), source, format='GTiff',
                                projWin=[x0,y1,x1,y0], xRes=resolution, yRes=resolution,
                                resampleAlg='average', creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        metadata = {'size':[output.RasterXSize,output.RasterYSize],
                    'geotransform':output.GetGeoTransform(),
                    'nodata':output.GetRasterBand(1).GetNoDataValue()}
        output = None; source = None
        record(name, manifest, url=url, bbox=bounds, resolution_m=resolution,
               reduction='GDAL Translate average with source overview selection AUTO',
               epsg=25831, raster=metadata, gdal=gdal.VersionInfo())


def fetch_detail():
    """A bounded 5 m crop around the selected vacant parcel, and dated review orthos."""
    from osgeo import gdal
    from urllib.parse import urlencode
    gdal.UseExceptions()
    gdal.SetConfigOption('GDAL_DISABLE_READDIR_ON_OPEN', 'EMPTY_DIR')
    gdal.SetConfigOption('GDAL_HTTP_TIMEOUT', '90')
    manifest = initialise()
    bounds = (347200,4550750,348050,4551420)
    name = 'mdt-solar-pineda-5m.tif'
    if not cached(name, manifest):
        ds = gdal.Translate(str(PRIVATE/name), '/vsicurl/'+MDT,
                            projWin=[bounds[0],bounds[3],bounds[2],bounds[1]],
                            xRes=5,yRes=5,resampleAlg='nearest',
                            creationOptions=['COMPRESS=DEFLATE','TILED=YES'])
        ds = None
        record(name, manifest, url=MDT, bbox=bounds, resolution_m=5, epsg=25831,
               reduction='native 5 m crop, no coarsening')
    for name, bounds, size in [
            ('orto-pineda-2025.png',(347200,4550750,348050,4551420),(1020,804)),
            ('orto-refineria-2025.png',(350000,4558800,352000,4561300),(800,1000))]:
        if cached(name, manifest): continue
        params={'SERVICE':'WMS','VERSION':'1.3.0','REQUEST':'GetMap',
                'LAYERS':'ortofoto_25cm_color_2025','STYLES':'','CRS':'EPSG:25831',
                'BBOX':','.join(map(str,bounds)),'WIDTH':size[0],'HEIGHT':size[1],'FORMAT':'image/png'}
        url='https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?'+urlencode(params)
        with urllib.request.urlopen(url,timeout=90) as response: data=response.read(10_000_001)
        assert len(data)<=10_000_000 and data.startswith(b'\x89PNG\r\n\x1a\n')
        (PRIVATE/name).write_bytes(data)
        record(name,manifest,url=url,bbox=bounds,pixels=size,edition=2025,
               role='visual check of study-site selection; not an elevation model')


def models(sample_spacing=500, output_name='models'):
    """Offline, explicitly assumed experiments on real geometry and elevations."""
    import heapq
    import numpy as np
    import shapely
    from shapely.geometry import Point, mapping
    from osgeo import gdal, ogr, osr
    gdal.UseExceptions(); ogr.UseExceptions()
    manifest=initialise()
    for name in ['ambits.gpkg','parceles-dgc-43173.zip','parceles-dgc-43111.zip',
                 'mdt-regional-25m.tif','mds-regional-25m.tif','mdt-solar-pineda-5m.tif']:
        assert cached(name,manifest), name
    assert sample_spacing in (250,500) and output_name in ('models','models-20260930')
    output=PRIVATE/output_name; output.mkdir(exist_ok=True)
    crs=osr.SpatialReference();crs.ImportFromEPSG(25831)

    def parcel(code, reference):
        archive=PRIVATE/f'parceles-dgc-{code}.zip'
        with zipfile.ZipFile(archive) as z:
            name=next(n for n in z.namelist() if n.endswith('.cadastralparcel.gml'))
        source=ogr.Open('/vsizip/'+str(archive)+'/'+name)
        layer=source.GetLayer(0);layer.SetAttributeFilter(f"nationalCadastralReference = '{reference}'")
        features=list(layer);assert len(features)==1
        return shapely.from_wkb(bytes(features[0].GetGeometryRef().ExportToWkb()))

    def vector(path, name, rows, geometry_type):
        if path.exists():
            old=ogr.Open(str(path)); features=list(old.GetLayer(0))
            assert len(features)==len(rows),path
            for f,(label,geometry) in zip(features,rows):
                assert f['nom']==label and shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())).equals(geometry),path
            return
        ds=ogr.GetDriverByName('GPKG').CreateDataSource(str(path))
        layer=ds.CreateLayer(name,crs,geometry_type)
        layer.CreateField(ogr.FieldDefn('nom',ogr.OFTString))
        for label,geometry in rows:
            f=ogr.Feature(layer.GetLayerDefn());f['nom']=label
            geom=ogr.CreateGeometryFromWkb(geometry.wkb)
            if geometry_type==ogr.wkbMultiPolygon and geom.GetGeometryType()==ogr.wkbPolygon:
                geom=ogr.ForceToMultiPolygon(geom)
            f.SetGeometry(geom);layer.CreateFeature(f)
        ds=None

    def raster(path, array, ref, nodata):
        if path.exists():
            old=gdal.Open(str(path))
            assert old.GetGeoTransform()==ref.GetGeoTransform() and np.array_equal(old.ReadAsArray(),array),path
            return
        dtype=gdal.GDT_Byte if array.dtype==np.uint8 else gdal.GDT_Float32
        ds=gdal.GetDriverByName('GTiff').Create(str(path),array.shape[1],array.shape[0],1,dtype,
                                               ['COMPRESS=DEFLATE','TILED=YES'])
        ds.SetGeoTransform(ref.GetGeoTransform());ds.SetProjection(ref.GetProjection())
        band=ds.GetRasterBand(1);band.SetNoDataValue(nodata);band.WriteArray(array);ds=None

    def burn(ref, geometries):
        vectors=ogr.GetDriverByName('Memory').CreateDataSource('')
        layer=vectors.CreateLayer('mask',crs,ogr.wkbMultiPolygon)
        for geometry in geometries:
            f=ogr.Feature(layer.GetLayerDefn());f.SetGeometry(ogr.CreateGeometryFromWkb(geometry.wkb))
            layer.CreateFeature(f)
        ds=gdal.GetDriverByName('MEM').Create('',ref.RasterXSize,ref.RasterYSize,1,gdal.GDT_Byte)
        ds.SetGeoTransform(ref.GetGeoTransform());ds.SetProjection(ref.GetProjection())
        gdal.RasterizeLayer(ds,[1],layer,burn_values=[1])
        return ds.ReadAsArray().astype(bool)

    solar=parcel('43173','7713904CF4571D')
    industry=parcel('43111','1406801CF5610C')
    vector(output/'solar-pineda.gpkg','solar',[('Parcel·la cadastral 7713904CF4571D',solar)],ogr.wkbMultiPolygon)
    vector(output/'sector-petroquimic.gpkg','sector',[('Sector cadastral de la refineria nord',industry)],ogr.wkbMultiPolygon)
    local=gdal.Open(str(PRIVATE/'mdt-solar-pineda-5m.tif'))
    dem=local.ReadAsArray(); valid=dem != local.GetRasterBand(1).GetNoDataValue()
    assert valid.all(), 'The bounded walking experiment requires complete elevation coverage'
    inside=burn(local,[solar]); gt=local.GetGeoTransform()
    start=(347300.,4551050.); end=(347900.,4551030.)
    def cell(xy):return (int((xy[1]-gt[3])/gt[5]),int((xy[0]-gt[0])/gt[1]))
    a,b=cell(start),cell(end);assert not inside[a] and not inside[b]
    # Pure isotropic resistance: 1 outside, 1 or 20 inside. Cost units are
    # weighted metres, deliberately not calibrated walking seconds.
    neighbours=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    paths={};walking={}
    for name,penalty in [('obert',1),('penalitzat',20)]:
        friction=np.where(inside,penalty,1.).astype(np.float32)
        distance=np.full(dem.shape,np.inf);distance[a]=0;previous={};queue=[(0.,a)]
        while queue:
            cost,(y,x)=heapq.heappop(queue)
            if cost != distance[y,x]:continue
            for dy,dx in neighbours:
                yy,xx=y+dy,x+dx
                if not (0<=yy<dem.shape[0] and 0<=xx<dem.shape[1]):continue
                length=5*math.hypot(dy,dx)
                candidate=cost+.5*(friction[y,x]+friction[yy,xx])*length
                if candidate<distance[yy,xx]:
                    distance[yy,xx]=candidate;previous[(yy,xx)]=(y,x)
                    heapq.heappush(queue,(candidate,(yy,xx)))
        route=[b]
        while route[-1]!=a:route.append(previous[route[-1]])
        route.reverse()
        coords=[(gt[0]+(x+.5)*5,gt[3]-(y+.5)*5) for y,x in route]
        geometry=shapely.LineString(coords)
        vector(output/f'ruta-pineda-{name}.gpkg','ruta',[(name,geometry)],ogr.wkbLineString)
        raster(output/f'friccio-{name}.tif',friction,local,-9999)
        raster(output/f'cost-{name}.tif',distance.astype(np.float32),local,-9999)
        walking[name]={'length_m':geometry.length,'cost_weighted_m':float(distance[b]),
                       'inside_length_m':geometry.intersection(solar).length,
                       'inside_penalty':penalty}
        paths[name]=coords
    assert walking['obert']['inside_length_m']>100
    assert walking['penalitzat']['inside_length_m']<10
    vector(output/'extrems-pineda.gpkg','extrems',[('O',Point(start)),('D',Point(end))],ogr.wkbPoint)

    terrain=gdal.Open(str(PRIVATE/'mdt-regional-25m.tif'))
    elevation=terrain.ReadAsArray();valid=elevation != -9999
    admin=ogr.Open(str(PRIVATE/'ambits.gpkg'))
    counties=[shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())) for f in admin.GetLayerByName('comarques')]
    land=[shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb())) for f in admin.GetLayerByName('terra_catalunya')]
    county_mask=burn(terrain,counties);land_mask=burn(terrain,land)
    inland_missing=int((land_mask & ~valid).sum())
    print('NoData within land mask:',inland_missing,flush=True)
    # NoData is not specially handled by GDAL Viewshed. Sea is assumed flat at
    # 0 m. Terrestrial gaps are filled only for running the sweep, then every
    # potentially affected ray is excluded, with a one-cell neighbourhood buffer.
    # Conservative angular bins can exclude extra cells; they never assert an
    # unknown terrestrial height to be known sea level.
    rgt=terrain.GetGeoTransform()
    yy,xx=np.indices(elevation.shape)
    east=rgt[0]+(xx+.5)*25; north=rgt[3]-(yy+.5)*25
    gaps=land_mask & ~valid
    def known_rays(point):
        bins=16384
        threshold=np.full(bins,np.inf)
        gx=east[gaps]-point.x;gy=north[gaps]-point.y
        radius=3*25/math.sqrt(2)  # circumscribed 3x3-cell neighbourhood
        for x,y in zip(gx,gy):
            d=math.hypot(x,y)
            if d<=radius:raise RuntimeError('Observer too close to missing terrain')
            angle=math.atan2(y,x)%(2*math.pi);half=math.asin(radius/d)
            lo=math.floor((angle-half)/(2*math.pi)*bins)-1
            hi=math.ceil((angle+half)/(2*math.pi)*bins)+1
            indices=np.arange(lo,hi+1)%bins
            threshold[indices]=np.minimum(threshold[indices],d-radius)
        angles=(np.arctan2(north-point.y,east-point.x)%(2*math.pi))
        index=np.floor(angles/(2*math.pi)*bins).astype(int)
        return np.hypot(east-point.x,north-point.y)<threshold[index]
    work=gdal.GetDriverByName('MEM').CreateCopy('',terrain)
    work.GetRasterBand(1).WriteArray(np.where(valid,elevation,0))
    centre=industry.centroid
    bounds=industry.bounds
    spacing=sample_spacing
    targets=[Point(x,y) for x in np.arange(math.ceil(bounds[0]/spacing)*spacing+spacing/2,bounds[2],spacing)
                       for y in np.arange(math.ceil(bounds[1]/spacing)*spacing+spacing/2,bounds[3],spacing)
                       if industry.contains(Point(x,y))]
    assert len(targets)>=4
    vector(output/'objectius-petroquimica.gpkg','objectius',
           [('Centre',centre)]+[(f'Mostra {i+1}',p) for i,p in enumerate(targets)],ogr.wkbPoint)
    def viewshed(point,height,receiver):
        ds=gdal.ViewshedGenerate(work.GetRasterBand(1),'MEM','',[],point.x,point.y,
                                 height,receiver,1,0,255,255,0.85714,gdal.GVM_Edge,0)
        assert ds.GetGeoTransform()==terrain.GetGeoTransform()
        return ds.ReadAsArray()
    single=viewshed(centre,30,1.7)
    accumulated=sum((viewshed(p,30,1.7).astype(np.uint16) for p in targets))
    tall=viewshed(centre,60,1.7); roof=viewshed(centre,30,15)
    initial_mask=valid & county_mask
    mask=initial_mask & known_rays(centre)
    for p in targets:mask &= known_rays(p)
    assert (tall[mask]>=single[mask]).all() and (roof[mask]>=single[mask]).all()
    regional={}
    for name,arr in [('centre-30m',single),('acumulada-30m',accumulated),
                     ('centre-60m',tall),('receptor-15m',roof)]:
        values=np.where(mask,arr,255).astype(np.uint8)
        raster(output/f'visibilitat-{name}.tif',values,terrain,255)
        regional[name]={'visible_cells':int(((arr>0)&mask).sum()),
                        'valid_cells':int(mask.sum()),'cell_area_m2':625}
    controls={'walking':walking,'solar_area_m2':solar.area,'petrochemical_sector_area_m2':industry.area,
              'target_count':len(targets),'sample_spacing_m':sample_spacing,'model_folder':output_name,
              'regional':regional,'inland_missing':inland_missing,
              'marine_completion':'outside land mask, flat sea at 0 m',
              'coverage_ray_excluded_cells':int((initial_mask & ~mask).sum()),
              'coverage_handling':'all rays potentially crossing missing land excluded for every target; 3x3-cell neighbourhood; 16384 conservative angular bins',
              'viewshed':{'engine':'GDAL '+gdal.VersionInfo(),'mode':'edge','curvature_coefficient':.85714,
                          'heights':'assumed 30/60 m targets; 1.7/15 m receptors above terrain',
                          'surface':'MDT reduced to 25 m; MDS delivered separately for comparison'}}
    (output/'controls.json').write_text(json.dumps(controls,ensure_ascii=False,indent=2)+'\n')
    figure={'controls':controls,'solar':mapping(solar),'industry':mapping(industry),
            'walking_paths':paths,'walking_extent':[gt[0],gt[0]+5*dem.shape[1],gt[3]-5*dem.shape[0],gt[3]],
            'walking_mask':inside.astype(int).tolist(),'walking_start':start,'walking_end':end,
            'county_boundaries':[mapping(g.simplify(50)) for g in counties],
            'regional_extent':[311000,375000,4532000,4581000],
            'regional_single':np.where(mask,single,255)[::4,::4].tolist(),
            'regional_accumulated':np.where(mask,accumulated,255)[::4,::4].tolist(),
            'display_sampling':'one 25 m cell per 100 m display grid; full outputs retained in package',
            'targets':[[p.x,p.y] for p in targets],'centre':[centre.x,centre.y]}
    (ROOT/'context/inputs/practiques-mapes.json').write_text(json.dumps(figure,ensure_ascii=False,separators=(',',':'))+'\n')
    print(json.dumps(controls,indent=2),flush=True)


def network_model():
    import os
    import sys
    import numpy as np
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsVectorLayer,QgsProject,QgsCoordinateReferenceSystem,
                           QgsProcessingContext,QgsFeature,QgsField,QgsGeometry,QgsPointXY,
                           QgsVectorFileWriter,QgsLineSymbol,QgsMarkerSymbol)
    from qgis.PyQt.QtCore import QVariant
    app=QgsApplication([],False);app.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()
    manifest=initialise();assert cached('rtt-original.gpkg',manifest)
    # Mount the original read-only: QGIS can otherwise update SQLite file headers.
    source=QgsVectorLayer(str(PRIVATE/'rtt-original.gpkg')+'|layername=_35_transports_l','RTT original','ogr')
    assert source.isValid()
    allowed={'vcu','vpu','aut','vpd','vnc','vcd'}
    features=[f for f in source.getFeatures() if f['tipus'] in allowed]
    model=QgsVectorLayer('LineString?crs=EPSG:25831','Xarxa de prova','memory')
    model.dataProvider().addAttributes(source.fields())
    model.dataProvider().addAttributes([QgsField('sentit',QVariant.String),QgsField('v_kmh',QVariant.Double)])
    model.updateFields()
    for original in features:
        f=QgsFeature(model.fields());f.setGeometry(original.geometry());f.setAttributes(original.attributes()+['B',30.])
        model.dataProvider().addFeatures([f])
    model.updateExtents()
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    seeds=[QgsPointXY(344334,4552736),QgsPointXY(352914,4553335)]
    # Explicit vertices on the common main component, selected after inspecting
    # the original graph. The nearest independent snaps had no connecting route.
    endpoints=[QgsPointXY(344141.54,4553070.82),QgsPointXY(353180.77,4553971.06)]
    vertices={(p.x(),p.y()) for f in model.getFeatures() for p in f.geometry().asPolyline()}
    assert all((p.x(),p.y()) in vertices for p in endpoints)
    adjustments=[math.hypot(p.x()-s.x(),p.y()-s.y()) for p,s in zip(endpoints,seeds)]
    start,end=endpoints
    print('Explicit axis endpoints',[(p.x(),p.y()) for p in endpoints],'seed distances',adjustments,flush=True)
    params={'INPUT':model,'STRATEGY':0,'START_POINT':f'{start.x()},{start.y()} [EPSG:25831]',
            'END_POINT':f'{end.x()},{end.y()} [EPSG:25831]',
            'DIRECTION_FIELD':'sentit','VALUE_FORWARD':'F','VALUE_BACKWARD':'R','VALUE_BOTH':'B',
            'DEFAULT_DIRECTION':2,'SPEED_FIELD':'v_kmh','DEFAULT_SPEED':30.,
            'TOLERANCE':0.,'POINT_TOLERANCE':100.,'OUTPUT':'memory:'}
    base=processing.run('native:shortestpathpointtopoint',params,context=context)['OUTPUT']
    route=next(base.getFeatures()).geometry()
    candidates=[f for f in model.getFeatures() if f.geometry().intersection(route).length()>30
                and f.geometry().distance(QgsGeometry.fromPointXY(start))<1500]
    assert candidates,'No local route edge for controlled experiment'
    from qgis.core import QgsProcessingException
    attempts=[]
    for edge in sorted(candidates,key=lambda f:f.geometry().distance(QgsGeometry.fromPointXY(start))):
        line=edge.geometry().asPolyline()
        forward=route.lineLocatePoint(QgsGeometry.fromPointXY(line[0]))<route.lineLocatePoint(QgsGeometry.fromPointXY(line[-1]))
        model.dataProvider().changeAttributeValues({edge.id():{model.fields().indexFromName('sentit'):'R' if forward else 'F'}})
        try:
            direction=processing.run('native:shortestpathpointtopoint',params,context=context)['OUTPUT']
            length=next(direction.getFeatures()).geometry().length()
            attempts.append({'id':int(edge['id']),'length_m':length})
            if length>route.length()+1:break
        except QgsProcessingException as exc:
            if 'no route' not in str(exc).lower():raise
            attempts.append({'id':int(edge['id']),'result':'no route'})
        model.dataProvider().changeAttributeValues({edge.id():{model.fields().indexFromName('sentit'):'B'}})
    else:raise RuntimeError('No local edge with an alternative detour found')
    model.dataProvider().changeAttributeValues({edge.id():{model.fields().indexFromName('sentit'):'B',
                                                           model.fields().indexFromName('v_kmh'):3.}})
    impedance=processing.run('native:shortestpathpointtopoint',{**params,'STRATEGY':1},context=context)['OUTPUT']
    output=PRIVATE/'models';output.mkdir(exist_ok=True)
    def save(layer,name,colour,width):
        path=output/(name+'.gpkg');assert not path.exists(),path
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='GPKG';options.layerName=name
        status=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(path),project.transformContext(),options)
        assert status[0]==QgsVectorFileWriter.NoError,status
        final=QgsVectorLayer(str(path),name,'ogr')
        final.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':colour,'line_width':str(width)}))
        final.saveStyleToDatabase(name,'Experiment amb geometria ICGC i paràmetres assumits',True,'')
    results={}
    for name,layer,colour in [('base',base,'#bd3544'),('sentit',direction,'#228966'),('impedancia',impedance,'#cc7a00')]:
        f=next(layer.getFeatures());geometry=f.geometry()
        results[name]={'length_m':geometry.length(),'reported_cost':float(f['cost']),
                       'cost_unit':'hours at assumed speed' if name=='impedancia' else 'metres',
                       'geometry':json.loads(geometry.asJson())}
        save(layer,'ruta-xarxa-'+name,colour,1.)
    assert results['sentit']['length_m']>=results['base']['length_m']-.01
    save(model,'xarxa-copia-impedancia','#a4adb7',.2)
    controls={'algorithm':'native:shortestpathpointtopoint','project_ellipsoid':'NONE',
              'original_count':len(list(source.getFeatures())),'routing_count':len(features),
              'changed_source_id':int(edge['id']),'assumed_direction':'R' if forward else 'F',
              'default_speed_kmh':30,'penalised_speed_kmh':3,'topology_tolerance_m':0,
              'point_tolerance_m':100,'start':[start.x(),start.y()],'end':[end.x(),end.y()],
              'seed_to_axis_distance_m':adjustments,
              'endpoint_selection':'explicit vertices in the common main component; not municipal centres',
              'initial_nearest_snaps_result':'no route between independently snapped points',
              'local_edge_trials':attempts,
              'results':results,'turn_costs':'not supported by this native algorithm; not applied'}
    (output/'xarxa-controls.json').write_text(json.dumps(controls,ensure_ascii=False,indent=2)+'\n')
    # A full original and a distinct one-edge-modified working copy are retained.
    summary={**controls,'results':{k:{a:b for a,b in v.items() if a!='geometry'} for k,v in results.items()}}
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)


def capture_inputs():
    import shutil
    from osgeo import ogr
    ogr.UseExceptions()
    folder=ROOT/'tmp/dades-docents/qgis';folder.mkdir(exist_ok=True)
    for name in ['xarxa-copia-impedancia','ruta-xarxa-base','ruta-xarxa-sentit']:
        target=folder/(name+'.gpkg')
        assert not target.exists(),target
        shutil.copyfile(PRIVATE/'models'/(name+'.gpkg'),target)
    source=ogr.Open(str(PRIVATE/'models/xarxa-copia-impedancia.gpkg'))
    layer=source.GetLayer(0);layer.SetAttributeFilter('id=1331675')
    features=list(layer);assert len(features)==1
    target=folder/'xarxa-detall.gpkg';assert not target.exists()
    ds=ogr.GetDriverByName('GPKG').CreateDataSource(str(target))
    out=ds.CreateLayer('detall',layer.GetSpatialRef(),ogr.wkbPolygon)
    f=ogr.Feature(out.GetLayerDefn());f.SetGeometry(features[0].GetGeometryRef().Buffer(120));out.CreateFeature(f)
    ds=None
    print('Prepared real routing capture inputs',flush=True)


def packages():
    """Seal new, private Moodle archives; never overwrite an existing package."""
    import sqlite3
    from osgeo import ogr,osr
    ogr.UseExceptions()
    census=ROOT/'tmp/dades-docents/seccions'
    joined=census/'seccions-analisi.gpkg'
    features=json.loads((ROOT/'context/inputs/seccions-tarragones.geojson').read_text())['features']
    properties={f['properties']['cusec']:f['properties'] for f in features}
    if not joined.exists():
        source=ogr.Open('/vsizip/'+str(census/'originals/seccions-20240101.zip'))
        layer=source.GetLayer(0)
        target=ogr.GetDriverByName('GPKG').CreateDataSource(str(joined))
        out=target.CreateLayer('seccions',layer.GetSpatialRef(),ogr.wkbMultiPolygon)
        keys=sorted(set().union(*(p.keys() for p in properties.values())))
        for key in keys:
            values=[p[key] for p in properties.values() if p.get(key) is not None]
            sample=values[0]
            kind=ogr.OFTReal if isinstance(sample,float) else ogr.OFTInteger64 if isinstance(sample,(int,bool)) else ogr.OFTString
            out.CreateField(ogr.FieldDefn(key,kind))
        count=0
        for f in layer:
            code=f['MUNICIPI'][:5]+f['DISTRICTE'].zfill(2)+f['SECCIO'].zfill(3)
            if code not in properties:continue
            row=ogr.Feature(out.GetLayerDefn())
            row.SetGeometry(ogr.ForceToMultiPolygon(f.GetGeometryRef().Clone()))
            for key,value in properties[code].items():
                if value is None:continue
                if isinstance(value,list):value=json.dumps(value,ensure_ascii=False)
                if isinstance(value,bool):value=int(value)
                row.SetField(key,value)
            out.CreateFeature(row);count+=1
        assert count==151
        target=None
    check=ogr.Open(str(joined));assert check.GetLayer(0).GetFeatureCount()==151;check=None
    receipts=initialise()
    raw_names=['rtt-original.gpkg','ambits.gpkg','mdt-regional-25m.tif','mds-regional-25m.tif',
               'mdt-solar-pineda-5m.tif','orto-pineda-2025.png','orto-refineria-2025.png',
               'parceles-dgc-43173.zip','parceles-dgc-43111.zip']
    for name in raw_names:assert cached(name,receipts),name
    model_names=['controls.json','xarxa-controls.json','solar-pineda.gpkg','extrems-pineda.gpkg',
                 'sector-petroquimic.gpkg','objectius-petroquimica.gpkg',
                 'friccio-obert.tif','friccio-penalitzat.tif','cost-obert.tif','cost-penalitzat.tif',
                 'ruta-pineda-obert.gpkg','ruta-pineda-penalitzat.gpkg',
                 'visibilitat-centre-30m.tif','visibilitat-acumulada-30m.tif',
                 'visibilitat-centre-60m.tif','visibilitat-receptor-15m.tif',
                 'ruta-xarxa-base.gpkg','ruta-xarxa-sentit.gpkg','ruta-xarxa-impedancia.gpkg',
                 'xarxa-copia-impedancia.gpkg']
    common=[('README.md',ROOT/'context/dades/practiques-territorials.md')]
    practical=common+[(f'fonts/{n}',PRIVATE/n) for n in raw_names]
    practical += [(f'resultats/{n}',PRIVATE/'models'/n) for n in model_names]
    practical += [('procedencia.json',PRIVATE/'manifest.json'),
                  ('reproduccio/preparar_practiques.py',Path(__file__))]
    census_result=json.loads((ROOT/'context/inputs/seccions-resultats.json').read_text())
    census_files=common+[(f'fonts/{n}',census/'originals'/n) for n in census_result['sources_used']]
    census_files += [('seccions-analisi.gpkg',joined),
                     ('seccions-resultats.json',ROOT/'context/inputs/seccions-resultats.json'),
                     ('autoconsum-tarragona-20260928.gpkg',ROOT/'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'),
                     ('reproduccio/preparar_seccions.py',ROOT/'context/dades/preparar_seccions.py'),
                     ('reproduccio/preparar_icaen.py',ROOT/'context/qgis/preparar_icaen.py')]
    for n in ['icaen-coneguda.gpkg','icaen-ambit.gpkg','icaen-centres.gpkg','icaen-controls.json']:
        census_files.append((f'centres/{n}',ROOT/'tmp/dades-docents/qgis'/n))
    for name,files in [('demos-practiques-territorials-20260929.zip',practical),
                       ('demos-seccions-autoconsum-20260929.zip',census_files)]:
        target=ROOT/'tmp/dades-docents'/name
        if target.exists():raise RuntimeError(f'Existing package retained: {target}')
        inventory=[]
        with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
            for member,path in sorted(files):
                assert path.resolve().is_relative_to(ROOT) and path.is_file(),path
                if path.suffix=='.gpkg':
                    # SQLite backup includes any committed WAL pages and produces a
                    # self-contained portable snapshot without editing its source.
                    wal=path.with_name(path.name+'-wal')
                    uri=f'file:{path}?mode=ro'+('' if wal.exists() else '&immutable=1')
                    src=sqlite3.connect(uri,uri=True)
                    with path.open('rb') as header_file:
                        wal_header=header_file.read(20)[18:20]==b'\x02\x02'
                    dst=sqlite3.connect(':memory:');src.backup(dst)
                    assert dst.execute('PRAGMA integrity_check').fetchone()[0]=='ok',path
                    # Deserialised memory databases retain the on-disk WAL header.
                    # A temporary on-disk backup converts only the delivery copy.
                    import tempfile
                    with tempfile.TemporaryDirectory(dir=PRIVATE) as staging:
                        snapshot=Path(staging)/'snapshot.gpkg'
                        disk=sqlite3.connect(snapshot);dst.backup(disk)
                        disk.execute('PRAGMA journal_mode=DELETE');disk.close()
                        data=path.read_bytes() if not wal_header and not wal.exists() else snapshot.read_bytes()
                    src.close();dst.close()
                else:data=path.read_bytes()
                entry=zipfile.ZipInfo(member,(2026,9,29,0,0,0));entry.external_attr=0o100644<<16
                archive.writestr(entry,data,compress_type=zipfile.ZIP_DEFLATED)
                inventory.append({'path':member,'source':str(path.relative_to(ROOT)),
                                  'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
            archive.writestr('MANIFEST.json',json.dumps({'schema_version':1,'files':inventory},
                                                       ensure_ascii=False,indent=2)+'\n')
        with zipfile.ZipFile(target) as archive:
            assert archive.testzip() is None
            for item in inventory:
                assert hashlib.sha256(archive.read(item['path'])).hexdigest()==item['sha256']
        print('PACKAGE',name,'bytes',target.stat().st_size,'sha256',sha(target),'files',len(inventory),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--only', choices=['roads','rasters'])
    parser.add_argument('--retain-incomplete-roads', action='store_true')
    parser.add_argument('--fetch-detail', action='store_true')
    parser.add_argument('--models', action='store_true')
    parser.add_argument('--sample-spacing',type=int,default=500)
    parser.add_argument('--models-dir',default='models')
    parser.add_argument('--network-model', action='store_true')
    parser.add_argument('--capture-inputs', action='store_true')
    parser.add_argument('--package', action='store_true')
    args = parser.parse_args()
    if args.retain_incomplete_roads:
        manifest = initialise()
        original = PRIVATE/'rtt-original.gpkg'
        retained = PRIVATE/'rtt-extraccio-incompleta.gpkg'
        assert 'rtt-original.gpkg' not in manifest and not retained.exists()
        original.rename(retained)
        print('Retained incomplete extraction', sha(retained), flush=True)
    if args.fetch: fetch(args.only)
    if args.fetch_detail: fetch_detail()
    if args.models: models(args.sample_spacing,args.models_dir)
    if args.network_model: network_model()
    if args.capture_inputs: capture_inputs()
    if args.package: packages()
