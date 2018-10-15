import csv
import sys
from datetime import datetime
from urllib.request import urlopen

import psycopg2
from tqdm import tqdm

def ares_url(rejstrik, ico):
    if rejstrik == 'or':
        return 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_{}.cgi?ico={}&rozsah=1'.format(rejstrik, ico)

    return 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_{}.cgi?ico={}'.format(rejstrik, ico)

if __name__ == '__main__':
    rejstrik = sys.argv[1]
    assert rejstrik in ['res', 'or']

    conn = psycopg2.connect(host='localhost')
    while True:
        with conn, conn.cursor() as cursor:
            cursor.execute('select ico from ares.raw where rejstrik = %s and xml is null limit 1000',
                       (rejstrik,))
            icos = [j[0] for j in cursor.fetchall()]
            if len(icos) == 0: break

            for ico in tqdm(icos):
                assert isinstance(ico, int) and ico > 0 and len(str(ico)) <= 8, 'invalid format, {}'.format(ico)
                r = urlopen(ares_url(rejstrik, ico))
                dt = r.read()
                if b'Chyba 23 - chybn' in dt:
                    raise ValueError('nespravny format ico: {}'.format(ico))

                if (b'<dtt:faultcode>' in dt) or (b'nastala SQL chyba' in dt) or (b'Chyba 900' in dt):
                    raise ValueError(f'chyba v API ({ico})')

                found = b'Chyba 71 - nenalezeno' not in dt
                if not found:
                    print(ico, 'nenalezeno')

                # TODO: upsert? (kdybychom meli ICO odjinud)
                cursor.execute('update ares.raw set modified_on=%s, xml=%s, found=%s where rejstrik = %s and ico = %s',
                    (datetime.utcnow(), dt, found, rejstrik, ico))
