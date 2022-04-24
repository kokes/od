import csv
import os
from datetime import date
from urllib.request import urlopen

import lxml.etree
from tqdm import tqdm

HTTP_TIMEOUT = 60


def strip_ns(el):
    return el.tag.rpartition("}")[-1]


def el_dict(el):
    if el.text is not None:
        return el.text

    ret = dict()
    for ch in el.iterchildren():
        tg = strip_ns(ch)

        if tg not in ret:
            ret[tg] = el_dict(ch)
            continue

        if isinstance(ret[tg], list):
            ret[tg].append(el_dict(ch))
        else:
            ret[tg] = [ret[tg]] + [el_dict(ch)]

    return ret


def get_raw_data(partial: bool):
    url = "https://data.smlouvy.gov.cz/"
    with urlopen(url, timeout=HTTP_TIMEOUT) as r:
        et = lxml.etree.parse(r).getroot()

    keys = [
        "den",
        "mesic",
        "rok",
        "hashDumpu",
        "velikostDumpu",
        "casGenerovani",
        "dokoncenyMesic",
        "odkaz",
    ]

    for el in et:
        props = {
            k: getattr(el.find(f"{{{et.nsmap[None]}}}{k}"), "text", None) for k in keys
        }
        # chceme jen mesicni dumpy
        if props["den"]:
            continue
        if partial and int(props["rok"]) != date.today().year:
            continue

        fn = os.path.split(props["odkaz"])[-1]
        with urlopen(props["odkaz"], timeout=HTTP_TIMEOUT) as r:
            yield fn.replace(".xml", ".csv"), r


hds = [
    "dump",
    "id_verze",
    "id_smlouvy",
    "odkaz",
    "cas_zverejneni",
    "predmet",
    "datum_uzavreni",
    "cislo_smlouvy",
    "schvalil",
    "hodnotaBezDph",
    "hodnotaVcetneDph",
    "platny_zaznam",
]
hdu = [
    "dump",
    "smlouva",
    "subjekt",
    "ds",
    "nazev",
    "ico_raw",
    "ico",
    "adresa",
    "utvar",
    "platce",
    "prijemce",
]

nin = hdu.index("ico")  # kde mame ciselne ICO?


def main(outdir: str, partial: bool = False):
    outdir_smlouvy = os.path.join(outdir, "smlouvy")
    outdir_ucastnici = os.path.join(outdir, "ucastnici")
    os.makedirs(outdir_smlouvy, exist_ok=True)
    os.makedirs(outdir_ucastnici, exist_ok=True)

    for filename, data in get_raw_data(partial):
        tfn = os.path.join(outdir_smlouvy, filename)
        tfnu = os.path.join(outdir_ucastnici, filename)

        with open(tfn, "w", encoding="utf8") as fw, open(
            tfnu, "w", encoding="utf8"
        ) as fwu:
            cw = csv.writer(fw)
            cwu = csv.writer(fwu)
            cw.writerow(hds)
            cwu.writerow(hdu)
            rok, mesic = None, None

            et = lxml.etree.iterparse(data)

            for num, (_, el) in enumerate(tqdm(et, desc=filename)):
                if partial and num > 1e5:
                    break
                eln = strip_ns(el)
                if eln not in ("zaznam", "mesic", "rok"):
                    continue

                if eln != "zaznam":
                    if eln == "mesic":
                        mesic = el_dict(el)
                    elif eln == "rok":
                        rok = el_dict(el)
                    continue

                assert not (
                    rok is None or mesic is None
                ), "rok a mesic musi predchazet data"
                dt = el_dict(el)  # parsuj data
                el.clear()
                ts = f"{rok}-{mesic}"

                # smlouva samotna
                idv = int(dt["identifikator"]["idVerze"])
                row = [
                    ts,
                    idv,
                    int(dt["identifikator"]["idSmlouvy"]),
                    dt["odkaz"],
                    dt["casZverejneni"],
                    dt["smlouva"]["predmet"],
                    dt["smlouva"]["datumUzavreni"],
                    dt["smlouva"].get("cisloSmlouvy"),
                    dt["smlouva"].get("schvalil"),
                    dt["smlouva"].get("hodnotaBezDph"),
                    dt["smlouva"].get("hodnotaVcetneDph"),
                    dt["platnyZaznam"] == "1",
                ]
                row = [j.strip() if isinstance(j, str) else j for j in row]
                cw.writerow(row)

                # ucastnici (subjekt, pak smluvni strany)
                uc = [dt["smlouva"]["subjekt"]]
                if isinstance(dt["smlouva"]["smluvniStrana"], dict):
                    uc.append(dt["smlouva"]["smluvniStrana"])
                else:
                    uc.extend(dt["smlouva"]["smluvniStrana"])

                # pole subjekt
                for _, st in enumerate(uc):
                    row = [
                        ts,
                        idv,
                        False,
                        st.get("ds"),
                        st["nazev"],
                        st.get("ico"),
                        st.get("ico"),
                        st.get("adresa"),
                        st.get("utvar"),
                        st.get("platce"),
                        st.get("prijemce"),
                    ]
                    row = [j.strip() if isinstance(j, str) else j for j in row]
                    row[nin] = (
                        int(row[nin])
                        if (row[nin] and row[nin].isdigit() and (len(row[nin]) < 9))
                        else None
                    )

                    cwu.writerow(row)


if __name__ == "__main__":
    main(".")
