#!/usr/bin/env python
# coding: utf-8

import json
import csv
import zipfile
from contextlib import contextmanager
from functools import lru_cache
from io import BytesIO, TextIOWrapper

from dateutil.parser import parse
import psycopg2
import psycopg2.extras
import psycopg2.sql as pql
import requests


@lru_cache(maxsize=None)
def dl(url):
    r = requests.get(url)
    assert r.ok, r.status_code
    return BytesIO(r.content)

@contextmanager
def read_compressed(zipname, filename):
    burl = 'http://www.psp.cz/eknih/cdrom/opendata/{}'
    with zipfile.ZipFile(dl(burl.format(zipname))) as zf:
        yield TextIOWrapper(zf.open(filename), 'cp1250', errors='ignore')  # tisky.unl maj encoding chyby

def read_compressed_csv(zf, fn, cols):
    datetypes = { 'date', 'datetime(year to hour)', 'datum', 'datetime(year to minute)', 'datetime(year to second, fraction)', 'datetime year to hour', 'datetime year to minute', 'datetime year to day', 'datetime(year to second)' }
    with read_compressed(zf, fn) as f:
        cr = csv.reader(f, delimiter='|')
        for el in cr:
            dt = {}
            for k, v in zip(cols, el):
                if v == '':
                    dt[k] = None
                elif types[k] in datetypes:
                    dt[k] = parse(v)
                else:
                    dt[k] = v
                    
            yield dt


pg = psycopg2.connect(host='localhost')


with open('mapping.json') as f:
    mapping = json.load(f)


for mp in mapping:
    schema = 'psp'
    tbl = f'{mp["tema"]}_{mp["tabulka"]}'
    print(tbl)
    cols = [j['sloupec'] for j in mp['sloupce']]
    types = {j['sloupec']: j['typ'] for j in mp['sloupce']}
    qq = 'INSERT INTO {{}}.{{}}({{}}) VALUES({})'.format(', '.join(['%({})s'.format(j) for j in cols]))
    with pg, pg.cursor() as cur:
        cur.execute(pql.SQL('DELETE FROM {}.{}').format(pql.Identifier(schema), pql.Identifier(tbl)))
        for ffn in mp['soubory']:
            print('\t', ffn)
            zf, fn = ffn.split('/')
#             for el in read_compressed_csv(zf, fn, cols):
#                 cur.execute(pql.SQL(qq).format(pql.Identifier(schema), pql.Identifier(tbl),
#                                               pql.SQL(',').join([pql.Identifier(j) for j in cols])), el)

            query = pql.SQL(qq).format(pql.Identifier(schema), pql.Identifier(tbl),
                                              pql.SQL(',').join([pql.Identifier(j) for j in cols]))
            data = read_compressed_csv(zf, fn, cols)
            
            psycopg2.extras.execute_batch(cur, query, data, page_size=1000)
