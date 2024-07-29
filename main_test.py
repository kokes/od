import pytest


@pytest.mark.parametrize(
    ["module"],
    [
        ("ares",),
        ("cssz",),
        # czechinvest uplne zrusil svoje data asi - poptavam
        # ("czechinvest",),  # TODO
        ("czechpoint",),
        ("datovky",),
        ("dotinfo",),
        ("eufondy",),
        ("iissp",),
        ("justice",),
        # TODO: psp ma problem s konektivitou
        # ("psp",),
        # ("steno",),
        ("red",),
        ("res",),
        ("ruian",),
        ("smlouvy",),
        ("szif",),
        ("udhpsh",),
        ("volby",),
        ("zakazky",),
    ],
)
def test_partial(tmp_path, module):
    from . import main

    engine = None  # TODO: pridat

    main.main(
        base_outdir=tmp_path,
        module_name=module,
        partial=True,
        engine=engine,
    )
