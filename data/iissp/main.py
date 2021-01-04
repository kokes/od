import csv
import os
from datetime import date
from urllib.request import urlopen

import lxml.etree
from tqdm import tqdm

url = 'https://monitor.statnipokladna.cz/data/xml/ucjed.xml'
table_name = 'ucetni_jednotky'

# XSD nema vsechno, dafuq
cols = 'ucjed_id, csuis_ucjed_id, ico, start_date, end_date, nazev, dic, adresa, nuts_id, zrizovatel_id, zrizovatel_ico, cofog_id, isektor_id, kapitola_id, nace_id, druhuj_id, poddruhuj_id, konecplat, forma_id, katobyv_id, stat_id, zdrojfin_id, druhrizeni_id, veduc_id, zuj, sidlo, zpodm_id, kod_pou, typorg_id, pocob, kraj, obec, ulice, kod_rp, datumakt, aktorg_id, datumvzniku, psc, pou_id, orp_id, zuj_id'.split(
    ', ')

dates = 'start_date, end_date, konecplat, datumakt, datumvzniku'.split(', ')


def main(outdir: str):
    target_file = os.path.join(outdir, f'{table_name}.csv')
    with urlopen(url) as f, open(target_file, 'w', encoding='utf8') as fw:
        cw = csv.DictWriter(fw, fieldnames=cols)
        cw.writeheader()

        et = lxml.etree.iterparse(f)

        for action, element in tqdm(et):
            assert action == 'end', action

            if element.tag != 'row':
                continue

            row = {j.tag: j.text for j in element.getchildren()}

            if row['zrizovatel_ico'] == 'Chybí':
                row['zrizovatel_ico'] = None

            if '_' in row['ico']:
                print('preskakuju {}, nema spravne ico ({})'.format(
                    row['nazev'], row['ico']))
                continue

            for datecol in dates:
                if (not row[datecol] or row[datecol] == '00000000'):
                    row[datecol] = None
                    continue

                if '-' in row[datecol]:
                    # 21-11-2019
                    day, month, year = row[datecol][:2], row[datecol][3:5], row[datecol][6:]
                else:
                    # 20191121
                    day, month, year = row[datecol][6:], row[datecol][4:6], row[datecol][:4]
                row[datecol] = date(int(year), int(month), int(day))

            cw.writerow(row)
            element.clear()


if __name__ == '__main__':
    main('.')
