"""Repeat the workshop's point-wise QGIS algorithm without manual data entry.

Load this file in QGIS's Python console, then call calcula_lot(paquet, grup,
superficie). This is a consumer-owned calculation, not a screenshot renderer.
The package stays unchanged; each run requires a new output directory.
"""
import json
from pathlib import Path


def calcula_lot(paquet, grup='carretera', superficie='mdt', sortida=None):
    import numpy as np
    from osgeo import gdal
    from qgis.core import QgsProcessingFeedback
    import processing

    if grup not in ['carretera','area'] or superficie not in ['mdt','mds']:
        raise ValueError('Grup: carretera/area; superfície: mdt/mds.')
    paquet=Path(paquet).resolve()
    controls=json.loads((paquet/'controls/resultats.json').read_text())
    sources=[s for s in controls['sources'] if s['grup']==grup]
    if grup=='carretera' and superficie=='mds':
        sources=[s for s in sources if s['calculable']]
    sources.sort(key=lambda s:s['id'])
    assert sources and len(sources)<255
    destination=Path(sortida) if sortida else paquet/'treball'/f'lot-{grup}-{superficie}'
    destination.mkdir(parents=True,exist_ok=False)
    raw=destination/'intermedis';raw.mkdir()
    gdal.UseExceptions()
    terrain=gdal.Open(str(paquet/'dades/mdt-calcul.tif'))
    dtm=terrain.ReadAsArray().astype(float)
    valid=gdal.Open(str(paquet/'dades/domini-valid.tif')).ReadAsArray()==1
    count=np.zeros(dtm.shape,dtype=np.uint8)
    weighted=np.zeros(dtm.shape,dtype=float)
    feedback=QgsProcessingFeedback()
    records=[]

    def save(name,values,nodata,kind):
        path=destination/name
        ds=gdal.GetDriverByName('GTiff').Create(str(path),terrain.RasterXSize,terrain.RasterYSize,1,kind,
            ['COMPRESS=DEFLATE','TILED=YES'])
        ds.SetGeoTransform(terrain.GetGeoTransform());ds.SetProjection(terrain.GetProjection())
        ds.GetRasterBand(1).SetNoDataValue(nodata)
        ds.GetRasterBand(1).WriteArray(np.where(valid,values,nodata));ds=None
        return path

    for index,source in enumerate(sources,1):
        print(f'{index}/{len(sources)}: {source["id"]} · {superficie.upper()}',flush=True)
        params={'INPUT':str(paquet/f'dades/{superficie}-calcul.tif'),'BAND':1,
            'OBSERVER':f'{source["x"]},{source["y"]} [EPSG:25831]',
            'OBSERVER_HEIGHT':source[f'h_{superficie}_m'],'TARGET_HEIGHT':1.7 if superficie=='mdt' else 0,
            'MAX_DISTANCE':0,'EXTRA':'-cc 0.85714 -co COMPRESS=DEFLATE -co TILED=YES '+('-vv 1 -iv 0 -ov 255 -a_nodata 255' if superficie=='mdt' else '-om DEM -a_nodata -9999'),
            'OUTPUT':str(raw/f'{source["id"]}.tif')}
        output=processing.run('gdal:viewshed',params,feedback=feedback)['OUTPUT']
        ds=gdal.Open(output)
        assert ds.GetGeoTransform()==terrain.GetGeoTransform() and (ds.RasterYSize,ds.RasterXSize)==dtm.shape
        values=ds.ReadAsArray();ds=None
        visible=(values==1) if superficie=='mdt' else dtm+1.7>=values
        visible&=valid
        save(f'{source["id"]}.tif',visible.astype(np.uint8),255,gdal.GDT_Byte)
        count+=visible.astype(np.uint8);weighted+=visible*source['pes']
        records.append({'id':source['id'],'weight':source['pes'],'parameters':params})
    total_weight=sum(s['pes'] for s in sources)
    save('nombre.tif',count,255,gdal.GDT_Byte)
    save('percent.tif',100*weighted/total_weight,-9999,gdal.GDT_Float32)
    if grup=='area':
        torch=gdal.Open(str(paquet/f'resultats/torxa-{superficie}.tif')).ReadAsArray()
        save('alguna-part.tif',((count>0)|(torch==1)).astype(np.uint8),255,gdal.GDT_Byte)
    report={'algorithm':'gdal:viewshed','grup':grup,'superficie':superficie,
        'executions':len(sources),'total_weight':total_weight,'records':records,
        'comparison':'Fixed absolute endpoints; receivers at MDT + 1.7 m; common domain applied to every result.',
        'road_mds_note':'Only the 28 compatible origins; compare with the prepared 28-origin MDT result, not with all 37.'}
    (destination/'lot.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Lot complet: {destination}',flush=True)
    return destination
