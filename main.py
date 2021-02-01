import argparse
import os
import shutil
import sys
from importlib import import_module

from sqlalchemy import create_engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--connstring", type=str, help="connection string to the database you wish to use")
    parser.add_argument("--partial", action="store_true", help="only process a part of the source data to speed things up")
    parser.add_argument("modules", nargs="*", help="specify which datasets to include")
    args = parser.parse_args()

    base_outdir = "csv"
    os.makedirs(base_outdir, exist_ok=True)

    engine = None
    if args.connstring:
        engine = create_engine(args.connstring)

    # TODO: nejak pridat `czechinvest` - je to ready, jen nefunguje stahovani souboru
    # TODO: vyresit nejak zanoreny adresare (psp.steno) - aby se to nemlatilo u nazvu adresaru nebo schemat
    module_names = ["iissp", "cedr", "datovky", "szif", "upv", "wikidata", "dotinfo", "psp.steno", "cssz"]
    if args.modules:
        module_names = args.modules
    modules = {}
    schemas = {}
    # TODO: copy commands (or perhaps after `module(outdir)`? List that dir, open csv, do an executemany)

    for module in module_names:
        modules[module] = import_module(f"data.{module}.main").main
        schemas[module] = import_module(f"data.{module}.schema").schema

    if engine:
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

        module(outdir, partial=args.partial)
