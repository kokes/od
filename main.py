import os
import shutil
import sys
from importlib import import_module

from sqlalchemy import create_engine

if __name__ == "__main__":
    # TODO: argparse that accepts
    # - connstring,
    # - if we should even work with a db,
    # - if we should convert data etc.
    # - if we're doing partial processing

    base_outdir = "csv"
    os.makedirs(base_outdir, exist_ok=True)

    engine = create_engine("sqlite:///:memory:")  # TODO: testing for now

    # TODO: nejak pridat `czechinvest` - je to ready, jen nefunguje stahovani souboru
    module_names = ["iissp", "cedr", "datovky", "szif", "upv", "wikidata", "dotinfo"]
    if len(sys.argv) > 1:
        module_names = sys.argv[1:]
    modules = {}
    schemas = {}
    # TODO: copy commands (or perhaps after `module(outdir)`? List that dir, open csv, do an executemany)

    for module in module_names:
        modules[module] = import_module(f"data.{module}.main").main
        schemas[module] = import_module(f"data.{module}.schema").schema

    for module_name, schema in schemas.items():
        for table in schema:
            # TODO: if pg, set schema?
            table.create(engine, checkfirst=True)

    # TODO: multiprocessing
    for module_name, module in modules.items():
        print(module_name)
        print("=" * len(module_name))

        outdir = os.path.join(base_outdir, module_name)
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        os.makedirs(outdir, exist_ok=True)

        module(outdir, partial=True)  # TODO: partial hardcoded for now
