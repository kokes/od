import argparse
import csv
import os
import shutil
from collections import defaultdict
import sys
from importlib import import_module

from sqlalchemy import create_engine, Boolean

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connstring", type=str, help="connection string pro databazi tve volby"
    )
    parser.add_argument(
        "--schema_prefix", type=str, default="", help="prefix pro nazvy schemat (postgres) ci tabulek (sqlite)"
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
        "eufondy",
        "iissp",
        "justice",
        "psp",
        "steno",
        "smlouvy",
        "szif",
        "upv",
        "wikidata",
        "zakazky",
        "volby",
        "udhpsh",
        "res",
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
            table_loads = defaultdict(list)
            for table in schemas[module_name]:
                fn_cand = os.path.join(outdir, table.name+".csv")
                dir_cand = os.path.join(outdir, table.name)
                if os.path.isfile(fn_cand):
                    table_loads[(module_name, table.name)].append(fn_cand)
                elif os.path.isdir(dir_cand):
                    for basename in os.listdir(dir_cand):
                        table_loads[(module_name, table.name)].append(os.path.join(dir_cand, basename))
                else:
                    raise IOError(f"neexistujou data pro {module_name}.{table.name}")

            for table in schemas[module_name]:
                print(f"Nahravam {table.name} do {module_name}")
                files = table_loads[(module_name, table.name)]
                if engine.name == "postgresql":
                    table.schema = f"{args.schema_prefix}{module_name}"
                    full_table_name = f"{table.schema}.{table.name}"

                    engine.execute(f"CREATE SCHEMA IF NOT EXISTS {table.schema}")
                    table.create(engine, checkfirst=True)  # TODO: drop first?

                    conn = engine.raw_connection()
                    cur = conn.cursor()
                    cur.execute(f"TRUNCATE {full_table_name} CASCADE")  # TODO: cascade yolo
                    for filename in files:
                        with open(filename, "rt", encoding="utf-8") as f:
                            cur.copy_expert(f"COPY {full_table_name} FROM stdin WITH CSV HEADER", f)
                    conn.commit()  # TODO: proc nejde context manager? starej psycopg?
                elif engine.name == "sqlite":
                    table.name = f"{args.schema_prefix}{module_name}_{table.name}"
                    table.create(engine, checkfirst=True)  # TODO: drop first?
                    conn = engine.raw_connection()

                    ph = ", ".join(["?"]*len(table.columns))
                    query = f"INSERT INTO {table.name} VALUES({ph})"
                    bools = [isinstance(j.type, Boolean) for j in table.columns]
                    for filename in files:
                        buffer = []
                        with open(filename, "rt", encoding="utf-8") as f:
                            cr = csv.reader(f)
                            next(cr)  # header
                            for row in cr:
                                row = [bool(el) if bools[j] and el != "" else el for j, el in enumerate(row)]
                                row = [None if j == "" else j for j in row]
                                buffer.append(row)
                                if len(buffer) == 100:
                                    conn.executemany(query, buffer)
                                    buffer = []
                            if len(buffer) > 0:
                                conn.executemany(query, buffer)
                    conn.commit()
                else:
                    raise IOError(f"{engine.name} not supported yet")
