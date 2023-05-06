# - http://www.isvz.cz/ISVZ/Podpora/ISVZ_open_data_vz.aspx
# - http://www.isvz.cz/ISVZ/MetodickaPodpora/Napovedaopendata.pdf

import csv
import datetime as dt
import gzip
import io
import json
import shutil
import os
import re
import ssl
from contextlib import contextmanager
from datetime import datetime
from urllib.request import Request, urlopen

# ISVZ nema duveryhodny certy
# TODO(PR): overit
ssl._create_default_https_context = ssl._create_unverified_context


dtpt = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}$")
isodate = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
isodatetime = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$")


def fix_date(s):
    if s is None or len(s) == 0:
        return None

    if isodate.match(s) is not None:
        return dt.date.fromisoformat(s).isoformat()
    if isodatetime.match(s) is not None:
        return dt.datetime.fromisoformat(s).isoformat()

    if dtpt.match(s) is not None:
        d, m, y = map(int, s.split("."))
        return f"{y}-{m:02d}-{d:02d}"
    else:
        return datetime.strptime(s, "%d.%m.%Y %H:%M:%S").isoformat()


# '000 23 234' - takhle se obcas zadavaj ICO
def fix_ico(s):
    if s is None or len(s) == 0:
        return None
    elif s.isdigit():
        rv = int(s)
    elif s.startswith("CZ") and s[2:].isdigit():  # CZ00000205
        rv = int(s[2:])
    else:
        try:
            rv = int(s.replace(" ", "").replace("\xa0", ""))
        except ValueError:
            return None

    if rv < 100 * 10**6:
        return rv
    else:
        return None


@contextmanager
def read_url(url):
    request = Request(url, headers={"Accept-Encoding": "gzip"})
    with urlopen(request, timeout=60) as r:
        assert r.headers.get("Content-Encoding") == "gzip"
        yield gzip.open(r)


root_url = "https://isvz.nipez.cz/sites/default/files/content/opendata-predchozi/"
url_sources = {
    "zzvz": (
        root_url + "ODZZVZSS/{year}_{table}.csv",
        list(range(2016, 2022 + 1)),
    ),
    # TODO(PR): tohle je pro nas nove (a naopak vvz/etrziste nemame)
    # "zzvzmo": (
    #     root_url + "ODZZVZMOSS/{}_{}.csv",
    #     list(range(2016, 2022 + 1)),
    #     {"VerejnaZakazka": "vz", "CastiVerejneZakazky": "casti_vz"},
    # ),
    # TODO(PR): tohle v datech neni
    # "vvz": (
    #     root_url + "ODVVZ/{}.xml",
    #     list(range(2006, 2016 + 1)),
    # ),
    # "etrziste": (
    #     root_url + "ODET/{}.xml",
    #     list(range(2012, 2017 + 1)),
    # ),
}


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json")) as f:
        mapping = json.load(f)

    for dataset, mp in mapping.items():
        base_url, years = url_sources[dataset]
        for table, props in mp.items():
            for year in years:
                print(dataset, table, year)

                if partial and year != years[-1]:
                    continue
                tdir = os.path.join(outdir, f"{dataset}_{props['table']}")
                os.makedirs(tdir, exist_ok=True)
                tfn = os.path.join(tdir, f"{year}.csv")
                url = base_url.format(year=year, table=table)
                with read_url(url) as resp, open(tfn, "wt", encoding="utf-8") as fw:
                    r = io.TextIOWrapper(resp, encoding="utf-8")
                    cr = csv.DictReader(r)
                    # TODO: nemame garanci poradi klicu (je to impl. detail) - asi lepsi predelat ze slovniku
                    cw = csv.DictWriter(fw, lineterminator="\n", fieldnames=props["header"].values())
                    # cw = csv.writer(fw)
                    cw.writeheader()
                    for row in cr:
                        nrow = {v: row[k] for k, v in props["header"].items()}
                        for k, v in nrow.items():
                            if "ico" not in k:
                                continue
                            nrow[k] = fix_ico(v)

                        cw.writerow(nrow)


if __name__ == "__main__":
    main(".")
