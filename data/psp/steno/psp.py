import os
import csv
import zipfile
import re
from glob import iglob
from collections import Counter
from contextlib import closing
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin
from urllib.error import HTTPError

import lxml.html

urls = {
    2010: 'https://www.psp.cz/eknih/2010ps/stenprot/zip/index.htm',
    2013: 'https://www.psp.cz/eknih/2013ps/stenprot/zip/index.htm',
    2017: 'https://www.psp.cz/eknih/2017ps/stenprot/zip/'
}


poz = []
with open('pozice.txt', encoding='utf8') as f:
    for ln in f:
        poz.append(ln.strip())

def depozicuj(jmeno):
    if jmeno.startswith('Pan '):
        return None, jmeno[4:]

    for p in poz:
        if jmeno.startswith(p):
            return p, jmeno[len(p)+1:]

    if 'ČR' in jmeno:
        ind = jmeno.rindex('ČR')
        return jmeno[:ind+2], jmeno[ind + 3:]
    
    return None, jmeno

def vyrok(zf):
    aut, fun, tema = None, None, None
    buf = []
    for zfn in zf.filelist:
        if not zfn.filename.startswith('s'):
            continue

        ht = lxml.html.parse(zf.open(zfn.filename)).getroot()

        for p in ht.cssselect('p'):
            pt = p.text_content().strip().replace('\xa0', ' ')
            if len(pt) == 0: continue

            # v textu je odkaz (autor), ve 2010 exportech je <b>autor</b>
            od = p.find('a')
            if p.find('b') is not None and p.find('b').text_content() != p.text_content():
                od = p.find('b')
            tp = p.find('b')
            
            if tp is not None and tp.text_content() == p.text_content():
                tema = tp.text_content().replace('\xa0', ' ').replace('\n', '')
                continue
            
            if od is None:
                buf += [pt]
                continue

            if len(buf) > 0:
                yield {
                    'autor': aut,
                    'funkce': fun,
                    'schuze': int(re.match(r'^\d+', zf.filename.rpartition('/')[-1]).group()),
                    'fn': zfn.filename,
                    'datum': None, # TODO: dokazem ziskat datum z tech detailnich stranek
                    'tema': tema, # TODO: tema je v <b>
                    'text': '\n'.join(buf)
                }

            fun, aut = depozicuj(od.text_content().strip())
            buf = [pt[len(od.text_content())+1:].strip()] # pridame soucasny text (ale odseknem autora)


lnm = Counter()
for rok, url in urls.items():
    raw_dir = f'data/raw/{rok}'
    os.makedirs(raw_dir, exist_ok=True)

    with urlopen(url) as r:
        ht = lxml.html.parse(r).getroot()

    for ln in ht.cssselect('div#main-content a'):
        tfn = os.path.join(raw_dir, os.path.basename(ln.attrib['href']))
        if os.path.isfile(tfn):
            continue
        try:
            furl = urljoin(url, ln.attrib['href'])
            urlretrieve(furl, tfn)
        except HTTPError:
            print('error:', furl)

    csv_dir = 'data/csv/'
    os.makedirs(csv_dir, exist_ok=True)
    csv_fn = os.path.join(csv_dir, f'{rok}.csv')

    with open(csv_fn, 'w', encoding='utf8') as fw:
        cw = csv.DictWriter(fw, fieldnames=['rok', 'datum', 'schuze', 'fn', 'autor', 'funkce', 'tema', 'text'])
        cw.writeheader()
        for fn in iglob(os.path.join(raw_dir, '*.zip')):
            try:
                with closing(zipfile.ZipFile(fn)) as zf:
                    for v in vyrok(zf):
                        cw.writerow({
                            'rok': rok,
                            **v,
                        })
                        # depozicovali jsme vse?
                        if v['autor'] and len(v['autor'].split(' ')) > 2:
                            lnm.update([(v['funkce'], v['autor'])])
                        
            except zipfile.BadZipFile:
                print('bad zip file:', fn)

# naparsovali jsme správně politické funkce?
print('\nJe možné, že následující osoby jsme nenaparsovali správně, a bude možná nutné'
      ' jejich funkce doplnit do souboru pozice.txt\n')
for (fn, jm), num in sorted(lnm.items(), key=lambda x: (x[0][0], x[0][1])):
    print('Funkce: {}, jméno: {} ({})'.format(fn, jm, num))
