import json
import os
from functools import lru_cache
from urllib.parse import urljoin
from urllib.request import urlretrieve

import lxml.html
import requests
from tqdm import tqdm


@lru_cache(maxsize=None)
def req(url):
    r = requests.get(url)
    assert r.ok
    return r


def najdi_textem(root, element, text: str):
    els = [j for j in root.iterfind(f'.//{element}') if j.text == text]
    assert len(els) == 1, els
    return els[0]


def main(outdir: str, partial: bool = False):
    # TODO: odstranit generovani mapping.json, misto toho ho zaverzovat
    # (a zkratit nazvy tabulek, jsou moc dlouhy pro pg)
    burl = 'https://data.cssz.cz/web/otevrena-data/katalog-otevrenych-dat'
    r = req(burl)
    ht = lxml.html.fromstring(r.text)

    ds = []
    for num, tr in tqdm(enumerate(ht.cssselect('tbody.table-data')[0].findall('tr'))):
        if partial and num > 15:
            break
        a = tr.find('td').find('a')
        link = a.attrib['href']
        assert link.startswith('http://') or link.startswith('https://'), link
        dr = req(link)
        
        dht = lxml.html.fromstring(dr.text)
        scha = najdi_textem(dht, 'a', 'Schéma (JSON)')
        sch_url = urljoin(link, scha.attrib['href'])
        da = najdi_textem(dht, 'a', 'Data (CSV)')
        
        schema = req(sch_url).json()
        
        ds.append({
            'nazev': a.text,
            'nazev_ascii': link.rpartition('/')[-1].replace('-', '_'),
            'url': {
                'dataset': link,
                'schema': sch_url,
                'data': urljoin(link, da.attrib['href']),
            },
            'schema': schema,
        })
        
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, 'mapping.json'), 'w') as fw:
        json.dump(ds, fw, ensure_ascii=False, indent=2)

    for dataset in ds:
        tfn = os.path.join(outdir, dataset["nazev_ascii"] + ".csv")
        urlretrieve(dataset["url"]["data"], tfn)


if __name__ == '__main__':
    main(".")