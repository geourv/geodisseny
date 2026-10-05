"""Retain two licensed, version-pinned Commons illustrations without retouching.

Use --download once; the default invocation checks the retained bytes offline.
The source URLs, rights statements and output paths belong to this manual.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'context/inputs/imatges-historiques.json'
SOURCES=[
    {
        'id':'john-snow-1855',
        'path':'assets/img/historia/john-snow-1855.jpg',
        'url':'https://upload.wikimedia.org/wikipedia/commons/archive/2/27/20200506141216%21Snow-cholera-map-1.jpg',
        'source_page':'https://commons.wikimedia.org/w/index.php?title=File:Snow-cholera-map-1.jpg&oldid=1188845148',
        'file_timestamp':'2007-06-22T13:53:35Z',
        'expected_sha1':'5dedf1bc755d6034005024a29c54bcf3a85293ef',
        'expected_bytes':1183741,
        'commons_dimensions_px':[3045,2840],
        'creators':['John Snow','C. F. Cheffins (lithography)'],
        'depicted_event_year':1854,
        'publication_year':1855,
        'rights':'Public domain; Commons PD-Art / PD-old-100-expired',
        'rights_url':'https://creativecommons.org/publicdomain/mark/1.0/',
        'note':'Archived 2007 file, before the much larger 2020 replacement. Date of the outbreak and date of the second edition are distinguished.',
    },
    {
        'id':'biaix-supervivencia',
        'path':'assets/img/historia/biaix-supervivencia.svg',
        'url':'https://upload.wikimedia.org/wikipedia/commons/archive/b/b2/20220825203351%21Survivorship-bias.svg',
        'source_page':'https://commons.wikimedia.org/w/index.php?title=File:Survivorship-bias.svg&oldid=1176240698',
        'file_timestamp':'2021-03-21T12:47:29Z',
        'expected_sha1':'8ef03131e553ea14ce028921ac72ebd74f91f98a',
        'expected_bytes':107968,
        'commons_dimensions_px':[1338,997],
        'creators':['Martin Grandjean (vector)','McGeddon (picture)','US Air Force (hit plot concept)'],
        'creation_year':2021,
        'rights':'CC BY-SA 4.0',
        'rights_url':'https://creativecommons.org/licenses/by-sa/4.0/',
        'note':'Modern illustration with hypothetical impacts, not an original 1943 damage record. The SVG includes its white background.',
    },
]


def prepare(download=False):
    records=[]
    for source in SOURCES:
        target=ROOT/source['path']
        assert target.resolve().is_relative_to(ROOT/'assets/img/historia')
        if target.exists():
            data=target.read_bytes()
        elif download:
            request=urllib.request.Request(source['url'],headers={
                'User-Agent':'Geodisseny-manual/1.0 (https://github.com/geourv/geodisseny)'})
            with urllib.request.urlopen(request,timeout=90) as response:
                data=response.read(source['expected_bytes']+1)
        else:
            raise FileNotFoundError(f'{target}: run with --download to retain the declared source.')
        assert len(data)==source['expected_bytes'],source['id']
        assert hashlib.sha1(data).hexdigest()==source['expected_sha1'],source['id']
        if target.suffix=='.svg':
            image=ET.fromstring(data)
            assert image.tag=='{http://www.w3.org/2000/svg}svg'
            assert not any(node.tag.rsplit('}',1)[-1] in ['script','foreignObject'] for node in image.iter())
            for node in image.iter():
                for key,value in node.attrib.items():
                    if key.rsplit('}',1)[-1]=='href':assert value.startswith(('#','data:')),value
        else:
            assert data.startswith(b'\xff\xd8') and data.endswith(b'\xff\xd9')
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(data)
        records.append({**source,'sha256':hashlib.sha256(data).hexdigest(),
            'retained_on':'2026-10-04','changes':'None; exact file bytes copied, display size set by the chapter.'})
    manifest={'version':1,'owner':'context/dades/preparar_imatges_historiques.py','images':records}
    if download:
        MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    else:
        assert json.loads(MANIFEST.read_text())==manifest,'Image provenance differs from the declared sources.'
    print(json.dumps({'ok':True,'images':len(records),'files':[
        {'path':r['path'],'bytes':r['expected_bytes'],'sha256':r['sha256'],'rights':r['rights']} for r in records]},
        ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download',action='store_true')
    prepare(parser.parse_args().download)
