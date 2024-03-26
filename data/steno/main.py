import csv
import functools
import logging
import multiprocessing
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter
from contextlib import closing
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

import lxml.html
from tqdm import tqdm

HTTP_TIMEOUT = 90


def clean_lines(rel_path):
    return list(
        map(
            str.strip,
            (Path(__file__).parent / rel_path)
            .read_text(encoding="utf -8")
            .splitlines(),
        )
    )


urls = {
    2010: "https://www.psp.cz/eknih/2010ps/stenprot/zip/index.htm",
    2013: "https://www.psp.cz/eknih/2013ps/stenprot/zip/index.htm",
    2017: "https://www.psp.cz/eknih/2017ps/stenprot/zip/",
    2021: "https://www.psp.cz/eknih/2021ps/stenprot/zip/index.htm",
}


poz = clean_lines("pozice.txt")
dlh = set(clean_lines("dlouha_jmena.txt"))

# TODO: testy


# TODO(perf): kdyz materializujem to pridani "CR" do pozic a seradime
# sestupne podle delky, tak to bude rychlejsi
def depozicuj(jmeno, poz=poz):
    if jmeno.startswith("Pan "):
        return None, jmeno[4:]

    fn, nm = None, None
    for pr in poz:
        for p in (pr, pr + " ČR"):
            if jmeno.startswith(p):
                if fn is None or (fn and len(p) > len(fn)):
                    fn, nm = p, jmeno[len(p) + 1 :]

    if "ČR" in jmeno:
        ind = jmeno.rindex("ČR")
        if fn is None or (fn and len(p + " ČR") > len(fn)):
            fn, nm = jmeno[: ind + 2], jmeno[ind + 3 :]

    if fn:
        return fn, nm

    return None, jmeno


def vyrok(zf):
    aut, fun, tema = None, None, None
    buf = []
    for zfn in zf.filelist:
        if not zfn.filename.startswith("s"):
            continue

        ht = lxml.html.parse(zf.open(zfn.filename)).getroot()
        if ht is None:
            logging.info(f"Nepodarilo se nacist soubor {zfn.filename} ({zf.filename})")
            continue
        ps = ht.cssselect("p")

        for j, p in enumerate(ps):
            pt = p.text_content().strip().replace("\xa0", " ")
            if len(pt) == 0:
                continue

            # v textu je odkaz (autor), ve 2010 exportech je <b>autor</b>
            od = p.find("a")
            if (
                p.find("b") is not None
                and p.find("b").text_content() != p.text_content()
            ):
                od = p.find("b")
            tp = p.find("b")

            if tp is not None and tp.text_content() == p.text_content():
                tema = tp.text_content().replace("\xa0", " ").replace("\n", "")
                continue

            if od is None:
                buf += [pt]
                # v posledni iteraci je treba flushnout posledniho recnika, takze
                # nemuzem preskocit iteraci v tuhle chvili
                if j < len(ps) - 1:
                    continue

            if len(buf) > 0:
                yield {
                    "autor": aut,
                    "funkce": fun,
                    "schuze": int(
                        re.match(r"^\d+", os.path.split(zf.filename)[1]).group()
                    ),
                    "soubor": zfn.filename,
                    # TODO: dokazem ziskat datum z tech detailnich stranek
                    "datum": None,
                    # TODO: tema je v <b>
                    "tema": tema,
                    "text": "\n".join(buf),
                }

            if od is not None:
                fun, aut = depozicuj(od.text_content().strip())
                buf = [
                    pt[len(od.text_content()) + 1 :].strip()
                ]  # pridame soucasny text (ale odseknem autora)


def zpracuj_schuzi(outdir, params):
    rok, url = params  # kvuli imap_unordered
    lnm = Counter()
    with tempfile.TemporaryDirectory() as tmpdir:
        base_name = os.path.basename(urlparse(url).path)
        tfn = os.path.join(tmpdir, base_name)
        with urlopen(url, timeout=HTTP_TIMEOUT) as r, open(tfn, "wb") as fw:
            shutil.copyfileobj(r, fw)
        tdir = os.path.join(outdir, "psp")
        os.makedirs(tdir, exist_ok=True)
        csv_fn = os.path.join(tdir, f"{rok}_{os.path.splitext(base_name)[0]}.csv")
        assert not os.path.isfile(csv_fn)

        with open(csv_fn, "w", encoding="utf8") as fw:
            cw = csv.DictWriter(
                fw,
                fieldnames=[
                    "rok",
                    "datum",
                    "schuze",
                    "soubor",
                    "autor",
                    "funkce",
                    "tema",
                    "text",
                ],
                lineterminator="\n",
            )
            cw.writeheader()
            with closing(zipfile.ZipFile(tfn)) as zf:
                for v in vyrok(zf):
                    cw.writerow(
                        {
                            "rok": rok,
                            **v,
                        }
                    )
                    # depozicovali jsme vse?
                    if (
                        v["autor"]
                        and len(v["autor"].split(" ")) > 2
                        and v["autor"] not in dlh
                    ):
                        lnm.update([(v["funkce"], v["autor"])])

    return lnm


def main(outdir: str, partial: bool = False):
    logging.getLogger().setLevel(logging.INFO)
    jobs = []
    for rok, burl in urls.items():
        with urlopen(burl, timeout=HTTP_TIMEOUT) as r:
            ht = lxml.html.parse(r).getroot()

        for num, ln in enumerate(ht.cssselect("div#main-content a")):
            if partial and num > 3:
                break
            url = urljoin(burl, ln.attrib["href"])
            jobs.append((rok, url))

    ncpu = multiprocessing.cpu_count()
    if os.getenv("CI"):
        logging.info("Pouze jedno CPU, abychom nepretizili psp.cz")
        ncpu = 1
    func = functools.partial(zpracuj_schuzi, outdir)
    lnm = Counter()
    progress = tqdm(total=len(jobs))
    with multiprocessing.Pool(ncpu) as pool:
        for slnm in pool.imap_unordered(func, jobs):
            progress.update(1)
            lnm.update(slnm)

    # naparsovali jsme správně politické funkce?
    if lnm:
        print(
            "\nJe možné, že následující osoby jsme nenaparsovali správně, "
            "a bude možná nutné"
            " jejich funkce doplnit do souboru pozice.txt\n"
        )
        for (fn, jm), num in sorted(lnm.items(), key=lambda x: (x[0][0], x[0][1])):
            print("Funkce: {}, jméno: {} ({})".format(fn, jm, num))


if __name__ == "__main__":
    main(".")
