# - http://www.isvz.cz/ISVZ/Podpora/ISVZ_open_data_vz.aspx
# - http://www.isvz.cz/ISVZ/MetodickaPodpora/Napovedaopendata.pdf

import csv
import datetime as dt
import gzip
import json
import os
import re
import ssl
from contextlib import contextmanager
from datetime import datetime
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen

from lxml.etree import iterparse

# ISVZ nema duveryhodny certy
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
    with TemporaryDirectory() as tdir:
        tfn = os.path.join(tdir, "data")
        with urlopen(request, timeout=60) as r:
            assert r.headers.get("Content-Encoding") == "gzip"
            yield gzip.open(r)


root_url = "https://isvz.nipez.cz/sites/default/files/content/opendata-predchozi/"
url_sources = {
    "zzvz": (
        root_url + "ODZZVZ/{}.xml",
        list(range(2016, 2022 + 1)),
    ),
    "vvz": (
        root_url + "ODVVZ/{}.xml",
        list(range(2006, 2016 + 1)),
    ),
    "etrziste": (
        root_url + "ODET/{}.xml",
        list(range(2012, 2017 + 1)),
    ),
}


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json"), encoding="utf-8") as f:
        allmaps = json.load(f)

    assert list(allmaps.keys()) == ["etrziste", "vvz", "zzvz"]

    for ds, mapping in allmaps.items():
        filehandles, csvwriters = {}, {}

        for v in mapping.values():
            full_ds = f"{ds}_{v['table']}"
            tfn = os.path.join(outdir, f"{full_ds}.csv")
            filehandles[full_ds] = open(tfn, "w", encoding="utf8")
            # TODO: museli jsme vypnout DictWriter, protoze ZZVZ jsou garbage
            # pro roky 2021 a 2022
            csvwriters[full_ds] = csv.writer(
                filehandles[full_ds],
                # fieldnames=v["header"],
                lineterminator="\n",
            )
            # csvwriters[full_ds].writeheader()
            csvwriters[full_ds].writerow(v["header"])

        base_url, years = url_sources[ds]

        for year in years:
            if partial and year != years[-1]:
                continue
            print(ds, year)
            url = base_url.format(year)
            with read_url(url) as resp:
                for action, element in iterparse(resp):
                    assert action == "end"
                    if element.tag not in mapping:
                        continue
                    mp = mapping[element.tag]
                    full_ds = f"{ds}_{mp['table']}"

                    row = {
                        el.tag: el.text.strip() if el.text else None
                        for el in element.getchildren()
                    }

                    for k, v in row.items():
                        if k in mp.get("dates", []):
                            row[k] = fix_date(v)
                        if v and k in mp.get("numeric", []):
                            row[k] = v.replace(",", ".")
                        if "ICO" in k:
                            ico = fix_ico(v)
                            if ico is None and v is not None:
                                print("nevalidni ico", v, f"({full_ds}, {url})")
                            row[k] = ico

                    # TODO: `writerow(row)` az prejdem zpet na DictWriter
                    csvwriters[full_ds].writerow(row.values())

                    element.clear()

        for fh in filehandles.values():
            fh.close()


if __name__ == "__main__":
    main(".")
