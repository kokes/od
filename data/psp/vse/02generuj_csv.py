#!/usr/bin/env python
# coding: utf-8

import json
import csv
import os
import zipfile
from contextlib import contextmanager
from functools import lru_cache
from io import BytesIO, TextIOWrapper
from datetime import datetime

from dateutil.parser import parse
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
            # UNL soubory maj jeden extra sloupec
            # TODO: zapnout tohle, az opravi schema sbirky
            # assert len(el) == len(cols) + 1, (el, cols)
            dt = {}
            for k, v in zip(cols, el):
                if v.strip() == '':
                    dt[k] = None
                elif types[k] in datetypes:
                    try:
                        dt[k] = datetime.strptime(v, '%Y-%m-%d')
                    except ValueError:
                        dt[k] = parse(v, dayfirst=True)
                else:
                    dt[k] = v

            yield dt


csv_dir = 'data/csv'
os.makedirs(csv_dir, exist_ok=True)
with open('mapping.json') as f:
    mapping = json.load(f)


for mp in mapping:
    tbl = f'{mp["tema"]}_{mp["tabulka"]}'
    tfn = os.path.join(csv_dir, f'{tbl}.csv')
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
