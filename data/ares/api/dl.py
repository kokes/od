import csv
import sys
from datetime import datetime
from urllib.request import urlopen

import psycopg2

def ares_url(rejstrik, ico):
    if rejstrik == 'or':
        return 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_{}.cgi?ico={}&rozsah=1'.format(rejstrik, ico)

    return 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_{}.cgi?ico={}'.format(rejstrik, ico)


rejstrik = sys.argv[1]
assert rejstrik in ['res', 'or']

conn = psycopg2.connect(host='localhost')
with conn, conn.cursor() as cursor:
    cursor.execute('select ico from od.ares_raw where rejstrik = %s and xml is null order by ico asc limit 250000',
                   (rejstrik,)) # TODO: order by modified_on asc (and found is not false?)
    icos = [j[0] for j in cursor.fetchall()]

for j, ico in enumerate(icos):
    print('\t{}/{}'.format(j+1, len(icos)), end='\r')
    assert isinstance(ico, int) and ico > 0 and len(str(ico)) <= 8, 'invalid format, {}'.format(ico)
    r = urlopen(ares_url(rejstrik, ico))
    dt = r.read()
    if b'Chyba 23 - chybn' in dt:
        raise ValueError('nespravny format ico: {}'.format(ico))

    found = b'Chyba 71 - nenalezeno' not in dt
    if not found:
        print(ico, 'nenalezeno')

    with conn, conn.cursor() as cursor:
        # TODO: upsert? (kdybychom meli ICO odjinud)
        cursor.execute('update od.ares_raw set modified_on=%s, xml=%s, found=%s where rejstrik = %s and ico = %s',
            (datetime.utcnow(), dt, found, rejstrik, ico))
