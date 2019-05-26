import os
import csv
import json
import lxml.etree
from urllib.request import urlopen
from shutil import copyfileobj
import gzip
from multiprocessing import Pool


mapping = {
    'id': 'id',
    'type': 'type',
    'subtype': 'subtype',
    'firstName': 'name/person/firstName',
    'lastName': 'name/person/lastName',
    'middleName': 'name/person/middleName',
    'tradeName': 'name/tradeName',
    'ico': 'ico',
    'address': {
        'code': 'address/code',
        'city': 'address/city',
        'district': 'address/district',
        'street': 'address/street',
        'cp': 'address/cp',
        'co': 'address/co',
        'ce': 'address/ce',
        'zip': 'address/zip',
        'region': 'address/region',
        'addressPoint': 'address/addressPoint',
        'state': 'address/state',
        'fullAddress': 'address/fullAddress',
    },
    'pdz': 'pdz',
    'ovm': 'ovm',
    'hierarchy': {
         'isMaster': 'hierarchy/isMaster',
         'masterId': 'masterId',
    },
    'idOVM': 'idOVM'
}

def strip_ns(el):
    return el.tag.rpartition('}')[-1]


def find_el(el, path):
    ns = el.nsmap[None]
    parts = path.split('/')
    fel = el.find('{{{}}}'.format(ns) + ('/{{{}}}'.format(ns)).join(parts))
    return getattr(fel, 'text', None)

def parse_el(el, paths):
    ret = {}
    for k, v in paths.items():
        if isinstance(v, dict):
            ret[k] = parse_el(el, v)
        else:
            val = find_el(el, v)
            if val == 'true':
                val = True
            elif val == 'false':
                val = False
            if val is not None:
                ret[k] = val
        
    return ret if len(ret) > 0 else None


def parse_xml(ds):
    xfn = os.path.join(rdr, '{}.xml'.format(ds))
    cfn = os.path.join(cdr, '{}.csv'.format(ds))

    with open(xfn, 'rb') as f, open(cfn, 'wt', encoding='utf8') as fw:
        et = lxml.etree.iterparse(f)
        cw = csv.DictWriter(fw, fieldnames=mapping.keys())
        cw.writeheader()

        for _, el in et:
            if strip_ns(el) != 'box':
                continue

            row = parse_el(el, mapping)
            row = {k: json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v for k, v in row.items()}
            cw.writerow(row)
            el.clear()
            
    return ds

if __name__ == '__main__':
    urls = {
        'po': 'https://www.mojedatovaschranka.cz/sds/datafile.do?format=xml&service=seznam_ds_po',
        'pfo': 'https://www.mojedatovaschranka.cz/sds/datafile.do?format=xml&service=seznam_ds_pfo',
        'fo': 'https://www.mojedatovaschranka.cz/sds/datafile.do?format=xml&service=seznam_ds_fo',
        'ovm': 'https://www.mojedatovaschranka.cz/sds/datafile.do?format=xml&service=seznam_ds_ovm',
    }

    rdr = 'data/raw'
    cdr = 'data/csv'
    os.makedirs(rdr, exist_ok=True)
    os.makedirs(cdr, exist_ok=True)


    for ds, url in urls.items():
        fn = os.path.join(rdr, '{}.xml'.format(ds))    
        with urlopen(url) as r:
            assert r.headers.get('Content-Encoding') == 'gzip'

            with open(fn, 'wb') as fw, gzip.open(r) as gr:
                copyfileobj(gr, fw)

    with Pool(4) as p:
        for ds in p.imap_unordered(parse_xml, urls.keys()):
            print(ds)
