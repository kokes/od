import csv
import os
import shutil
import datetime as dt
from io import TextIOWrapper
from contextlib import closing
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from zipfile import ZipFile

url = "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb-20211202.zip"

# convert a date-like string into an ISO-8601-formatted string
def isofy(v: str) -> str:
    # convert 06-JAN-2006 into ISO-8601
    if v[2] == "-":
        return dt.datetime.strptime(v, r"%d-%b-%Y").date().isoformat()
    # ... or "Sep 25, 2012"
    elif "," in v:
        return dt.datetime.strptime(v, r"%b %d, %Y").date().isoformat()
    elif len(v) == 4 and v.isdigit():
        return f"{v}-01-01" # simplify year-only dates to be Jan 1
    # ... or 04/27/05
    elif len(v) == 8 and v[2] == "/":
        pass # cannot implement this now, because these are ambiguous
    else:
        # now we assume it's ISO-8601, which is fine
        dt.date.fromisoformat(v)
        return v
    

def main(outdir: str, partial: bool = False):
    # tmpf = NamedTemporaryFile()
    # with closing(urlopen(url)) as rr:
    #     shutil.copyfileobj(rr, tmpf)

    # with ZipFile(tmpf.name) as zf:
    with ZipFile("full-oldb-20211202.zip") as zf:
        for member in zf.filelist:
            with zf.open(member) as f:
                print(f"processing {member.filename}")
                tr = TextIOWrapper(f)
                cr = csv.DictReader(tr)
                target = os.path.join(outdir, member.filename.replace("nodes-", ""))
                # this is now slightly redundant, because we could just use .extract as before,
                # but we have this in place in case ICIJ fixes their date issues
                with open(target, "wt", encoding="utf-8") as fw:
                    cw = csv.DictWriter(fw, fieldnames=cr.fieldnames)
                    cw.writeheader()
                    nullable = set()
                    for line in cr:
                        for k, v in line.items():
                            if not v:
                                nullable.add(k)
                        # cannot use this now because there are many many ambiguities
                        # for k, v in line.items():
                        #     if k.endswith("_date") and v:
                        #         line[k] = isofy(v)
                        cw.writerow(line)

                    print(member.filename, nullable)


if __name__ == "__main__":
    main(".")
