import csv
import zipfile
import json
import os
import shutil
import zipfile
from urllib.request import urlopen
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
        with urlopen(url) as r, open(tfn, 'wb') as fw:
            shutil.copyfileobj(r, fw)
    
    zf = zipfile.ZipFile(tfn)
    yield zf
    zf.close()


def extract_elements(zf, fn, nodename):
    if fn.lower().endswith('.xml'):
        with zf.open(fn) as f:
            et = lxml.etree.parse(f).getroot()
            ns = et.nsmap[None]

        for node in et.iterfind(f'./{{{ns}}}{nodename}'):
            yield dict((j.tag[j.tag.rindex('}')+1:], j.text) for j in node.iterchildren())
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
    print(volby)
    csv_dir = f'data/csv/{volby}'
    os.makedirs(csv_dir, exist_ok=True)
    
    fnmap = {}
    for ds, spec in mp['ds'].items():
        for fn in spec['fn']:
            fnmap[fn] = (ds, spec)
        
        sch.append(f'''drop table if exists od.volby_{volby}_{ds};\ncreate table od.volby_{volby}_{ds} (datum date,
{" varchar not null,".join(spec['schema'])} varchar not null);
''')
    for datum, urls in mp['url'].items():
        print('\t', datum)
        for url in urls:
            with load_remote_data(url) as zf:
                for ff in map(lambda x: x.filename, zf.filelist):
                    if ff not in fnmap: continue
                    ds, fmp = fnmap[ff]
                    tfn = os.path.join(csv_dir, f'{datum}_{ds}.csv')
                    qq.append(f"echo {tfn}\ncat {tfn} | psql -c 'copy od.volby_{volby}_{ds} from stdin csv header'")
                    if os.path.isfile(tfn): continue # TODO: smaz
                    with open(tfn, 'w') as fw:
                        cw = csv.DictWriter(fw, fieldnames=['DATUM'] + fmp['schema'])
                        cw.writeheader()
                        for el in extract_elements(zf, ff, fmp['klic']):
                            cw.writerow({
                                'DATUM': datum,
                                **el,
                            })

with open('init_raw.sql', 'w') as f:
    f.write('\n'.join(sch))
    
with open('copy.sh', 'w') as f:
    f.write('psql < init.sql\n')
    f.write('\n'.join(qq))
