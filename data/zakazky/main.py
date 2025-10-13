import csv
import shutil
import hashlib
import json
import os
import logging
from contextlib import contextmanager
from urllib.request import Request, urlopen


CACHE_DIR = "cache"
START_YEAR, START_MONTH = 2024, 2


# TODO(PR):
# - zpracovat vsechny mesice
# - rozdelit VZ tabulku na vic tabulek (jsou tam obrovsky JSONB sloupce)
# - opravit db sloupce, at nemaj tak dlouhy nazvy


@contextmanager
def read_url(url):
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    cache_filename = os.path.join(CACHE_DIR, f"{url_hash}")

    if os.path.exists(cache_filename):
        print(f"Nahravam z cache {url}")
        with open(cache_filename, "rb") as cached_file:
            yield cached_file
        return

    request = Request(url, headers={"Accept-Encoding": "gzip"})
    with urlopen(request, timeout=60) as r:
        with open(cache_filename, "wb") as cache_file:
            shutil.copyfileobj(r, cache_file)

        with read_url(url) as cached_file:
            yield cached_file


def main(outdir: str, partial: bool = False):
    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "mapping.json"), encoding="utf-8") as f:
        mp = json.load(f)

    for ds, mapping in mp.items():
        base_url = mapping["base_url"]
        key = mapping["key"]
        header = mapping["srcheader"]
        dbheader = mapping["dbheader"]

        os.makedirs(os.path.join(outdir, ds), exist_ok=True)

        for idx in range(0, 1):
            year = START_YEAR + (START_MONTH + idx - 1) // 12
            month = (START_MONTH + idx - 1) % 12 + 1
            URL = base_url.format(year=year, month=month)
            logging.info("Nahravam %s", URL)

            fn = os.path.join(
                outdir, ds, os.path.splitext(os.path.basename(URL))[0] + ".csv"
            )
            with read_url(URL) as f, open(fn, "wt", encoding="utf-8") as fw:
                cw = csv.DictWriter(fw, fieldnames=dbheader)
                cw.writeheader()
                data = json.load(f)
                for rel in data["data"]:
                    el = rel[key]
                    assert list(el.keys()) == header, el.keys()
                    row = {dk: el[sk] for sk, dk in zip(header, dbheader)}

                    for k, v in row.items():
                        if isinstance(v, (list, dict)):
                            row[k] = json.dumps(v, ensure_ascii=False)
                    cw.writerow(row)


if __name__ == "__main__":
    main(".")
