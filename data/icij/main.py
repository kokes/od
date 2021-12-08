import os
import shutil
from contextlib import closing
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from zipfile import ZipFile

url = "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb-20211202.zip"


def main(outdir: str, partial: bool = False):
    tmpf = NamedTemporaryFile()
    with closing(urlopen(url)) as rr:
        shutil.copyfileobj(rr, tmpf)

    with ZipFile(tmpf.name) as zf:
        for member in zf.filelist:
            zf.extract(member, path=outdir)
            if member.filename.startswith("nodes-"):
                target = os.path.join(outdir, member.filename)
                new_target = target.replace("nodes-", "")
                os.rename(target, new_target)


if __name__ == "__main__":
    main(".")
