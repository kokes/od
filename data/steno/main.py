import os
import csv
import zipfile
import re
from glob import glob
from collections import Counter
from contextlib import closing
from tempfile import TemporaryDirectory
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin
from urllib.error import HTTPError

import lxml.html
from tqdm import tqdm

urls = {
    2010: 'https://www.psp.cz/eknih/2010ps/stenprot/zip/index.htm',
    2013: 'https://www.psp.cz/eknih/2013ps/stenprot/zip/index.htm',
    2017: 'https://www.psp.cz/eknih/2017ps/stenprot/zip/',
}


poz = []
cdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cdir, 'pozice.txt'), encoding='utf8') as f:
    for ln in f:
        poz.append(ln.strip())

# TODO: testy
def depozicuj(jmeno):
    if jmeno.startswith('Pan '):
        return None, jmeno[4:]

    for p in poz:
        if jmeno.startswith(p + " ČR"):
            return p + " ČR", jmeno[len(p)+3+1:]
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
        ps = ht.cssselect('p')

        for j, p in enumerate(ps):
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
                # v posledni iteraci je treba flushnout posledniho recnika, takze
                # nemuzem preskocit iteraci v tuhle chvili
                if j < len(ps) - 1:
                    continue

            if len(buf) > 0:
                yield {
                    'autor': aut,
                    'funkce': fun,
                    'schuze': int(re.match(r'^\d+', os.path.split(zf.filename)[1]).group()),
                    'soubor': zfn.filename,
                    'datum': None, # TODO: dokazem ziskat datum z tech detailnich stranek
                    'tema': tema, # TODO: tema je v <b>
                    'text': '\n'.join(buf)
                }

            if od is not None:
                fun, aut = depozicuj(od.text_content().strip())
                with open("autori.txt", "a+") as fw:
                    fw.write(f"{od.text_content().strip()};{fun};{aut}\n")
                buf = [pt[len(od.text_content())+1:].strip()] # pridame soucasny text (ale odseknem autora)


def main(outdir: str, partial: bool = False):
    lnm = Counter()
    for rok, url in urls.items():
        with urlopen(url) as r:
            ht = lxml.html.parse(r).getroot()

        with TemporaryDirectory() as tmpdir:
            for num, ln in enumerate(tqdm(ht.cssselect('div#main-content a'), desc=f'stahovani ({rok})')):
                if partial and num > 3:
                    break
                tfn = os.path.join(tmpdir, os.path.basename(ln.attrib['href']))
                try:
                    furl = urljoin(url, ln.attrib['href'])
                    urlretrieve(furl, tfn)
                except HTTPError:
                    print(f'nepodaril se stahnout stenoprotokol na adrese {furl} (odkazovan na {url})')

            tdir = os.path.join(outdir, "psp")
            os.makedirs(tdir, exist_ok=True)
            csv_fn = os.path.join(tdir, f'{rok}.csv')

            with open(csv_fn, 'w', encoding='utf8') as fw:
                cw = csv.DictWriter(fw, fieldnames=['rok', 'datum', 'schuze', 'soubor', 'autor', 'funkce', 'tema', 'text'])
                cw.writeheader()
                for fn in tqdm(glob(os.path.join(tmpdir, '*.zip')), desc=f'parsovani ({rok})'):
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

if __name__ == "__main__":
    main(".")
