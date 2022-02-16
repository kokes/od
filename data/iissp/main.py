import csv
import gzip
import os
from datetime import date
from typing import List
from urllib.request import Request, urlopen

import lxml.etree
from tqdm import tqdm

url = "https://monitor.statnipokladna.cz/data/xml/ucjed.xml"
table_name = "ucetni_jednotky"


def resources() -> List[str]:
    return [url]


# XSD nema vsechno, dafuq
cols = [
    "ucjed_id",
    "csuis_ucjed_id",
    "ico",
    "start_date",
    "end_date",
    "nazev",
    "dic",
    "adresa",
    "nuts_id",
    "zrizovatel_id",
    "zrizovatel_ico",
    "cofog_id",
    "isektor_id",
    "kapitola_id",
    "nace_id",
    "druhuj_id",
    "poddruhuj_id",
    "konecplat",
    "forma_id",
    "katobyv_id",
    "stat_id",
    "zdrojfin_id",
    "druhrizeni_id",
    "veduc_id",
    "zuj",
    "sidlo",
    "zpodm_id",
    "kod_pou",
    "typorg_id",
    "pocob",
    "kraj",
    "obec",
    "ulice",
    "kod_rp",
    "datumakt",
    "aktorg_id",
    "datumvzniku",
    "psc",
    "pou_id",
    "orp_id",
    "zuj_id",
]

dates = "start_date, end_date, konecplat, datumakt, datumvzniku".split(", ")


def main(outdir: str, partial: bool = False):
    target_file = os.path.join(outdir, f"{table_name}.csv")
    request = Request(url, headers={"Accept-Encoding": "gzip"})
    with urlopen(request, timeout=60) as f, open(
        target_file, "w", encoding="utf8"
    ) as fw:
        if f.info().get("Content-Encoding") == "gzip":
            f = gzip.GzipFile(fileobj=f)

        cw = csv.DictWriter(fw, fieldnames=cols)
        cw.writeheader()

        et = lxml.etree.iterparse(f)

        for num, (action, element) in tqdm(enumerate(et)):
            if partial and num > 4e5:
                break

            assert action == "end", action

            if element.tag != "row":
                continue

            row = {j.tag: j.text for j in element.getchildren()}

            if row["zrizovatel_ico"] == "Chybí":
                row["zrizovatel_ico"] = None

            if "_" in row["ico"]:
                print(
                    "preskakuju {}, nema spravne ico ({})".format(
                        row["nazev"], row["ico"]
                    )
                )
                continue

            for datecol in dates:
                if (
                    not row[datecol]
                    or row[datecol] == "00000000"
                    or row[datecol] == "9999-12-31"
                ):
                    row[datecol] = None
                    continue

                row[datecol] = date.fromisoformat(row[datecol])

            cw.writerow(row)
            element.clear()


if __name__ == "__main__":
    main(".")
