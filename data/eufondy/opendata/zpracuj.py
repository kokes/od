import csv
import json
import os
from urllib.request import urlopen

from lxml.etree import iterparse


def find_el(el, path):
    ns = el.nsmap[None]
    parts = path.split('/')
    fel = el.find('{{{}}}'.format(ns) + ('/{{{}}}'.format(ns)).join(parts))
    return getattr(fel, 'text', None)


def parse_el(el, paths):
    ret = {}
    for k, v in paths.items():
        if isinstance(v, dict):
            ret[k] = json.dumps(parse_el(el, v), ensure_ascii=False)
        else:
            ret[k] = find_el(el, v)

    return ret if len(ret) > 0 else None


schema = {
    'id': 'ID',
    'id_vyzva': 'ID_VYZVA',
    'kod': 'KOD',
    'naz': 'NAZ',
    'nazeva': 'NAZEVA',
    'popis': 'POPIS',
    'problem': 'PROBLEM',
    'cil': 'CIL',
    'datum_zahajeni': 'DZRSKUT',
    'datum_ukonceni_predp': 'DURPRED',
    'datum_ukonceni_skut': 'DURSKUT',
    'suk': 'SUK',
    'zadatel_nazev': 'ZAD/NAZ',
    'zadatel_ico': 'ZAD/IC',
    'zadatel_pravni_forma': 'ZAD/HPF',
    'zadatel_adresa': {
        'ruian': 'ZAD/ADR/RUIAN',
        'kkod': 'ZAD/ADR/KKOD',
        'knazev': 'ZAD/ADR/KNAZEV',
        'okkod': 'ZAD/ADR/OKKOD',
        'oknazev': 'ZAD/ADR/OKNAZEV',
        'obkod': 'ZAD/ADR/OBKOD',
        'obnazev': 'ZAD/ADR/OBNAZEV',
        'cobcenazev': 'ZAD/ADR/COBCENAZEV',
        'psc': 'ZAD/ADR/PSC',
        'cp': 'ZAD/ADR/CP',
        'cisor': 'ZAD/ADR/CISOR',
        'ul': 'ZAD/ADR/UL',
        'www': 'ZAD/ADR/WWW',
    },
    'cile_projektu': 'PRJSC/SC',
    # 'um': 'UM', # TODO: rozlisit dopadove umisteni a realizacni
    'financovani_czv': 'PF/CZV',
    'financovani_eu': 'PF/EU',
    'financovani_cnv': 'PF/CNV',
    'financovani_sn': 'PF/SN',
    'financovani_s': 'PF/S',
    'financovani_esif': 'PF/ESIF',
    'financovani_cv': 'PF/CV',
    'cilove_skupiny': 'CILSKUP/CSKOD',
}

if __name__ == '__main__':
    sloupce = ['id', 'id_vyzva', 'kod', 'naz', 'nazeva', 'popis', 'problem', 'cil', 'datum_zahajeni',
               'datum_ukonceni_predp', 'datum_ukonceni_skut', 'suk', 'zadatel_nazev', 'zadatel_ico', 'zadatel_pravni_forma',
               'zadatel_adresa', 'cile_projektu', 'financovani_czv', 'financovani_eu', 'financovani_cnv',
               'financovani_sn', 'financovani_s', 'financovani_esif', 'financovani_cv', 'cilove_skupiny']

    os.makedirs('data', exist_ok=True)
    with open('data/projekty.csv', 'w', encoding='utf8') as fw:
        cw = csv.DictWriter(fw, fieldnames=sloupce)
        cw.writeheader()
        r = urlopen('https://ms14opendata.mssf.cz/SeznamProjektu.xml')
        et = iterparse(r)

        for action, element in et:
            assert action == 'end'
            if not element.tag.endswith('}PRJ'):
                continue
            projekt = parse_el(element, schema)

            cw.writerow(projekt)
            element.clear()
