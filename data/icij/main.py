import csv
import datetime as dt
import os
import shutil
from contextlib import closing
from io import TextIOWrapper
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from zipfile import ZipFile

url = "https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb-20211202.zip"

# these date columns are not ambiguous
processable_dates = {
    "nodes-entities.csv": {
        "incorporation_date",
        "inactivation_date",
        "struck_off_date",
        "dorm_date",
    },
    "nodes-others.csv": {"incorporation_date", "closed_date", "struck_off_date"},
}

# convert a date-like string into an ISO-8601-formatted string
def isofy(v: str) -> str:
    # convert 06-JAN-2006 into ISO-8601
    if v[2] == "-":
        return dt.datetime.strptime(v, r"%d-%b-%Y").date().isoformat()
    # ... or "Sep 25, 2012"
    elif "," in v:
        return dt.datetime.strptime(v, r"%b %d, %Y").date().isoformat()
    else:
        # now we assume it's ISO-8601, which is fine
        dt.date.fromisoformat(v)
        return v


def main(outdir: str, partial: bool = False):
    tmpf = NamedTemporaryFile()
    with closing(urlopen(url, timeout=60)) as rr:
        shutil.copyfileobj(rr, tmpf)

    with ZipFile(tmpf.name) as zf:
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
                    for line in cr:
                        for k, v in line.items():
                            if (
                                k.endswith("_date")
                                and v
                                and member.filename in processable_dates
                                and k in processable_dates[member.filename]
                            ):
                                line[k] = isofy(v)
                        cw.writerow(line)


if __name__ == "__main__":
    main(".")
