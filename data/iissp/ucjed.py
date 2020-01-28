import csv
from datetime import date
from urllib.request import urlopen

import lxml.etree

url = 'https://monitor.statnipokladna.cz/data/ucjed.xml'

# XSD nema vsechno, dafuq
cols = 'ico, start_date, end_date, ucjed_nazev, dic, adresa, nuts_id, zrizovatel_ico, cofog_id, isektor_id, kapitola_id, nace_id, druhuj_id, poddruhuj_id, konecplat, forma_id, katobyv_id, obec, kraj, stat_id, zdrojfin_id, druhrizeni_id, veduc_id, zuj, sidlo, zpodm_id, kod_pou, typorg_id, pocob, ulice, kod_rp, datumakt, aktorg_id, datumvzniku, psc'.split(
    ', ')

dates = 'start_date, end_date, konecplat, datumakt, datumvzniku'.split(', ')

with urlopen(url) as f, open('ucjed.csv', 'w', encoding='utf8') as fw:
    cw = csv.DictWriter(fw, fieldnames=cols)
    cw.writeheader()

    et = lxml.etree.iterparse(f)

    for action, element in et:
        assert action == 'end', action

        if element.tag != 'Radek':
            continue

        row = {j.tag: j.text for j in element.getchildren()}

        if not row['ico'].isdigit():
            print('preskakuju {}, nema spravne ico ({})'.format(
                row['ucjed_nazev'], row['ico']))
            continue

        for datecol in dates:
            if row[datecol]:
                day, month, year = row[datecol][:2], row[datecol][3:5], row[datecol][6:]
                row[datecol] = date(int(year), int(month), int(day))

        if row['zrizovatel_ico'] == 'Chybí':
            row['zrizovatel_ico'] = ''

        cw.writerow(row)
