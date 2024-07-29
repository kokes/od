import pytest


@pytest.mark.parametrize(
    ["module"],
    [
        ("ares",),
        ("red",),
    ],
)
def test_partial(tmp_path, module):
    from . import main

    main.main(outdir=tmp_path, module=module)

    pass
