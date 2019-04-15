import json
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve

import requests
from tqdm import tqdm

if __name__ == '__main__':
    csv_dir = 'data/csv'
    os.makedirs(csv_dir, exist_ok=True)

    px = 'Toto pole obsahuje '
    typemap = {
        'integer': 'int',
        'default': 'varchar',
        'date': 'date',
        'decimal': 'numeric(12, 4)',
    }

    with open('mapping.json') as f:
        mps = json.load(f)

    qs = ['CREATE SCHEMA IF NOT EXISTS cssz;', 'BEGIN;']
    cp = ['BEGIN;']
    for mp in mps:
        nazev = mp['nazev_ascii']
        tn = f'cssz.{nazev}'
        sloupce = []
        slns = set() # seznam nazvu, at muzem profiltrovat PK (chyba ve schematech)
        for sl in mp['schema']['fields']:
            sln = sl['name'].replace('-', '_')
            slns.add(sln)
            slt = typemap[sl['type']]
            sloupce.append(f'{sln} {slt}')
            
        if 'primaryKey' in mp['schema']:
            pk = mp['schema']['primaryKey']
            pk = [pk] if isinstance(pk, str) else pk
            ne = [j for j in pk if j not in slns]
            if len(ne) > 0:
                print('CHYBI', tn, ne)
            
            pk = [j for j in pk if j in slns]

            sloupce.append(f'PRIMARY KEY({", ".join(pk)})')
        
        qs.append(f'DROP TABLE IF EXISTS {tn};')
        qs.append(f'CREATE TABLE {tn} ({", ".join(sloupce)});')
        
        for sl in mp['schema']['fields']:
            desc = sl['description']
            if desc.startswith(px):
                desc = desc[len(px):].capitalize()
            qs.append(f"COMMENT ON COLUMN {tn}.{sl['name'].replace('-', '_')} IS '{desc}';")
        
        tfn = os.path.join(csv_dir, mp['nazev_ascii'] + '.csv')
        cp.append(f'COPY {tn} FROM \'{os.path.abspath(tfn)}\' CSV HEADER;')

    qs.append('COMMIT;')
    cp.append('COMMIT;')
    with open('init.sql', 'w') as fw:
        fw.write('\n'.join(qs))
        
    with open('copy.sql', 'w') as fw:
        fw.write('\n'.join(cp))

    # sql COPY generovani
    for mp in tqdm(mps):
        tfn = os.path.join(csv_dir, mp['nazev_ascii'] + '.csv')
        urlretrieve(mp['url']['data'], tfn)
