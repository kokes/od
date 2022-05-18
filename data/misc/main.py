import csv
import io
import os
from urllib.request import urlopen

URL_ODSOUZENE_PO = "https://eservice-po.rejtr.justice.cz/public/odsouzeni_csv"


def main(outdir: str, partial: bool = False):
    # urlretrieve(URL_ODSOUZENE_PO, os.path.join(outdir, "odsouzene_po.csv"))
    with urlopen(URL_ODSOUZENE_PO) as r, open(
        os.path.join(outdir, "odsouzene_po.csv"), "w", encoding="utf-8"
    ) as fw:
        cw = csv.writer(fw, lineterminator="\n")
        for row in csv.reader(io.TextIOWrapper(r, encoding="utf-8")):
            cw.writerow(row)


if __name__ == "__main__":
    main(".")
