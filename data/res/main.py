import csv
import gzip
import io
import os
from contextlib import contextmanager
from urllib.request import Request, urlopen

CLS_BASE_URL = "https://apl.czso.cz/iSMS/cisexp.jsp"
CLS_URLS = [
    CLS_BASE_URL + j
    for j in (
        "?kodcis=109&typdat=0&cisjaz=203&format=2&separator=%2C",
        "?kodcis=572&typdat=0&cisjaz=203&format=2&separator=%2C",
        "?kodcis=579&typdat=0&cisjaz=203&format=2&separator=%2C",
        "?kodcis=51&typdat=0&cisjaz=203&format=2&separator=%2C",
        "?kodcis=5161&typdat=0&cisjaz=203&format=2&separator=%2C",
        "?kodcis=73&typdat=0&cisjaz=203&format=2&separator=%2C",
        "?kodcis=564&typdat=0&cisjaz=203&format=2&separator=%2C",
    )
]

CLS_URLS.extend(
    [
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=CZ_NACE_RES",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=56",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=149",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=109",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=572",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=579",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=51",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=5161",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=73",
        "https://vdb.czso.cz/opendata/ciselniky/polozky?kod=564",
    ]
)

DATA = ("https://opendata.czso.cz/data/od_org03/res_data.csv", "subjekty.csv")
NACE = ("https://opendata.czso.cz/data/od_org03/res_pf_nace.csv", "nace.csv")
HTTP_TIMEOUT = 30


DS_CLS = {
    # res sloupce:
    "OKRESLAU": 109,
    "ZPZAN": 572,
    "FORMA": 56,
    "ROSFORMA": 149,
    "KATPO": 579,
    "NACE": 80004,
    "ICZUJ": 51,
    "CISS2010": 5161,
    # TODO: tohle bude chtit nacist RUIAN data z
    # https://nahlizenidokn.cuzk.cz/StahniAdresniMistaRUIAN.aspx
    # "adresni_misto":
    "TYPCDOM": 73,
    # nace sloupce:
    "ZDRUD": 564,
}


@contextmanager
def open_remote_gzipped(url: str, partial: bool):
    req = Request(url)
    req.add_header("Accept-Encoding", "gzip")
    with urlopen(req, timeout=HTTP_TIMEOUT) as r:
        if r.headers["Content-Encoding"] == "gzip":
            yield gzip.open(r, "rt", encoding="utf-8")
        else:
            yield io.TextIOWrapper(r, encoding="cp1250")


def main(outdir: str, partial: bool = False):
    cls_data = dict()
    for cls_url in CLS_URLS:
        with open_remote_gzipped(cls_url, partial) as r:
            cr = csv.DictReader(r)
            for row in cr:
                # jsou dva typy ciselniku, tak musime nacitat hodnoty z ruznych klicu
                kodcis = row.get("KODCIS", row.get("ciselnik"))
                chodnota = row.get("CHODNOTA", row.get("kod_polozky"))
                text = row.get("TEXT", row.get("text"))

                if not (kodcis and chodnota and text):
                    raise ValueError(f"nerozumim radce v {cls_url}: {row}")

                cls_data[(int(kodcis), chodnota)] = text

    for url, filename in [DATA, NACE]:
        path = os.path.join(outdir, filename)
        with open_remote_gzipped(url, partial) as r, open(
            path, "wt", encoding="utf-8"
        ) as fw:
            cr = csv.DictReader(r)
            for n, row in enumerate(cr):
                if partial and n > 1e5:
                    break
                for k, v in row.items():
                    if k not in DS_CLS or v == "":
                        continue

                    row[k] = cls_data[(DS_CLS[k], v)]

                if n == 0:
                    cw = csv.DictWriter(fw, fieldnames=row.keys(), lineterminator="\n")
                cw.writerow(row)


if __name__ == "__main__":
    main(".")
