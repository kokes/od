import pytest

from main import fix_name


@pytest.mark.parametrize(
    "fname,lname,efname,elname",
    [
        ("", "", "", ""),
        (None, None, None, None),
        ("JAN", "NOVÁK", "Jan", "Novák"),
        ("ANNA MARIE", "KALINGROVÁ", "Anna Marie", "Kalingrová"),
        ("", "0", "", ""),
        ("", "neuvedeno", "", ""),
        ("", '"neuvedeno"', "", ""),
    ],
)
def test_basic_issues(fname, lname, efname, elname):
    row = {"jmeno": fname, "prijmeni": lname}
    expected = {"jmeno": efname, "prijmeni": elname}
    result = fix_name(row, first_name_key="jmeno", last_name_key="prijmeni")
    assert result == expected
