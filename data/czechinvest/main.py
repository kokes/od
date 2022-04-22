import csv
import json
import os
from datetime import date, timedelta

import xlrd


def intuj(el):
    if isinstance(el, str) and len(el) == 0:
        return None

    if isinstance(el, str):
        el = el.rstrip(". ").replace(" ", "")

    return int(el)


mesic = {
    "březen": 3,
    "duben": 4,
    "květen": 5,
    "leden": 1,
    "listopad": 11,
    "prosinec": 12,
    "srpen": 8,
    "září": 9,
    "únor": 2,
    "červen": 6,
    "červenec": 7,
    "říjen": 10,
}


def mesicuj(el):
    if isinstance(el, str):
        return mesic[el.strip()]

    dt = date(1899, 12, 31) + timedelta(days=int(el) - 1)
    return dt.month


data_url = (
    "https://www.czechinvest.org/getattachment/Unsere-Dienstleistungen/"
    "Investitionsanreize/Udelene-investicni-pobidky.xls"
)

# partial neimplementujem, protoze to je stejne malinkaty


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "data", "mapping.json"), encoding="utf-8") as f:
        mapping = json.load(f)

    firmy = {}
    with open(os.path.join(cdir, "data", "slovnik.csv"), encoding="utf-8") as f:
        cr = csv.DictReader(f)
        for el in cr:
            firmy[el["firma"]] = int(el["ico"])

    wb_path = os.path.join(cdir, "Udelene-investicni-pobidky.xls")
    if not os.path.isfile(wb_path):
        raise IOError(
            "bohuzel czechinvest nechce moc davat lidem data v lidsky forme, takze "
            "si je musite napred stahnout v prohlizeci z "
            "https://www.czechinvest.org/cz/Sluzby-pro-investory/Investicni-pobidky"
        )

    wb = xlrd.open_workbook(wb_path)
    sh = wb.sheet_by_name("PROJEKTY")

    hd1 = [j.value for j in sh.row(1)]
    hd2 = [j.value for j in sh.row(2)]
    assert mapping["hd1"] == hd1, [
        (j, val, hd1[j]) for j, val in enumerate(mapping["hd1"]) if val != hd1[j]
    ]
    assert mapping["hd2"] == hd2, [
        (j, val, hd2[j]) for j, val in enumerate(mapping["hd2"]) if val != hd2[j]
    ]

    with open(os.path.join(outdir, "pobidky.csv"), "w", encoding="utf8") as fw:
        cw = csv.DictWriter(fw, fieldnames=mapping["tghd"])
        cw.writeheader()
        for rn in range(3, sh.nrows):
            row = [
                j.value.strip() if isinstance(j.value, str) else j.value
                for j in sh.row(rn)
            ]
            drow = dict(zip(mapping["tghd"], row))

            # posledni radek se sumou
            if drow["cislo"] == "":
                break

            for c in ["cislo", "ico", "nova_mista", "podani", "rozh_den", "rozh_rok"]:
                drow[c] = intuj(drow[c])

            if drow["ico"] is None:
                drow["ico"] = firmy[drow["firma"]]

            drow["rozh_mesic"] = mesicuj(drow["rozh_mesic"])
            drow["strop"] = None if drow["strop"] == "-" else drow["strop"]
            drow["msp"] = {"Ano": True, "Ne": False}[drow["msp"]]
            drow["zruseno"] = True if drow["zruseno"] == "x" else False

            cw.writerow(drow)


if __name__ == "__main__":
    main(".")
