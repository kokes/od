import csv
import json
import os
import tarfile
from tempfile import TemporaryDirectory
from urllib.request import urlopen, urlretrieve

import lxml.etree
import re

BASE_URL = "https://wwwinfo.mfcr.cz/ares/ares_vreo_all.tar.gz"


def attr(root, parts, nsmap):
    ret = []
    for j in parts:
        el = root.find("./are:%s" % j, namespaces=nsmap)
        if el is None:
            ret.append(None)
        else:
            ret.append(el.text)

    return ret

def attri(root, parts, nsmap, fnc):
    ret = []
    dat_d = {}
    for j in parts:
        el = root.findall("./are:%s" % j, namespaces=nsmap)
        if len(el) > 0:
            for x in fnc(el): 
                f_dict=json.loads(x)
                for k in f_dict.keys():
                    dat_d[k] = dat_d.get(k,"") + f_dict[k] + ";" 

    ret.append(json.dumps(dat_d,ensure_ascii=False))
    return ret

def obj(root, multiple_same_tag = False):
    if root is None:
        return None

    els = {}
    if multiple_same_tag:
        {els.setdefault(root.tag + j.tag, [] ).append(j.text.strip().replace('\n'," ").replace('\t'," ").replace('"','').replace(u'\xa0',' ')) for i,j in enumerate(root.getchildren())}
        pp = re.compile("\{.*\}(.+)\{.*\}(.+)")
        els = { pp.match(j).group(1) + pp.match(j).group(2) : ";".join(k) for j,k in els.items()}
    else:
        els = {j.tag : j.text.strip().replace('\n'," ").replace('\t'," ").replace('"','').replace(u'\xa0',' ') for j in root.getchildren()}
        els = {j[j.rindex("}") + 1 :]: k for j, k in els.items()}
    
    return json.dumps(els, ensure_ascii=False)

def list_obj(el):
    ret = []
    for eli in el:
        ret.append(obj(eli, True))
    return ret

def organi(root, ico, nsmap):
    nazev = root.find("./are:Nazev", namespaces=nsmap).text

    fosoby, posoby = [], []
    for cl in root.findall("./are:Clen", namespaces=nsmap):
        rw = [ico]
        dza = cl.attrib.get("dza", None)
        dvy = cl.attrib.get("dvy", None)
        nf = cl.find("./are:funkce/are:nazev", namespaces=nsmap)
        if nf is not None:
            nf = nf.text

        rw.extend([nazev, dza, dvy, nf])

        fosoba = cl.find("./are:fosoba", namespaces=nsmap)
        posoba = cl.find("./are:posoba", namespaces=nsmap)
        if fosoba is None and posoba is None:
            continue  # chybí oboje, třeba u 00049549

        if fosoba is not None:
            rw.extend(
                attr(fosoba, ["jmeno", "prijmeni", "titulPred", "titulZa"], nsmap)
            )
            rw.append(obj(fosoba.find("./are:adresa", namespaces=nsmap)))
            rw.append(obj(fosoba.find("./are:bydliste", namespaces=nsmap)))
            fosoby.append(rw)
        else:
            rw.extend(attr(posoba, ["ObchodniFirma", "ICO"], nsmap))
            rw.append(obj(posoba.find("./are:adresa", namespaces=nsmap)))
            posoby.append(rw)

    return {"fosoby": fosoby, "posoby": posoby}


def remote_data(partial):
    with TemporaryDirectory() as tdr:
        tfn = os.path.join(tdr, "ares_vreo_all.tar.gz")
        # pri castecnym loadu stahni jen megabyte
        if partial:
            with urlopen(BASE_URL) as r, open(tfn, "wb") as fw:
                fw.write(r.read(1000_000))
        else:
            urlretrieve(BASE_URL, tfn)
        with tarfile.open(tfn, "r:gz") as tf:
            try:
                for el in tf:
                    yield (el, tf.extractfile(el).read())
            except EOFError:
                if partial:
                    return
                raise


def main(outdir: str, partial: bool = False):
    with open(os.path.join(outdir, "firmy.csv"), "w", encoding="utf8") as ud, open(
        os.path.join(outdir, "fosoby.csv"), "w", encoding="utf8"
    ) as fo, open(os.path.join(outdir, "posoby.csv"), "w", encoding="utf8") as po:
        udc = csv.writer(ud, lineterminator="\n")
        foc = csv.writer(fo, lineterminator="\n")
        poc = csv.writer(po, lineterminator="\n")

        cols = [
            "zdroj",
            "aktualizace_db",
            "datum_vypisu",
            "cas_vypisu",
            "typ_vypisu",
            "rejstrik",
            "ico",
            "obchodni_firma",
            "datum_zapisu",
            "datum_vymazu",
            "sidlo",
            "cinnosti",
        ]
        udc.writerow(cols)
        foc.writerow(
            [
                "ico",
                "nazev_organu",
                "datum_zapisu",
                "datum_vymazu",
                "nazev_funkce",
                "jmeno",
                "prijmeni",
                "titul_pred",
                "titul_za",
                "adresa",
                "bydliste",
            ]
        )
        poc.writerow(
            [
                "ico",
                "nazev_organu",
                "datum_zapisu",
                "datum_vymazu",
                "nazev_funkce",
                "obchodni_firma",
                "ico_organ",
                "adresa",
            ]
        )

        for rw, (el, fl) in enumerate(remote_data(partial)):
            et = lxml.etree.fromstring(fl)

            odp = et.findall("./are:Odpoved", namespaces=et.nsmap)
            assert len(odp) == 1

            # muze jich byt vic, ale to jsou odstepne zavody, ktere neresime
            vypis = odp[0].find(".//are:Vypis_VREO", namespaces=et.nsmap)
            if vypis is None:
                print(el.name, "is not a valid record")
                continue

            dt = [el.name]
            ch = [j.tag for j in vypis.getchildren()]
            ch = [j[j.rindex("}") + 1 :] for j in ch]

            # TODO: chybi zastoupeni dane PO jeji FO
            sekce = set(["Uvod", "Zakladni_udaje", "Statutarni_organ", "Jiny_organ"])
            if len(set(ch).difference(sekce)) > 0:
                raise ValueError(" ".join(ch))

            uvod = vypis.find("./are:Uvod", namespaces=et.nsmap)
            uvod_cols = [
                "Aktualizace_DB",
                "Datum_vypisu",
                "Cas_vypisu",
                "Typ_vypisu",
            ]

            dt.extend(attr(uvod, uvod_cols, et.nsmap))

            zakl = vypis.find("./are:Zakladni_udaje", namespaces=et.nsmap)

            # pro pozdejsi pouziti u vazebnych tabulek
            ico_el = zakl.find("./are:ICO", namespaces=et.nsmap)

            if ico_el is None:
                # odštěpné závod nemívají IČO
                ico = os.path.split(el.name)[1][:8]
            else:
                ico = ico_el.text

            zakl_cols = [
                "Rejstrik",
                "ICO",
                "ObchodniFirma",
                "DatumZapisu",
                "DatumVymazu",
            ]
            zi = attr(zakl, zakl_cols, et.nsmap)
            # někde chybí IČO jako element (např. odštěpný závod GEAM)
            zi[1] = ico if zi[1] is None else zi[1]

            dt.extend(zi)
            dt.append(obj(zakl.find("./are:Sidlo", namespaces=et.nsmap)))

            # zaznamy o predmetu cinnosti
            cinn = zakl.find("./are:Cinnosti", namespaces=et.nsmap)
            cinn_cols = [
                "PredmetPodnikani",
                "Ucel",
                "DoplnkovaCinnost",
                "PredmetCinnosti",
            ]

            pr = attri(cinn, cinn_cols, et.nsmap, list_obj) if cinn is not None else ['{}']
            dt.extend(pr)

            # zapis dat do master tabulky
            udc.writerow(dt)

            st = vypis.findall("./are:Statutarni_organ", namespaces=et.nsmap)
            jo = vypis.findall("./are:Jiny_organ", namespaces=et.nsmap)

            for rr in ([] if st is None else st) + ([] if jo is None else jo):
                org = organi(rr, ico, et.nsmap)
                for j in org["fosoby"]:
                    foc.writerow(j)
                for j in org["posoby"]:
                    poc.writerow(j)


if __name__ == "__main__":
    main(".")
