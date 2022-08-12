import codecs
import csv
import os
import ssl
import zipfile
from datetime import date
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve

header = {
    "Evidenční číslo dotace": "evidencni_cislo_dotace",
    "Identifikator dotace": "identifikator_dotace",
    "Název dotace": "nazev_dotace",
    "Účastník": "ucastnik",
    "IČ účastníka": "ic_ucastnika",
    "Účel dotace": "ucel_dotace",
    "Poskytovatel dotace": "poskytovatel_dotace",
    "IČ poskytovatele": "ic_poskytovatele",
    "Částka požadovaná": "castka_pozadovana",
    "Částka schválená": "castka_schvalena",
    "Datum poskytnutí dotace": "datum_poskytnuti",
}


def main(outdir: str, partial: bool = False):
    ssl._create_default_https_context = ssl._create_unverified_context
    with TemporaryDirectory() as tmpdir:
        rawpath = os.path.join(tmpdir, "raw.zip")
        urlretrieve(
            "https://data.mfcr.cz/katalog/sites/default/files/"
            "DotInfo_report_31_01_2022_0.zip",
            rawpath,
        )

        with zipfile.ZipFile(rawpath) as zf, zf.open(
            "DotInfo_report_31_01_2022_IIb.csv"
        ) as f, open(os.path.join(outdir, "dotace.csv"), "w", encoding="utf8") as fw:
            ut = codecs.iterdecode(f, encoding="cp1250")
            cr = csv.DictReader(ut, delimiter=";")
            cw = csv.DictWriter(fw, fieldnames=header.values(), lineterminator="\n")
            cw.writeheader()
            exphd = set(header.keys())
            for j, row in enumerate(cr):
                if partial and j > 1e3:
                    break
                if j == 0:
                    rem = set(row.keys()) - exphd
                    if rem:
                        print("vynechavame sloupce: ", rem)

                row = {k: None if v == "NULL" else v for k, v in row.items()}
                remapped = {header[k]: v for k, v in row.items() if k in header}

                if remapped["datum_poskytnuti"]:
                    day, month, year = remapped["datum_poskytnuti"].split(".")
                    remapped["datum_poskytnuti"] = date(
                        year=int(year), month=int(month), day=int(day)
                    )

                if remapped["ic_ucastnika"] and not remapped["ic_ucastnika"].isdigit():
                    print("nevalidni ICO", remapped["ic_ucastnika"])
                    remapped["ic_ucastnika"] = None

                if (
                    remapped["ic_poskytovatele"]
                    and not remapped["ic_poskytovatele"].isdigit()
                ):
                    print("nevalidni ICO", remapped["ic_poskytovatele"])
                    remapped["ic_poskytovatele"] = None

                cw.writerow(remapped)


if __name__ == "__main__":
    main(".")
