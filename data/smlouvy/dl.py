import gzip
import os
import shutil
import hashlib
from glob import iglob
from urllib.request import urlopen
from urllib.parse import urlparse

import lxml.etree
from tqdm import tqdm

def hash_gzipped_file(fn: str) -> str:
    h = hashlib.sha1()
    with gzip.open(fn) as f:
        while True:
            dt = f.read(8192)
            if not dt:
                break

            h.update(dt)

    return h.hexdigest()

tdir = 'data/raw'
url = 'https://data.smlouvy.gov.cz/'

if __name__ == '__main__':
    os.makedirs(tdir, exist_ok=True)
    r = urlopen(url)
    et = lxml.etree.parse(r).getroot()

    keys = ['mesic', 'rok', 'hashDumpu', 'velikostDumpu', 'casGenerovani', 'dokoncenyMesic', 'odkaz']

    for el in tqdm(et):
        dt = {k: el.find(f'{{{et.nsmap[None]}}}{k}').text for k in keys}

        fn = os.path.split(dt['odkaz'])[-1]
        tfn = os.path.join(tdir, fn + '.gz')
        if not os.path.isfile(tfn) or dt['hashDumpu'] != hash_gzipped_file(tfn):
            # TODO: urlretrieve?
            r = urlopen(dt['odkaz'])
            with gzip.open(tfn, 'w') as gf:
                shutil.copyfileobj(r, gf)
