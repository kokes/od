import csv
import gzip
import json
import os
from urllib.request import urlopen

import lxml.etree

URL = "https://www.czechpoint.cz/spravadat/ovm/datafile.do?format=xml&service=seznamovm"

COLS = [
    "Zkratka",
    "ICO",
    "Nazev",
    "AdresaUradu",
    "Email",
    "TypSubjektu",
    "PravniForma",
    "PrimarniOvm",
    "IdDS",
    "TypDS",
    "StavDS",
    "StavSubjektu",
    "DetailSubjektu",
    "IdentifikatorOvm",
    "KategorieOvm",
]


def obj(root):
    children = root.getchildren()
    if not children:
        return root.text
    ret = {}
    for el in children:
        tag = el.tag.rpartition("}")[-1]
        ret[tag] = obj(el)

    return ret


def arr(root):
    return [obj(k) for k in root.getchildren()]


def main(outdir: str, partial: bool = False):
    with urlopen(URL) as r, open(
        os.path.join(outdir, "subjekty.csv"), "wt", encoding="utf-8"
    ) as fw:
        cw = csv.DictWriter(fw, fieldnames=COLS, lineterminator="\n")
        cw.writeheader()

        gr = gzip.open(r)
        et = lxml.etree.iterparse(gr)
        for j, (action, element) in enumerate(et):
            assert action == "end"

            if partial and j > 1000:
                break

            if not element.tag.endswith("}Subjekt"):
                continue
            row = {}
            for child in element.getchildren():
                tag = child.tag.rpartition("}")[-1]
                if tag == "Email":
                    row[tag] = arr(child)
                else:
                    row[tag] = obj(child)

            row = {
                k: json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
                for k, v in row.items()
            }
            row["PrimarniOvm"] = {"Ano": True, "Ne": False, None: None}[
                row.get("PrimarniOvm")
            ]
            cw.writerow(row)
            element.clear()


if __name__ == "__main__":
    main(".")
