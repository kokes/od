import argparse
import os
import shutil
import sys
from importlib import import_module

from sqlalchemy import create_engine

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connstring", type=str, help="connection string pro databazi tve volby"
    )
    parser.add_argument(
        "--partial",
        action="store_true",
        help="procesuj jen cast vstupnich dat - vhodne pro testovani, CI apod.",
    )
    parser.add_argument("--all", action="store_true", help="procesuj vsechny moduly")
    parser.add_argument("modules", nargs="*", help="specify which datasets to include")
    args = parser.parse_args()

    if args.all and len(args.modules) > 0:
        raise argparse.ArgumentError(
            "specifikuj bud --all, nebo specificke datasety, ne oboji"
        )

    base_outdir = "csv"
    os.makedirs(base_outdir, exist_ok=True)

    engine = None
    if args.connstring:
        engine = create_engine(args.connstring)

    # TODO: nejak pridat `czechinvest` - je to ready, jen nefunguje stahovani souboru
    module_names = [
        "cedr",
        # TODO: docasne vypnuto, protoze jsem zkracoval nazvy tabulek, ktery
        # ted nesedej mezi schematem a mappingem
        # "cssz",
        "datovky",
        "dotinfo",
        "iissp",
        "justice",
        "psp",
        "steno",
        "smlouvy",
        "szif",
        "upv",
        "wikidata",
        "zakazky",
        "ares",  # schvalne na konci, protoze nacita hodne dat
    ]
    if args.modules:
        module_names = args.modules
    modules = {}
    schemas = {}
    # TODO: copy commands (or perhaps after `module(outdir)`? List that dir, open csv, do an executemany)
    # also make sure we TRUNCATE each table before we insert into it (because we may have skipped the CREATE part)

    for module in module_names:
        modules[module] = import_module(f"data.{module}.main").main
        schemas[module] = import_module(f"data.{module}.schema").schema

    if engine:
        for module_name, schema in schemas.items():
            for table in schema:
                if engine.name == "postgresql":
                    table.schema = module_name
                    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {module_name}")
                else:
                    table.name = f"{module_name}_{table.name}"
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

        if engine:
            if engine.name == "postgresql":
                for table in schemas[module_name]:
                    print(f"Nahravam {table} do {module_name}")
                    full_table_name = f"{module_name}.{table.name}"
                    copy_statement = f"COPY {full_table_name} FROM stdin WITH CSV HEADER"
                    truncate_statement = f"TRUNCATE {full_table_name} CASCADE"  # TODO: cascade yolo
                    fn_cand = os.path.join(outdir, table.name+".csv")
                    dir_cand = os.path.join(outdir, table.name)
                    if os.path.isfile(fn_cand):
                        conn = engine.raw_connection()
                        with conn.cursor() as cur, open(fn_cand, "rt", encoding="utf-8") as f:
                            cur.execute(truncate_statement)
                            cur.copy_expert(copy_statement, f)
                        conn.commit()  # TODO: proc nejde context manager? starej psycopg?
                    elif os.path.isdir(dir_cand):
                        for basename in os.listdir(dir_cand):
                            filename = os.path.join(dir_cand, basename)
                            # TODO: nasledujici se opakuje, abstrahovat
                            conn = engine.raw_connection()
                            with conn.cursor() as cur, open(filename, "rt", encoding="utf-8") as f:
                                cur.execute(truncate_statement)
                                cur.copy_expert(copy_statement, f)
                            conn.commit()
                    else:
                        raise IOError(f"neexistujou data pro {module_name}.{table.name}")

                # TODO: copy_expert nebo copy_from, truncate pred tim
                # list dir, copy using raw conn
                pass
            elif engine.name == "sqlite":
                # TODO: executemany
                raise ValueError("sqlite not supported yet")
            else:
                raise ValueError(f"{engine.name} not supported yet")
