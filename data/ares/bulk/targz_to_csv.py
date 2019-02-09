import tarfile
import lxml.etree
import json, csv
import os

vstupy = '.'
vystupy = '.'


def attr(root, parts):
    ret = []
    for j in parts:
        el = root.find('./are:%s' % j, namespaces=et.nsmap)
        if el is None:
            ret.append(None)
        else:
            ret.append(el.text)

    return ret


def obj(root):
    if root is None:
        return None
    els = {j.tag: j.text for j in root.getchildren()}
    els = {j[j.rindex('}') + 1:]: k for j, k in els.items()}

    return json.dumps(els, ensure_ascii=False)


def organi(root, ico):
    nazev = root.find('./are:Nazev', namespaces=et.nsmap).text

    fosoby, posoby = [], []
    for cl in root.findall('./are:Clen', namespaces=et.nsmap):
        rw = [ico]
        dza = cl.attrib.get('dza', None)
        dvy = cl.attrib.get('dvy', None)
        nf = cl.find('./are:funkce/are:nazev', namespaces=et.nsmap)
        if nf is not None:
            nf = nf.text

        rw.extend([nazev, dza, dvy, nf])

        fosoba = cl.find('./are:fosoba', namespaces=et.nsmap)
        posoba = cl.find('./are:posoba', namespaces=et.nsmap)
        if fosoba is None and posoba is None:
            continue  # chybí oboje, třeba u 00049549

        if fosoba is not None:
            rw.extend(
                attr(fosoba, ['jmeno', 'prijmeni', 'titulPred', 'titulZa']))
            rw.append(obj(fosoba.find('./are:adresa', namespaces=et.nsmap)))
            rw.append(obj(fosoba.find('./are:bydliste', namespaces=et.nsmap)))
            fosoby.append(rw)
        else:
            rw.extend(attr(posoba, ['ObchodniFirma', 'ICO']))
            rw.append(obj(posoba.find('./are:adresa', namespaces=et.nsmap)))
            posoby.append(rw)

    return {'fosoby': fosoby, 'posoby': posoby}


# -----------------------------------------------------------------------------

with tarfile.open(os.path.join(
        vstupy, 'ares_vreo_all.tar.gz'), 'r:gz') as tf, open(
            os.path.join(vystupy, 'firmy.csv'), 'w', encoding='utf8') as ud, open(
                os.path.join(vystupy, 'fosoby.csv'), 'w', encoding='utf8') as fo, open(
                    os.path.join(vystupy, 'posoby.csv'), 'w', encoding='utf8') as po:
    udc = csv.writer(ud)
    foc = csv.writer(fo)
    poc = csv.writer(po)

    cols = [
        'zdroj', 'aktualizace_db', 'datum_vypisu', 'cas_vypisu', 'typ_vypisu',
        'rejstrik', 'ico', 'obchodni_firma', 'datum_zapisu', 'datum_vymazu',
        'sidlo'
    ]
    udc.writerow(cols)
    foc.writerow([
        'ico', 'nazev_organu', 'datum_zapisu', 'datum_vymazu', 'nazev_funkce',
        'jmeno', 'prijmeni', 'titul_pred', 'titul_za', 'adresa', 'bydliste'
    ])
    poc.writerow([
        'ico', 'nazev_organu', 'datum_zapisu', 'datum_vymazu', 'nazev_funkce',
        'obchodni_firma', 'ico_organ', 'adresa'
    ])

    for rw, el in enumerate(tf):
        if rw % 5000 == 0:
            print(' %d' % rw, end='\r')

        fl = tf.extractfile(el)
        et = lxml.etree.fromstring(fl.read())

        odp = et.findall('./are:Odpoved', namespaces=et.nsmap)
        assert len(odp) == 1

        # muze jich byt vic, ale to jsou odstepne zavody, ktere neresime
        vypis = odp[0].find('.//are:Vypis_VREO', namespaces=et.nsmap)
        if vypis is None:
            print(el.name, 'is not a valid record')
            continue

        dt = [el.name]
        ch = [j.tag for j in vypis.getchildren()]
        ch = [j[j.rindex('}') + 1:] for j in ch]

        sekce = set(
            ['Uvod', 'Zakladni_udaje', 'Statutarni_organ', 'Jiny_organ'])
        if len(set(ch).difference(sekce)) > 0:
            raise ValueError(' '.join(ch))

        uvod = vypis.find('./are:Uvod', namespaces=et.nsmap)
        uvod_cols = ['Aktualizace_DB', 'Datum_vypisu', 'Cas_vypisu', 'Typ_vypisu']

        dt.extend(attr(uvod, uvod_cols))

        zakl = vypis.find('./are:Zakladni_udaje', namespaces=et.nsmap)

        # pro pozdejsi pouziti u vazebnych tabulek
        ico_el = zakl.find('./are:ICO', namespaces=et.nsmap)

        if ico_el is None:
            # odštěpné závod nemívají IČO
            ico = os.path.split(el.name)[1][:8]
        else:
            ico = ico_el.text

        zakl_cols = ['Rejstrik', 'ICO', 'ObchodniFirma', 'DatumZapisu', 'DatumVymazu']
        zi = attr(zakl, zakl_cols)
        # někde chybí IČO jako element (např. odštěpný závod GEAM)
        zi[1] = ico if zi[1] is None else zi[1]

        dt.extend(zi)
        dt.append(obj(zakl.find('./are:Sidlo', namespaces=et.nsmap)))

        # zapis dat do master tabulky
        udc.writerow(dt)

        st = vypis.findall('./are:Statutarni_organ', namespaces=et.nsmap)
        jo = vypis.findall('./are:Jiny_organ', namespaces=et.nsmap)

        for rr in ([] if st is None else st) + ([] if jo is None else jo):
            org = organi(rr, ico)
            for j in org['fosoby']:
                foc.writerow(j)
            for j in org['posoby']:
                poc.writerow(j)
