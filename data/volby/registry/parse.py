import csv
import zipfile
import json
import os
import shutil
import sys
import zipfile
from fnmatch import fnmatch
from urllib.request import urlopen, Request
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import lxml.etree
from dbfread import DBF

@contextmanager
def load_remote_data(url: str):
    raw_dir = 'data/raw'
    os.makedirs(raw_dir, exist_ok=True)
    fn = os.path.basename(url)
    tfn = os.path.join(raw_dir, fn)
    if not os.path.isfile(tfn):
        req = Request(url, headers={'User-Agent': 'https://github.com/kokes/od'})
        with urlopen(req) as r, open(tfn, 'wb') as fw:
            shutil.copyfileobj(r, fw)
    
    zf = zipfile.ZipFile(tfn)
    yield zf
    zf.close()


def extract_elements(zf, fn, nodename):
    if fn.lower().endswith('.xml'):
        with zf.open(fn) as f:
            et = lxml.etree.iterparse(f)

            for _, node in et:
                if not node.tag.endswith(f'}}{nodename}'):
                    continue

                yield dict((j.tag[j.tag.rindex('}')+1:], j.text) for j in node.iterchildren())
                node.clear()

    elif fn.lower().endswith('dbf'):
        with zf.open(fn) as f, NamedTemporaryFile() as temp:
            shutil.copyfileobj(f, temp)  # dbfread neumi cist z filehandleru, https://github.com/olemb/dbfread/issues/25
            temp.flush()
            d = DBF(temp.name, encoding='cp852')
            yield from d
    else:
        raise NotImplementedError(fn)


with open('mapping.json') as f:
    mps = json.load(f)

qq = []
sch=[]
for volby, mp in mps.items():
    if len(sys.argv) > 1 and volby not in sys.argv[1:]: continue
    print(volby)
    csv_dir = f'data/csv/{volby}'
    os.makedirs(csv_dir, exist_ok=True)
    
    fnmap = {}
    for ds, spec in mp['ds'].items():
        for fn in spec['fn']:
            fnmap[fn] = (ds, spec)
        
        sch.append(f'''drop table if exists volby.{volby}_{ds};\ncreate table volby.{volby}_{ds} (datum date,
{" varchar not null,".join(spec['schema'])} varchar not null);
''')
    for datum, urls in mp['url'].items():
        print('\t', datum)
        for url in urls:
            with load_remote_data(url) as zf:
                for ff in map(lambda x: x.filename, zf.filelist):
                    patterns = [j for j in fnmap.keys() if fnmatch(ff, j)]
                    if len(patterns) == 0: continue
                    if len(patterns) > 1:
                        raise KeyError('ambiguous keys: {}'.format(patterns))

                    ds, fmp = fnmap.get(patterns[0])
                    tfn = os.path.join(csv_dir, f'{datum}_{ds}.csv')
                    qq.append(f"echo {tfn}\ncat {tfn} | psql -c 'copy volby.{volby}_{ds} from stdin csv header'")
                    fnexists = os.path.isfile(tfn)
                    with open(tfn, 'a+', encoding='utf8') as fw:
                        cw = csv.DictWriter(fw, fieldnames=['DATUM'] + fmp['schema'] + fmp.get('extra_schema', []))
                        if not fnexists:
                            cw.writeheader()
                        for el in extract_elements(zf, ff, fmp['klic']):
                            for k in fmp.get('vynechej', []):
                                el.pop(k, None)

                            # TODO: TEST: HLASY_01 vs. HLASY_K1
                            hk = [k for k in el.keys() if k.startswith('HLASY_') and k.partition('_')[-1].isdigit()]
                            if hk:
                                strany, hlasy = [], []
                                for k in hk:
                                    hlasy.append(el[k] or 0)
                                    del el[k]

                                # pg array representation - '{a, b, c}'
                                el['HLASY'] = '{{{}}}'.format(','.join(map(str, hlasy)))

                            cw.writerow({
                                'DATUM': datum,
                                **el,
                            })

with open('init_raw.sql', 'w', encoding='utf8') as f:
    f.write('\n'.join(sch))
    
with open('copy.sh', 'w', encoding='utf8') as f:
    f.write('psql < init.sql\n')
    f.write('\n'.join(sorted(list(set(qq)))))
