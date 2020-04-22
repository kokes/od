import csv
import json
import os
from itertools import zip_longest
from urllib.request import urlretrieve

import xlrd

# TODO: nechcem strptime?
def predatuj(s):
    if len(s) == 0:
        return None

    d, m, y = map(int, s.split('.'))
    return f'{y}-{m:02d}-{d:02d}'

def intify(s):
    if isinstance(s, str) and len(s) == 0:
        s = None
    else:
        assert s == int(s)
        s = int(s)

    return s

if __name__ == '__main__':
    os.makedirs('data/raw', exist_ok=True)
    with open('hlavicka1420.json', encoding='utf8') as f:
        hd = json.load(f)

    source_url = 'https://dotaceeu.cz/getmedia/15745468-87e0-4b13-8791-08e55d90ddb7/2020_04_Seznam-operaci-_-List-of-operations2.xls.aspx?ext=.xls'
    target_filename = 'data/raw/2014_2020_seznam_operaci.xls'
    print(f'Stahuji z seznam operací z {source_url}, ale nemusí to být nejaktuálnější export - překontroluj stránku https://dotaceeu.cz/cs/statistiky-a-analyzy/seznamy-prijemcu')
    urlretrieve(source_url, target_filename)

    wb = xlrd.open_workbook(target_filename)
    sh = wb.sheet_by_name('Seznam operací')

    fr = [j.value.strip() for j in sh.row(2)]
    assert fr == hd['ocekavane'],  [(a, b) for a,b in zip_longest(fr, hd['ocekavane']) if a != b]

    with open('data/operace_2014_2020.csv', 'w', encoding='utf8') as fw:
        cw = csv.writer(fw)
        cw.writerow(hd['hlavicka'])
        for j in range(6, sh.nrows):
            row = [l.value for l in sh.row(j)]

            row[6] = intify(row[6]) # ICO
            row[8] = intify(row[8]) # PSC

            for cl in [9, 10, 11]:
                row[cl] = predatuj(row[cl])

            cw.writerow(row)
