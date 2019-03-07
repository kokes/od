import json
import os
import zipfile

import requests
import lxml.html


objs = [
    ('poslanci', 1301),
    ('hlasovani', 1302),
    ('tisky', 1303),
    ('interp', 1305),
    ('schuze', 1308),
    ('steno', 1310),
    ('dokumenty', 1309),
    ('sbirka', 1306),
]

url = 'http://www.psp.cz/sqw/hp.sqw?k={}'


spec = []
for topic, obj in objs:
    files = set()
    fn = f'data/raw/{topic}.zip'
    if os.path.isfile(fn):
        with zipfile.ZipFile(fn) as fl:
            files = set([j.filename for j in fl.filelist])
    
    r = requests.get(url.format(obj))
    assert r.ok

    ht = lxml.html.fromstring(r.text)

    h2s = ht.cssselect('div#main-content h2')
    tables = [j for j in ht.cssselect('div#main-content table')
              if [k.find('strong').text for k in j.find('tbody').find('tr').findall('td')] == ['Sloupec', 'Typ', 'Použití a vazby']]

    assert len(h2s) == len(tables)
    
    for h2, table in zip(h2s, tables):
        assert h2.text.startswith('Tabulka ')
        table_name = h2.text[len('Tabulka '):].strip()

        trs = table.find('tbody').findall('tr')

        cols = []
        for tr in trs[1:]:
            col, typ, comm = [j.text for j in tr.findall('td')]
            cols.append({
                'sloupec': col,
                'typ': typ,
                'popis': comm,
            })
            
        spec.append({
            'tema': topic,
            'tabulka': table_name,
            'soubory': [f'{topic}.zip/{table_name}.unl'] if f'{table_name}.unl' in files else [],
            'sloupce': cols,
        })

with open('mapping_raw.json', 'w') as fw:
    json.dump(spec, fw, ensure_ascii=False, indent=2)
