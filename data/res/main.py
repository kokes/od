import csv
import gzip
import io
import logging
import os
from contextlib import contextmanager
from urllib.request import Request, urlopen

CLS_BASE_URL = "https://apl.czso.cz/iSMS/do_cis_export"
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

COLMAP = {
    "ICO": "ico",
    "OKRESLAU": "okres_lau",
    "DDATVZN": "datum_vznik",
    "DDATZAN": "datum_zanik",
    "ZPZAN": "zpusob_zanik",
    "DDATPAKT": "datum_aktualizace",
    "FORMA": "pravni_forma",
    "ROSFORMA": "pravni_forma_ros",
    "KATPO": "kategorie_zamestnanci",
    "NACE": "nace",
    "ICZUJ": "ic_zuj",
    "FIRMA": "firma",
    "CISS2010": "esa2010",
    "KODADM": "adresni_misto",
    "TEXTADR": "adresa",
    "PSC": "psc",
    "OBEC_TEXT": "obec",
    "COBCE_TEXT": "cast_obce",
    "ULICE_TEXT": "ulice",
    "TYPCDOM": "typ_cislo_domovni",
    "CDOM": "cislo_domovni",
    "COR": "cislo_orientacni",
    "DATPLAT": "datum_platnost",
    "PRIZNAK": "priznak",
    # nace
    "ZDRUD": "zdroj_udaj",
    "KODCIS": "kod_ciselnik",
    "HODN": "hodnota",
}


@contextmanager
def open_remote_gzipped(url: str, partial: bool):
    req = Request(url)
    req.add_header("Accept-Encoding", "gzip")
    with urlopen(req, timeout=HTTP_TIMEOUT) as r:
        enc = "utf-8"
        if "windows-1250" in r.headers.get("content-type", ""):
            enc = "cp1250"
        if r.headers["Content-Encoding"] == "gzip":
            yield gzip.open(r, "rt", encoding=enc)
        else:
            yield io.TextIOWrapper(r, encoding=enc)


def main(outdir: str, partial: bool = False):
    logging.getLogger().setLevel(logging.INFO)
    cls_data = dict()
    for cls_url in CLS_URLS:
        logging.info("Nacitam %s", cls_url)
        with open_remote_gzipped(cls_url, partial) as r:
            cr = csv.DictReader(r)
            for row in cr:
                # jsou dva typy ciselniku, tak musime nacitat hodnoty z ruznych klicu
                kodcis = row.get("KODCIS", row.get("kodcis", row.get("ciselnik")))
                chodnota = row.get(
                    "CHODNOTA", row.get("chodnota", row.get("kod_polozky"))
                )
                text = row.get("TEXT", row.get("text"))

                if not (kodcis and chodnota and text):
                    raise ValueError(f"nerozumim radce v {cls_url}: {row}")

                cls_data[(int(kodcis), chodnota)] = text

    logging.info("Ciselniky hotove")

    for url, filename in [DATA, NACE]:
        logging.info("Nacitam %s", url)
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
                    header = [COLMAP[j] for j in row.keys()]
                    cw = csv.DictWriter(fw, fieldnames=header, lineterminator="\n")
                    cw.writeheader()
                cw.writerow({COLMAP[k]: v for k, v in row.items()})


if __name__ == "__main__":
    main(".")
