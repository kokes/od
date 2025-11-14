import pytest
from sqlalchemy import create_engine


@pytest.mark.parametrize(
    ["module"],
    [
        # TODO: zapnout postupne dalsi
        ("ares",),
        ("czechpoint",),
        ("datovky",),
        ("dotinfo",),
        # ("eufondy",),
        ("iissp",),
        # ("justice",),
        # TODO: psp ma problem s konektivitou
        # ("psp",),
        # ("steno",),
        # ("red",),
        ("res",),
        ("ruian",),
        ("smlouvy",),
        ("szif",),
        ("udhpsh",),
        # ("volby",),
        # TODO: ze by MMR zase blokovalo zahranicni servery?
        # ("zakazky",),
    ],
)
def test_partial(tmp_path, module):
    from . import main

    engine = create_engine(f"sqlite:///{tmp_path / 'data.db'}")

    main.main(
        base_outdir=tmp_path,
        module_name=module,
        partial=True,
        engine=engine,
    )
