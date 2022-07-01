import csv
import json
import os
from urllib.request import urlopen

HTTP_TIMEOUT = 60

indices = {
    "2017": "https://zpravy.udhpsh.cz/export/vfz2017-index.json",
    "2018": "https://zpravy.udhpsh.cz/zpravy/vfz2018.json",
    "2019": "https://zpravy.udhpsh.cz/zpravy/vfz2019.json",
    "2020": "https://zpravy.udhpsh.cz/zpravy/vfz2020.json",
    "2021": "https://zpravy.udhpsh.cz/zpravy/vfz2021.json",
}
years = sorted(indices.keys())

mappings = {
    "penizefo": {
        "date": "datum",
        "money": "castka",
        "lastName": "prijmeni",
        "firstName": "jmeno",
        "titleBefore": "titul_pred",
        "titleAfter": "titul_za",
        "birthDate": "datum_narozeni",
        "addrCity": "adresa_mesto",
    },
    "penizepo": {
        "date": "datum",
        "money": "castka",
        "companyId": "ico_darce",
        "company": "spolecnost",
        "addrStreet": "adresa_ulice",
        "addrCity": "adresa_mesto",
        "addrZip": "adresa_psc",
    },
}


def main(outdir: str, partial: bool = False):
    for dataset, mapping in mappings.items():
        print(f"Nahravam dataset: {dataset}")
        with open(os.path.join(outdir, dataset + ".csv"), "w", encoding="utf8") as fw:
            columns = ["rok", "ico_prijemce", "nazev_prijemce"] + list(mapping.values())
            cw = csv.DictWriter(fw, fieldnames=columns, lineterminator="\n")
            cw.writeheader()
            for year, index in indices.items():
                if partial and year not in years[-2:]:
                    continue
                print(f"zpracovavam rok: {year}")
                with urlopen(index, timeout=HTTP_TIMEOUT) as r:
                    dt = json.load(r)

                    for jp, party in enumerate(dt["parties"]):
                        if partial and jp > 20:
                            break
                        relfiles = [
                            j["url"]
                            for j in party["files"]
                            if j["subject"] == dataset and j["format"] == "json"
                        ]
                        for relfile in relfiles:
                            for item in json.load(
                                urlopen(relfile, timeout=HTTP_TIMEOUT)
                            ):
                                row = {mapping[k]: v for k, v in item.items()}
                                if row.get("ico_darce") is not None and (
                                    not isinstance(row["ico_darce"], int)
                                    or row["ico_darce"] > 99999999
                                ):
                                    print(f"preskakuju zaznam s neplatnym ICO: {row}")
                                    row["ico_darce"] = None

                                cw.writerow(
                                    {
                                        **row,
                                        "rok": year,
                                        "ico_prijemce": party["ic"],
                                        "nazev_prijemce": party["longName"],
                                    }
                                )


if __name__ == "__main__":
    main(".")
