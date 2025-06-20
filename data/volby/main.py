import csv
import gzip
import io
import json
import logging
import multiprocessing
import os
import random
import shutil
import string
import zipfile
from collections import defaultdict
from contextlib import contextmanager
from fnmatch import fnmatch
from tempfile import TemporaryDirectory
from urllib.error import URLError
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

import lxml.etree
from tqdm import tqdm

HTTP_TIMEOUT = 30
RETRIES = 5
DVOUKOLAK = ("senat", "prezident")


@contextmanager
def fetch_as_file(url, tfn=None, retries=RETRIES):
    req = Request(url, headers={"User-Agent": "https://github.com/kokes/od"})
    with TemporaryDirectory() as tmpdir:
        tfn = os.path.join(
            tmpdir,
            "".join([random.choice(string.ascii_letters) for _ in range(10)]),
        )

        for j in range(retries):
            try:
                with urlopen(req, timeout=HTTP_TIMEOUT) as r, open(tfn, "wb") as fw:
                    if r.headers.get("content-encoding") == "gzip":
                        r = gzip.open(r)
                    shutil.copyfileobj(r, fw)
                    break
            except (URLError, TimeoutError) as e:
                if j == retries - 1:
                    raise e
                print(f"{e}, retrying {url}")
                continue

        yield tfn


@contextmanager
def load_remote_data(url: str):
    with fetch_as_file(url) as tfn:
        with zipfile.ZipFile(tfn) as zf:
            yield zf


def process_url(outdir, partial, fnmap, url: str, volby: str, datum: str):
    # specialni handling davkovych exportu (nejsou v zipu)
    if not url.endswith(".zip"):
        ds, fmp = fnmap[volby]["davky.xml"]  # 'davky.xml' je dummy hodnota
        ddir = os.path.join(outdir, f"{volby}_davky")
        os.makedirs(ddir, exist_ok=True)
        tfn = os.path.join(ddir, f"{datum}.csv")
        with open(tfn, "wt", encoding="utf8") as fw:
            schema = ["DATUM"] + [j for j in fmp["schema"]]
            if volby in DVOUKOLAK:
                schema.insert(1, "KOLO")
            cw = csv.DictWriter(
                fw,
                fieldnames=schema,
                lineterminator="\n",
            )
            cw.writeheader()

            parsed = urlparse(url)
            qs = dict(parse_qsl(parsed.query))
            for kolo in [1, 2]:
                for davka in range(1, 1000):
                    if volby in DVOUKOLAK:
                        qs["kolo"] = kolo
                    elif kolo == 2:
                        break
                    qs["davka"] = davka
                    parsed = parsed._replace(query=urlencode(qs))
                    with fetch_as_file(urlunparse(parsed)) as tfn:
                        with open(tfn, "rb") as r:
                            et = lxml.etree.parse(r).getroot()
                    ns = et.nsmap[None]
                    if et.find(f"./{{{ns}}}CHYBA") is not None:
                        break

                    okrsky = et.findall(f"./{{{ns}}}OKRSEK")
                    # assert len(okrsky) > 0
                    for okrsek in okrsky:
                        ks = okrsek.attrib.keys()
                        assert set(ks) == set(fmp["schema"]), (volby, ks)
                        row = dict(okrsek.attrib)
                        row["DATUM"] = datum
                        if volby in DVOUKOLAK:
                            row["KOLO"] = kolo
                        cw.writerow(row)
        return

    # bezny prubeh extrakce ze zipu
    with load_remote_data(url) as zf:
        # zpravidla (ale ne vzdy!) mame zdvojena data:
        # 'csv/eprk.csv', 'csv/eprkl.csv', 'csv/eprkl_slozeni.csv', 'csv_od/eprk.csv',
        # 'csv_od/eprk.json', 'csv_od/eprkl.csv', 'csv_od/eprkl.json',
        # 'csv_od/eprkl_slozeni.csv', 'csv_od/eprkl_slozeni.json'
        # tak musime tuto situaci detekovat a deduplikovat
        # bacha - csv_od jsou utf-8 s ',' delimitery, csv jsou cp1250 s ';' delimitery
        filenames = [j.filename for j in zf.filelist]
        if any(j.startswith("csv_od/") for j in filenames):
            filenames = [j for j in filenames if not j.startswith("csv_od/")]
        for ff in filenames:
            patterns = [
                j for j in fnmap[volby].keys() if fnmatch(os.path.basename(ff), j)
            ]
            if len(patterns) == 0:
                continue
            if len(patterns) > 1:
                raise KeyError("ambiguous keys: {}".format(patterns))

            ds, fmp = fnmap[volby].get(patterns[0])
            tdir = os.path.join(outdir, f"{volby}_{ds}")
            os.makedirs(tdir, exist_ok=True)
            url_path = os.path.splitext(os.path.basename(urlparse(url).path))[0]
            # windows neumi mit v nazvu souboru hvezdicku
            tfn = os.path.join(
                tdir, f"{datum.replace('*', 'vse')}_{url_path}_{os.path.basename(ff)}"
            )
            if os.path.isfile(tfn):
                raise IOError(f"necekany prepis souboru: {tfn}")

            with open(tfn, "wt", encoding="utf8") as fw:
                scols = list(fmp["schema"])
                if "JMENO" in scols:
                    scols.remove("PRIJMENI")
                    scols[scols.index("JMENO")] = "JMENO_PRIJMENI"

                cw = csv.DictWriter(
                    fw,
                    fieldnames=["DATUM"] + scols + fmp.get("extra_schema", []),
                    lineterminator="\n",
                )
                cw.writeheader()
                with zf.open(ff) as f:
                    cr = csv.DictReader(
                        io.TextIOWrapper(f, encoding="cp1250"),
                        delimiter=";",
                    )
                    for ne, el in enumerate(cr):
                        if partial and ne > 1e4:
                            break
                        for k in fmp.get("vynechej", []):
                            el.pop(k, None)

                        if "JMENO" in el:
                            el["JMENO_PRIJMENI"] = (
                                f"{el['JMENO'] or ''} "
                                f"{el['PRIJMENI'] or ''}".strip().title()
                            )
                            del el["JMENO"]
                            del el["PRIJMENI"]

                        # TODO: TEST: HLASY_01 vs. HLASY_K1
                        hk = [
                            k
                            for k in el.keys()
                            if k.startswith("HLASY_") and k.partition("_")[-1].isdigit()
                        ]
                        if hk:
                            hlasy = []
                            for k in hk:
                                hlasy.append(el[k] or 0)
                                del el[k]

                            # pg array representation - '{a, b, c}'
                            el["HLASY"] = "{{{}}}".format(",".join(map(str, hlasy)))

                        # mandat str -> bool
                        if "MANDAT" in el and el["MANDAT"] not in ("", None):
                            assert el["MANDAT"] in ("A", "1", "N", "0", 1, 0)
                            el["MANDAT"] = (
                                "true" if el["MANDAT"] in ("A", "1", 1) else "false"
                            )

                        # u nekterych voleb je uvedeno, ke kteremu dni plati, protoze
                        # treba soud rozhodl o nejake zmene - tak pak muze byt datum
                        # uvedeno dvakrat
                        # 20181223 -> 2018-12-23
                        if "DATUMVOLEB" in el:
                            dv = el["DATUMVOLEB"]
                            assert dv.isdigit(), dv
                            assert len(dv) == 8, dv
                            el["DATUMVOLEB"] = f"{dv[:4]}-{dv[4:6]}-{dv[6:8]}"

                        el["DATUM"] = datum if datum != "*" else None
                        # v pripade senatu mame bulk data za vsechno, takze musime
                        # inferovat datum voleb jen z dat, ne z mappingu
                        if volby == "senat" and datum == "*" and "DATUMVOLEB" in el:
                            el["DATUM"] = el["DATUMVOLEB"]
                            del el["DATUMVOLEB"]

                        miss = set(cw.fieldnames) - set(el)
                        if miss:
                            logging.info("chybejici sloupce v datech: %s", miss)

                        cw.writerow(el)


def job_processor(args):
    return process_url(*args)


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json"), encoding="utf-8") as f:
        mps = json.load(f)

    ncpu = multiprocessing.cpu_count()
    jobs = []
    fnmap = defaultdict(dict)
    for volby, mp in mps.items():
        for ds, spec in mp["ds"].items():
            for fn in spec["fn"]:
                assert fn not in fnmap, fn
                fnmap[volby][fn] = (ds, spec)

        for datum, urls in mp["url"].items():
            if partial and datum not in ("*", sorted(mp["url"].keys())[-1]):
                continue
            for url in urls:
                jobs.append((outdir, partial, fnmap, url, volby, datum))

    progress = tqdm(total=len(jobs))
    with multiprocessing.Pool(ncpu) as pool:
        for _ in pool.imap_unordered(job_processor, jobs):
            progress.update(n=1)


if __name__ == "__main__":
    main(".")
