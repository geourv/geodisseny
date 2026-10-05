"""Municipal QGIS teaching inputs and explicit interval-imputation scenarios.

--fetch retains the exact ICGC WMS request. --build uses readonly originals in
the pinned QGIS image and a fresh private destination. No PySAL is required.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys
from urllib.parse import urlencode
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'tmp/dades-docents/qgis/punts-municipals-20261004'
SOURCE = ROOT/'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'
ADMIN = ROOT/'tmp/dades-docents/moodle/ambits-tarragona-20260120.gpkg'
IMAGE = 'sha256:950ee7bf7cbab5163849415d4f7fd72dc400b1e81127913ff308244ae4a6ebdc'
BOUNDS = (343500,4554000,353500,4563000)
CODES = [430957,430430,430477]
NAMES = {430957:'El Morell',430430:'El Catllar',430477:'Constantí'}
BANDS = {'Pot <= 5kW':(0,2.5,5),'5 < Pot <= 25 kW':(5,15,25),'25 < Pot <= 100 kW':(25,62.5,100)}
FIELDS = ['w_inf','w_mid','w_sup']
_APP = None


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def dump(path,data):
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def expressions():
    return {field:'CASE WHEN "POT_KW" IS NOT NULL THEN "POT_KW" '+
        ' '.join(f'WHEN "INTERVAL" = \'{label}\' THEN {values[i]}' for label,values in BANDS.items())+
        ' ELSE NULL END' for i,field in enumerate(FIELDS)}


def fetch():
    target=ROOT/'context/inputs/constanti-ortofoto-2025.png'
    manifest=target.with_suffix('.json')
    if target.exists():
        assert manifest.exists() and sha(target)==json.loads(manifest.read_text())['sha256'];return
    params={'SERVICE':'WMS','VERSION':'1.3.0','REQUEST':'GetMap','LAYERS':'ortofoto_25cm_color_2025',
        'STYLES':'','CRS':'EPSG:25831','BBOX':','.join(map(str,BOUNDS)),
        'WIDTH':1250,'HEIGHT':1125,'FORMAT':'image/png'}
    url='https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?'+urlencode(params)
    with urllib.request.urlopen(url,timeout=120) as response:content=response.read(15_000_001)
    assert content.startswith(b'\x89PNG\r\n\x1a\n') and len(content)<15_000_000
    target.write_bytes(content)
    dump(manifest,{'producer':'ICGC','url':url,'edition':2025,'request':params,'bounds':BOUNDS,
        'requested_resolution_m':8,'source_product_resolution_m':.25,'sha256':sha(target),
        'licence_url':'https://www.icgc.cat/condicions','derivation':'WMS GetMap rendered at 8 m/pixel; not a native 25 cm tile.'})
    print('Retained WMS image:',target,sha(target))


def build():
    global _APP
    import numpy as np
    from osgeo import gdal
    from qgis.core import (QgsApplication,QgsProject,QgsCoordinateReferenceSystem,QgsVectorLayer,QgsVectorFileWriter,
        QgsField,QgsFeature,QgsGeometry,QgsPointXY,QgsVariantUtils,QgsMarkerSymbol,QgsFillSymbol,
        QgsCategorizedSymbolRenderer,QgsRendererCategory,QgsRuleBasedRenderer,QgsSymbolLayer,QgsProperty,
        QgsPalLayerSettings,QgsVectorLayerSimpleLabeling,QgsTextFormat,QgsRasterLayer,QgsReferencedRectangle,Qgis)
    from qgis.PyQt.QtCore import QVariant
    from qgis.PyQt.QtGui import QColor
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen');gdal.UseExceptions()
    _APP=QgsApplication([],False);_APP.initQgis();sys.path.insert(0,'/usr/share/qgis/python/plugins')
    from processing.core.Processing import Processing
    Processing.initialize();import processing
    assert sha(SOURCE)=='1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'
    assert sha(ADMIN)=='444411b1418625ca24d03487b9c55a62cad4541c246b882bc11969d7b3c6e124'
    OUT.mkdir(exist_ok=True);assert not (OUT/'municipis.gpkg').exists(),'Fresh output required.'
    project=QgsProject.instance();project.setCrs(QgsCoordinateReferenceSystem('EPSG:25831'));project.setEllipsoid('NONE')
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    ro=QgsVectorLayer.LayerOptions();ro.forceReadOnly=True
    original=QgsVectorLayer(str(SOURCE)+'|layername=autoconsum_tarragones','Original','ogr',ro);assert original.isValid()
    rows_all=list(original.getFeatures())
    opened=[{'municipi':f['MUNICIPI'],'code':f['CODI_MUN'],'interval':f['INTERVAL']}
        for f in rows_all if QgsVariantUtils.isNull(f['POT_KW']) and f['INTERVAL'] not in BANDS]
    assert len(opened)==1 and opened[0]['code']==431536
    operations=[]
    def run(ident,**parameters):
        parameters.setdefault('OUTPUT','memory:')
        algorithm=QgsApplication.processingRegistry().algorithmById(ident)
        assert algorithm and set(parameters)<={p.name() for p in algorithm.parameterDefinitions()}
        operations.append({'id':ident,'parameters':{k:v.name() if isinstance(v,QgsVectorLayer) else str(v) for k,v in parameters.items()}})
        return processing.run(ident,parameters)['OUTPUT']
    def save(layer,name,title=None):
        opts=QgsVectorFileWriter.SaveVectorOptions();opts.driverName='GPKG';opts.layerName=name
        target=OUT/'municipis.gpkg'
        opts.actionOnExistingFile=QgsVectorFileWriter.CreateOrOverwriteLayer if target.exists() else QgsVectorFileWriter.CreateOrOverwriteFile
        result=QgsVectorFileWriter.writeAsVectorFormatV3(layer,str(target),project.transformContext(),opts)
        assert result[0]==QgsVectorFileWriter.NoError,result
        output=QgsVectorLayer(str(target)+'|layername='+name,title or name,'ogr');assert output.isValid()
        project.addMapLayer(output);return output
    selected=run('native:extractbyexpression',INPUT=original,EXPRESSION='"CODI_MUN" IN (430957,430430,430477)')
    base=run('native:multiparttosingleparts',INPUT=selected);assert base.featureCount()==672
    raw=save(base,'punts_base','Registres municipals')
    weighted=base
    for field,formula in expressions().items():
        weighted=run('native:fieldcalculator',INPUT=weighted,FIELD_NAME=field,FIELD_TYPE=0,
                     FIELD_LENGTH=20,FIELD_PRECISION=2,FORMULA=formula)
    weighted=run('native:fieldcalculator',INPUT=weighted,FIELD_NAME='imputat',FIELD_TYPE=1,
                 FIELD_LENGTH=1,FIELD_PRECISION=0,FORMULA='"POT_KW" IS NULL')
    weighted=run('native:fieldcalculator',INPUT=weighted,FIELD_NAME='etiqueta',FIELD_TYPE=2,
                 FIELD_LENGTH=2,FIELD_PRECISION=0,FORMULA='CASE WHEN "CODI_MUN" = 430477 AND "POT_KW" = 450 THEN \'A\' END')
    all_features=list(weighted.getFeatures());groups={code:[f for f in all_features if f['CODI_MUN']==code] for code in CODES}
    assert sum(not QgsVariantUtils.isNull(f['etiqueta']) for f in all_features)==1
    for f in all_features:
        p=None if QgsVariantUtils.isNull(f['POT_KW']) else float(f['POT_KW'])
        for index,field in enumerate(FIELDS):
            expected=p if p is not None else BANDS[f['INTERVAL']][index]
            assert float(f[field])==expected
    centres_native={}
    for mode,weight in [('registres',None),*zip(FIELDS,FIELDS)]:
        result=run('native:meancoordinates',INPUT=weighted,WEIGHT=weight,UID='CODI_MUN')
        centres_native[mode]={f['CODI_MUN']:f.geometry().asPoint() for f in result.getFeatures()}
        assert len(centres_native[mode])==3
    centre_layer=QgsVectorLayer('Point?crs=EPSG:25831','Centres','memory')
    centre_layer.dataProvider().addAttributes([QgsField('CODI_MUN',QVariant.Int),QgsField('tipus',QVariant.String),QgsField('total_kw',QVariant.Double)])
    centre_layer.updateFields();summaries=[]
    for code,features in groups.items():
        xy=np.array([[f.geometry().asPoint().x(),f.geometry().asPoint().y()] for f in features]);mean=xy.mean(axis=0)
        record={'code':code,'name':NAMES[code],'n':len(features),'n_imputed':sum(int(f['imputat']) for f in features),
            'published_kw':sum(float(f['POT_KW']) for f in features if not QgsVariantUtils.isNull(f['POT_KW'])),
            'null_bands':dict(Counter(f['INTERVAL'] for f in features if f['imputat'])),'mean':mean.tolist(),'scenarios':{}}
        for mode,title in [('registres','Registres'),('w_inf','Inferior'),('w_mid','Central'),('w_sup','Superior')]:
            weights=np.ones(len(features)) if mode=='registres' else np.array([f[mode] for f in features],dtype=float)
            centre=np.average(xy,axis=0,weights=weights);native=centres_native[mode][code]
            assert np.allclose(centre,[native.x(),native.y()],atol=1e-6,rtol=0)
            centred=xy-centre;cov=(centred.T*weights)@centred/weights.sum();eigen,vectors=np.linalg.eigh(cov)
            s={'centre':centre.tolist(),'sum_weights':float(weights.sum()),'shift_m':float(np.linalg.norm(centre-mean)),
               'sd_m':float(np.sqrt(np.trace(cov))),'covariance':cov.tolist(),'semiaxes_m':np.sqrt(eigen[::-1]).tolist(),
               'angle_east_deg':float(np.degrees(np.arctan2(vectors[1,-1],vectors[0,-1]))%180)}
            record['scenarios'][mode]=s
            f=QgsFeature(centre_layer.fields());f.setAttributes([code,title,None if mode=='registres' else float(weights.sum())])
            f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*centre)));centre_layer.dataProvider().addFeatures([f])
        lo,mid,hi=[record['scenarios'][field] for field in FIELDS]
        assert mid['sum_weights']==(lo['sum_weights']+hi['sum_weights'])/2
        expected=(lo['sum_weights']*np.array(lo['centre'])+hi['sum_weights']*np.array(hi['centre']))/(lo['sum_weights']+hi['sum_weights'])
        assert np.allclose(mid['centre'],expected,atol=1e-6,rtol=0)
        record['low_high_distance_m']=float(np.linalg.norm(np.array(lo['centre'])-hi['centre']))
        order=sorted(features,key=lambda f:float(f['w_mid']),reverse=True)
        record['top_five_share_pct']=100*sum(float(f['w_mid']) for f in order[:5])/mid['sum_weights']
        record['points']=[{'xy':[f.geometry().asPoint().x(),f.geometry().asPoint().y()],
            'published':None if QgsVariantUtils.isNull(f['POT_KW']) else float(f['POT_KW']),
            'interval':f['INTERVAL'],'weights':[float(f[field]) for field in FIELDS],
            'label':'' if QgsVariantUtils.isNull(f['etiqueta']) else f['etiqueta']} for f in features]
        summaries.append(record)
    scenario=save(weighted,'punts_escenaris','Punts amb escenaris');centres=save(centre_layer,'centres','Centres comparats')
    admin=QgsVectorLayer(str(ADMIN)+'|layername=municipis_provincia','Municipis','ogr',ro)
    limits=save(run('native:extractbyexpression',INPUT=admin,EXPRESSION='"CODIMUNI" IN (\'430957\',\'430430\',\'430477\')'),'limits','Límits municipals')
    constant=next(row for row in summaries if row['code']==430477)
    c=constant['scenarios']['registres'];cov=np.array(c['covariance'])
    parameters=QgsVectorLayer('Point?crs=EPSG:25831','Paràmetres','memory')
    params={'Sxx':cov[0,0],'Syy':cov[1,1],'Sxy':cov[0,1],'D_m':c['sd_m'],
            'a_m':c['semiaxes_m'][0],'b_m':c['semiaxes_m'][1],'azimut':(90-c['angle_east_deg'])%180}
    parameters.dataProvider().addAttributes([QgsField(k,QVariant.Double) for k in params]);parameters.updateFields()
    f=QgsFeature(parameters.fields());f.setAttributes(list(params.values()));f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(*c['centre'])))
    parameters.dataProvider().addFeatures([f]);parameters=save(parameters,'dispersio','Centre i dispersió de Constantí')
    contours=[]
    for name,formula in [('cercle','make_circle($geometry, "D_m", 72)'),('ellipse','make_ellipse($geometry, "a_m", "b_m", "azimut", 72)')]:
        layer=save(run('native:geometrybyexpression',INPUT=parameters,OUTPUT_GEOMETRY=0,WITH_Z=False,WITH_M=False,EXPRESSION=formula),name)
        coords=np.array(json.loads(next(layer.getFeatures()).geometry().asJson())['coordinates'][0])[:-1,:2]
        if name=='cercle':assert np.allclose(np.linalg.norm(coords-c['centre'],axis=1),c['sd_m'],atol=1e-5)
        else:assert np.allclose(2*np.cov(coords,rowvar=False,ddof=0),cov,rtol=1e-6,atol=.01)
        contours.append(layer)
    raw.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name':'circle','color':'#006699','size':'1.8','outline_color':'white','outline_width':'.15'}))
    rules=QgsRuleBasedRenderer.Rule(None)
    for flag,label,colour in [(0,'Potència publicada','#006699'),(1,'Pes assignat','#e69f00')]:
        symbol=QgsMarkerSymbol.createSimple({'name':'circle','color':colour,'outline_color':'#333333','outline_width':'.15'})
        symbol.symbolLayer(0).setDataDefinedProperty(QgsSymbolLayer.PropertySize,QgsProperty.fromExpression('0.35 * sqrt("w_mid")'))
        rules.appendChild(QgsRuleBasedRenderer.Rule(symbol,filterExp=f'"imputat" = {flag}',label=label))
    scenario.setRenderer(QgsRuleBasedRenderer(rules))
    pal=QgsPalLayerSettings();pal.fieldName='etiqueta';fmt=QgsTextFormat();fmt.setSize(12);fmt.setColor(QColor('#222222'));pal.setFormat(fmt)
    scenario.setLabeling(QgsVectorLayerSimpleLabeling(pal));scenario.setLabelsEnabled(True)
    categories=[]
    for title,shape,colour in [('Registres','diamond','#b22d43'),('Inferior','cross','#444444'),('Central','star','#111111'),('Superior','square','#7b3294')]:
        symbol=QgsMarkerSymbol.createSimple({'name':shape,'color':colour,'outline_color':'white','outline_width':'.35','size':'5'})
        categories.append(QgsRendererCategory(title,symbol,title))
    centres.setRenderer(QgsCategorizedSymbolRenderer('tipus',categories))
    limits.renderer().setSymbol(QgsFillSymbol.createSimple({'style':'no','outline_color':'#303b44','outline_width':'.6'}))
    for layer in contours:
        layer.renderer().setSymbol(QgsFillSymbol.createSimple({'style':'no','outline_color':'#b87924' if layer.name()=='cercle' else '#006699','outline_width':'.8','outline_style':'dash' if layer.name()=='cercle' else 'solid'}))
    for layer in [raw,scenario,centres,limits,parameters,*contours]:layer.saveStyleToDatabase('docent','Cas municipal amb escenaris explícits',True,'')
    image=ROOT/'context/inputs/constanti-ortofoto-2025.png';metadata=json.loads(image.with_suffix('.json').read_text());assert sha(image)==metadata['sha256']
    a,b,c_,d=BOUNDS
    raster=gdal.Translate(str(OUT/'ortofoto.tif'),str(image),format='GTiff',outputSRS='EPSG:25831',outputBounds=[a,d,c_,b],creationOptions=['COMPRESS=DEFLATE'])
    assert raster.RasterXSize==1250 and raster.RasterYSize==1125;raster=None
    background=QgsRasterLayer(str(OUT/'ortofoto.tif'),'Ortofoto ICGC 2025 · 8 m/píxel');background.setOpacity(.55)
    background.saveNamedStyle(str(OUT/'ortofoto.qml'));project.addMapLayer(background)
    raw.setSubsetString('"CODI_MUN" = 430477');scenario.setSubsetString('"CODI_MUN" = 430477')
    limits.setSubsetString('"CODIMUNI" = \'430477\'');centres.setSubsetString('"CODI_MUN" = 430477 AND "tipus" IN (\'Registres\',\'Central\')')
    tree=project.layerTreeRoot();tree.setHasCustomLayerOrder(True)
    tree.setCustomLayerOrder([centres,scenario,*contours,raw,parameters,limits,background])
    for layer in [raw,parameters,*contours]:tree.findLayer(layer.id()).setItemVisibilityChecked(False)
    from qgis.core import QgsRectangle
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*BOUNDS),project.crs()))
    assert project.write(str(OUT/'constanti.qgz'))
    report={'runtime_image':IMAGE,'qgis':Qgis.QGIS_VERSION,'source_sha256':sha(SOURCE),'admin_sha256':sha(ADMIN),
        'bands':BANDS,'expressions':expressions(),'open_records':opened,'municipalities':summaries,'constanti_dispersion':params,
        'basemap':metadata,'native_field_values_verified':True,'native_centres_verified':12,'manual_click_by_click':False,'operations':operations}
    dump(OUT/'controls.json',report)
    print(json.dumps({**{k:v for k,v in report.items() if k not in ['municipalities','operations','basemap']},
        'municipalities':[{k:v for k,v in row.items() if k!='points'} for row in summaries]},ensure_ascii=False,indent=2),flush=True)


def finalise():
    with sqlite3.connect(OUT/'municipis.gpkg') as db:
        db.execute('PRAGMA wal_checkpoint(TRUNCATE)');db.execute('PRAGMA journal_mode=DELETE')
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert db.execute('SELECT COUNT(*), SUM(w_mid) FROM punts_escenaris WHERE CODI_MUN=430477').fetchone()==(124,2970.0)


def verify(directory,report_path):
    global _APP
    import numpy as np
    from qgis.core import (QgsApplication,QgsProject,QgsMapLayerType,QgsVectorLayer,
        QgsExpression,QgsExpressionContext,QgsExpressionContextUtils)
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen');_APP=QgsApplication([],False);_APP.initQgis()
    directory=Path(directory).resolve()
    hashes={p.name:sha(p) for p in directory.iterdir() if p.suffix in ['.gpkg','.qgz','.tif','.qml']}
    project=QgsProject();assert project.read(str(directory/'constanti.qgz'))
    assert project.crs().authid()=='EPSG:25831' and project.ellipsoid()=='NONE'
    details=[]
    for layer in project.mapLayers().values():
        assert layer.isValid(),layer.name()
        assert Path(layer.source().split('|')[0]).resolve().is_relative_to(directory)
        row={'name':layer.name(),'source':layer.source().split('|')[0]}
        if layer.type()==QgsMapLayerType.VectorLayer:
            features=list(layer.getFeatures());assert features and len(features)==layer.featureCount()
            row['features']=len(features)
        details.append(row)
    assert len(details)==8
    with sqlite3.connect(f'file:{directory/"municipis.gpkg"}?mode=ro',uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        totals=db.execute('SELECT CODI_MUN,COUNT(*),SUM(imputat),SUM(w_inf),SUM(w_mid),SUM(w_sup) FROM punts_escenaris GROUP BY CODI_MUN ORDER BY CODI_MUN').fetchall()
        assert totals==[(430430,437,111,1881.0,2338.5,2796.0),(430477,124,26,2825.0,2970.0,3115.0),(430957,111,24,651.0,771.0,891.0)],totals
        assert db.execute('SELECT COUNT(*) FROM punts_escenaris WHERE POT_KW IS NOT NULL AND (w_inf != POT_KW OR w_mid != POT_KW OR w_sup != POT_KW)').fetchone()[0]==0
    ro=QgsVectorLayer.LayerOptions();ro.forceReadOnly=True
    points=QgsVectorLayer(str(directory/'municipis.gpkg')+'|layername=punts_base','Constantí','ogr',ro)
    assert points.setSubsetString('"CODI_MUN" = 430477') and points.featureCount()==124
    QgsProject.instance().addMapLayer(points)
    centre=QgsVectorLayer(str(directory/'municipis.gpkg')+'|layername=dispersio','Centre','ogr',ro)
    context=QgsExpressionContext();context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(centre));feature=next(centre.getFeatures());context.setFeature(feature)
    formulas={
        'Sxx':"with_variable('cx',x($geometry),aggregate('Constantí','mean',(x($geometry)-@cx)^2))",
        'Syy':"with_variable('cy',y($geometry),aggregate('Constantí','mean',(y($geometry)-@cy)^2))",
        'Sxy':"with_variable('cx',x($geometry),with_variable('cy',y($geometry),aggregate('Constantí','mean',(x($geometry)-@cx)*(y($geometry)-@cy))))"}
    for name,formula in formulas.items():
        expression=QgsExpression(formula);value=expression.evaluate(context)
        assert not expression.hasEvalError() and np.isclose(value,feature[name],rtol=0,atol=1e-6),(name,value)
    assert all(sha(directory/name)==digest for name,digest in hashes.items())
    dump(report_path,{'ok':True,'readonly':True,'offline':True,'layers':details,'hashes':hashes,'totals':totals,'native_dispersion_expressions_verified':True})
    print('Verified relocated project, 8 layers, scenario fields and native dispersion expressions.',flush=True)


def bundle(report_path):
    report=json.loads(Path(report_path).read_text());assert report['ok']
    for name,digest in report['hashes'].items():assert sha(OUT/name)==digest
    target=ROOT/'tmp/dades-docents/practica-punts-municipals-20261004.zip';assert not target.exists()
    dump(OUT/'verificacio.json',report)
    (OUT/'captures').mkdir(exist_ok=True);(OUT/'reproduccio').mkdir(exist_ok=True);(OUT/'figures').mkdir(exist_ok=True)
    for name in ['dades','camp','centre','resultat','ellipse']:
        stem='municipals-'+name
        receipt=json.loads((ROOT/'context/qgis/manifests'/f'{stem}.yml').read_text());assert receipt['ok'] and not receipt['warnings']
        for suffix in ['.png','.annotations.svg']:shutil.copyfile(ROOT/'assets/captures'/(stem+suffix),OUT/'captures'/(stem+suffix))
        shutil.copyfile(ROOT/'context/qgis/manifests'/(stem+'.yml'),OUT/'captures'/(stem+'.yml'))
    for name in ['constanti-pesos','punts-escenaris','punts-municipis']:
        shutil.copyfile(ROOT/'assets/img/generated'/(name+'.svg'),OUT/'figures'/(name+'.svg'))
    for path in [Path(__file__),ROOT/'context/qgis/punts-municipals.yml',ROOT/'context/qgis/punts-municipals.md',ROOT/'context/inputs/constanti-ortofoto-2025.json']:
        shutil.copyfile(path,OUT/'reproduccio'/path.name)
    (OUT/'LLEGIU-ME.md').write_text(
        '# Punts municipals: Constantí, el Morell i el Catllar\n\n'
        'Benito Zaragozí · Preparació del 4/10/2026 · Material per a revisió.\n\n'
        'Obre constanti.qgz amb QGIS. Les dades són locals, en EPSG:25831, amb rutes relatives.\n'
        'La vista inicial mostra pesos centrals i els centres dels registres i dels pesos.\n'
        'Per repetir el procés, copia punts_base al teu GeoPackage de treball i filtra CODI_MUN=430477.\n'
        'Connecta municipis.gpkg a l’Explorador per veure totes les capes.\n\n'
        '## Dades i regles\n\n'
        'punts_base: 672 registres originals dels tres municipis. punts_escenaris afegeix camps decimals.\n'
        'POT_KW es conserva. Si és buit, w_inf/w_mid/w_sup assignen 0/2.5/5, 5/15/25 o 25/62.5/100\n'
        'segons l’interval. Zero i els altres llindars inferiors són valors límit d’un escenari.\n'
        'La classe oberta no té punt mitjà ni màxim; el cas buit de Torredembarra no és en aquesta selecció.\n'
        'imputat identifica valors assignats. Les expressions completes i els controls són a controls.json.\n\n'
        '## Comprovacions\n\n'
        'Constantí: 124 punts, 98 potències publicades i 26 assignacions. Sumes 2825/2970/3115 kW.\n'
        'Centre central a 1832 m del centre dels registres; els centres inferior/superior se separen 194 m.\n'
        'El Morell: 111 punts i 771 kW centrals. El Catllar: 437 punts i 2338.5 kW centrals.\n'
        'centres conté els resultats per municipi i escenari; dispersio/cercle/ellipse corresponen als124punts\n'
        'de Constantí sense ponderar. Les captures són diàlegs configurats i resultats comprovats per separat.\n\n'
        '## Fonts\n\n'
        'ICAEN: extracció del28/09/2026; consumidors associats, no petjades dels panells.\n'
        'https://icaen.gencat.cat/ca/energia/autoconsum/Observatori-de-lautoconsum-a-catalunya/localitzacio-dinstallacions/\n'
        'ICGC: límits20/01/2026 i ortofoto2025, petició WMS a8m/píxel; URL i hash a reproduccio/.\n'
        'Condicions ICGC: https://www.icgc.cat/condicions\n'
        'Els scripts de reproduccio/ esperen el repositori geodisseny; els exercicis funcionen amb aquestes dades.\n')
    files=[{'path':str(p.relative_to(OUT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*'))
           if p.is_file() and not p.name.endswith(('~','-wal','-shm')) and p.name!='MANIFEST.json']
    dump(OUT/'MANIFEST.json',{'files':files,'runtime_image':IMAGE,'manual_click_by_click':False})
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in files:z.write(OUT/f['path'],'punts-municipals/'+f['path'])
        z.write(OUT/'MANIFEST.json','punts-municipals/MANIFEST.json')
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for f in files:assert hashlib.sha256(z.read('punts-municipals/'+f['path'])).hexdigest()==f['sha256']
    receipt={'path':str(target.relative_to(ROOT)),'sha256':sha(target),'bytes':target.stat().st_size,'files':len(files)+1}
    dump(target.with_suffix('.receipt.json'),receipt);print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fetch',action='store_true');p.add_argument('--build',action='store_true');p.add_argument('--finalise',action='store_true');p.add_argument('--record',action='store_true')
    p.add_argument('--verify');p.add_argument('--report');p.add_argument('--bundle',action='store_true');args=p.parse_args()
    if args.fetch:fetch()
    if args.build:build()
    if args.finalise:finalise()
    if args.record:dump(ROOT/'context/inputs/punts-escenaris.json',json.loads((OUT/'controls.json').read_text()))
    if args.verify:
        assert args.report;verify(args.verify,args.report)
    if args.bundle:
        assert args.report;bundle(args.report)
    if _APP is not None:
        from qgis.core import QgsProject
        import gc
        QgsProject.instance().clear();gc.collect();_APP.exitQgis()
