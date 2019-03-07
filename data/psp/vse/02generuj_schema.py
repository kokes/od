# TODO: not null, primary key

import json

with open('mapping.json') as f:
    mapping = json.load(f)

typemap = {
    'int': 'int', 
    'char(X)': 'varchar',
    'date': 'date',
    'datetime(year to hour)': 'timestamp',
    'datetime(hour to minute)': 'time',
    'datum': 'timestamp',
    'datetime(year to minute)': 'timestamp',
    'char(1)': 'char(1)',
    'datetime(year to second, fraction)': 'timestamp',
    'datetime year to hour': 'timestamp',
    'datetime year to minute': 'timestamp',
    'char(Y)': 'varchar',
    'datetime year to day': 'date',
    'datetime(year to second)': 'timestamp',
}

q = []
q.append('CREATE SCHEMA IF NOT EXISTS psp;')

for mp in mapping:
    tbl = f'psp.{mp["tema"]}_{mp["tabulka"]}'
    q.append(f'DROP TABLE IF EXISTS {tbl};')
    q.append(f'CREATE TABLE {tbl} (')
    for j, col in enumerate(mp['sloupce']):
        comma = ',' if j < len(mp['sloupce'])-1 else ''
        typ = typemap[col["typ"]]
        q.append(f'\t"{col["sloupec"]}" {typ}{comma}')
    
    q.append(');\n')
                 
    for col in mp['sloupce']:
        desc = (col['popis'] or '').replace("'", '')
        q.append(f"COMMENT ON COLUMN {tbl}.{col['sloupec']} IS '{desc}';")

    q.append('\n\n')
    
with open('schema.sql', 'w') as fw:
    fw.write('\n'.join(q))
