import os
import shutil
import sys
from importlib import import_module

if __name__ == "__main__":
    base_outdir = "csv"
    os.makedirs(base_outdir, exist_ok=True)

    module_names = ["iissp", "cedr"]
    if len(sys.argv) > 1:
        module_names = sys.argv[1:]
    modules = {}

    for module in module_names:
        modules[module] = import_module(f"data.{module}.main").main

    # TODO: multiprocessing
    for module_name, module in modules.items():
        print(module_name)
        print("=" * len(module_name))

        outdir = os.path.join(base_outdir, module_name)
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        os.makedirs(outdir, exist_ok=True)

        module(outdir)
