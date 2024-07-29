import pytest


@pytest.mark.parametrize(
    ["module"],
    [
        ("ares",),
        # ("red",),
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
