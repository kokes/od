import csv
import gzip
import os
from glob import glob

import lxml.etree
from tqdm import tqdm

def strip_ns(el):
    return el.tag.rpartition('}')[-1]

def el_dict(el):
    if el.text is not None:
        return el.text

    ret = dict()
    for ch in el.iterchildren():
        tg = strip_ns(ch)
        
        if tg not in ret:
            ret[tg] = el_dict(ch)
            continue
        
        if isinstance(ret[tg], list):
            ret[tg].append(el_dict(ch))
        else:
            ret[tg] = [ret[tg]] + [el_dict(ch)]
        
    return ret

hds = ['dump', 'id_verze', 'id_smlouvy', 'odkaz', 'cas_zverejneni', 'predmet', 'datum_uzavreni',       'cislo_smlouvy', 'schvalil', 'hodnotaBezDph', 'hodnotaVcetneDph', 'platny_zaznam']
hdu = ['dump', 'smlouva', 'subjekt', 'ds', 'nazev', 'ico_raw', 'ico', 'adresa', 'utvar', 'platce', 'prijemce']

nin = hdu.index('ico') # kde mame ciselne ICO?

tdir = 'data/csv/'

if __name__ == '__main__':
    os.makedirs(tdir, exist_ok=True)
    for fn in tqdm(glob('data/raw/*.gz')):
        bn = os.path.split(fn)[-1]
        tbn = bn[:bn.rindex('.xml.gz')]
        tfn = os.path.join(tdir, tbn + '_smlouvy.csv')
        tfnu = os.path.join(tdir, tbn + '_ucastnici.csv')

        with open(tfn, 'w') as fw, open(tfnu, 'w') as fwu:
            cw = csv.writer(fw)
            cwu = csv.writer(fwu)
            cw.writerow(hds)
            cwu.writerow(hdu)
            rok, mesic = None, None

            with gzip.open(fn) as gf:
                et = lxml.etree.parse(gf).getroot()

                for el in tqdm(et, desc=bn):
                    eln = strip_ns(el)
                    if eln != 'zaznam':
                        if eln == 'mesic':
                            mesic = el_dict(el)
                        elif eln == 'rok':
                            rok = el_dict(el)
                        continue

                    assert not (rok is None or mesic is None), 'rok a mesic musi predchazet data'
                    dt = el_dict(el) # parsuj data
                    ts = f'{rok}-{mesic}'

                    # smlouva samotna
                    idv = int(dt['identifikator']['idVerze'])
                    row = [ts, idv, int(dt['identifikator']['idSmlouvy']), dt['odkaz'], dt['casZverejneni'], dt['smlouva']['predmet'], dt['smlouva']['datumUzavreni'], dt['smlouva'].get('cisloSmlouvy'), dt['smlouva'].get('schvalil'),                  dt['smlouva'].get('hodnotaBezDph'), dt['smlouva'].get('hodnotaVcetneDph'), dt['platnyZaznam'] == '1']
                    row = [j.strip() if isinstance(j, str) else j for j in row]
                    cw.writerow(row)

                    # ucastnici (subjekt, pak smluvni strany)
                    uc = [dt['smlouva']['subjekt']]
                    if isinstance(dt['smlouva']['smluvniStrana'], dict):
                        uc.append(dt['smlouva']['smluvniStrana'])
                    else:
                        uc.extend(dt['smlouva']['smluvniStrana'])

                    # pole subjekt
                    for l, st in enumerate(uc):
                        row = [ts, idv, False, st.get('ds'), st['nazev'], st.get('ico'), st.get('ico'), st.get('adresa'), st.get('utvar'), st.get('platce'), st.get('prijemce')]
                        row = [j.strip() if isinstance(j, str) else j for j in row]
                        row[nin] = int(row[nin]) if (row[nin] and row[nin].isdigit() and (len(row[nin]) < 9)) else None

                        cwu.writerow(row)

