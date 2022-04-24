import gzip
import os
import shutil
from io import TextIOWrapper
from urllib.request import Request, urlopen

DATA = ("https://opendata.czso.cz/data/od_org03/res_data.csv", "subjekty.csv")
NACE = ("https://opendata.czso.cz/data/od_org03/res_pf_nace.csv", "nace.csv")
HTTP_TIMEOUT = 30


def download_gzipped(url: str, filename: str, partial: bool):
    req = Request(url)
    req.add_header("Accept-Encoding", "gzip")
    with urlopen(req, timeout=HTTP_TIMEOUT) as r:
        assert r.headers["Content-Encoding"] == "gzip"
        gr = gzip.GzipFile(fileobj=r)
        if partial:
            with open(filename, "wt", encoding="utf-8") as fw:
                for j, line in enumerate(TextIOWrapper(gr, encoding="utf-8")):
                    if j > 100_000:
                        break
                    fw.write(line)
        else:
            with open(filename, "wb") as fw:
                shutil.copyfileobj(gr, fw)


# TODO: ciselniky pro ruzne sloupce
def main(outdir: str, partial: bool = False):
    for url, filename in [DATA, NACE]:
        path = os.path.join(outdir, filename)
        download_gzipped(url, path, partial)


if __name__ == "__main__":
    main(".")
