import csv
import os

from main import depozicuj


def test_depozicovani():
    cdir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(cdir, "testdata.txt"), "rt", encoding="utf-8") as f:
        cr = csv.DictReader(f, delimiter=";")

        for row in cr:
            funkce, autor = depozicuj(row["original"])
            assert funkce == (row["funkce"] or None)
            assert autor == row["autor"]
