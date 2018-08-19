# - http://www.isvz.cz/ISVZ/Podpora/ISVZ_open_data_vz.aspx
# - http://www.isvz.cz/ISVZ/MetodickaPodpora/Napovedaopendata.pdf

import csv
import json
import gzip
import re
from glob import iglob, glob
from datetime import datetime
import os

from tqdm import tqdm

def get_fn(ds, tp):
    return os.path.join(tdir, '{}.csv'.format(tp))

def najdi_typy(hd, typy):
    ind = dict() # {'date': [15, 22], 'numeric': [7, 8, 9]}
    for k, v in typy.items():
        ind[k] = []

        for cl in v:
            try:
                j = hd.index(cl)
                ind[k].append(j)
            except ValueError:
                pass

    return ind

dtpt = re.compile('^\d{1,2}\.\d{1,2}\.\d{4}$')
def fix_date(s):
    if len(s) == 0:
        return None
    
    if dtpt.match(s) is not None:
        d, m, y = map(int, s.split('.'))
        return f'{y}-{m:02d}-{d:02d}'
    else:
        return datetime.strptime(s, '%d.%m.%Y %H:%M:%S').isoformat()

def fix_numeric(s):
    if len(s) == 0:
        return None
    return float(s.replace(',', '.'))

# '000 23 234' - takhle se obcas zadavaj ICO
def fix_ico(s):
    if len(s) == 0:
        return None
    elif s.isdigit():
        rv = int(s)
    elif s.startswith('CZ') and s[2:].isdigit(): # CZ00000205
        rv = int(s[2:])
    else:
        try:
            rv = int(s.replace(' ', '').replace('\xa0', ''))
        except:
            print('nevalidni ICO', s)
            return None
    
    if rv < 100*10**6:
        return rv
    else:
        print('ICO overflow', rv)
        return None

if __name__ == '__main__':
    with open('mapping.json') as f:
        allmaps = json.load(f)

    assert list(allmaps.keys()) == ['etrziste', 'vvz', 'zzvz']

    for ds, mapping in allmaps.items():
        print(ds)
        tblmap = {tuple(v): k for k,v in mapping['tabulky'].items()}

        sdir = f'data/raw/{ds}'
        tdir = f'data/processed/{ds}'
        if not os.path.isdir(tdir):
            os.makedirs(tdir, exist_ok=True)


        for k, v in tblmap.items():
            with open(get_fn(ds, v), 'w') as fw:
                cw = csv.writer(fw)
                cw.writerow(k)

        # sorted, abychom sli chronologicky
        for fn in tqdm(sorted(glob(os.path.join(sdir, '*.gz'))), desc=ds):
            with gzip.open(fn, mode='rt', encoding='utf-8-sig') as gf:
                cr = csv.reader(gf, delimiter=';')

                for ln in cr:
                    if len(ln) > 0 and ln[0] == mapping['hlavicka']:
                        assert len(next(cr)) == 0 # prazdny radek po hlavicce
                        hd = tuple(next(cr))
                        tpmap = najdi_typy(hd, mapping['typy'])
                        tp = tblmap[hd] # document type
                        f = open(get_fn(ds, tp), 'a')
                        cw = csv.writer(f)
                        continue
                        
                    if len(ln) == 0:
                        continue
                        
                    for k, v in tpmap.items():
                        for cln in v:
                            if k == 'date':
                                ln[cln] = fix_date(ln[cln])
                            elif k == 'numeric':
                                ln[cln] = fix_numeric(ln[cln])
                            elif k == 'ico':
                                ln[cln] = fix_ico(ln[cln])
                            else:
                                raise ValueError(k)

                    cw.writerow(ln)

        f.close()

