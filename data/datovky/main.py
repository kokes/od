import csv
import gzip
import json
import os
from typing import List
from urllib.request import urlopen

import lxml.etree

BASE_URL = "https://www.mojedatovaschranka.cz/sds/datafile.do?format=xml&service="
urls = {
    "po": BASE_URL + "seznam_ds_po",
    "pfo": BASE_URL + "seznam_ds_pfo",
    "fo": BASE_URL + "seznam_ds_fo",
    "ovm": BASE_URL + "seznam_ds_ovm",
}


def resources() -> List[str]:
    return list(urls.values())


mapping = {
    "id": "id",
    "type": "type",
    "subtype": "subtype",
    "firstName": "name/person/firstName",
    "lastName": "name/person/lastName",
    "middleName": "name/person/middleName",
    "tradeName": "name/tradeName",
    "ico": "ico",
    "address": {
        "code": "address/code",
        "city": "address/city",
        "district": "address/district",
        "street": "address/street",
        "cp": "address/cp",
        "co": "address/co",
        "ce": "address/ce",
        "zip": "address/zip",
        "region": "address/region",
        "addressPoint": "address/addressPoint",
        "state": "address/state",
        "fullAddress": "address/fullAddress",
    },
    "pdz": "pdz",
    "ovm": "ovm",
    "hierarchy": {
        "isMaster": "hierarchy/isMaster",
        "masterId": "masterId",
    },
    "idOVM": "idOVM",
}


def strip_ns(el):
    return el.tag.rpartition("}")[-1]


def find_el(el, path):
    ns = el.nsmap[None]
    parts = path.split("/")
    fel = el.find("{{{}}}".format(ns) + ("/{{{}}}".format(ns)).join(parts))
    return getattr(fel, "text", None)


def parse_el(el, paths):
    ret = {}
    for k, v in paths.items():
        if isinstance(v, dict):
            ret[k] = parse_el(el, v)
        else:
            val = find_el(el, v)
            if val == "true":
                val = True
            elif val == "false":
                val = False
            if val is not None:
                ret[k] = val

    return ret if len(ret) > 0 else None


def parse_xml(source, target_fn, partial):
    with open(target_fn, "wt", encoding="utf8") as fw:
        et = lxml.etree.iterparse(source)
        cw = csv.DictWriter(fw, fieldnames=mapping.keys())
        cw.writeheader()

        for num, (_, el) in enumerate(et):
            if partial and num > 1e5:
                break
            if strip_ns(el) != "box":
                continue

            row = parse_el(el, mapping)
            row = {
                k: json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v
                for k, v in row.items()
            }
            cw.writerow(row)
            el.clear()


def main(outdir: str, partial: bool = False):
    tdir = os.path.join(outdir, "datovky")
    os.makedirs(tdir, exist_ok=True)
    for ds, url in urls.items():
        with urlopen(url, timeout=30) as r:
            assert r.headers.get("Content-Encoding") == "gzip"

            with gzip.open(r) as gr:
                target_fn = os.path.join(tdir, f"{ds}.csv")
                parse_xml(gr, target_fn, partial)


if __name__ == "__main__":
    main(".")
