import contextlib
import csv
import datetime as dt
import functools
import glob
import gzip
import hashlib
import json
import multiprocessing
import os
import re
import shutil
import time
from collections import defaultdict
from urllib.parse import urlparse
from urllib.request import urlopen

import lxml.etree
from tqdm import tqdm

NON_ISO_DATUM = re.compile(r"^(\d{1,2})[\.\-](\d{1,2})[\.\-](\d{4})$")
HTTP_TIMEOUT = 180
CACHE_DIR = "cache"
CACHE_ENABLED = bool(int(os.environ.get("CACHE_ENABLED", "0")))
CURRENT_YEAR_ONLY = bool(int(os.environ.get("CURRENT_YEAR_ONLY", "1")))


def gen_schema(element, parent=None):
    ret = {}
    for j in element:
        ch = j.getchildren()
        if len(ch) > 0:
            ret[j.tag] = gen_schema(j, (parent or []) + [j.tag])
        elif hasattr(j, "text") and j.text is None:
            pass
        else:
            ret[j.tag] = "/".join((parent or []) + [j.tag])

    return ret


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def extrahuj(node, schema):
    ret = {}
    for k, v in schema.items():
        if isinstance(v, dict):
            ret[k] = extrahuj(node, v)
        else:
            ret[k] = getattr(node.find(v), "text", None)

    return ret


def uprav_data(row, mapping):
    "Bude inlinovano behem refactoringu"
    for col in mapping.get("non_iso_datum", []):
        if not row[col]:
            continue
        den, mesic, rok = NON_ISO_DATUM.match(row[col]).groups()
        row[col] = dt.date(int(rok), int(mesic), int(den))

    return row


@contextlib.contextmanager
def cached_urlopen(url, timeout=HTTP_TIMEOUT):
    shasum = hashlib.sha256(url.encode("utf-8")).hexdigest()
    if url.endswith(".gz"):
        shasum += ".gz"
    fn_path = os.path.join(CACHE_DIR, shasum)
    if os.path.isfile(fn_path):
        with open(fn_path, "rb") as f:
            yield f
        return

    with urlopen(url, timeout=timeout) as r:
        if not CACHE_ENABLED:
            yield r
            return
        fn_tmp = fn_path + ".tmp"
        with open(fn_tmp, "wb") as f:
            shutil.copyfileobj(r, f)
        os.rename(fn_tmp, fn_path)
        with cached_urlopen(url, timeout) as r:
            yield r


def nahraj_ds(url):
    with cached_urlopen(url, timeout=HTTP_TIMEOUT) as r:
        with gzip.open(r, "rb") as f:
            et = lxml.etree.iterparse(f)
            yield from et


def zpracuj_ds(url, schemas, outdir, partial, autogen, icos):
    et = nahraj_ds(url)

    fs, csvs, schemasd = dict(), dict(), dict()
    ds = os.path.basename(urlparse(url).path).partition(".")[0]

    os.makedirs(os.path.join(outdir, "subjekty"), exist_ok=True)
    fs["subjekty"] = open(
        os.path.join(outdir, "subjekty", f"{ds}.csv"), "w", encoding="utf8"
    )
    csvs["subjekty"] = csv.writer(fs["subjekty"], lineterminator="\n")
    csvs["subjekty"].writerow(["ico", "nazev", "datum_zapis", "datum_vymaz"])

    for el in schemas:
        udaje = [el["udaj"]] if isinstance(el["udaj"], str) else el["udaj"]
        if el.get("ignore"):
            for udaj in udaje:
                schemasd[udaj] = el
            continue

        fn = f"{ds}.csv"
        os.makedirs(os.path.join(outdir, el["soubor"]), exist_ok=True)
        ffn = os.path.join(outdir, el["soubor"], fn)
        f = open(ffn, "w", encoding="utf8")
        cw = csv.DictWriter(
            f, fieldnames=["ico"] + list(el["schema"].keys()), lineterminator="\n"
        )
        cw.writeheader()

        for udaj in udaje:
            schemasd[udaj] = el
            fs[udaj] = f
            csvs[udaj] = cw

    for num, (action, el) in enumerate(et):
        if partial and num > 1e5:
            break
        assert action == "end", action
        if el.tag != "Subjekt":
            continue
        ch = {j.tag for j in el.getchildren()}
        dch = ch - {"ico", "nazev", "udaje", "zapisDatum", "vymazDatum"}
        assert len(dch) == 0, dch

        nazev = el.find("nazev").text
        zapis = el.find("zapisDatum").text
        vymaz = getattr(el.find("vymazDatum"), "text", None)
        ico = getattr(el.find("ico"), "text", None)

        if not ico:
            # TODO(PR): multiprocessing unsafe
            # with open("chybejici_ico.log", encoding="utf-8", mode="a+") as fw:
            #     fw.write(f"{nazev}\t{el.sourceline}\t{url}\n")
            continue

        # kdyz zpracovavame data starsi nez letosni, musime
        # zahazovat jiz zpracovana data
        if ico in icos:
            el.clear()
            continue
        icos.add(ico)

        csvs["subjekty"].writerow([ico, nazev, zapis, vymaz])

        for udaj_raw in el.find("udaje").iterchildren():
            # tohle je asi irelevantni, asi nas zajimaj jen podudaje??
            # beru zpet - tohle nas zajima prave tehdy, kdyz nemame podudaje
            # beru opet zpet - třeba u zastoupení v dozorčí radě nás zajímá obojí :(

            udaj_typ = udaj_raw.find("udajTyp/kod").text

            if udaj_typ not in schemasd:
                # print("nenalezeno", udaj_typ, url)
                autogen.put((udaj_typ, gen_schema(udaj_raw)))
                continue

            if not schemasd[udaj_typ].get("ignore", False):
                schema = schemasd[udaj_typ]["schema"]
                row = extrahuj(udaj_raw, schema)
                row = uprav_data(row, schemasd[udaj_typ])
                row = {
                    k: json.dumps(v) if isinstance(v, dict) else v
                    for k, v in row.items()
                }
                row["ico"] = ico
                csvs[udaj_typ].writerow(row)

            if udaj_raw.find("podudaje") is not None:
                podudaje = udaj_raw.find("podudaje").getchildren()
                podpodudaje = udaj_raw.find("podudaje/Udaj/podudaje")
                if podpodudaje is not None:
                    podudaje += podpodudaje.getchildren()

                for podudaj_raw in podudaje:
                    podudaj_typ = podudaj_raw.find("udajTyp/kod").text

                    if podudaj_typ not in schemasd:
                        # print("nenalezeno", podudaj_typ, url)
                        autogen.put((podudaj_typ, gen_schema(podudaj_raw)))
                        continue

                    if not schemasd[podudaj_typ].get("ignore", False):
                        schema = schemasd[podudaj_typ]["schema"]
                        row = extrahuj(podudaj_raw, schema)
                        row = uprav_data(row, schemasd[podudaj_typ])
                        row = {
                            k: json.dumps(v) if isinstance(v, dict) else v
                            for k, v in row.items()
                        }
                        row["ico"] = ico
                        # TODO: obezlicka, kterou je treba resit
                        # mozna ukladat ico_angos jen pro ceske firmy
                        if "ico_angos" in row:
                            row["ico_angos"] = (
                                int(row["ico_angos"])
                                if row["ico_angos"]
                                and row["ico_angos"].isdigit()
                                and len(row["ico_angos"]) <= 8
                                else None
                            )
                        csvs[podudaj_typ].writerow(row)
            else:
                pass  # TODO: handluj non-podudaje

        el.clear()

    for el in fs.values():
        el.close()

    return url, icos


def main(outdir: str, partial: bool = False):
    os.makedirs(CACHE_DIR, exist_ok=True)
    for file in glob.glob(os.path.join(CACHE_DIR, "*.tmp")):
        os.remove(file)

    # package_list a package_list_compact se asi lisi - ten nekompaktni endpoint
    # nejde filtrovat??? Tak to asi udelame na klientovi
    url_pl = "https://dataor.justice.cz/api/3/action/package_list"

    with cached_urlopen(url_pl, timeout=HTTP_TIMEOUT) as r:
        data = json.load(r)
        assert data["success"]

    dss = [ds for ds in data["result"] if "-full-" in ds]
    print(f"celkem {len(dss)} datasetu")

    dsm = defaultdict(list)
    for ds in dss:
        year = ds.rpartition("-")[-1]
        dsm[year].append(ds)

    years = sorted(dsm.keys(), reverse=True)
    print(f"mame data pro roky: {years}")
    if CURRENT_YEAR_ONLY:
        print(f"zpracovavame jen rok {years[0]}")
        years = years[:1]

    cdir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cdir, "xml_schema.json"), encoding="utf-8") as f:
        schemas = json.load(f)

    # samotna multiprocessing.queue z nejakyho duvodu nefungovala
    autogen = multiprocessing.Manager().Queue()

    # TODO: chcem fakt jet naplno? co kdyz budem parametrizovat jednotlivy moduly?
    ncpu = multiprocessing.cpu_count()

    processed = set()
    for year in years:
        dss = dsm[year]

        urls = []
        for j, ds in enumerate(tqdm(dss, desc=f"{year} meta")):
            if partial and len(urls) > 20:
                break
            url = f"https://dataor.justice.cz/api/3/action/package_show?id={ds}"
            with cached_urlopen(url, timeout=HTTP_TIMEOUT) as r:
                dtp = json.load(r)
                assert dtp["success"]
            ds_url = [
                j["url"]
                for j in dtp["result"]["resources"]
                if j["url"].endswith(".xml.gz")
            ]
            assert len(ds_url) == 1

            # mohli bychom to omezit jen na mensi soubory, ale radsi
            # prectu trosku z vicero dat
            # if partial:
            #     req = urlopen(ds_url[0])
            #     if int(req.headers.get("Content-Length")) > 10_000_000:
            #         continue

            urls.append(ds_url[0])

        progress = tqdm(total=len(urls), desc=f"{year} data")

        zpracuj = functools.partial(
            zpracuj_ds,
            schemas=schemas,
            outdir=outdir,
            partial=partial,
            autogen=autogen,
            icos=set(list(processed)),  # bojim se konkurence
        )

        year_icos = set()
        t = time.time()
        with multiprocessing.Pool(ncpu) as pool:
            for _, icos in pool.imap_unordered(zpracuj, urls):
                # logging.debug(url)?
                progress.update(n=1)
                year_icos.update(icos)

        progress.close()
        processed.update(year_icos)
        print(f"zpracovano {year} za {time.time() - t:.2f}s")

    # nezpracovany objekty je treba rucne projit
    schema_autogen = dict()
    while not autogen.empty():
        obj, schema = autogen.get()
        schema_autogen[obj] = merge(
            schema,
            schema_autogen.get(obj, {}),
        )
    if len(schema_autogen):
        print(f"nalezeno {len(schema_autogen)} neznamych objektu ve zdrojovych datech")
        print("exportuji xml_schema_chybejici.json")
        with open("xml_schema_chybejici.json", "w") as fw:
            json.dump(schema_autogen, fw, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main(".")
