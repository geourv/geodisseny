"""One municipal sequence for chapters 4/5; read-only retained originals.

Build a new destination, run public QGIS Processing and independent numerical
controls. Captures/figures use this data, not sealed previous teaching bundles.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'tmp/dades-docents/qgis/constanti-pedagogia-20261005'
OLD = ROOT / 'tmp/dades-docents/qgis/punts-municipals-20261004'
IMAGE = 'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'
BOUNDS = (343500, 4554000, 353500, 4563000)
SEED = 20261005
_APP = None

def sha(path):
    with Path(path).open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()

def dump(path,value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def build():
    global _APP
    import numpy as np
    from osgeo import gdal
    from qgis.core import (QgsApplication,QgsProject,QgsVectorLayer,QgsVectorFileWriter,QgsFeature,
        QgsField,QgsGeometry,QgsPointXY,QgsCoordinateReferenceSystem,QgsRectangle,QgsReferencedRectangle,
        QgsMarkerSymbol,QgsFillSymbol,QgsLineSymbol,QgsCategorizedSymbolRenderer,QgsRendererCategory,
        QgsGraduatedSymbolRenderer,QgsRendererRange,QgsRasterLayer,QgsColorRampShader,QgsRasterShader,
        QgsSingleBandPseudoColorRenderer,QgsRuleBasedRenderer,QgsProperty,QgsSymbolLayer,
        QgsPalLayerSettings,QgsVectorLayerSimpleLabeling,QgsTextFormat,QgsTextBufferSettings,
        QgsProcessingContext,QgsProcessingFeedback,Qgis)
    from qgis.PyQt.QtCore import QVariant
    from qgis.PyQt.QtGui import QColor
    import libpysal,esda
    from libpysal.weights import KNN,lag_spatial
    from esda import Moran,Moran_Local
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    assert not OUT.exists() or {p.name for p in OUT.iterdir()} <= {'constanti.gpkg'},'Fresh destination or this preparation’s incomplete first GeoPackage required.'
    OUT.mkdir(exist_ok=True)
    _APP=QgsApplication([],False);_APP.initQgis()
    sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize();import processing
    cache=ROOT/'tmp/qgis/cache/plugins/sha256-950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc-139383569f94'
    sys.path.insert(0,str(cache))
    from HotSpotAnalysis_v3.processing.provider import HotspotProvider
    provider=HotspotProvider();QgsApplication.processingRegistry().addProvider(provider)
    controls={'image':IMAGE,'qgis':Qgis.QGIS_VERSION,'libpysal':libpysal.__version__,'esda':esda.__version__,
              'seed':SEED,'operations':[],'sources':{},'manual_click_by_click':False}
    for path in [OLD/'municipis.gpkg',OLD/'ortofoto.tif',OLD/'ortofoto.qml']:
        controls['sources'][str(path.relative_to(ROOT))]=sha(path)
    reference=json.loads((OLD/'controls.json').read_text())
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    layers={};target=OUT/'constanti.gpkg';first=True
    ro=QgsVectorLayer.LayerOptions();ro.forceReadOnly=True

    def run(ident,**params):
        params.setdefault('OUTPUT','memory:')
        alg=QgsApplication.processingRegistry().algorithmById(ident)
        assert alg and set(params)<={p.name() for p in alg.parameterDefinitions()},(ident,params)
        feedback=QgsProcessingFeedback();context=QgsProcessingContext();context.setProject(project)
        result=processing.run(ident,params,context=context,feedback=feedback)['OUTPUT']
        controls['operations'].append({'id':ident,'parameters':{k:v.source() if isinstance(v,QgsVectorLayer) else str(v) for k,v in params.items()},'feedback':feedback.textLog()})
        return result

    def save(layer,name,title):
        nonlocal first
        opts=QgsVectorFileWriter.SaveVectorOptions();opts.driverName='GPKG';opts.layerName=name
        opts.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteFile if first else QgsVectorFileWriter.CreateOrOverwriteLayer
        result=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(target),project.transformContext(),opts)
        assert result[0]==QgsVectorFileWriter.NoError,result
        first=False
        result=QgsVectorLayer(str(target)+'|layername='+name,title,'ogr');assert result.isValid()
        assert result.featureCount()==layer.featureCount()
        layers[name]=result;return result

    original=QgsVectorLayer(str(OLD/'municipis.gpkg')+'|layername=punts_escenaris','Source','ogr',ro)
    assert original.isValid()
    selected=run('native:extractbyexpression',INPUT=original,EXPRESSION='"CODI_MUN" = 430477')
    assert selected.featureCount()==124
    points=save(selected,'punts','Constantí · 124 punts')
    points.startEditing();points.addAttribute(QgsField('llegenda',QVariant.String));points.updateFields()
    for f in points.getFeatures():
        points.changeAttributeValue(f.id(),points.fields().indexFromName('llegenda'),'450 kW' if f['POT_KW']==450 else '')
    assert points.commitChanges()
    unknown=sum(bool(f['imputat']) for f in points.getFeatures());assert unknown==26
    controls.update(n_all=124,n_known=98,known_kw=2770,assigned_mid_kw=200,mid_kw=2970)
    known_source=run('native:extractbyexpression',INPUT=points,EXPRESSION='"POT_KW" > 0')
    # Stable order is needed for KNN ties and values/weight alignment.
    known_sorted=QgsVectorLayer('Point?crs=EPSG:25831','Ordered','memory')
    known_sorted.dataProvider().addAttributes([f for f in known_source.fields() if f.name()!='fid']);known_sorted.updateFields()
    ordered=sorted(list(known_source.getFeatures()),key=lambda f:f['gml_id'])
    fresh=[]
    for source_feature in ordered:
        f=QgsFeature(known_sorted.fields());f.setGeometry(source_feature.geometry())
        f.setAttributes([source_feature[field.name()] for field in known_sorted.fields()]);fresh.append(f)
    known_sorted.dataProvider().addFeatures(fresh)
    known_sorted.updateExtents();known=save(known_sorted,'coneguda','Potències · 98 punts')
    coords=np.array([[f.geometry().asPoint().x(),f.geometry().asPoint().y()] for f in known.getFeatures()])
    features=list(known.getFeatures());ids=[f['gml_id'] for f in features];y=np.array([f['POT_KW'] for f in features],float)
    assert len(y)==98 and y.sum()==2770 and ids==sorted(ids)
    w=KNN.from_array(coords,k=8);w.transform='r';matrix,_=w.full()
    centred=y-y.mean();direct=centred@matrix@centred/(centred@centred)
    np.random.seed(SEED);m=Moran(y,w,permutations=9999)
    print('Moran raw control:',direct,m.I,flush=True)
    assert np.isclose(direct,m.I,atol=1e-12) and np.isclose(m.I,.19185630104632875)
    local=Moran_Local(y,w,seed=SEED,permutations=9999,n_jobs=1,keep_simulations=False)
    lag=lag_spatial(w,y);p=(1+np.count_nonzero(m.sim>=m.I))/10000
    assert p==.0004
    order=np.argsort(local.p_sim);accepted=local.p_sim[order]<=.05*np.arange(1,99)/98
    cutoff=float(local.p_sim[order][np.flatnonzero(accepted)[-1]]) if np.any(accepted) else -1
    k450=int(np.flatnonzero(y==450)[0])
    small_candidates=[i for i,f in enumerate(features) if y[i]==3 and coords[i,0]>349500]
    low=min(small_candidates,key=lambda i:lag[i])
    picked={'industrial':k450,'nucli':low}
    controls['point_examples']={name:{'gml_id':ids[i],'xy':coords[i].tolist(),'kw':float(y[i]),'neighbors_kw':y[w.neighbors[i]].tolist(),
        'lag_kw':float(lag[i]),'I_local':float(local.Is[i]),'quadrant':int(local.q[i]),'p_ref':float(local.p_sim[i])} for name,i in picked.items()}
    controls['moran']={'n':98,'mean_kw':float(y.mean()),'I':float(m.I),'expected_I':float(m.EI),'p_positive':p,
        'permutations':9999,'tail_count':int(np.count_nonzero(m.sim>=m.I)),'fdr_cutoff':cutoff,
        'nominal_counts':dict(Counter(str(local.q[i]) for i in range(98) if local.p_sim[i]<.05)),
        'fdr_counts':dict(Counter(str(local.q[i]) for i in range(98) if local.p_sim[i]<=cutoff)),
        'components':int(w.n_components),'longest_link_m':float(max(np.linalg.norm(coords[i]-coords[j]) for i in range(98) for j in w.neighbors[i]))}
    controls['local_reference']=[{'id':ids[i],'kw':float(y[i]),'lag_kw':float(lag[i]),'I_local':float(local.Is[i]),
        'p_ref':float(local.p_sim[i]),'q_ref':int(local.q[i]),'fdr':bool(local.p_sim[i]<=cutoff)} for i in range(98)]
    shuffled=np.random.default_rng(SEED).permutation(y)
    shuffled_c=shuffled-shuffled.mean();permuted_I=float(shuffled_c@matrix@shuffled_c/(shuffled_c@shuffled_c))
    histogram,edges=np.histogram(m.sim,bins=40)
    controls['permutation_example']={'I':permuted_I,'values_kw':shuffled.tolist(),'histogram':histogram.tolist(),'edges':edges.tolist(),
        'maximum':float(m.sim.max()),'percentiles':np.quantile(m.sim,[.025,.5,.975]).tolist()}
    known.startEditing()
    for i,f in enumerate(known.getFeatures()):
        label='450 kW' if i==k450 else '3 kW' if i==low else ''
        known.changeAttributeValue(f.id(),known.fields().indexFromName('llegenda'),label)
    assert known.commitChanges()
    lisa=run('hotspotanalysis:moranlocal',INPUT=known,FIELD='POT_KW',WEIGHTS_TYPE=1,KNN_K=8,
        OPTIMIZE=False,BINARY_WEIGHTS=True,DISTANCE_METRIC=0,ROW_STANDARDIZE=True,PERMUTATIONS=9999,TWO_TAILED=False)
    lisa=save(lisa,'moran','Moran · potències en kW')
    output=list(lisa.getFeatures());assert len(output)==98
    assert all(int(f['q_value'])==int(local.q[i]) for i,f in enumerate(output))
    controls['qgis_local']=[{'id':f['gml_id'],'q':int(f['q_value']),'p':float(f['p_value'])} for f in output]
    controls['qgis_nominal_counts']=dict(Counter(str(f['q_value']) if f['p_value']<.05 else 'NS' for f in output))
    link_layer=QgsVectorLayer('LineString?crs=EPSG:25831','Links','memory')
    link_layer.dataProvider().addAttributes([QgsField('punt',QVariant.String)]);link_layer.updateFields()
    for name,i in picked.items():
        for j in w.neighbors[i]:
            f=QgsFeature(link_layer.fields());f.setAttributes([name]);f.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(*coords[i]),QgsPointXY(*coords[j])]))
            link_layer.dataProvider().addFeatures([f])
    links=save(link_layer,'veins','Vuit veïns dels registres')
    neighbour_layer=QgsVectorLayer('Point?crs=EPSG:25831','Neighbours','memory')
    neighbour_layer.dataProvider().addAttributes([QgsField('valor',QVariant.String)]);neighbour_layer.updateFields()
    for i in [k450,*w.neighbors[k450]]:
        f=QgsFeature(neighbour_layer.fields());f.setAttributes([f'{int(y[i])} kW']);f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*coords[i])))
        neighbour_layer.dataProvider().addFeatures([f])
    detailed=save(neighbour_layer,'veins_industrial','450 kW i vuit potències veïnes')
    # Same 124 cases for descriptive summaries.
    centres_unweighted=run('native:meancoordinates',INPUT=points)
    centres_weighted=run('native:meancoordinates',INPUT=points,WEIGHT='w_mid')
    xyall=np.array([[f.geometry().asPoint().x(),f.geometry().asPoint().y()] for f in points.getFeatures()])
    xymean=xyall.mean(axis=0);weight=np.array([f['w_mid'] for f in points.getFeatures()],float)
    weighted=np.average(xyall,axis=0,weights=weight)
    assert np.allclose([next(centres_unweighted.getFeatures()).geometry().asPoint().x(),next(centres_unweighted.getFeatures()).geometry().asPoint().y()],xymean)
    assert np.allclose([next(centres_weighted.getFeatures()).geometry().asPoint().x(),next(centres_weighted.getFeatures()).geometry().asPoint().y()],weighted)
    centre_layer=QgsVectorLayer('Point?crs=EPSG:25831','Centres','memory')
    centre_layer.dataProvider().addAttributes([QgsField('nom',QVariant.String)]);centre_layer.updateFields()
    for name,xy in [('Centre dels registres',xymean),('Centre ponderat',weighted)]:
        f=QgsFeature(centre_layer.fields());f.setAttributes([name]);f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*xy)));centre_layer.dataProvider().addFeatures([f])
    centres=save(centre_layer,'centres','Centres de Constantí')
    controls['centres']={'all':xymean.tolist(),'weighted_mid':weighted.tolist(),'shift_m':float(np.linalg.norm(weighted-xymean))}
    for name,title in [('dispersio','Centre i dispersió'),('cercle','Cercle · radi 2.001 m'),('ellipse','El·lipse · semieixos 1.934 i 510 m')]:
        old_layer=QgsVectorLayer(str(OLD/'municipis.gpkg')+'|layername='+name,name,'ogr',ro)
        layer=save(old_layer,name,title)
        if name=='dispersio':
            controls['dispersion']={k:next(layer.getFeatures())[k] for k in ['Sxx','Syy','Sxy','D_m','a_m','b_m','azimut']}
    cov=np.cov(xyall,rowvar=False,ddof=0)
    assert np.isclose(np.sqrt(np.trace(cov)),controls['dispersion']['D_m'])
    assert np.allclose(np.sqrt(np.linalg.eigvalsh(cov)[::-1]),[controls['dispersion']['a_m'],controls['dispersion']['b_m']])
    oldlimits=QgsVectorLayer(str(OLD/'municipis.gpkg')+'|layername=limits','Source limit','ogr',ro)
    limits=save(run('native:extractbyexpression',INPUT=oldlimits,EXPRESSION='"CODIMUNI" = \'430477\''),'limit','Límit de Constantí')
    grid=run('native:creategrid',TYPE=2,EXTENT=QgsRectangle(*BOUNDS),HSPACING=1000,VSPACING=1000,HOVERLAY=0,VOVERLAY=0,CRS=QgsCoordinateReferenceSystem('EPSG:25831'))
    grid=save(grid,'malla','Quadrats d’1 km²')
    counts=run('native:countpointsinpolygon',POLYGONS=grid,POINTS=points,FIELD='n_punts')
    counts=run('native:countpointsinpolygon',POLYGONS=counts,POINTS=known,WEIGHT='POT_KW',FIELD='kw_pub')
    counts=save(counts,'recompte','Recompte · 124 registres')
    assert grid.featureCount()==90 and sum(f['n_punts'] for f in counts.getFeatures())==124
    assert sum(f['kw_pub'] for f in counts.getFeatures())==2770
    cells=[]
    for f in counts.getFeatures():
        g=f.geometry();box=g.boundingBox()
        test=sum(box.contains(QgsPointXY(*xy)) for xy in xyall)
        assert test==f['n_punts']
        cells.append({'n':int(f['n_punts']),'known_kw':float(f['kw_pub']),'geometry':json.loads(g.asJson()),'bounds':[box.xMinimum(),box.yMinimum(),box.xMaximum(),box.yMaximum()]})
    controls['grid']={'cells':90,'size_m':1000,'n_total':124,'kw_total':2770,'counts':cells,
        'largest_count':max(cells,key=lambda f:f['n']),'largest_known_kw':max(cells,key=lambda f:f['known_kw'])}
    kernels=[]
    for radius in [500,1500]:
        raw=OUT/f'kernel-{radius}-raw.tif'
        run('qgis:heatmapkerneldensityestimation',INPUT=points,RADIUS=radius,PIXEL_SIZE=100,KERNEL=0,DECAY=0,OUTPUT_VALUE=0,OUTPUT=str(raw))
        ds=gdal.Open(str(raw));band=ds.GetRasterBand(1);v=band.ReadAsArray();valid=v!=band.GetNoDataValue()
        normalized=np.where(valid,v*3e6/(np.pi*radius**2),-9999).astype('float32')
        mass=float(normalized[valid].sum(dtype='float64'))*.01;assert abs(mass-124)/124<.03
        path=OUT/f'densitat-{radius}.tif';dest=gdal.GetDriverByName('GTiff').Create(str(path),ds.RasterXSize,ds.RasterYSize,1,gdal.GDT_Float32,options=['COMPRESS=DEFLATE'])
        dest.SetGeoTransform(ds.GetGeoTransform());dest.SetProjection(ds.GetProjection());dest.GetRasterBand(1).WriteArray(normalized);dest.GetRasterBand(1).SetNoDataValue(-9999);dest=None
        gt=ds.GetGeoTransform();ds=None
        kernels.append({'radius':radius,'file':path.name,'mass':mass,'max':float(normalized[valid].max()),
            'shape':list(normalized.shape),'extent':[gt[0],gt[0]+100*normalized.shape[1],gt[3]-100*normalized.shape[0],gt[3]],
            'values':np.where(valid,normalized,np.nan).tolist()})
    # JSON null, not NaN, for raster cells without a calculated contribution.
    for row in kernels:
        row['values']=[[None if np.isnan(v) else float(v) for v in line] for line in row['values']]
    controls['kernels']=[{k:v for k,v in row.items() if k!='values'} for row in kernels]
    def labels(layer,field,size=11):
        pal=QgsPalLayerSettings();pal.fieldName=field;fmt=QgsTextFormat();fmt.setSize(size);fmt.setColor(QColor('#173646'))
        buf=QgsTextBufferSettings();buf.setEnabled(True);buf.setColor(QColor('white'));buf.setSize(.9);fmt.setBuffer(buf);pal.setFormat(fmt)
        layer.setLabeling(QgsVectorLayerSimpleLabeling(pal));layer.setLabelsEnabled(True)
    points.renderer().setSymbol(QgsMarkerSymbol.createSimple({'color':'#00739b','size':'2','outline_color':'white','outline_width':'.15'}));labels(points,'llegenda')
    rules=QgsRuleBasedRenderer.Rule(None)
    for lo,hi,c in [(0,5,'#65b5cf'),(5,25,'#2786ad'),(25,100,'#9c4f38'),(100,500,'#682b39')]:
        symbol=QgsMarkerSymbol.createSimple({'color':c,'size':'2.8','outline_color':'white','outline_width':'.15'})
        rules.appendChild(QgsRuleBasedRenderer.Rule(symbol,filterExp=f'"POT_KW" > {lo} AND "POT_KW" <= {hi}',label=f'{lo}-{hi} kW'))
    known.setRenderer(QgsRuleBasedRenderer(rules));labels(known,'llegenda')
    # A separate proportional view retains the complete 124 cases and imputations.
    weights_layer=save(points,'pesos','Pesos · publicats o assignats')
    rules=QgsRuleBasedRenderer.Rule(None)
    for flag,c,name in [(0,'#00739b','Potència publicada'),(1,'#d39220','Pes assignat')]:
        symbol=QgsMarkerSymbol.createSimple({'color':c,'outline_color':'#293640','outline_width':'.15'})
        symbol.symbolLayer(0).setDataDefinedProperty(QgsSymbolLayer.PropertySize,QgsProperty.fromExpression('0.45 * sqrt("w_mid")'))
        rules.appendChild(QgsRuleBasedRenderer.Rule(symbol,filterExp=f'"imputat" = {flag}',label=name))
    weights_layer.setRenderer(QgsRuleBasedRenderer(rules));labels(weights_layer,'llegenda')
    centres.setRenderer(QgsCategorizedSymbolRenderer('nom',[QgsRendererCategory(name,QgsMarkerSymbol.createSimple({'name':shape,'color':c,'size':'5.5','outline_color':'white','outline_width':'.4'}),name)
        for name,shape,c in [('Centre dels registres','diamond','#b42b43'),('Centre ponderat','star','#222222')]]));labels(centres,'nom')
    for name,c,style in [('cercle','#c46e17','dash'),('ellipse','#0072b2','solid'),('limit','#3e464c','solid')]:
        layers[name].renderer().setSymbol(QgsFillSymbol.createSimple({'style':'no','outline_color':c,'outline_width':'.9' if name!='limit' else '.4','outline_style':style}))
    grid.renderer().setSymbol(QgsFillSymbol.createSimple({'style':'no','outline_color':'#69747b','outline_width':'.2'}))
    ranges=[]
    for lo,hi,c,label in [(-.1,.5,'255,255,255,0','0'),(.5,5.5,'#dae9f0','1-5'),(5.5,20.5,'#9bc5d6','6-20'),(20.5,50.5,'#468fae','21-50'),(50.5,124,'#0d577c','51-124')]:
        ranges.append(QgsRendererRange(lo,hi,QgsFillSymbol.createSimple({'color':c,'outline_color':'#667781','outline_width':'.15'}),label+' registres/km²'))
    counts.setRenderer(QgsGraduatedSymbolRenderer('n_punts',ranges))
    palette={1:'#b32d42',2:'#92bdd3',3:'#246991',4:'#e1a277',0:'#dddddd'}
    expr='CASE WHEN "p_value" >= 0.05 THEN 0 ELSE "q_value" END'
    lisa.setRenderer(QgsCategorizedSymbolRenderer(expr,[QgsRendererCategory(q,QgsMarkerSymbol.createSimple({'color':palette[q],'size':'3','outline_color':'white','outline_width':'.15'}),label)
        for q,label in [(1,'Alta amb veïns alts'),(3,'Baixa amb veïns baixos'),(4,'Alta amb veïns baixos'),(2,'Baixa amb veïns alts'),(0,'No destacada')]]));labels(lisa,'llegenda')
    links.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color':'#ce4960','line_width':'.6'}))
    detailed.renderer().setSymbol(QgsMarkerSymbol.createSimple({'color':'#276981','size':'3','outline_color':'white','outline_width':'.2'}));labels(detailed,'valor',12)
    for layer in layers.values():layer.saveStyleToDatabase('docent','Context Constantí i camps de lectura',True,'')
    for row in kernels:
        layer=QgsRasterLayer(str(OUT/row['file']),f'Densitat · radi {row["radius"]} m');assert layer.isValid()
        maximum=max(r['max'] for r in kernels)
        shader=QgsColorRampShader(0,maximum);shader.setColorRampType(QgsColorRampShader.Interpolated)
        shader.setColorRampItemList([QgsColorRampShader.ColorRampItem(maximum*t,QColor(c),f'{maximum*t:.0f} registres/km²') for t,c in [(0,'#fff2d4'),(.25,'#ffcf83'),(.5,'#f6955b'),(.75,'#cf4c46'),(1,'#831f3a')]])
        raster_shader=QgsRasterShader();raster_shader.setRasterShaderFunction(shader)
        renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,raster_shader);renderer.setClassificationMin(0);renderer.setClassificationMax(maximum)
        layer.setRenderer(renderer);layer.saveNamedStyle(str((OUT/row['file']).with_suffix('.qml')));layers[f'kde{row["radius"]}']=layer
    shutil.copyfile(OLD/'ortofoto.tif',OUT/'ortofoto.tif');shutil.copyfile(OLD/'ortofoto.qml',OUT/'ortofoto.qml')
    ortho=QgsRasterLayer(str(OUT/'ortofoto.tif'),'Ortofoto ICGC 2025');assert ortho.isValid();ortho.loadNamedStyle(str(OUT/'ortofoto.qml'));layers['ortho']=ortho
    projects={
        '01-recompte':['punts','recompte','limit','ortho'],
        '02-centres':['centres','pesos','limit','ortho'],
        '03-dispersio':['punts','centres','cercle','ellipse','limit','ortho'],
        '04-kernel':['punts','kde500','limit','ortho'],
        '05-moran':['veins','moran','coneguda','limit','ortho']}
    for name,visible in projects.items():
        project.clear();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE');project.setFilePathStorage(Qgis.FilePathType.Relative)
        for key in reversed(visible):
            layer=layers[key].clone()
            if name=='03-dispersio' and key=='centres':layer.setSubsetString('"nom" = \'Centre dels registres\'')
            project.addMapLayer(layer)
            if name=='05-moran' and key=='coneguda':project.layerTreeRoot().findLayer(layer.id()).setItemVisibilityChecked(False)
        project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*BOUNDS),project.crs()))
        assert project.write(str(OUT/(name+'.qgz')))
    project.clear()
    controls['projects']=list(projects)
    assert all(sha(ROOT/path)==digest for path,digest in controls['sources'].items())
    dump(OUT/'controls.json',controls)
    # Small retained plotting input; no personal IDs. Spatial rendering needs
    # only the positions/attribute already used by the municipal figures.
    figure={'bounds':BOUNDS,'sources':controls['sources'],'n_all':124,'n_known':98,'mean_kw':float(y.mean()),
        'known_points':[{'xy':coords[i].tolist(),'kw':float(y[i]),'lag_kw':float(lag[i]),'index':i} for i in range(98)],
        'examples':{name:{**{k:v for k,v in data.items() if k!='gml_id'},'index':picked[name]} for name,data in controls['point_examples'].items()},
        'neighbors':{name:[int(j) for j in w.neighbors[i]] for name,i in picked.items()},'moran':controls['moran'],'permutation':controls['permutation_example'],
        'grid':controls['grid'],'kernels':kernels,'all_points':xyall.tolist()}
    dump(OUT/'figure-input.json',figure)
    print(json.dumps({k:controls[k] for k in ['n_all','n_known','point_examples','moran','qgis_nominal_counts','centres','dispersion','kernels']},ensure_ascii=False,indent=2),flush=True)
    print('Grid cells:',controls['grid']['largest_count'],controls['grid']['largest_known_kw'],flush=True)

def record():
    dump(ROOT/'context/inputs/constanti-pedagogia.json',json.loads((OUT/'figure-input.json').read_text()))

def finish():
    """Retain plotting input after a JSON-only failure, without rerunning inference."""
    import numpy as np
    from osgeo import ogr,gdal
    from libpysal.weights import KNN
    c=json.loads((OUT/'controls.json').read_text());ds=ogr.Open(str(OUT/'constanti.gpkg'),0)
    known=list(ds.GetLayerByName('coneguda'));all_points=list(ds.GetLayerByName('punts'))
    xy=np.array([[f.GetGeometryRef().GetX(),f.GetGeometryRef().GetY()] for f in known]);ids=[f['gml_id'] for f in known]
    assert ids==sorted(ids)
    reference={r['id']:r for r in c['local_reference']};w=KNN.from_array(xy,k=8)
    examples={name:{**{k:v for k,v in example.items() if k!='gml_id'},'index':ids.index(example['gml_id'])} for name,example in c['point_examples'].items()}
    kernels=[]
    for spec in c['kernels']:
        raster=gdal.Open(str(OUT/spec['file']));values=raster.ReadAsArray();gt=raster.GetGeoTransform()
        kernels.append({**spec,'shape':list(values.shape),'extent':[gt[0],gt[0]+100*values.shape[1],gt[3]-100*values.shape[0],gt[3]],
            'values':[[None if v==-9999 else float(v) for v in row] for row in values]})
    figure={'bounds':BOUNDS,'sources':c['sources'],'n_all':124,'n_known':98,'mean_kw':c['moran']['mean_kw'],
        'known_points':[{'xy':xy[i].tolist(),'kw':reference[key]['kw'],'lag_kw':reference[key]['lag_kw'],'index':i} for i,key in enumerate(ids)],
        'examples':examples,'neighbors':{name:[int(j) for j in w.neighbors[example['index']]] for name,example in examples.items()},
        'moran':c['moran'],'permutation':c['permutation_example'],'grid':c['grid'],'kernels':kernels,
        'all_points':[[f.GetGeometryRef().GetX(),f.GetGeometryRef().GetY()] for f in all_points]}
    dump(OUT/'figure-input.json',figure)
    print(json.dumps({k:c[k] for k in ['point_examples','moran','qgis_nominal_counts','centres','dispersion','kernels']},ensure_ascii=False,indent=2),flush=True)
    print('Grid examples:',c['grid']['largest_count']['n'],c['grid']['largest_count']['known_kw'],c['grid']['largest_known_kw']['n'],c['grid']['largest_known_kw']['known_kw'])

def renda_labels():
    """Derive labelled presentation copies only; retain the previous inference."""
    global _APP
    from qgis.core import (QgsApplication,QgsVectorLayer,QgsVectorFileWriter,QgsProject,
        QgsPalLayerSettings,QgsTextFormat,QgsTextBufferSettings,QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QColor
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen');_APP=QgsApplication([],False);_APP.initQgis()
    parent=ROOT/'tmp/dades-docents/qgis/autocorrelacio-20261005'
    source=parent/'autocorrelacio.gpkg';source_sha=sha(source);target=OUT/'renda.gpkg'
    assert not target.exists()
    ro=QgsVectorLayer.LayerOptions();ro.forceReadOnly=True
    mapping={'4314807013':'Tarragona 07013','4314808012':'Tarragona 08012','4304701002':'Constantí 01002'}
    project=QgsProject.instance()
    for old,name in [('seccions','renda'),('renda_lisa','renda_lisa'),('renda_gi','renda_gi'),('renda_veins','renda_veins')]:
        layer=QgsVectorLayer(str(source)+'|layername='+old,old,'ogr',ro);assert layer.isValid()
        opts=QgsVectorFileWriter.SaveVectorOptions();opts.driverName='GPKG';opts.layerName=name
        opts.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteLayer if target.exists() else QgsVectorFileWriter.CreateOrOverwriteFile
        assert QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(target),project.transformContext(),opts)[0]==QgsVectorFileWriter.NoError
        copy=QgsVectorLayer(str(target)+'|layername='+name,name,'ogr');assert copy.isValid()
        copy.setRenderer(layer.renderer().clone());copy.startEditing()
        field='etiqueta' if name=='renda_veins' else 'cas'
        for f in copy.getFeatures():
            text=f'{int(f["renda"]):,} €/persona'.replace(',','.') if field=='etiqueta' else mapping.get(f['cusec'],'')
            copy.changeAttributeValue(f.id(),copy.fields().indexFromName(field),text)
        assert copy.commitChanges()
        pal=QgsPalLayerSettings();pal.fieldName=field;fmt=QgsTextFormat();fmt.setSize(11);fmt.setColor(QColor('#193c50'))
        buf=QgsTextBufferSettings();buf.setEnabled(True);buf.setSize(.9);buf.setColor(QColor('white'));fmt.setBuffer(buf);pal.setFormat(fmt)
        copy.setLabeling(QgsVectorLayerSimpleLabeling(pal));copy.setLabelsEnabled(True)
        copy.saveStyleToDatabase('docent','Valors i identificadors de secció, sense lletres de cas',True,'')
        if name=='renda':
            opts=QgsVectorFileWriter.SaveVectorOptions();opts.driverName='ESRI Shapefile';opts.fileEncoding='UTF-8'
            assert QgsVectorFileWriter.writeAsVectorFormatV3(copy,str(OUT/'renda.shp'),project.transformContext(),opts)[0]==QgsVectorFileWriter.NoError
            copy.saveNamedStyle(str(OUT/'renda.qml'))
    assert sha(source)==source_sha
    dump(OUT/'renda-presentacio.json',{'source':str(source.relative_to(ROOT)),'sha256':source_sha,'labels':mapping,'inference_reused':True})

def presentation():
    """Polish consumer-owned labels/styles; no statistical values are recalculated."""
    global _APP
    from qgis.core import (QgsApplication,QgsVectorLayer,QgsVectorFileWriter,QgsProject,QgsMarkerSymbol,
        QgsSingleSymbolRenderer,QgsColorRampLegendNodeSettings,QgsRasterLayer)
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen');_APP=QgsApplication([],False);_APP.initQgis()
    project=QgsProject.instance();target=OUT/'constanti.gpkg'
    original=QgsVectorLayer(str(target)+'|layername=centres','Centre','ogr')
    original.setSubsetString('"nom" = \'Centre dels registres\'');assert original.featureCount()==1
    opts=QgsVectorFileWriter.SaveVectorOptions();opts.driverName='GPKG';opts.layerName='centre_registres';opts.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteLayer
    assert QgsVectorFileWriter.writeAsVectorFormatV3(original,str(target),project.transformContext(),opts)[0]==QgsVectorFileWriter.NoError
    centre=QgsVectorLayer(str(target)+'|layername=centre_registres','Centre dels registres','ogr');assert centre.featureCount()==1
    centre.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple({'name':'diamond','color':'#b42b43','size':'5.5','outline_color':'white','outline_width':'.4'})))
    centre.setLabeling(original.labeling().clone());centre.setLabelsEnabled(True);centre.saveStyleToDatabase('docent','Centre sense ponderació',True,'')
    layer=QgsVectorLayer(str(OUT/'renda.gpkg')+'|layername=renda_veins','Renda','ogr')
    renderer=layer.renderer()
    for i,category in enumerate(renderer.categories()):
        renderer.updateCategoryLabel(i,'Tarragona 07013' if category.value()=='A' else 'Tres seccions veïnes')
    layer.saveStyleToDatabase('docent','Contactes amb noms i valors',True,'')
    for radius in [500,1500]:
        layer=QgsRasterLayer(str(OUT/f'densitat-{radius}.tif'),'Densitat');layer.loadNamedStyle(str(OUT/f'densitat-{radius}.qml'))
        settings=QgsColorRampLegendNodeSettings();settings.setMinimumLabel('0 registres/km²');settings.setMaximumLabel('124 registres/km²')
        layer.renderer().shader().rasterShaderFunction().setLegendSettings(settings)
        layer.saveNamedStyle(str(OUT/f'densitat-{radius}.qml'))

def finalise():
    for name in ['constanti.gpkg','renda.gpkg']:
        with sqlite3.connect(OUT/name) as db:
            db.execute('PRAGMA wal_checkpoint(TRUNCATE)');db.execute('PRAGMA journal_mode=DELETE')
            assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not any(p.name.endswith(('-wal','-shm')) for p in OUT.iterdir())

def verify(directory,report):
    """Portable projects and independent geometry/statistic checks, read-only."""
    global _APP
    import numpy as np
    from osgeo import ogr,gdal
    from qgis.core import QgsApplication,QgsProject
    from libpysal.weights import KNN,Queen
    from esda import Moran
    directory=Path(directory).resolve();ogr.UseExceptions()
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen');_APP=QgsApplication([],False);_APP.initQgis()
    hashes={p.name:sha(p) for p in directory.iterdir() if p.suffix in ['.gpkg','.tif','.qml','.shp','.shx','.dbf','.prj','.cpg','.qgz']}
    c=json.loads((directory/'controls.json').read_text());project=QgsProject.instance();projects=[]
    for name in c['projects']:
        assert project.read(str(directory/(name+'.qgz')))
        layers=list(project.mapLayers().values());assert layers and all(layer.isValid() for layer in layers)
        assert all(Path(layer.source().split('|')[0]).resolve().is_relative_to(directory) for layer in layers)
        projects.append({'project':name,'layers':len(layers),'valid':True});project.clear()
    ds=ogr.Open(str(directory/'constanti.gpkg'),0)
    layer=ds.GetLayerByName('punts');assert layer.GetFeatureCount()==124
    xy=np.array([[f.GetGeometryRef().GetX(),f.GetGeometryRef().GetY()] for f in layer]);centre=xy.mean(axis=0)
    cov=np.cov(xy,rowvar=False,ddof=0)
    assert np.allclose(centre,c['centres']['all'],atol=1e-8)
    assert np.isclose(np.sqrt(np.trace(cov)),c['dispersion']['D_m'],atol=1e-8)
    for name in ['cercle','ellipse']:
        f=ds.GetLayerByName(name).GetNextFeature();vertices=np.array(json.loads(f.GetGeometryRef().ExportToJson())['coordinates'][0])[:-1,:2]
        if name=='cercle':assert np.allclose(np.linalg.norm(vertices-centre,axis=1),c['dispersion']['D_m'],atol=1e-5)
        else:assert np.allclose(2*np.cov(vertices,rowvar=False,ddof=0),cov,atol=.01)
    known=list(ds.GetLayerByName('coneguda'));assert len(known)==98
    coords=np.array([[f.GetGeometryRef().GetX(),f.GetGeometryRef().GetY()] for f in known]);y=np.array([f['POT_KW'] for f in known],float)
    w=KNN.from_array(coords,k=8);w.transform='r';mat,_=w.full();z=y-y.mean()
    assert np.isclose(z@mat@z/(z@z),c['moran']['I'],atol=1e-12)
    assert sum(f['n_punts'] for f in ds.GetLayerByName('recompte'))==124
    assert sum(f['kw_pub'] for f in ds.GetLayerByName('recompte'))==2770
    for row in c['kernels']:
        raster=gdal.Open(str(directory/row['file']));band=raster.GetRasterBand(1);values=band.ReadAsArray();valid=values!=band.GetNoDataValue()
        assert np.isclose(values[valid].sum(dtype='float64')*.01,row['mass'],atol=1e-6)
    renda=ogr.Open(str(directory/'renda.gpkg'),0)
    assert [renda.GetLayerByName(name).GetFeatureCount() for name in ['renda','renda_lisa','renda_gi','renda_veins']]==[151,151,151,4]
    shape=ogr.Open(str(directory/'renda.shp'),0);values=np.array([f['renda'] for f in shape.GetLayer(0)])
    weights=Queen.from_shapefile(str(directory/'renda.shp'))
    assert len(values)==weights.n==151 and not weights.islands
    assert np.isclose(Moran(values,weights,permutations=0).I,.57191693318354,atol=1e-12)
    assert all(sha(directory/name)==digest for name,digest in hashes.items())
    result={'ok':True,'offline':True,'readonly':True,'path':str(directory),'projects':projects,'hashes':hashes,
        'matrix_moran_verified':True,'dispersion_geometry_verified':True,'grid_totals_verified':True,'kernel_masses_verified':True,'renda_verified':True}
    dump(report,result);print(json.dumps({k:v for k,v in result.items() if k!='hashes'},ensure_ascii=False,indent=2),flush=True)

def docs():
    shots=['c4-'+name for name in ['constanti-dades','recompte-caixa','recompte-parametres','recompte-resultat','centres-menu','centres-caixa',
        'centre-parametres','centres-resultat','cercle-ellipse','kernel-caixa','kernel-parametres','kernel-resultat']]
    shots+=['c5-'+name for name in ['punts-dades','punts-veins','punts-eines','punts-parametres','punts-resultat','renda-resultat','renda-veins']]
    for name in ['captures','reproduccio']:(OUT/name).mkdir(exist_ok=True)
    for stem in shots:
        receipt=ROOT/'context/qgis/manifests'/f'{stem}.yml';meta=json.loads(receipt.read_text())
        assert meta['ok'] and not meta['warnings'] and meta['image_digest']==IMAGE and meta['device_pixel_ratio']==1 and meta['backend']=='x11'
        for suffix in ['.png','.annotations.svg']:shutil.copyfile(ROOT/'assets/captures'/(stem+suffix),OUT/'captures'/(stem+suffix))
        shutil.copyfile(receipt,OUT/'captures'/receipt.name)
    for source in [Path(__file__),ROOT/'context/qgis/constanti-pedagogia.yml',ROOT/'context/qgis/constanti-pedagogia.md',
        ROOT/'context/qgis/autocorrelacio-exemples.yml',ROOT/'context/qgis/autocorrelacio-exemples.md']:
        shutil.copyfile(source,OUT/'reproduccio'/source.name)
    for filename,target in [('constanti-pedagogia.md','GUIA.md'),('constanti-pedagogia-docent.md','SOLUCIONS.md')]:
        shutil.copyfile(ROOT/'context/practiques'/filename,OUT/target)
    image='ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:9e0b3a45753c170b795e9a9d6df61580085c113436beac5bf6c8de69b6562097'
    for name in ['GUIA','SOLUCIONS']:
        cmd=['docker','run','--rm','--pull=never','--network','none','--user',f'{os.getuid()}:{os.getgid()}',
            '--env','HOME=/tmp','--env','SOURCE_DATE_EPOCH=0','--mount',f'type=bind,src={OUT},dst=/data','--workdir','/data','--entrypoint','pandoc',image,
            name+'.md','-o',name+'.pdf','--pdf-engine=xelatex','-V','fontfamily=fontspec','-V','mainfont=DejaVu Sans','-V','monofont=DejaVu Sans Mono','-V','fontsize=11pt','-V','geometry=a4paper,margin=18mm']
        if name=='GUIA':cmd+=['--toc','--toc-depth=2']
        subprocess.run(cmd,check=True)

def package():
    portable=json.loads((OUT/'portabilitat.json').read_text());assert portable['ok']
    assert all(sha(OUT/name)==digest for name,digest in portable['hashes'].items())
    pdfs=json.loads((OUT/'verificacio-pdf.json').read_text())
    for name in ['GUIA','SOLUCIONS']:
        assert not pdfs[name]['overflow'] and sha(OUT/(name+'.pdf'))==pdfs[name]['sha256']
        assert sha(OUT/(name+'.md'))==pdfs[name]['source_sha256']
        assert pdfs[name]['complete_body_headings']>0
    shutil.copyfile(Path(__file__),OUT/'reproduccio'/Path(__file__).name)
    files=[{'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='sealed.json']
    assert all(not p.is_symlink() and not p.name.endswith(('-wal','-shm')) for p in OUT.rglob('*'))
    dump(OUT/'sealed.json',{'files':files,'image':IMAGE,'human_approved':False,'status':'private-author-review'})
    target=OUT.parent.parent/'practica-constanti-pedagogia-20261005.zip';temporary=target.with_suffix('.zip.partial')
    assert not target.exists() and not temporary.exists()
    with zipfile.ZipFile(temporary,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for path in sorted(OUT.rglob('*')):
            if path.is_file():archive.write(path,'constanti/'+str(path.relative_to(OUT)))
    with zipfile.ZipFile(temporary) as archive:
        assert archive.testzip() is None
        assert all(hashlib.sha256(archive.read('constanti/'+f['path'])).hexdigest()==f['sha256'] for f in files)
    temporary.rename(target)
    receipt={'path':str(target.relative_to(ROOT)),'sha256':sha(target),'bytes':target.stat().st_size,'files':len(files)+1,'status':'private-author-review'}
    dump(target.with_suffix('.receipt.json'),receipt);print(json.dumps(receipt,indent=2),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--build',action='store_true');parser.add_argument('--record',action='store_true');parser.add_argument('--finish',action='store_true');parser.add_argument('--renda-labels',action='store_true');parser.add_argument('--presentation',action='store_true')
    parser.add_argument('--finalise',action='store_true');parser.add_argument('--verify');parser.add_argument('--report')
    parser.add_argument('--docs',action='store_true');parser.add_argument('--package',action='store_true')
    args=parser.parse_args()
    if (OUT/'sealed.json').exists() and any((args.build,args.finish,args.renda_labels,args.presentation,args.finalise,args.docs,args.package)):
        raise SystemExit('Paquet segellat: utilitza una destinació nova per a qualsevol modificació.')
    if args.build:build()
    if args.finish:finish()
    if args.renda_labels:renda_labels()
    if args.presentation:presentation()
    if args.finalise:finalise()
    if args.verify:
        assert args.report;verify(args.verify,args.report)
    if args.docs:docs()
    if args.package:package()
    if args.record:record()
