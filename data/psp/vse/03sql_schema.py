import json
import os

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

schema = 'psp'
csv_dir = 'data/csv'
q, cp, cm, idx = [], [], [], []  # CTEs, COPY, COMMENT, indexes
q.append('CREATE SCHEMA IF NOT EXISTS {};'.format(schema))

for mp in mapping:
    tbl = f'{mp["tema"]}_{mp["tabulka"]}'
    full_tbl = f'{schema}.{tbl}'

    tfn = os.path.abspath(os.path.join(csv_dir, f'{tbl}.csv'))

    print(tbl)

    q.append(f'DROP TABLE IF EXISTS {full_tbl};')
    q.append(f'CREATE TABLE {full_tbl} (')
    for j, col in enumerate(mp['sloupce']):
        # CTE
        comma = ',' if j < len(mp['sloupce'])-1 else ''
        typ = typemap[col["typ"]]
        null = '' if col.get('nullable', True) else ' NOT NULL '
        q.append(f'\t"{col["sloupec"]}" {typ}{null}{comma}')

        # comments
        desc = (col['popis'] or '').replace("'", '')
        cm.append(f"COMMENT ON COLUMN {full_tbl}.{col['sloupec']} IS '{desc}';")

        # indexes
        if col.get('unique'):
            idx.append(
                f'CREATE UNIQUE INDEX {schema}_{tbl}_{col["sloupec"]}_unique_idx ON {schema}.{tbl}({col["sloupec"]});')

    # more indexes (non unique)
    for el in mp.get('index', []):
        idx.append(f'CREATE INDEX {schema}_{tbl}_{"_".join(el)}_idx ON {schema}.{tbl}({", ".join(el)});')

    # COPY
    cp.append(f'COPY {full_tbl} FROM \'{tfn}\' CSV HEADER;')

    q.append(');\n')

# one-time updates
otu = []
otu.append("UPDATE psp.poslanci_osoby SET narozeni = NULL WHERE narozeni = '1900-01-01';")

with open('schema.sql', 'w') as fw:
    fw.write('\n'.join(q + cm + cp + otu + idx))
