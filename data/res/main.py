import gzip
import os
import shutil
from urllib.request import Request, urlopen

DATA = ("https://opendata.czso.cz/data/od_org03/res_data.csv", "subjekty.csv")
NACE = ("https://opendata.czso.cz/data/od_org03/res_pf_nace.csv", "nace.csv")


def download_gzipped(url: str, filename: str):
    req = Request(url)
    req.add_header("Accept-Encoding", "gzip")
    with open(filename, "wb") as fw, urlopen(req) as r:
        assert r.headers["Content-Encoding"] == "gzip"
        gr = gzip.GzipFile(fileobj=r)
        shutil.copyfileobj(gr, fw)


# TODO: implement partial?
# TODO: ciselniky pro ruzne sloupce
def main(outdir: str, partial: bool = False):
    for url, filename in [DATA, NACE]:
        path = os.path.join(outdir, filename)
        download_gzipped(url, path)


if __name__ == "__main__":
    main(".")
