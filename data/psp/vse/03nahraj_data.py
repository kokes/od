#!/usr/bin/env python
# coding: utf-8

import json
import csv
import os
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


def read_compressed_csv(zf, fn, mp):
    datetypes = {'date', 'datetime(year to hour)', 'datum', 'datetime(year to minute)', 'datetime(year to second, fraction)',
                 'datetime year to hour', 'datetime year to minute', 'datetime year to day', 'datetime(year to second)'}

    cols = [j['sloupec'] for j in mp]
    types = {j['sloupec']: j['typ'] for j in mp}
    with read_compressed(zf, fn) as f:
        cr = csv.reader(f, delimiter='|')
        for el in cr:
            dt = {}
            for k, v in zip(cols, el):
                if v.strip() == '':
                    dt[k] = None
                elif types[k] in datetypes:
                    dt[k] = parse(v)
                else:
                    dt[k] = v

            yield dt


def nm_fn(tema, tabulka):
    tbl = f'{mp["tema"]}_{mp["tabulka"]}'
    tfn = os.path.join(csv_dir, f'{tbl}.csv')
    return tbl, tfn


csv_dir = 'data/csv'
os.makedirs(csv_dir, exist_ok=True)
run_csv = False
run_sql = True
with open('mapping.json') as f:
    mapping = json.load(f)


if run_csv:
    for mp in mapping:
        tbl, tfn = nm_fn(mp["tema"], mp["tabulka"])
        print(tbl)
        cols = [j['sloupec'] for j in mp['sloupce']]
        with open(tfn, 'w') as fw:
            cw = csv.DictWriter(fw, fieldnames=cols)
            cw.writeheader()
            for ffn in mp['soubory']:
                print('\t', ffn)
                zf, fn = ffn.split('/')
                for el in read_compressed_csv(zf, fn, mp['sloupce']):
                    cw.writerow(el)

if run_sql:
    pg = psycopg2.connect(host='localhost')
    schema = 'psp'
    for mp in mapping:
        tbl, tfn = nm_fn(mp["tema"], mp["tabulka"])
        absfn = os.path.abspath(tfn)
        print(tbl)
        with pg, pg.cursor() as cur:
            cur.execute(pql.SQL('TRUNCATE {}.{}').format(pql.Identifier(schema), pql.Identifier(tbl)))
            cur.execute(pql.SQL("COPY {{}}.{{}} FROM '{}' CSV HEADER".format(
                absfn)).format(pql.Identifier(schema), pql.Identifier(tbl)))
