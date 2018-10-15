"""
Stahne potencialne nova IC ze zmenovych souboru ARES a vlozi je do
ares.raw, kde pak muzeme stahnout jejich udaje.
"""
import csv
import os
import logging
from contextlib import closing

import requests
import lxml.etree
import psycopg2
from tqdm import tqdm

url = 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_zm.cgi?cislo_zdroje=2&cislo_davky_od={}&cislo_davky_do={}'
def get_ic():
    r = requests.get(url.format(-1, -1))
    assert r.ok
    et = lxml.etree.fromstring(r.content)

    zad = et.find('are:Odpoved/D:Zadani', namespaces=et.nsmap)
    cod, cdo = zad.find('D:C_davky_od', namespaces=et.nsmap).text, zad.find('D:C_davky_do', namespaces=et.nsmap).text

    for cs in range(int(cod), int(cdo)+1):
        yield from get_batch(cs)

def get_batch(bid):
    r = requests.get(url.format(bid, bid))
    assert r.ok

    eto = lxml.etree.fromstring(r.content)
    ic = eto.iterfind('are:Odpoved/D:S/D:ic', namespaces=eto.nsmap)
    for el in ic:
        yield int(el.text)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    tdir = os.path.dirname(os.path.abspath(__file__))
    tfn = 'data/nova_ic.csv'
    absfn = os.path.join(tdir, tfn)

    with open(absfn, 'w') as fw:
        logging.info('zapisuju nova ICO do %s', absfn)
        cw = csv.writer(fw)
        cw.writerow(['ico', 'rejstrik'])
        for ico in tqdm(get_ic()):
            cw.writerow([ico, 'res'])
            cw.writerow([ico, 'or'])

    logging.info('vkladam nova ICO do databaze')
    con = psycopg2.connect(host='localhost')
    with closing(con), con, con.cursor() as cursor:
        cursor.execute('drop table if exists ares.nova_ic')
        cursor.execute('create table ares.nova_ic(ico int, rejstrik varchar)')
        cursor.execute('copy ares.nova_ic from \'{}\' csv header'.format(absfn))
        cursor.execute('''insert into ares.raw(ico, rejstrik)
        (select ico, rejstrik from ares.nova_ic) on conflict do nothing''')
        cursor.execute('drop table ares.nova_ic')
