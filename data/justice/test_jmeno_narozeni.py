import pytest

from main import jmeno_narozeni

# Jakub Nakup, Nar. 10.09.1964
# Honza Jan, Dat. Nar. 9.2.1963
# Ondra Bondra, Nar. 07.06.49

@pytest.mark.parametrize(
    ["jmeno", "jmeno_final", "narozeni"],
    [
        ("Jan Pan", "Jan Pan", None),
    ],
)
def test_inline(jmeno, jmeno_final, narozeni):
    assert jmeno_narozeni(jmeno) == (jmeno_final, narozeni)
