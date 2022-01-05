import csv
import gzip
import json
import logging
import os
from urllib.parse import urljoin
from urllib.request import urlopen


def remote_csv(url):
    if not url.startswith("https://"):
        url = urljoin("https://cedropendata.mfcr.cz/c3lod/", url)

    with urlopen(url, timeout=30) as r, gzip.open(r, "rt") as f:
        cr = csv.DictReader((line.replace("\0", "") for line in f))
        yield from cr


def main(outdir: str, partial: bool = False):
    logging.getLogger().setLevel(logging.INFO)
    cdir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(cdir, "ciselnik.json")) as f:
        csmp = json.load(f)

    csl = dict()

    logging.info("Nacitam ciselniky")
    for cs in csmp:
        for ln in remote_csv(cs["url"]):
            csl[ln[cs["id"]]] = ln[cs["nazev"]]

    mapping = dict()
    logging.info("Nacitam prijemce pomoci (ICO)")

    for num, el in enumerate(remote_csv("PrijemcePomoci.csv.gz")):
        if partial and num > 2e5:
            break
        mapping[el["idPrijemce"]] = int(el["ico"]) if len(el["ico"]) > 0 else None

    headers = {
        "Dotace": [
            "idDotace",
            "idPrijemce",
            "projektKod",
            "podpisDatum",
            "subjektRozliseniKod",
            "ukonceniPlanovaneDatum",
            "ukonceniSkutecneDatum",
            "zahajeniPlanovaneDatum",
            "zahajeniSkutecneDatum",
            "zmenaSmlouvyIndikator",
            "projektIdnetifikator",
            "projektNazev",
            "iriOperacniProgram",
            "iriPodprogram",
            "iriPriorita",
            "iriOpatreni",
            "iriPodopatreni",
            "iriGrantoveSchema",
            "iriProgramPodpora",
            "iriTypCinnosti",
            "iriProgram",
            "dPlatnost",
            "dtAktualizace",
        ],
        "Rozhodnuti": [
            "idRozhodnuti",
            "idDotace",
            "castkaPozadovana",
            "castkaRozhodnuta",
            "iriPoskytovatelDotace",
            "iriCleneniFinancnichProstredku",
            "iriFinancniZdroj",
            "rokRozhodnuti",
            "investiceIndikator",
            "navratnostIndikator",
            "refundaceIndikator",
            "dPlatnost",
            "dtAktualizace",
        ],
        "RozpoctoveObdobi": [
            "idObdobi",
            "idRozhodnuti",
            "castkaCerpana",
            "castkaUvolnena",
            "castkaVracena",
            "castkaSpotrebovana",
            "rozpoctoveObdobi",
            "vyporadaniKod",
            "iriDotacniTitul",
            "iriUcelovyZnak",
            "dPlatnost",
            "dtAktualizace",
        ],
    }

    for ds, exphd in headers.items():
        logging.info("Nacitam %s", ds)
        tfn = os.path.join(outdir, f"{ds.lower()}.csv")
        with open(tfn, "w") as fw:
            cw = csv.DictWriter(fw, fieldnames=exphd)
            cw.writeheader()

            for num, ln in enumerate(remote_csv(f"{ds}.csv.gz")):
                if partial and num > 5e3:
                    break
                # vypln info z ciselniku
                for k, v in ln.items():
                    if v.startswith("http://") or v.startswith("https://"):
                        # tohle proste spadne, kdyz bude chybet klasifikator
                        ln[k] = csl[v]

                if ds == "Dotace":
                    # v castecnym zpracovani nemame vsechna data, tak je holt vynechame
                    if partial and ln["idPrijemce"] not in mapping:
                        continue
                    ln["idPrijemce"] = mapping[ln["idPrijemce"]]  # idPrijemce -> ico
                # assert ln[3].endswith('T00:00:00.000Z') # v krajnich pripadech
                # tam je cas, ale v jednom z milionu
                # ln[3] = ln[3][:10] # z podpisDatum nas zajima datum, ne cas

                cw.writerow(ln)


if __name__ == "__main__":
    main(".")
