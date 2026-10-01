"""Prepare the real census-section demonstration; raw sources remain private.

Fetch official, explicitly selected products with the host Python standard library.
The retained download manifest binds each local snapshot to its URL and SHA-256.
"""
import argparse
import hashlib
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / 'tmp/dades-docents/seccions'
ORIGINALS = PRIVATE / 'originals'
MUNICIPALITIES = [
    '43012','43907','43043','43047','43050','43095','43097','43100',
    '43103','43109','43111','43122','43126','43131','43135','43905',
    '43144','43148','43153','43164','43171','43166',
]
SECTION_URL = ('https://datacloud.icgc.cat/datacloud/bseccen_etrs89/shp/'
               'bseccenv10sh1f1_20240101_0.zip')
CADASTRE_FEED = 'https://www.catastro.hacienda.gob.es/INSPIRE/buildings/43/ES.SDGC.BU.atom_43.xml'
# Names and codes checked against the Idescat county list and the official DGC feed.
# Codes are not interchangeable: Tarragona is INE 43148 but DGC 43900.
INE_TO_CADASTRE = {
    '43012':('43012','ALTAFULLA'), '43907':('43039','LA CANONJA'),
    '43043':('43044','EL CATLLAR'), '43047':('43048','CONSTANTI'),
    '43050':('43051','CREIXELL'), '43095':('43096','EL MORELL'),
    '43097':('43099','LA NOU DE GAIA'), '43100':('43102','PALLARESOS ELS'),
    '43103':('43105','PERAFORT'), '43109':('43111','LA POBLA DE MAFUMET'),
    '43111':('43113','LA POBLA DE MONTORNES'), '43122':('43124','RENAU'),
    '43126':('43128','LA RIERA DE GAIA'), '43131':('43133','RODA DE BERA'),
    '43135':('43137','SALOMO'), '43905':('43185','SALOU'),
    '43144':('43146','LA SECUITA'), '43148':('43900','TARRAGONA'),
    '43153':('43155','TORREDEMBARRA'), '43164':('43166','VESPELLA DE GAIA'),
    '43171':('43173','VILA SECA'), '43166':('43168','VILALLONGA DEL CAMP'),
}
ALLOWED_HOSTS = {'datacloud.icgc.cat', 'www.catastro.hacienda.gob.es'}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def fetch_sources(limit=None):
    ORIGINALS.mkdir(parents=True, exist_ok=True)
    manifest_path = PRIVATE / 'downloads.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    def fetch(url, name, maximum=80_000_000):
        assert urllib.parse.urlparse(url).hostname in ALLOWED_HOSTS
        path = ORIGINALS / name
        if path.exists():
            if name not in manifest or digest(path) != manifest[name]['sha256']:
                raise RuntimeError(f'Unmanaged or changed source: {path}')
            return path
        request = urllib.request.Request(urllib.parse.quote(url, safe=':/?=&%'),
                                         headers={'User-Agent':'Geodisseny educational source preparation'})
        with urllib.request.urlopen(request, timeout=120) as response:
            if urllib.parse.urlparse(response.url).hostname not in ALLOWED_HOSTS:
                raise RuntimeError('Unexpected download host')
            content = response.read(maximum + 1)
            if len(content) > maximum:
                raise RuntimeError(f'Download exceeds limit: {name}')
        temporary = path.with_suffix(path.suffix + '.part')
        temporary.write_bytes(content)
        if name.endswith('.zip') and not content.startswith(b'PK'):
            raise RuntimeError(f'Not a ZIP: {name}')
        temporary.rename(path)
        manifest[name] = {'url':url, 'sha256':digest(path), 'bytes':path.stat().st_size,
                          'retrieved':'2026-09-29'}
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
        print(name, path.stat().st_size, manifest[name]['sha256'], flush=True)
        return path

    fetch(SECTION_URL, 'seccions-20240101.zip')
    feed = fetch(CADASTRE_FEED, 'catastro-tarragona-20260821.xml', maximum=2_000_000)
    tree = ET.parse(feed)
    ns = {'a':'http://www.w3.org/2005/Atom'}
    entries = {}
    for entry in tree.findall('a:entry', ns):
        title = entry.findtext('a:title', namespaces=ns).strip()
        for code, (cadastre_code, name) in INE_TO_CADASTRE.items():
            if title == f'{cadastre_code}-{name} buildings':
                link = entry.find('a:link[@rel="enclosure"]', ns)
                entries[code] = link.attrib['href']
    missing = set(MUNICIPALITIES) - set(entries)
    if missing:
        raise RuntimeError(f'Municipalities missing from official feed: {sorted(missing)}')
    for code in MUNICIPALITIES[:limit]:
        cadastre_code, _ = INE_TO_CADASTRE[code]
        fetch(entries[code], f'cadastre-dgc-{cadastre_code}.zip')
        time.sleep(.15)


def analyse():
    """Spatial joins and inference in the pinned QGIS/PySAL analysis container."""
    import numpy as np
    import shapely
    from shapely import STRtree
    from shapely.geometry import mapping
    from osgeo import ogr, osr, gdal
    import libpysal
    import esda
    from libpysal.weights import Queen, KNN, w_subset
    from esda import Moran, Moran_Local

    ogr.UseExceptions()
    manifest = json.loads((PRIVATE/'downloads.json').read_text())
    used_names = ['seccions-20240101.zip','catastro-tarragona-20260821.xml']
    used_names += [f'cadastre-dgc-{INE_TO_CADASTRE[m][0]}.zip' for m in MUNICIPALITIES]
    for name in used_names:
        assert digest(ORIGINALS/name) == manifest[name]['sha256'], name
    sections_ds = ogr.Open('/vsizip/'+str(ORIGINALS/'seccions-20240101.zip'))
    layer = sections_ds.GetLayer(0)
    reference = osr.SpatialReference();reference.ImportFromEPSG(25831)
    assert layer.GetSpatialRef().IsSame(reference)
    sections=[]
    for feature in layer:
        municipality=feature['MUNICIPI'][:5]
        if municipality not in MUNICIPALITIES:continue
        geometry=shapely.from_wkb(bytes(feature.GetGeometryRef().ExportToWkb()))
        assert geometry.is_valid
        code=municipality+feature['DISTRICTE'].zfill(2)+feature['SECCIO'].zfill(3)
        sections.append({'geometry':geometry,'cusec':code,'mundissec':feature['MUNDISSEC'],
                         'municipi_ine':municipality,'pv_n':0,'pv_known_n':0,'pv_kw':0.,
                         'pv_edifici_n':0,'pv_edifici_known_n':0,'pv_edifici_kw':0.,
                         'buildings_n':0,'functional_n':0,'year_exact':[],
                         'age_min':[],'age_max':[],'date_interval_n':0})
    sections.sort(key=lambda x:x['cusec'])
    geometries=[s['geometry'] for s in sections]
    assert len({s['cusec'] for s in sections})==len(sections)
    tree=STRtree(geometries)
    audit={'pv_input':0,'pv_unmatched':0,'pv_ambiguous':0,'buildings_input':0,
           'buildings_unmatched':0,'buildings_ambiguous':0,'buildings_invalid_geometry':0,
           'buildings_missing_geometry':0,'buildings_duplicate_id':0,
           'building_id_reused_in_distinct_municipal_entities':0,
           'building_date_missing_or_invalid':0,'building_municipality_mismatch':0}

    def assign(point,kind):
        matches=tree.query(point,predicate='intersects')
        if len(matches)==0:
            audit[kind+'_unmatched']+=1;return None
        if len(matches)>1:
            audit[kind+'_ambiguous']+=1;return None
        return sections[int(matches[0])]

    pv_path=ROOT/'tmp/dades-docents/moodle/autoconsum-tarragona-20260928.gpkg'
    assert digest(pv_path)=='1c8b4bda31ac5bfa35fd8ac4b1fbf36990d01065590c673b579e0670291ac9c8'
    pv_ds=ogr.Open(str(pv_path));pv_layer=pv_ds.GetLayerByName('autoconsum_tarragones')
    for f in pv_layer:
        audit['pv_input']+=1
        geometry=shapely.from_wkb(bytes(f.GetGeometryRef().ExportToWkb()))
        point=geometry.geoms[0] if geometry.geom_type=='MultiPoint' else geometry
        s=assign(point,'pv')
        if s is None:continue
        p=f['POT_KW'];known=p is not None and p>0
        s['pv_n']+=1
        if known:s['pv_known_n']+=1;s['pv_kw']+=float(p)
        if f['UBICACIO']=='Edifici':
            s['pv_edifici_n']+=1
            if known:s['pv_edifici_known_n']+=1;s['pv_edifici_kw']+=float(p)
    assert audit['pv_input']==5102
    assert sum(s['pv_n'] for s in sections)+audit['pv_unmatched']+audit['pv_ambiguous']==5102

    ids={}
    for municipality in MUNICIPALITIES:
        dgc,name=INE_TO_CADASTRE[municipality]
        archive=ORIGINALS/f'cadastre-dgc-{dgc}.zip'
        with zipfile.ZipFile(archive) as z:
            source=next(n for n in z.namelist() if n.endswith('.building.gml'))
        ds=ogr.Open('/vsizip/'+str(archive)+'/'+source)
        buildings=ds.GetLayerByName('Building')
        assert buildings.GetSpatialRef().IsSame(reference)
        count=0
        for f in buildings:
            count+=1;audit['buildings_input']+=1
            key=f['gml_id']
            raw=f.GetGeometryRef()
            if raw is None:audit['buildings_missing_geometry']+=1;continue
            geometry=shapely.from_wkb(bytes(raw.ExportToWkb()))
            signature=tuple(f[k] for k in ['beginning','end','conditionOfConstruction','currentUse','numberOfDwellings'])
            if key in ids:
                old_geometry,old_signature,old_municipality=ids[key]
                if geometry.equals(old_geometry) and signature==old_signature:
                    audit['buildings_duplicate_id']+=1;continue
                if old_municipality==municipality or geometry.intersects(old_geometry):
                    raise RuntimeError(f'Conflicting repeated Building ID: {key}')
                # Distinct, non-overlapping municipal objects: keep both and qualify
                # their identifiers by source municipality, rather than dropping one.
                audit['building_id_reused_in_distinct_municipal_entities']+=1
                print('Repeated ID in distinct municipal objects',old_municipality,municipality,
                      round(geometry.distance(old_geometry),2),'metres apart',flush=True)
            ids[key]=(geometry,signature,municipality)
            if not geometry.is_valid:
                audit['buildings_invalid_geometry']+=1;geometry=shapely.make_valid(geometry)
            if geometry.is_empty:audit['buildings_missing_geometry']+=1;continue
            s=assign(geometry.representative_point(),'buildings')
            if s is None:continue
            s['buildings_n']+=1
            if s['municipi_ine']!=municipality:audit['building_municipality_mismatch']+=1
            if f['conditionOfConstruction']!='functional':continue
            s['functional_n']+=1
            try:
                start=int(f['beginning'][:4]);end=int(f['end'][:4])
                assert 1000<=start<=end<=2026
            except (TypeError,ValueError,AssertionError):
                audit['building_date_missing_or_invalid']+=1;continue
            s['age_min'].append(2026-end);s['age_max'].append(2026-start)
            if start==end:s['year_exact'].append(start)
            else:s['date_interval_n']+=1
        print('Buildings',municipality,dgc,name,count,flush=True)

    def median(values):return float(np.median(values)) if values else None
    for s in sections:
        s['age_exact_n']=len(s['year_exact'])
        s['age_median_exact']=median([2026-v for v in s['year_exact']])
        s['age_median_min']=median(s['age_min']);s['age_median_max']=median(s['age_max'])
        s['age_exact_fraction']=s['age_exact_n']/s['functional_n'] if s['functional_n'] else None
        s['pv_known_fraction']=s['pv_edifici_known_n']/s['pv_edifici_n'] if s['pv_edifici_n'] else None
        # A zero here means no known registered kW, not zero actual installed capacity.
        s['kw_per_100_buildings']=100*s['pv_edifici_kw']/s['functional_n'] if s['functional_n'] else None
        s['association_sample']=bool(s['age_exact_n']>=10 and s['pv_edifici_known_n']>0)
        s['moran_sample']=bool(s['functional_n']>0 and
            (s['pv_edifici_n']==0 or s['pv_edifici_known_n']>0))

    # Queen uses full source geometry; only the displayed copy is simplified later.
    queen=Queen.from_iterable(geometries,ids=list(range(len(sections))))
    included=[i for i,s in enumerate(sections) if s['moran_sample']]
    w=w_subset(queen,included)
    excluded_islands=list(w.islands)
    included=[i for i in included if i not in excluded_islands]
    w=w_subset(queen,included);w.transform='r'
    assert list(w.id_order)==included and not w.islands
    y=np.log1p([sections[i]['kw_per_100_buildings'] for i in included])
    np.random.seed(20260929)
    global_moran=Moran(y,w,permutations=9999)
    local=Moran_Local(y,w,permutations=9999,seed=20260929,n_jobs=1,keep_simulations=False)
    p=np.asarray(local.p_sim)
    rank=np.argsort(p);threshold=.05*np.arange(1,len(p)+1)/len(p)
    accepted=p[rank]<=threshold
    cutoff=float(p[rank][np.where(accepted)[0][-1]]) if np.any(accepted) else -1.
    labels={1:'HH',2:'LH',3:'LL',4:'HL'}
    z=(y-y.mean())/y.std(ddof=0)
    lag=libpysal.weights.lag_spatial(w,z)
    for position,index in enumerate(included):
        s=sections[index]
        s.update({'moran_i':float(local.Is[position]),'moran_p_sim':float(p[position]),
                  'moran_quadrant':labels[int(local.q[position])],
                  'moran_fdr':bool(p[position]<=cutoff),'moran_z':float(z[position]),
                  'moran_lag':float(lag[position]),
                  'neighbors':[sections[j]['cusec'] for j in w.neighbors[index]]})
    centroids=np.array([[geometries[i].centroid.x,geometries[i].centroid.y] for i in included])
    contrast=KNN.from_array(centroids,k=4);contrast.transform='r'
    np.random.seed(20260929)
    other=Moran(y,contrast,permutations=9999)

    sample=[s for s in sections if s['association_sample']]
    age=np.array([s['age_median_exact'] for s in sample])
    raw=np.log1p([s['pv_edifici_kw'] for s in sample])
    normalized=np.log1p([s['kw_per_100_buildings'] for s in sample])
    slope,intercept=np.polyfit(age,normalized,1)
    correlation=float(np.corrcoef(age,normalized)[0,1])
    np.random.seed(20260929)
    association_weights=w_subset(queen,[i for i,s in enumerate(sections) if s['association_sample']])
    association_weights.transform='r'
    residuals=normalized-(intercept+slope*age)
    residual_moran=Moran(residuals,association_weights,permutations=9999)
    result={
        'source_dates':{'sections':'2024-01-01','cadastre_feed':'2026-08-21',
                        'icaen_download':'2026-09-28','icaen_metadata_revision':'2024-06-30',
                        'icaen_effective_date_verified':False,'age_reference_year':2026},
        'runtime':{'gdal':gdal.VersionInfo(),'numpy':np.__version__,
                   'libpysal':libpysal.__version__,'esda':esda.__version__},
        'sources_used':{n:manifest[n] for n in used_names},
        'municipality_correspondence':INE_TO_CADASTRE,
        'audit':audit,'section_count':len(sections),
        'totals':{k:sum(s[k] for s in sections) for k in [
            'pv_n','pv_known_n','pv_kw','pv_edifici_n','pv_edifici_known_n','pv_edifici_kw',
            'buildings_n','functional_n','age_exact_n','date_interval_n']},
        'moran':{'variable':'log1p(known registered building kW per 100 functional cadastral buildings)',
                 'weights':'queen, full geometry, row standardised, county only',
                 'n':len(included),'excluded_islands':[sections[i]['cusec'] for i in excluded_islands],
                 'I':float(global_moran.I),'expected_I':float(global_moran.EI),
                 'p_sim':float(global_moran.p_sim),'permutations':9999,'seed':20260929,
                 'local_p_convention':'esda.Moran_Local.p_sim (one-tailed pseudo-p)',
                 'fdr_method':'Benjamini-Hochberg, alpha=0.05','fdr_cutoff':cutoff,
                 'fdr_counts':{v:int(sum(s.get('moran_fdr',False) and s.get('moran_quadrant')==v for s in sections)) for v in labels.values()},
                 'fdr_sections':[s['cusec'] for s in sections if s.get('moran_fdr',False)],
                 'excluded_data_sections':[s['cusec'] for s in sections if not s['moran_sample']],
                 'knn4_I':float(other.I),'knn4_p_sim':float(other.p_sim)},
        'association':{'n':len(sample),'x':'median age of functional buildings with beginning year = end year',
                       'y':'log1p(known registered building kW per 100 functional buildings)',
                       'selection':'at least 10 exact-date functional buildings and at least one known positive building PV power',
                       'pearson_r':correlation,'R2':correlation**2,
                       'pearson_r_log_raw_kw':float(np.corrcoef(age,raw)[0,1]),
                       'slope_per_year':float(slope),'intercept':float(intercept),
                       'residual_moran_I':float(residual_moran.I),
                       'residual_moran_p_sim':float(residual_moran.p_sim)},
        'display_geometry_simplification_m':5,
        'limits':['Different source dates; ecological exploratory association, not causation.',
                  'ICAEN coordinates identify associated consumers, not panel footprints.',
                  'Missing PV power remains missing; known kW are an incomplete sum.',
                  'DGC beginning/end are the oldest/newest construction-unit years, not confidence bounds; multi-year objects are excluded from the single-year age indicator.',
                  'Cadastral buildings are not dwellings or building parts.']}
    output_dir=ROOT/'context/inputs';output_dir.mkdir(parents=True,exist_ok=True)
    features=[]
    for s in sections:
        properties={k:v for k,v in s.items() if k not in ['geometry','year_exact','age_min','age_max']}
        features.append({'type':'Feature','properties':properties,
                         'geometry':mapping(s['geometry'].simplify(5,preserve_topology=True))})
    geojson={'type':'FeatureCollection','name':'seccions_tarragones_2024',
             'crs':{'type':'name','properties':{'name':'EPSG:25831'}},
             'attribution':'Seccions: ICGC/Idescat, CC BY 4.0. Edificis: Dirección General del Catastro. Autoconsum: ICAEN.',
             'features':features}
    (output_dir/'seccions-tarragones.geojson').write_text(json.dumps(geojson,ensure_ascii=False,separators=(',',':'))+'\n')
    (output_dir/'seccions-resultats.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['audit','section_count','totals','moran','association']},indent=2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--analyse', action='store_true')
    args = parser.parse_args()
    if args.fetch:
        fetch_sources(args.limit)
    if args.analyse:
        analyse()
