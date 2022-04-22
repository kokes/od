#!/usr/bin/env python
import csv
import gzip
import json
import logging
import os
from urllib.parse import urlparse
from urllib.request import Request, urlopen

# TODO: mozna nebude treba, mozna budou URL nemenne
DATASETS_GRAPHQL_QUERY = (
    """
{
  datasets(limit: 100, filters: {isPartOf: "%s"}) {
    data {
      distribution {
        accessURL
      }
    }
    pagination {
      totalCount
    }
  }
}
"""
    % "https://data.gov.cz/zdroj/datové-sady/00006947/4e4762f06ca63a491efc360e793abc09"
)


DATASETS = ["prijemce", "dotace", "rozhodnuti", "rozpoctoveobdobi"]
ID_COLS = ("iriDotace", "iriPrijemce", "iriRozhodnuti", "iriRozpoctoveObdobi")


def remote_csv(url):
    with urlopen(url, timeout=30) as r, gzip.open(r, encoding="utf-8", mode="rt") as f:
        cr = csv.DictReader((line.replace("\0", "") for line in f), strict=True)
        yield from cr


def main(outdir: str, partial: bool = False):
    logging.getLogger().setLevel(logging.INFO)
    cdir = os.path.dirname(os.path.abspath(__file__))

    req = Request("https://data.gov.cz/graphql")
    req.add_header("content-type", "application/json")
    with urlopen(
        req, json.dumps({"query": DATASETS_GRAPHQL_QUERY}).encode(), timeout=10
    ) as r:
        distribution_urls = json.load(r)["data"]["datasets"]["data"]

    urls = []
    for dist in distribution_urls:
        csd = [j for j in dist["distribution"] if j["accessURL"].endswith("csv.gz")]
        assert len(csd) == 1, csd
        urls.append(csd[0]["accessURL"])

    fn_url_mapping = {urlparse(url).path.rpartition("/")[-1]: url for url in urls}

    with open(os.path.join(cdir, "ciselnik.json"), encoding="utf-8") as f:
        csmp = json.load(f)

    csl = dict()

    logging.info("Nacitam ciselniky")
    for cs in csmp:
        for ln in remote_csv(fn_url_mapping[cs["filename"]]):
            csl[ln[cs["id"]]] = ln[cs["nazev"]]

    for ds in DATASETS:
        logging.info("Nacitam %s", ds)
        tfn = os.path.join(outdir, f"{ds}.csv")
        with open(tfn, encoding="utf-8", mode="wt") as fw:
            for num, ln in enumerate(remote_csv(fn_url_mapping[f"{ds}.csv.gz"])):
                if num == 0:
                    clean_header = [
                        ("id" + j[3:] if j in ID_COLS else j)
                        for j in ln.keys()
                        if j is not None
                    ]
                    # TODO: trochu duplicity, dole delam to stejny
                    clean_header = [
                        (j[3].lower() + j[4:] if j.startswith("iri") else j)
                        for j in clean_header
                    ]
                    cw = csv.DictWriter(fw, fieldnames=clean_header)
                    cw.writeheader()
                if partial and num > 5e3:
                    break

                if None in ln:
                    raise ValueError(f"extra sloupce v souboru {ds}")

                # vypln info z ciselniku
                for k, v in ln.items():
                    # ID sebe samo nepotrebujem nahrazovat
                    # taky nenahrazujem cizi klic
                    # jen odsekneme vetsinu URL
                    if k in ID_COLS:
                        ln[k] = v.rpartition("/")[-1]
                        continue

                    if v.startswith("http://") or v.startswith("https://"):
                        # tohle proste spadne, kdyz bude chybet klasifikator
                        if v not in csl:
                            raise KeyError("chybi", k, v)
                            continue

                        ln[k] = csl[v]

                # iri -> id
                # u identifikatoru zmen z iriFoo na idFoo
                # u ciselniku zmen z iriFooBar na fooBar
                for key in list(ln.keys()):
                    if not key.startswith("iri"):
                        continue
                    val = ln[key]
                    new_key = key[3:]  # strip 'iri'
                    if key in ID_COLS:
                        ln["id" + new_key] = val
                    else:
                        ln[new_key[0].lower() + new_key[1:]] = val

                    del ln[key]

                cw.writerow(ln)


if __name__ == "__main__":
    main(".")
