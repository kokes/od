import os
from contextlib import closing
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from zipfile import ZipFile

# TODO(PR): black, isort

url = "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb-20211202.zip"

def main(outdir: str, partial: bool = False):
    # TODO(PR): finish
    # tmpf = NamedTemporaryFile()
    # with closing(urlopen(url)) as rr:
    #     shutil.copyfileobj(rr, tmpf)

    # zf = ZipFile(tmpf.name)
    fn = "full-oldb-20211202.zip"
    zf = ZipFile(fn)
    for member in zf.filelist:
        zf.extract(member, path = outdir)
        if member.filename.startswith("nodes-"):
            target = os.path.join(outdir, member.filename)
            new_target = target.replace("nodes-", "")
            os.rename(target, new_target)

if __name__ == "__main__":
    main(".")
