import csv
import gzip
import json
import os
import sys
import re
from datetime import date
from itertools import islice
from urllib.parse import urlparse
from urllib.request import urlretrieve, urlopen

import lxml.etree
from tqdm import tqdm


NON_ISO_DATUM = re.compile(r'^(\d{1,2})\.(\d{1,2})\.(\d{4})$')


def gen_schema(element, parent=None):
    ret = {}
    for j in element:
        ch = j.getchildren()
        if len(ch) > 0:
            ret[j.tag] = gen_schema(j, (parent or []) + [j.tag])
        elif hasattr(j, 'text') and j.text is None:
            pass
        else:
            ret[j.tag] = '/'.join((parent or []) + [j.tag])

    return ret


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def extrahuj(node, schema):
    ret = {}
    for k, v in schema.items():
        if isinstance(v, dict):
            ret[k] = extrahuj(node, v)
        else:
            ret[k] = getattr(node.find(v), 'text', None)

    return ret

def uprav_data(row, mapping):
    'Bude inlinovano behem refactoringu'
    for col in mapping.get('non_iso_datum', []):
        den, mesic, rok = NON_ISO_DATUM.match(row[col]).groups()
        row[col] = date(int(rok), int(mesic), int(den))

    return row


def nahraj_ds(url):
    fn = os.path.split(urlparse(url).path)[-1]
    tfn = os.path.join(rdir, fn)
    if not os.path.isfile(tfn):
        urlretrieve(url, tfn)

    with gzip.open(tfn) as f:
        et = lxml.etree.iterparse(f)
        yield from et


if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1e17

    # package_list a package_list_compact se asi lisi - ten nekompaktni endpoint nejde filtrovat??? Tak to asi udelame na klientovi
    year = date.today().year
    url_pl = 'https://dataor.justice.cz/api/3/action/package_list'

    r = urlopen(url_pl)
    dt = json.load(r)
    assert dt['success']

    dss = [ds for ds in dt['result'] if ds.endswith(
        '-{}'.format(year)) and '-full-' in ds]

    urls = []
    for ds in tqdm(dss):
        url = 'https://dataor.justice.cz/api/3/action/package_show?id={}'.format(
            ds)
        r = urlopen(url)
        dtp = json.load(r)
        assert dtp['success']
        ds_url = [j['url'] for j in dtp['result']
                  ['resources'] if j['url'].endswith('.xml.gz')]
        assert len(ds_url) == 1
        urls.append(ds_url[0])

    rdir = 'data/raw'
    cdir = 'data/csv'
    os.makedirs(rdir, exist_ok=True)
    os.makedirs(cdir, exist_ok=True)

    neumim = set()  #  TODO

    schemasd = dict()
    schema_autogen = dict()  # TODO
    fs = dict()
    csvs = dict()
    with open('xml_schema.json') as f:
        schemas = json.load(f)
        for el in schemas:
            udaje = [el['udaj']] if isinstance(el['udaj'], str) else el['udaj']
            if el.get('ignore'):
                for udaj in udaje:
                    schemasd[udaj] = el
                continue

            fn = el.get('soubor', el['udaj']).replace('/', '-') + '.csv'
            f = open(os.path.join(cdir, fn), 'w', encoding='utf8')
            cw = csv.DictWriter(
                f, fieldnames=['ico'] + list(el['schema'].keys()))
            cw.writeheader()

            for udaj in udaje:
                schemasd[udaj] = el
                fs[udaj] = f
                csvs[udaj] = cw

    fs['subjekty'] = open(os.path.join(cdir, 'subjekty.csv'), 'w', encoding='utf8')
    csvs['subjekty'] = csv.writer(fs['subjekty'])
    csvs['subjekty'].writerow(['ico', 'nazev', 'zapisDatum', 'vymazDatum'])

    for url in tqdm(urls):
        et = nahraj_ds(url)

        for action, el in islice(et, limit):  # sniz pro testovani
            assert action == 'end', action
            if el.tag != 'Subjekt':
                continue
            ch = {j.tag for j in el.getchildren()}
            dch = ch - {'ico', 'nazev', 'udaje', 'zapisDatum', 'vymazDatum'}
            assert len(dch) == 0, dch

            nazev = el.find('nazev').text
            zapis = el.find('zapisDatum').text
            vymaz = getattr(el.find('vymazDatum'), 'text', None)
            ico = getattr(el.find('ico'), 'text', None)
            if not ico:
                with open('chybejici_ico.log', 'a+') as fw:
                    fw.write(f'{nazev}\t{el.sourceline}\t{url}\n')
                continue

            csvs['subjekty'].writerow([ico, nazev, zapis, vymaz])

            for udaj_raw in el.find('udaje').iterchildren():
                # tohle je asi irelevantni, asi nas zajimaj jen podudaje??
                # beru zpet - tohle nas zajima prave tehdy, kdyz nemame podudaje
                # beru opet zpet - třeba u zastoupení v dozorčí radě nás zajímá obojí :(

                udaj_typ = udaj_raw.find('udajTyp/kod').text

                if udaj_typ not in schemasd:
                    neumim.add(udaj_typ)
                    continue

                if not schemasd[udaj_typ].get('ignore', False):
                    schema = schemasd[udaj_typ]['schema']
                    row = extrahuj(udaj_raw, schema)
                    row = uprav_data(row, schemasd[udaj_typ])
                    row = {k: json.dumps(v) if isinstance(v, dict) else v for k, v in row.items()}
                    row['ico'] = ico
                    csvs[udaj_typ].writerow(row)

                if udaj_raw.find('podudaje') is not None:
                    podudaje = udaj_raw.find('podudaje').getchildren()
                    podpodudaje = udaj_raw.find('podudaje/Udaj/podudaje')
                    if podpodudaje is not None:
                        podudaje += podpodudaje.getchildren()

                    for podudaj_raw in podudaje:
                        podudaj_typ = podudaj_raw.find('udajTyp/kod').text

                        if podudaj_typ not in schemasd:
                            neumim.add(podudaj_typ)
                            schema_autogen[podudaj_typ] = merge(gen_schema(
                                podudaj_raw), schema_autogen.get(podudaj_typ, {}))
                            continue

                        if not schemasd[podudaj_typ].get('ignore', False):
                            schema = schemasd[podudaj_typ]['schema']
                            row = extrahuj(podudaj_raw, schema)
                            row = uprav_data(row, schemasd[podudaj_typ])
                            row = {k: json.dumps(v) if isinstance(v, dict) else v for k, v in row.items()}
                            row['ico'] = ico
                            csvs[podudaj_typ].writerow(row)
                else:
                    pass  # TODO: handluj non-podudaje

            el.clear()

    for el in fs.values():
        el.close()

    with open('xml_schema_chybejici.json', 'w') as fw:
        json.dump(schema_autogen, fw, indent=2, ensure_ascii=False)
