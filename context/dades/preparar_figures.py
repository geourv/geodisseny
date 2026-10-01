"""Retain project-specific figure resources and exact optional QGIS plugins."""
import argparse
import configparser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[2]


def sha(data):return hashlib.sha256(data).hexdigest()


def ortho():
    private=ROOT/'tmp/dades-docents/practiques'
    manifest=json.loads((private/'manifest.json').read_text())
    record=manifest['orto-pineda-2025.png']
    data=(private/'orto-pineda-2025.png').read_bytes()
    assert sha(data)==record['sha256']
    output=ROOT/'context/inputs/ortofoto-pineda-2025.png'
    if output.exists():assert output.read_bytes()==data
    else:output.write_bytes(data)
    metadata={**record,'producer':'Institut Cartogràfic i Geològic de Catalunya',
              'layer':'ortofoto_25cm_color_2025','crs':'EPSG:25831',
              'input_path':str(output.relative_to(ROOT))}
    (ROOT/'context/inputs/ortofoto-pineda-2025.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    print('Retained orthophoto',record['sha256'],record['bbox'])


def plugins(directory,replace_unlocked=False):
    directory=Path(directory).resolve()
    assert directory.is_relative_to(ROOT/'tmp/qgis/cache/plugins')
    assert directory.is_dir(), 'Prepare the confined plugin-cache parent first'
    definitions=[
        ('HotSpotAnalysis_v3','4.0.0','https://codeload.github.com/geografiadascoisas/HotSpotAnalysis_Plugin/zip/f00561970149787664fc2cabe26a110cc2d4226a'),
        ('processing_saga_nextgen','1.3.0',
         'https://codeload.github.com/baswein/qgis-processing-saga-nextgen/zip/e358ef0eb027f95afc64729b61451c8015abe8b0')]
    lock_path=ROOT/'context/qgis/plugins-lock.json'
    prior=json.loads(lock_path.read_text()) if lock_path.exists() else {'plugins':{}}
    if replace_unlocked:
        # Only adopt a newly downloader-created cache, never replace the cache
        # already named by our exact source lock. Preserve the downloaded trees.
        assert str(directory.relative_to(ROOT))!=prior.get('cache')
        assert (directory/'.downloads').is_dir()
        for key,_,_ in definitions:
            target=directory/key
            if target.exists():
                metadata=sha((target/'metadata.txt').read_bytes())[:12]
                backup=directory/'.original-downloads'/f'{key}-{metadata}'
                assert not backup.exists(),backup
                backup.parent.mkdir(exist_ok=True)
                target.rename(backup)
    records={}
    for key,version,url in definitions:
        with urllib.request.urlopen(url,timeout=90) as response:data=response.read(20_000_001)
        assert len(data)<=20_000_000
        if key in prior['plugins']:assert sha(data)==prior['plugins'][key]['archive_sha256'],key
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            roots=[PurePosixPath(n).parent for n in archive.namelist() if n.endswith('/metadata.txt')]
            assert len(roots)==1,(key,roots)
            prefix=roots[0];files={}
            for entry in archive.infolist():
                path=PurePosixPath(entry.filename)
                assert not path.is_absolute() and '..' not in path.parts
                assert not stat.S_ISLNK(entry.external_attr>>16)
                if entry.is_dir() or not path.is_relative_to(prefix):continue
                relative=path.relative_to(prefix)
                content=archive.read(entry);target=directory/key/relative
                assert target.resolve().is_relative_to(directory)
                if target.exists():assert target.read_bytes()==content,target
                else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
                files[str(relative)]=sha(content)
            config=configparser.ConfigParser();config.read(directory/key/'metadata.txt')
            assert config['general']['version']==version
            records[key]={'version':version,'url':url,'archive_sha256':sha(data),'files':files,
                          'qgis_min':config['general'].get('qgisMinimumVersion'),
                          'qgis_max':config['general'].get('qgisMaximumVersion')}
        print('Pinned plugin',key,version,sha(data),flush=True)
    lock={'runtime':'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc',
          'cache':str(directory.relative_to(ROOT)),'plugins':records}
    lock_path.write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n')


def qgis_inputs():
    import os,sys,shutil
    import numpy as np
    from osgeo import gdal,ogr
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
    from qgis.core import (QgsApplication,QgsVectorLayer,QgsRasterLayer,QgsProject,QgsCoordinateReferenceSystem,
                           QgsProcessingContext,QgsVectorFileWriter,QgsMarkerSymbol,QgsFillSymbol,
                           QgsRendererCategory,QgsCategorizedSymbolRenderer,QgsField)
    from qgis.PyQt.QtCore import QVariant
    app=QgsApplication([],False);app.initQgis()
    lock=json.loads((ROOT/'context/qgis/plugins-lock.json').read_text())
    sys.path[:0]=['/usr/share/qgis/python/plugins',str(ROOT/lock['cache'])]
    from processing.core.Processing import Processing
    Processing.initialize()
    from HotSpotAnalysis_v3.processing.provider import HotspotProvider
    provider=HotspotProvider();QgsApplication.processingRegistry().addProvider(provider)
    import processing
    folder=ROOT/'tmp/dades-docents/qgis'
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    context=QgsProcessingContext();context.setProject(project)
    ro=QgsVectorLayer.LayerOptions();ro.forceReadOnly=True
    def save(layer,name):
        path=folder/(name+'.gpkg')
        if path.exists():return QgsVectorLayer(str(path),name,'ogr',ro)
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='GPKG';options.layerName=name
        result=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(path),project.transformContext(),options)
        assert result[0]==QgsVectorFileWriter.NoError,result
        return QgsVectorLayer(str(path),name,'ogr')
    points=QgsVectorLayer(str(folder/'icaen-punts-simples.gpkg'),'ICAEN punts','ogr',ro)
    mean=processing.run('native:meancoordinates',{'INPUT':points,'OUTPUT':'memory:'},context=context)['OUTPUT']
    save(mean,'icaen-centre-mitja')
    temperatures=ROOT/'tmp/dades-docents/temperatures-20260930'
    for original,name in [('estacions.gpkg','tmax-estacions.gpkg'),('idw-catalunya.tif','tmax-idw.tif'),
                           ('kriging-ajustat-catalunya.tif','tmax-kriging.tif')]:
        target=folder/name
        if target.exists() and original=='kriging-ajustat-catalunya.tif' and target.read_bytes()!=(temperatures/original).read_bytes():
            assert target.read_bytes()==(temperatures/'kriging-lineal-catalunya.tif').read_bytes()
            shutil.copyfile(temperatures/original,target)
        if not target.exists():shutil.copyfile(temperatures/original,target)
    # Bounded inland example: full elevation coverage avoids introducing unknown
    # marine/terrestrial gaps into the first GUI viewshed calculation.
    gdal.UseExceptions();ogr.UseExceptions()
    bounds=[347000,4555500,355000,4565500]
    terrain=folder/'mdt-visibilitat.tif'
    if not terrain.exists():
        ds=gdal.Translate(str(terrain),str(ROOT/'tmp/dades-docents/practiques/mdt-regional-25m.tif'),
                          projWin=[bounds[0],bounds[3],bounds[2],bounds[1]],creationOptions=['COMPRESS=DEFLATE'])
        assert (ds.ReadAsArray()!=-9999).all();ds=None
    raster=QgsRasterLayer(str(terrain),'MDT 25 m');assert raster.isValid()
    observer='350900.88274222304,4560059.918881127 [EPSG:25831]'
    output=folder/'conca-centre.tif'
    if not output.exists():
        processing.run('gdal:viewshed',{'INPUT':raster,'BAND':1,'OBSERVER':observer,'OBSERVER_HEIGHT':30,
            'TARGET_HEIGHT':1.7,'MAX_DISTANCE':0,'EXTRA':'-vv 1 -iv 0 -ov 255 -a_nodata 255 -cc 0.85714',
            'OUTPUT':str(output)},context=context)
    receptors=folder/'receptors-visibilitat.gpkg'
    if not receptors.exists():
        source=ogr.Open(str(ROOT/'tmp/dades-docents/originals/icgc-20260120/divisions-administratives-v2r2-20260120.gpkg'))
        caps=source.GetLayerByName('_10_caps-municipi');caps.SetSpatialFilterRect(*bounds)
        ds=ogr.GetDriverByName('GPKG').CreateDataSource(str(receptors));layer=ds.CopyLayer(caps,'receptors')
        assert layer.GetFeatureCount()>=3;ds=None
    receptors_layer=QgsVectorLayer(str(receptors),'Receptors municipals','ogr',ro)
    sampled=processing.run('native:rastersampling',{'INPUT':receptors_layer,'RASTERCOPY':str(output),
                           'COLUMN_PREFIX':'centre_','OUTPUT':'memory:'},context=context)['OUTPUT']
    save(sampled,'receptors-mostreig')
    print('VISIBILITY',[(f['NOMCAP'],f['centre_1']) for f in sampled.getFeatures()],flush=True)
    # QGIS LISA on the same one-variable census-section indicator as the book.
    sections=QgsVectorLayer(str(ROOT/'tmp/dades-docents/seccions/seccions-analisi.gpkg'),'Seccions','ogr',ro)
    selected=processing.run('native:extractbyexpression',{'INPUT':sections,'EXPRESSION':'"moran_sample"=1','OUTPUT':'memory:'},context=context)['OUTPUT']
    selected=processing.run('native:fieldcalculator',{'INPUT':selected,'FIELD_NAME':'log_pot','FIELD_TYPE':0,
        'FIELD_LENGTH':20,'FIELD_PRECISION':8,'FORMULA':'ln(1+"kw_per_100_buildings")','OUTPUT':'memory:'},context=context)['OUTPUT']
    assert selected.featureCount()==150
    save(selected,'seccions-moran')
    shape=folder/'seccions-moran.shp'
    if not shape.exists():
        reduced=processing.run('native:retainfields',{'INPUT':selected,'FIELDS':['cusec','log_pot'],'OUTPUT':'memory:'},context=context)['OUTPUT']
        options=QgsVectorFileWriter.SaveVectorOptions();options.driverName='ESRI Shapefile';options.fileEncoding='UTF-8'
        status=QgsVectorFileWriter.writeAsVectorFormatV3(reduced,str(shape),project.transformContext(),options)
        assert status[0]==QgsVectorFileWriter.NoError,status
    selected=QgsVectorLayer(str(shape),'Seccions Moran','ogr',ro)
    if not (folder/'seccions-lisa.gpkg').exists():
        np.random.seed(20260930)
        result=processing.run('hotspotanalysis:moranlocal',{'INPUT':selected,'FIELD':'log_pot','WEIGHTS_TYPE':2,
            'OPTIMIZE':False,'BINARY_WEIGHTS':True,'ROW_STANDARDIZE':True,'DISTANCE_METRIC':0,
            'PERMUTATIONS':9999,'TWO_TAILED':False,'OUTPUT':'memory:'},context=context)['OUTPUT']
        if isinstance(result,str):result=context.getMapLayer(result)
        result.startEditing();result.addAttribute(QgsField('classe',QVariant.String));result.updateFields()
        labels={1:'Alt–alt',2:'Baix–alt',3:'Baix–baix',4:'Alt–baix'}
        for f in result.getFeatures():
            result.changeAttributeValue(f.id(),result.fields().indexFromName('classe'),
                labels[int(f['q_value'])] if f['p_value']<.05 else 'No destacat')
        assert result.commitChanges()
        out=save(result,'seccions-lisa')
        colors={'Alt–alt':'#b42b3b','Baix–baix':'#236b9b','Alt–baix':'#eba798','Baix–alt':'#add6ec','No destacat':'#d8dde1'}
        out.setRenderer(QgsCategorizedSymbolRenderer('classe',[QgsRendererCategory(k,QgsFillSymbol.createSimple(
            {'color':v,'outline_color':'#697680','outline_width':'.12'}),k) for k,v in colors.items()]))
        out.saveStyleToDatabase('Moran local','p < 0.05, sense correcció múltiple',True,'')
        print('LISA',out.featureCount(),flush=True)
    if not (folder/'seccions-gi.gpkg').exists():
        parameters={'INPUT':selected,'FIELD':'log_pot','WEIGHTS_TYPE':2,'OPTIMIZE':False,
                    'BINARY_WEIGHTS':True,'ROW_STANDARDIZE':False,'DISTANCE_METRIC':0,
                    'PERMUTATIONS':9999,'TWO_TAILED':True,'OUTPUT':'memory:'}
        result=processing.run('hotspotanalysis:getisordgistar',parameters,context=context)['OUTPUT']
        if isinstance(result,str):result=context.getMapLayer(result)
        result.startEditing();result.addAttribute(QgsField('classe',QVariant.String));result.updateFields()
        from collections import Counter
        counts=Counter()
        for f in result.getFeatures():
            assert np.isfinite(f['Z_score']) and 0<=f['p_value']<=1
            label=('Concentració alta' if f['Z_score']>0 else 'Concentració baixa') if f['p_value']<.05 else 'No destacat'
            counts[label]+=1
            result.changeAttributeValue(f.id(),result.fields().indexFromName('classe'),label)
        assert result.commitChanges()
        out=save(result,'seccions-gi')
        colors={'Concentració alta':'#b42b3b','Concentració baixa':'#236b9b','No destacat':'#d8dde1'}
        out.setRenderer(QgsCategorizedSymbolRenderer('classe',[QgsRendererCategory(k,QgsFillSymbol.createSimple(
            {'color':v,'outline_color':'#697680','outline_width':'.12'}),k) for k,v in colors.items()]))
        out.saveStyleToDatabase('Gi estrella','p bilateral < 0.05, sense correcció múltiple',True,'')
        (ROOT/'tmp/dades-docents/estadistica-20260930/gi-controls.json').write_text(json.dumps(
            {'n':out.featureCount(),'counts':dict(counts),'parameters':{k:v for k,v in parameters.items() if k!='INPUT'}},ensure_ascii=False,indent=2)+'\n')
        print('GI',out.featureCount(),dict(counts),flush=True)
    # Compact, inspected attributes for the geometry-expression dialog. These
    # are the covariance summaries, not fitted confidence limits.
    summary=json.loads((ROOT/'tmp/dades-docents/estadistica-20260930/controls.json').read_text())
    centre=processing.run('native:meancoordinates',{'INPUT':points,'OUTPUT':'memory:'},context=context)['OUTPUT']
    for name,value in [('D_m',summary['standard_distance_m']),('a_m',summary['ellipse_semiaxes_m'][0]),
                       ('b_m',summary['ellipse_semiaxes_m'][1]),('azimut',90-summary['angle_from_east_deg'])]:
        centre=processing.run('native:fieldcalculator',{'INPUT':centre,'FIELD_NAME':name,'FIELD_TYPE':0,
            'FIELD_LENGTH':20,'FIELD_PRECISION':8,'FORMULA':str(value),'OUTPUT':'memory:'},context=context)['OUTPUT']
    save(centre,'icaen-parametres-dispersio')
    from qgis.core import (QgsRasterShader,QgsColorRampShader,QgsSingleBandPseudoColorRenderer,
                           QgsGraduatedSymbolRenderer,QgsRendererRange,QgsPalLayerSettings,
                           QgsTextFormat,QgsTextBufferSettings,QgsVectorLayerSimpleLabeling)
    from qgis.PyQt.QtGui import QColor
    def raster_style(path,items,exact=False):
        layer=QgsRasterLayer(str(path),path.stem);assert layer.isValid()
        function=QgsColorRampShader();function.setColorRampType(QgsColorRampShader.Exact if exact else QgsColorRampShader.Interpolated)
        function.setColorRampItemList([QgsColorRampShader.ColorRampItem(value,QColor(color),label) for value,color,label in items])
        function.setMinimumValue(items[0][0]);function.setMaximumValue(items[-1][0])
        shader=QgsRasterShader();shader.setRasterShaderFunction(function)
        renderer=QgsSingleBandPseudoColorRenderer(layer.dataProvider(),1,shader)
        renderer.setClassificationMin(items[0][0]);renderer.setClassificationMax(items[-1][0])
        layer.setRenderer(renderer);message,ok=layer.saveNamedStyle(str(path.with_suffix('.qml')));assert ok,message
    temperature_items=[(15,'#440154','15 °C'),(22.5,'#3b528b','22,5'),(30,'#21918c','30'),(37.5,'#5ec962','37,5'),(45,'#fde725','45 °C')]
    for name in ['tmax-idw','tmax-kriging']:raster_style(folder/(name+'.tif'),temperature_items)
    raster_style(folder/'conca-centre.tif',[(0,'#f3ede1','0 · Ocult'),(1,'#39734d','1 · Visible')],True)
    for radius in [500,1500]:
        path=folder/f'icaen-densitat-{radius}.tif'
        if not path.exists():
            source=gdal.Open(str(folder/f'icaen-kernel-{radius}.tif'));a=source.ReadAsArray()
            a=np.where(a==source.GetRasterBand(1).GetNoDataValue(),0,a)*3e6/(np.pi*radius**2)
            out=gdal.GetDriverByName('GTiff').CreateCopy(str(path),source,options=['COMPRESS=DEFLATE'])
            out.GetRasterBand(1).WriteArray(a);out.GetRasterBand(1).SetNoDataValue(-9999);out=None
        raster_style(path,[(0,'#ffffcc','0 punts/km²'),(25,'#fed976','25'),(75,'#fd8d3c','75'),(150,'#e31a1c','150'),(320,'#800026','320')])
    grid=QgsVectorLayer(str(folder/'icaen-recompte.gpkg'),'Recompte','ogr')
    breaks=[-.5,.5,9.5,24.5,49.5,99.5,1000]
    colors=['#ffffe5','#fff7bc','#fee391','#fec44f','#fe9929','#cc4c02']
    labels=['0','1–9','10–24','25–49','50–99','100 o més']
    grid.setRenderer(QgsGraduatedSymbolRenderer('n_punts',[QgsRendererRange(lo,hi,QgsFillSymbol.createSimple(
        {'color':color,'outline_color':'white','outline_width':'.08'}),label) for lo,hi,color,label in zip(breaks,breaks[1:],colors,labels)]))
    grid.saveStyleToDatabase('Recompte','Punts per quadrat d’un km²',True,'')
    sampled=QgsVectorLayer(str(folder/'receptors-mostreig.gpkg'),'Mostreig','ogr')
    sampled.setRenderer(QgsCategorizedSymbolRenderer('centre_1',[QgsRendererCategory(value,QgsMarkerSymbol.createSimple(
        {'name':'circle','size':'2.6','color':color,'outline_color':'white','outline_width':'.4'}),label)
        for value,color,label in [(0,'#9e512f','Ocult'),(1,'#006699','Visible')]]))
    settings=QgsPalLayerSettings();settings.fieldName='NOMCAP'
    text=QgsTextFormat();text.setSize(9);buffer=QgsTextBufferSettings();buffer.setEnabled(True);buffer.setSize(1)
    text.setBuffer(buffer);settings.setFormat(text)
    sampled.setLabeling(QgsVectorLayerSimpleLabeling(settings));sampled.setLabelsEnabled(True)
    sampled.saveStyleToDatabase('Receptors','Valor centre_1 de la conca visual',True,'')


def package():
    """Create a new private teaching archive with standalone SQLite snapshots."""
    import shutil,sqlite3
    private=ROOT/'tmp/dades-docents'
    destination=private/'demos-ampliacio-20260930.zip'
    stage=private/'lliurament-ampliacio-20260930'
    assert not destination.exists() and not stage.exists(), 'Existing delivery retained; choose a new name'
    sources=[]
    def collect(folder,prefix,patterns):
        for pattern in patterns:
            for path in sorted(folder.glob(pattern)):
                if path.is_file() and not path.is_symlink():sources.append((path,Path(prefix)/path.name))
    collect(private/'qgis','qgis',['*.gpkg','*.shp','*.shx','*.dbf','*.prj','*.cpg','*.tif','*.qml'])
    collect(private/'practiques/models-20260930','models-28-mostres',['*.gpkg','*.tif','controls.json'])
    collect(private/'practiques','fonts-territorials',['ambits.gpkg','mdt-regional-25m.tif','mds-regional-25m.tif','manifest.json'])
    collect(private/'temperatures-20260930','temperatures',[
        'estacions.gpkg','dades.json','fonts.json','idw.tif','idw-catalunya.tif',
        'kriging-ajustat*','variancia-ajustada*','saga-ajustat-log.txt','variograma.dbf'])
    collect(private/'temperatures-20260930/originals','temperatures/originals',['*.json'])
    collect(private/'estadistica-20260930','controls',['*.json','*.txt','*.md','*.html'])
    collect(ROOT/'context/inputs','columbus',['columbus.geojson','columbus-resultats.json'])
    collect(ROOT/'context/dades','reproduccio',['preparar_estadistica.py','preparar_temperatures.py','preparar_figures.py','preparar_practiques.py'])
    sources.append((ROOT/'context/qgis/plugins-lock.json',Path('reproduccio/plugins-lock.json')))
    assert len({str(relative) for _,relative in sources})==len(sources)
    stage.mkdir();records=[]
    for source,relative in sources:
        target=stage/relative;target.parent.mkdir(parents=True,exist_ok=True)
        before=sha(source.read_bytes())
        if source.suffix=='.gpkg':
            connection=sqlite3.connect(f'file:{source}?mode=ro',uri=True)
            output=sqlite3.connect(target)
            connection.backup(output);connection.close()
            output.execute('PRAGMA journal_mode=DELETE')
            assert output.execute('PRAGMA integrity_check').fetchone()[0]=='ok',source
            output.close()
        else:shutil.copyfile(source,target)
        assert sha(source.read_bytes())==before,source
        records.append({'path':str(relative),'source':str(source.relative_to(ROOT)),
                        'source_sha256':before,'sha256':sha(target.read_bytes()),'bytes':target.stat().st_size})
    readme="""# Ampliació docent — 30 de setembre de 2026

Obriu les dades amb QGIS 3.44.11. Aquest paquet acompanya el manual
d'Anàlisi Espacial i Geodisseny; distribució local per Moodle.

- qgis/: punts ICAEN, centres, cercle/el·lipse, graella, recompte, KDE cru i
  normalitzat; seccions per Moran/Gi*; MDT local, conca visual i receptors;
  temperatures i prediccions amb estils. Shapefile: conservar tots els auxiliars.
- models-28-mostres/: visibilitat regional amb 28 punts a 250 m, altures
  assumides 30/60 m i receptors 1,7/15 m; controls i domini comú.
- fonts-territorials/: límits i MDT/MDS ICGC 2021–2023 reduïts a 25 m.
- temperatures/: observacions Meteocat 15-08-2025, 48 intervals vàlids per
  estació, 182 casos; màxima en TU. IDW p=2 i kriging ordinari lineal
  a+b*x/100000, a=2.79123, b=19.5643, graella de 2000 m. variograma.dbf:
  Class, Distance, Count, Variance, Cum.Var., Covariance, Cum.Covar.
- columbus/: exemple PySAL de 49 barris (Anselin, 1988), coordenades en
  unitats arbitràries; no assignar-hi un CRS mètric inventat.
- controls/: estadístics, expressions i metadades. KDE normalitzat en
  punts/km² = quartic cru × 3e6/(pi*radi^2).

SAGA NextGen 1.3.0 requereix SAGA 9.8.0; Hotspot Analysis v4.0.0 requereix
libpysal 4.13.0 i esda 2.7.1. Fonts exactes a reproduccio/plugins-lock.json.
No cal el complement SDEllipse: el cercle/el·lipse es dibuixa amb expressions
natives i els atributs de icaen-parametres-dispersio.gpkg.

Els mapes GUI de Moran i Gi* no porten correcció múltiple. Moran local:
pseudo-p unilateral nominal <0.05. Gi*: pesos binaris, estrella, pseudo-p
bilateral <0.05; 7 altes, 13 baixes i 130 no destacades. No confondre amb
el mapa BH-FDR del paquet censal anterior. Les prediccions de temperatures
usen totes les estacions: no són una validació fora de mostra.

Fonts: ICAEN (consumidors associats, no petjades de panells), ICGC/Idescat
(límits i elevacions), Cadastre (parcel·les i edificis), Meteocat (XEMA).
Conservar crèdits, dates i condicions originals; les dades Meteocat remeten
a https://www.meteo.cat/wpweb/avis-legal/ i no es reetiqueten CC BY.
Els scripts de reproduccio/ esperen les rutes del repositori geodisseny;
les activitats GUI es fan obrint les dades, sense executar els preparadors.
Per a les extraccions territorials i cadastral/ICAEN completes, conservar
també els dos paquets demos-*-20260929.zip anteriors.

MANIFEST.json verifica cada fitxer. Els GeoPackage del lliurament són
instantànies SQLite autònomes, sense dependència de fitxers WAL.
"""
    (stage/'LLEGEIX-ME.md').write_text(readme)
    records.append({'path':'LLEGEIX-ME.md','sha256':sha(readme.encode()),'bytes':len(readme.encode())})
    (stage/'MANIFEST.json').write_text(json.dumps({'files':records},ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(destination,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for item in sorted(stage.rglob('*')):
            if item.is_file():archive.write(item,item.relative_to(stage))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        for item in records:assert sha(archive.read(item['path']))==item['sha256'],item['path']
    receipt={'path':str(destination.relative_to(ROOT)),'sha256':sha(destination.read_bytes()),
             'bytes':destination.stat().st_size,'files':len(records)+1}
    (private/'demos-ampliacio-20260930.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--ortho',action='store_true')
    parser.add_argument('--plugin-dir')
    parser.add_argument('--replace-unlocked-plugin-cache',action='store_true')
    parser.add_argument('--qgis',action='store_true')
    parser.add_argument('--package',action='store_true')
    args=parser.parse_args()
    if args.ortho:ortho()
    if args.plugin_dir:plugins(args.plugin_dir,args.replace_unlocked_plugin_cache)
    if args.qgis:qgis_inputs()
    if args.package:package()
