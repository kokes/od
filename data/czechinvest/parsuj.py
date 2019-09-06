import csv
import json
from datetime import date, timedelta

import xlrd


def intuj(el):
    if isinstance(el, str) and len(el) == 0:
        return None

    if isinstance(el, str):
        el = el.rstrip('. ').replace(' ', '')

    return int(el)


mesic = {
    'březen': 3,
    'duben': 4,
    'květen': 5,
    'leden': 1,
    'listopad': 11,
    'prosinec': 12,
    'srpen': 8,
    'září': 9,
    'únor': 2,
    'červen': 6,
    'červenec': 7,
    'říjen': 10,
}


def mesicuj(el):
    if isinstance(el, str):
        return mesic[el.strip()]

    dt = date(1899, 12, 31) + timedelta(days=int(el)-1)
    return dt.month


if __name__ == '__main__':
    with open('data/mapping.json') as f:
        mapping = json.load(f)

    firmy = {}
    with open('data/slovnik.csv') as f:
        cr = csv.DictReader(f)
        for el in cr:
            firmy[el['firma']] = int(el['ico'])

    wb = xlrd.open_workbook('data/Udelene-investicni-pobidky-k-30-6-2019.xlsx')
    sh = wb.sheet_by_name('PROJEKTY')

    assert mapping['hd1'] == [j.value for j in sh.row(1)], [j.value for j in sh.row(1)]
    assert mapping['hd2'] == [j.value for j in sh.row(2)], [j.value for j in sh.row(2)]

    with open('data/pobidky.csv', 'w', encoding='utf8') as fw:
        cw = csv.DictWriter(fw, fieldnames=mapping['tghd'])
        cw.writeheader()
        for rn in range(3, sh.nrows):
            row = [j.value.strip() if isinstance(j.value, str) else j.value for j in sh.row(rn)]
            drow = dict(zip(mapping['tghd'], row))

            # posledni radek se sumou
            if drow['cislo'] == '':
                break

            for c in ['cislo', 'ico', 'nova_mista', 'podani', 'rozh_den', 'rozh_rok']:
                drow[c] = intuj(drow[c])

            if drow['ico'] is None:
                drow['ico'] = firmy[drow['firma']]

            drow['rozh_mesic'] = mesicuj(drow['rozh_mesic'])
            drow['strop'] = None if drow['strop'] == '-' else drow['strop']
            drow['msp'] = {'Ano': True, 'Ne': False}[drow['msp']]
            drow['zruseno'] = True if drow['zruseno'] == 'x' else False

            cw.writerow(drow)
