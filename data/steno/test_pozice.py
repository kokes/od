import csv
import os

import pytest

from main import depozicuj


def test_depozicovani():
    cdir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(cdir, "testdata.txt"), "rt", encoding="utf-8") as f:
        cr = csv.DictReader(f, delimiter=";")

        for row in cr:
            funkce, autor = depozicuj(row["original"])
            assert funkce == (row["funkce"] or None), row["original"]
            assert autor == row["autor"], row["original"]


@pytest.mark.parametrize(
    ["pozice", "jmeno", "funkce", "autor"],
    [
        (["pan"], "pan prezident", "pan", "prezident"),
        # chcem nejdelsi match, na poradi nezalezi
        (["pan", "pan vážený"], "pan vážený prezident", "pan vážený", "prezident"),
        (["pan vážený", "pan"], "pan vážený prezident", "pan vážený", "prezident"),
    ],
)
def test_inline(pozice, jmeno, funkce, autor):
    assert depozicuj(jmeno, pozice) == (funkce, autor)
