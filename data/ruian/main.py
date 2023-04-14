import csv
import os
import zipfile
from io import TextIOWrapper
from tempfile import TemporaryDirectory
from urllib.request import urlopen, urlretrieve

import lxml.etree
import pyproj
from shapely.geometry import Point
from shapely.ops import transform
from tqdm import tqdm

# RSS feed for data
URL = "https://atom.cuzk.cz/RUIAN-CSV-ADR-ST/datasetFeeds/CZ-00025712-CUZK_RUIAN-CSV-ADR-ST_1.xml"  # noqa

# https://www.cuzk.cz/Uvod/Produkty-a-sluzby/RUIAN/2-Poskytovani-udaju-RUIAN-ISUI-VDP/Dopady-zmeny-zakona-c-51-2020-Sb/Adresni-mista-CSV_atributy.aspx
COLS = {
    "Kód ADM": "kod_adm",
    "Kód obce": "kod_obce",
    "Název obce": "nazev_obce",
    "Kód MOMC": "kod_momc",
    "Název MOMC": "nazev_momc",
    "Kód obvodu Prahy": "kod_obvodu_prahy",
    "Název obvodu Prahy": "nazev_obvodu_prahy",
    "Kód části obce": "kod_casti_obce",
    "Název části obce": "nazev_casti_obce",
    "Kód ulice": "kod_ulice",
    "Název ulice": "nazev_ulice",
    "Typ SO": "typ_so",
    "Číslo domovní": "cislo_domovni",
    "Číslo orientační": "cislo_orientacni",
    "Znak čísla orientačního": "znak_cisla_orientacniho",
    "PSČ": "psc",
    "Souřadnice Y": "souradnice_y",
    "Souřadnice X": "souradnice_x",
    "Platí Od": "plati_od",
    "Zeměpisná šířka": "zemepisna_sirka",
    "Zeměpisná délka": "zemepisna_delka",
}


def read_compressed():
    response = urlopen(URL).read()
    et = lxml.etree.fromstring(response)
    burl = et.find("./entry/link", namespaces=et.nsmap).attrib["href"]
    print("Stahuji soubor ", burl)

    with TemporaryDirectory() as tdir:
        tfn = os.path.join(tdir, "tmp.zip")
        urlretrieve(burl, tfn)
        with zipfile.ZipFile(tfn) as zf:
            for f in tqdm(zf.namelist()):
                with zf.open(f, "r") as infile:
                    yield TextIOWrapper(infile, "cp1250")


def main(outdir: str, partial: bool = False):
    wgs84 = pyproj.CRS("EPSG:4326")
    jtsk = pyproj.CRS("EPSG:5514")

    project = pyproj.Transformer.from_crs(jtsk, wgs84, always_xy=True).transform

    ofn = os.path.join(outdir, "adresni_mista.csv")

    with open(ofn, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLS.values(), lineterminator="\n")
        writer.writeheader()

        for i, f in enumerate(read_compressed()):
            if partial and i > 100:
                break
            cr = csv.DictReader(f, delimiter=";")
            for row in cr:
                if row["Souřadnice Y"] != "":
                    # coordinates in RUIAN and S-JTSK system have negative values
                    ruain_pt = Point(
                        float(row["Souřadnice Y"]) * -1, float(row["Souřadnice X"]) * -1
                    )
                    utm_point = transform(project, ruain_pt)
                    row["Zeměpisná šířka"] = utm_point.y
                    row["Zeměpisná délka"] = utm_point.x
                else:
                    row["Zeměpisná šířka"] = None
                    row["Zeměpisná délka"] = None

                writer.writerow({COLS[k]: v for k, v in row.items()})


if __name__ == "__main__":
    main(".")
