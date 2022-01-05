import csv
import json
import os
import re
from urllib.parse import quote
from urllib.request import urlopen


def main(outdir: str, partial: bool = False):
    url = "https://query.wikidata.org/sparql?query={}&format=json"
    query = """SELECT ?person ?personLabel ?date_of_birth WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "cs". }
    VALUES ?politician {wd:Q18941264 wd:Q19803234}
    ?person wdt:P39 ?politician.

    ?person wdt:P569 ?date_of_birth.
  }

  LIMIT 10000"""
    if partial:
        query = query.replace("LIMIT 10000", "LIMIT 100")

    r = urlopen(url.format(quote(query)), timeout=60)
    dt = json.load(r)
    rr = re.compile(r"\s+\(.+\)")

    with open(os.path.join(outdir, "politici.csv"), "w", encoding="utf8") as fw:
        cw = csv.writer(fw)
        cw.writerow(["wikidata", "jmeno_prijmeni", "datum_narozeni"])
        for el in dt["results"]["bindings"]:
            cw.writerow(
                [
                    el["person"]["value"].rpartition("/")[-1],
                    rr.sub("", el["personLabel"]["value"]),
                    el["date_of_birth"]["value"][:10],
                ]
            )


if __name__ == "__main__":
    main(".")
