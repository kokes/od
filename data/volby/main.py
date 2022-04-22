import csv
import json
import os
import shutil
import zipfile
from contextlib import contextmanager
from fnmatch import fnmatch
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen

import lxml.etree
from dbfread import DBF


@contextmanager
def load_remote_data(url: str):
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    fn = os.path.basename(url)
    tfn = os.path.join(raw_dir, fn)
    if not os.path.isfile(tfn):
        req = Request(url, headers={"User-Agent": "https://github.com/kokes/od"})
        with urlopen(req, timeout=60) as r, open(tfn, "wb") as fw:
            shutil.copyfileobj(r, fw)

    zf = zipfile.ZipFile(tfn)
    yield zf
    zf.close()


def extract_elements(zf, fn, nodename):
    if fn.lower().endswith(".xml"):
        with zf.open(fn) as f:
            et = lxml.etree.iterparse(f)

            for _, node in et:
                if not node.tag.endswith(f"}}{nodename}"):
                    continue

                yield dict(
                    (j.tag[j.tag.rindex("}") + 1 :], j.text)
                    for j in node.iterchildren()
                )
                node.clear()

    elif fn.lower().endswith("dbf"):
        # dbfread neumi cist z filehandleru,
        # https://github.com/olemb/dbfread/issues/25
        with TemporaryDirectory() as tempdir:
            tfn = zf.extract(fn, tempdir)
            d = DBF(tfn, encoding="cp852")
            yield from d
    else:
        raise NotImplementedError(fn)


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json"), encoding="utf-8") as f:
        mps = json.load(f)

    for volby, mp in mps.items():
        print(volby)

        fnmap = {}
        for ds, spec in mp["ds"].items():
            for fn in spec["fn"]:
                fnmap[fn] = (ds, spec)

        for datum, urls in mp["url"].items():
            if partial and datum != sorted(mp["url"].keys())[-1]:
                continue
            print("\t", datum)
            for url in urls:
                with load_remote_data(url) as zf:
                    for ff in map(lambda x: x.filename, zf.filelist):
                        patterns = [j for j in fnmap.keys() if fnmatch(ff, j)]
                        if len(patterns) == 0:
                            continue
                        if len(patterns) > 1:
                            raise KeyError("ambiguous keys: {}".format(patterns))

                        ds, fmp = fnmap.get(patterns[0])
                        tdir = os.path.join(outdir, f"{volby}_{ds}")
                        os.makedirs(tdir, exist_ok=True)
                        tfn = os.path.join(tdir, f"{datum}.csv")
                        fnexists = os.path.isfile(tfn)
                        with open(tfn, "a+", encoding="utf8") as fw:
                            cw = csv.DictWriter(
                                fw,
                                fieldnames=["DATUM"]
                                + fmp["schema"]
                                + fmp.get("extra_schema", []),
                            )
                            if not fnexists:
                                cw.writeheader()
                            for el in extract_elements(zf, ff, fmp["klic"]):
                                for k in fmp.get("vynechej", []):
                                    el.pop(k, None)

                                # TODO: TEST: HLASY_01 vs. HLASY_K1
                                hk = [
                                    k
                                    for k in el.keys()
                                    if k.startswith("HLASY_")
                                    and k.partition("_")[-1].isdigit()
                                ]
                                if hk:
                                    hlasy = []
                                    for k in hk:
                                        hlasy.append(el[k] or 0)
                                        del el[k]

                                    # pg array representation - '{a, b, c}'
                                    el["HLASY"] = "{{{}}}".format(
                                        ",".join(map(str, hlasy))
                                    )

                                cw.writerow(
                                    {
                                        "DATUM": datum,
                                        **el,
                                    }
                                )


if __name__ == "__main__":
    main(".")
