import csv
import io
import os
from urllib.request import urlopen

from lxml.etree import iterparse

HTTP_TIMEOUT = 10
XML_BASE_URL = (
    "https://www.szif.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2F"
    "dokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2Fspd{year}.xml"
)
CSV_BASE_URL_22 = (
    "https://szif.gov.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2F"
    "dokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2Fspd2022.csv"
)
CSV_BASE_URL = (
    "https://szif.gov.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2F"
    "dokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2Fspd{year}czk.csv"
)

URLS = {
    2017: XML_BASE_URL.format(year=2017),
    2018: XML_BASE_URL.format(year=2018),
    2019: XML_BASE_URL.format(year=2019),
    2020: XML_BASE_URL.format(year=2020),
    2021: XML_BASE_URL.format(year=2021),
    2022: CSV_BASE_URL_22,
    2023: CSV_BASE_URL.format(year=2023),
    2024: CSV_BASE_URL.format(year=2024),
}


def parse_xml(r, partial):
    et = iterparse(r)
    elyear = None
    for num, (action, element) in enumerate(et):
        if partial and num > 1e3:
            break
        assert action == "end"

        if element.tag != "zadatel":
            continue

        platba = {"rok": elyear}
        for key in ["jmeno_nazev", "obec", "okres"]:
            platba[key] = element.find(key).text

        for elplatba in element.findall("platby/platba") + element.findall(
            "platby_pvp/platba_pvp"
        ):
            for key in [
                "fond_typ_podpory",
                "opatreni",
                "zdroje_cr",
                "zdroje_eu",
                "celkem_czk",
            ]:
                platba[key] = getattr(elplatba.find(key), "text", None)

            yield platba

        element.clear()


def parse_csv(r, partial):
    tr = io.TextIOWrapper(r, encoding="utf8")
    cr = csv.DictReader(tr)
    for num, row in enumerate(cr):
        if partial and num > 1e3:
            break
        yield {
            "datum": row["Datum nabytí právní moci"],
            "jmeno_nazev": row["Jméno/Název"],
            "obec": row["Obec"],
            "okres": row["Okres"],
            "fond_typ_podpory": row["Typ fondu"],
            "opatreni": row["Opatření"],
            "zdroje_cr": row["Zdroje ČR"],
            "zdroje_eu": row["Zdroje EU"],
            "celkem_czk": row["Celkem CZK"],
        }


def parse_csv_czk(r, partial):
    tr = io.TextIOWrapper(r, encoding="utf8")
    cr = csv.DictReader(tr)
    for num, row in enumerate(cr):
        if partial and num > 1e3:
            break
        yield {
            "datum": row["Datum nabytí právní moci rozhodnutí"],
            "jmeno_nazev": row["Název příjemce (právnická osoba)"]
            or row["Příjmení a jméno příjemce"],
            "obec": row["Obec"],
            "okres": row["Okres (NUTS 4)"],
            "fond_typ_podpory": row["Fond"],
            "opatreni": row["Název opatření"],
            "zdroje_cr": row[
                "Celková částka spolufinancovaná pro tohoto příjemce EZZF"
            ],
            "zdroje_eu": row["Celková částka z EU pro tohoto příjemce"],
            "celkem_czk": row["Celkem EZZF a spolufinancované částky"],
        }


def main(outdir: str, partial: bool = False):
    with (
        open(os.path.join(outdir, "platby.csv"), "w", encoding="utf8") as fp,
    ):
        cp = csv.DictWriter(
            fp,
            [
                "rok",
                "datum",
                "jmeno_nazev",
                "obec",
                "okres",
                "fond_typ_podpory",
                "opatreni",
                "zdroje_cr",
                "zdroje_eu",
                "celkem_czk",
            ],
            lineterminator="\n",
        )

        cp.writeheader()

        for year, url in URLS.items():
            print(f"Downloading {year} data from {url}")
            with urlopen(url, timeout=HTTP_TIMEOUT) as r:
                if url.endswith(".xml"):
                    parser = parse_xml
                elif url.endswith("czk.csv"):
                    parser = parse_csv_czk
                elif url.endswith(".csv"):
                    parser = parse_csv
                else:
                    raise ValueError(f"Unknown file type: {url}")

                for platba in parser(r, partial):
                    platba["rok"] = year
                    cp.writerow(platba)
