from urllib.request import urlopen, urlretrieve
from tempfile import NamedTemporaryFile
import shutil
from zipfile import ZipFile
from contextlib import closing

from lxml.etree import iterparse
from itertools import chain

import csv
import os

urls = {
    2018: 'https://www.szif.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2Fdokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2F1563197121858.zip',
    2017: 'https://www.szif.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2Fdokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2F1563197147275.zip',
}

id_prijemce = 1

os.makedirs('data', exist_ok=True)
with open('data/zadatele.csv', 'w', encoding='utf8') as fz, open('data/platby.csv', 'w', encoding='utf8') as fp:
    cz = csv.DictWriter(fz, ['id_prijemce', 'rok', 'jmeno_nazev', 'obec', 'okres', 'castka_bez_pvp'])
    cp = csv.DictWriter(fp, ['id_prijemce', 'rok', 'fond_typ_podpory', 'opatreni', 'zdroje_cr', 'zdroje_eu', 'celkem_czk'])
    
    cz.writeheader()
    cp.writeheader()
    
    for rok_ds, url in urls.items():
        tmpf = NamedTemporaryFile()

        with closing(urlopen(url)) as rr:
            shutil.copyfileobj(rr, tmpf)

        zf = ZipFile(tmpf.name)

        assert len(zf.filelist) == 1, 'Vic souboru nez ocekavano: {}'.format(zf.filelist)

        et = iterparse(zf.open(zf.filelist[0].filename))

        rok = None
        for action, element in et:
            assert action == 'end'
            if element.tag == 'rok':
                rok = int(element.text)
                assert rok == rok_ds, 'Necekany rok v datech'

            if element.tag != 'zadatel':
                continue

            zadatel = {'id_prijemce': id_prijemce, 'rok': rok}

            for key in ['jmeno_nazev', 'obec', 'okres', 'castka_bez_pvp']:
                zadatel[key] = element.find(key).text

            for elplatba in element.findall('platby/platba') + element.findall('platby_pvp/platba_pvp'):
                platba = {'id_prijemce': id_prijemce, 'rok': rok}
                for key in ['fond_typ_podpory', 'opatreni', 'zdroje_cr', 'zdroje_eu', 'celkem_czk']:
                    platba[key] = getattr(elplatba.find(key), 'text', None)

                cp.writerow(platba)

            cz.writerow(zadatel)
            id_prijemce += 1

            element.clear()
