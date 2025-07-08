import datetime as dt
import pytest

from main import jmeno_narozeni

@pytest.mark.parametrize(
    ["jmeno", "jmeno_final", "narozeni"],
    [
        ("Jan Pan", "Jan Pan", None),
        ("Jakub Nakup, Nar. 10.09.1964", "Jakub Nakup", dt.date(1964, 9, 10)),
        ("Honza Jan, Dat. Nar. 9.2.1963", "Honza Jan", dt.date(1963, 2, 9)),
        ("Ondra Bondra, Nar. 07.06.49", "Ondra Bondra", dt.date(1949, 6, 7)),
        ("Alex Malex  Nar. 28.09.1976", "Alex Malex", dt.date(1976, 9, 28)),
        ("Jura Bura,Dat.Nar.1.8.1968", "Jura Bura", dt.date(1968, 8, 1)),
    ],
)
def test_inline(jmeno, jmeno_final, narozeni):
    assert jmeno_narozeni(jmeno) == (jmeno_final, narozeni)
