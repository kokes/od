#!/usr/bin/env python
# coding: utf-8

import csv
import json
import os
import zipfile
from contextlib import contextmanager
from datetime import datetime
from io import TextIOWrapper
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve


@contextmanager
def read_compressed(zipname, filename):
    burl = "http://www.psp.cz/eknih/cdrom/opendata/{}"
    with TemporaryDirectory() as tdir:
        tfn = os.path.join(tdir, "tmp.zip")
        urlretrieve(burl.format(zipname), tfn)
        with zipfile.ZipFile(tfn) as zf, zf.open(filename) as zfh:
            # tisky.unl maj encoding chyby
            yield TextIOWrapper(zfh, "cp1250", errors="ignore")


def read_compressed_csv(zf, fn, mp, partial):
    datetypes = {
        "date",
        "datetime(year to hour)",
        "datum",
        "datetime(year to minute)",
        "datetime(year to second, fraction)",
        "datetime year to hour",
        "datetime year to minute",
        "datetime year to day",
        "datetime(year to second)",
    }

    cols = [j["sloupec"] for j in mp]
    types = {j["sloupec"]: j["typ"] for j in mp}
    with read_compressed(zf, fn) as f:
        cr = csv.reader(f, delimiter="|")
        for j, el in enumerate(cr):
            if partial and j > 1000:
                break
            # UNL soubory maj jeden extra sloupec
            # TODO: zapnout tohle, az opravi schema sbirky
            # assert len(el) == len(cols) + 1, (el, cols)
            dt = {}
            for k, v in zip(cols, el):
                if v.strip() == "":
                    dt[k] = None
                elif types[k] in datetypes:
                    lv = len(v)
                    if lv == 10:
                        if "-" in v:
                            dt[k] = datetime.strptime(v, "%Y-%m-%d")
                        elif "." in v:
                            dt[k] = datetime.strptime(v, "%d.%m.%Y")
                        else:
                            raise ValueError(v)
                    elif lv == 13:
                        dt[k] = datetime.strptime(v, "%Y-%m-%d %H")
                    elif lv == 16:
                        dt[k] = datetime.strptime(v, "%Y-%m-%d %H:%M")
                    elif lv == 19:
                        # 2013-11-27 14:06:11
                        dt[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                    elif lv == 25:
                        # 1999-01-12 14:14:41.35000
                        dt[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        raise ValueError(v)
                else:
                    dt[k] = v

            yield dt


# je to kratky, tak neimplementuju `partial`
def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json"), encoding="utf-8") as f:
        mapping = json.load(f)

    for mp in mapping:
        tbl = f'{mp["tema"]}_{mp["tabulka"]}'
        tfn = os.path.join(outdir, f"{tbl}.csv")
        print(tbl)
        cols = [j["sloupec"] for j in mp["sloupce"]]
        with open(tfn, encoding="utf-8", mode="wt") as fw:
            cw = csv.DictWriter(fw, fieldnames=cols)
            cw.writeheader()
            for ffn in mp["soubory"]:
                # tohle nepujde s postgresou kvůli foreign keys, ale to neva
                if partial and ffn not in mp["soubory"][-2:]:
                    continue
                print("\t", ffn)
                zf, fn = ffn.split("/")
                for el in read_compressed_csv(zf, fn, mp["sloupce"], partial):
                    cw.writerow(el)


if __name__ == "__main__":
    main(".")
