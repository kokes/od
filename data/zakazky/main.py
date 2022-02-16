# - http://www.isvz.cz/ISVZ/Podpora/ISVZ_open_data_vz.aspx
# - http://www.isvz.cz/ISVZ/MetodickaPodpora/Napovedaopendata.pdf

import csv
import datetime as dt
import gzip
import json
import os
import re
import ssl
from codecs import iterdecode
from contextlib import contextmanager
from datetime import datetime
from urllib.request import Request, urlopen

# ISVZ nema duveryhodny certy
ssl._create_default_https_context = ssl._create_unverified_context


def najdi_typy(hd, typy):
    ind = dict()  # {'date': [15, 22], 'numeric': [7, 8, 9]}
    for k, v in typy.items():
        ind[k] = []

        for cl in v:
            try:
                j = hd.index(cl)
                ind[k].append(j)
            except ValueError:
                pass

    return ind


dtpt = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}$")
isodate = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def fix_date(s):
    if len(s) == 0:
        return None

    if isodate.match(s) is not None:
        return dt.date.fromisoformat(s).isoformat()

    if dtpt.match(s) is not None:
        d, m, y = map(int, s.split("."))
        return f"{y}-{m:02d}-{d:02d}"
    else:
        return datetime.strptime(s, "%d.%m.%Y %H:%M:%S").isoformat()


def fix_numeric(s):
    if len(s) == 0:
        return None
    return float(s.replace(",", "."))


# '000 23 234' - takhle se obcas zadavaj ICO
def fix_ico(s):
    if len(s) == 0:
        return None
    elif s.isdigit():
        rv = int(s)
    elif s.startswith("CZ") and s[2:].isdigit():  # CZ00000205
        rv = int(s[2:])
    else:
        try:
            rv = int(s.replace(" ", "").replace("\xa0", ""))
        except ValueError:
            print("nevalidni ICO", s)
            return None

    if rv < 100 * 10**6:
        return rv
    else:
        print("ICO overflow", rv)
        return None


@contextmanager
def read_url(url):
    request = Request(url, headers={"Accept-Encoding": "gzip"})
    with urlopen(request, timeout=60) as r:
        assert r.headers.get("Content-Encoding") == "gzip"
        with gzip.open(r) as gr:
            yield iterdecode(gr, encoding="utf-8-sig")


root_url = "https://isvz.nipez.cz/sites/default/files/content/opendata-predchozi/"
url_sources = {
    "zzvz": (
        root_url + "ODZZVZ/{}.csv",
        list(range(2016, 2021 + 1)),
    ),
    "vvz": (
        root_url + "ODVVZ/{}.csv",
        list(range(2006, 2016 + 1)),
    ),
    "etrziste": (
        root_url + "ODET/{}.csv",
        list(range(2012, 2017 + 1)),
    ),
}


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json")) as f:
        allmaps = json.load(f)

    assert list(allmaps.keys()) == ["etrziste", "vvz", "zzvz"]

    for ds, mapping in allmaps.items():
        print(ds)
        tblmap = {tuple(v): k for k, v in mapping["tabulky"].items()}

        for k, v in tblmap.items():
            tfn = os.path.join(outdir, f"{ds}_{v}.csv")
            with open(tfn, "w", encoding="utf8") as fw:
                cw = csv.writer(fw)
                cw.writerow(k)

        base_url, years = url_sources[ds]

        for year in years:
            # v `partial` procesnem jen posledni rok - nemuzem procesovat casti
            # souboru, protoze co soubor, to nekolik datasetu
            if partial and year != years[-1]:
                continue
            url = base_url.format(year)
            with read_url(url) as resp:
                cr = csv.reader(resp, delimiter=";")

                for nrow, ln in enumerate(cr):
                    if (len(ln) > 0 and ln[0] == mapping["hlavicka"]) or nrow == 0:
                        if ln[0] == mapping["hlavicka"]:
                            assert len(next(cr)) == 0  # prazdny radek po hlavicce
                            hd = tuple(next(cr))
                        else:
                            # od 2021 nemaj některý soubory hlavičku
                            hd = tuple(ln)
                        tpmap = najdi_typy(hd, mapping["typy"])
                        tp = tblmap[hd]  # document type
                        f = open(
                            os.path.join(outdir, f"{ds}_{tp}.csv"), "a", encoding="utf8"
                        )
                        cw = csv.writer(f)
                        continue

                    if len(ln) == 0:
                        continue

                    # TODO: az to opravi, tak tu exituj
                    if len(hd) != len(ln):
                        print(f"Necekane dlouha radka ({nrow}. v {url})")
                        continue
                        # with open("errs.csv", "a+") as ffw:
                        #     ccw = csv.writer(ffw)
                        #     ccw.writerow(ln)
                        # continue

                    for k, v in tpmap.items():
                        for cln in v:
                            if k == "date":
                                ln[cln] = fix_date(ln[cln])
                            elif k == "numeric":
                                ln[cln] = fix_numeric(ln[cln])
                            elif k == "ico":
                                ln[cln] = fix_ico(ln[cln])
                            else:
                                raise ValueError(k)

                    cw.writerow(ln)

        f.close()


if __name__ == "__main__":
    main(".")
