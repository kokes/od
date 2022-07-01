import csv
import os
from urllib.request import urlopen

from lxml.etree import iterparse

BASE_URL = (
    "https://www.szif.cz/cs/CmDocument?rid=%2Fapa_anon%2Fcs%2F"
    "dokumenty_ke_stazeni%2Fpkp%2Fspd%2Fopendata%2Fspd{year}.xml"
)
years = [2017, 2018, 2019, 2020, 2021]


def main(outdir: str, partial: bool = False):
    id_prijemce = 1

    with open(os.path.join(outdir, "zadatele.csv"), "w", encoding="utf8") as fz, open(
        os.path.join(outdir, "platby.csv"), "w", encoding="utf8"
    ) as fp:
        cz = csv.DictWriter(
            fz,
            ["id_prijemce", "rok", "jmeno_nazev", "obec", "okres", "castka_bez_pvp"],
            lineterminator="\n",
        )
        cp = csv.DictWriter(
            fp,
            [
                "id_prijemce",
                "rok",
                "fond_typ_podpory",
                "opatreni",
                "zdroje_cr",
                "zdroje_eu",
                "celkem_czk",
            ],
            lineterminator="\n",
        )

        cz.writeheader()
        cp.writeheader()

        for year in years:
            url = BASE_URL.format(year=year)

            with urlopen(url) as r:
                et = iterparse(r)

                elyear = None
                for num, (action, element) in enumerate(et):
                    if partial and num > 1e3:
                        break
                    assert action == "end"
                    if element.tag == "rok":
                        elyear = int(element.text)
                        assert elyear == year, "Necekany rok v datech"

                    if element.tag != "zadatel":
                        continue

                    zadatel = {"id_prijemce": id_prijemce, "rok": elyear}

                    for key in ["jmeno_nazev", "obec", "okres", "castka_bez_pvp"]:
                        zadatel[key] = element.find(key).text

                    for elplatba in element.findall("platby/platba") + element.findall(
                        "platby_pvp/platba_pvp"
                    ):
                        platba = {"id_prijemce": id_prijemce, "rok": elyear}
                        for key in [
                            "fond_typ_podpory",
                            "opatreni",
                            "zdroje_cr",
                            "zdroje_eu",
                            "celkem_czk",
                        ]:
                            platba[key] = getattr(elplatba.find(key), "text", None)

                        cp.writerow(platba)

                    cz.writerow(zadatel)
                    id_prijemce += 1

                    element.clear()
