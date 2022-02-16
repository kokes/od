from importlib import import_module
from urllib.request import urlopen

modules = [
    "ares",
    "res",
    "udhpsh",
    "cssz",
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
    "icij",
]

# TODO(PR): docs
if __name__ == "__main__":
    # TODO(PR): problemy:
    # - udhpsh a par dalsich (no last modified)
    # - justice (megamoc datafilu)

    for module in modules:
        # TODO(PR): tohle triggeruje importy z toho main.py, takze by
        # to chtelo ty URL vyseparovat jinam mozna (a nebo poustet ve venvu)
        try:
            resources = import_module(f"data.{module}.main").resources()
        except AttributeError:
            print(module, "not found")
            continue
        for resource in resources:
            with urlopen(resource) as req:
                print(module, "\t", resource, "\t", req.headers.get("Last-Modified"))
