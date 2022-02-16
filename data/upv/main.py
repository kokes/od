import csv
import json
import os
import zipfile
from glob import glob
from tempfile import TemporaryDirectory
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, urlretrieve

import lxml.etree
import lxml.html
from tqdm import tqdm

TM_PATH = "/".join(
    [
        "TradeMarkTransactionBody",
        "TransactionContentDetails",
        "TransactionData",
        "TradeMarkDetails",
        "TradeMark",
    ]
)


def extract(element, mapping):
    ret = {}
    for v in mapping:
        k = v["column"]
        if not v.get("path"):
            ret[k] = element.text
            continue

        if v["path"].startswith("#"):
            ret[k] = element.attrib[v["path"][1:]]
            continue

        els = element.findall(v["path"])
        if len(els) == 0:
            ret[k] = None
            continue

        if v.get("array", False) is False and len(els) > 1:
            raise ValueError("unexpected length: {}".format(k))

        ret[k] = []
        for el in els:
            for ak, av in v.get("attrs", {}).items():
                if el.attrib[ak] != av:
                    raise KeyError(
                        'unexpected attribute value: "{}": "{}"'.format(ak, av)
                    )

            if "mapping" in v:
                ret[k].append(extract(el, v["mapping"]))
            else:
                ret[k].append(el.text)

        if not v.get("array", False):
            ret[k] = ret[k][0]

    return ret


def main(outdir: str, partial: bool = False):
    burl = "https://isdv.upv.cz/webapp/webapp.opendata.tm"

    with urlopen(burl, timeout=60) as u:
        ht = lxml.html.parse(u)

    lnks = [
        urljoin(burl, j.attrib["href"])
        for j in ht.findall(".//a")
        if j.attrib["href"].endswith(".zip")
        and not j.attrib["href"].endswith("_PIC.zip")
    ]

    with TemporaryDirectory() as tmpdir:
        for num, lnk in tqdm(enumerate(lnks)):
            if partial and num > 5:
                break
            fn = os.path.basename(urlparse(lnk).path)
            tfn = os.path.join(tmpdir, fn)
            urlretrieve(lnk, tfn)

        cdir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cdir, "mapping.json")) as f:
            mp = json.load(f)

        zfns = glob(os.path.join(tmpdir, "*.zip"))
        with open(os.path.join(outdir, "inserts.csv"), "wt") as fi, open(
            os.path.join(outdir, "deletes.csv"), "wt"
        ) as fd:
            ci = csv.DictWriter(fi, fieldnames=[j["column"] for j in mp["insert"]])
            cd = csv.DictWriter(fd, fieldnames=[j["column"] for j in mp["delete"]])
            ci.writeheader()
            cd.writeheader()

            for zfn in tqdm(zfns):
                with zipfile.ZipFile(zfn) as zf:
                    xfns = [
                        j.filename for j in zf.filelist if j.filename.endswith(".xml")
                    ]

                    for xfn in xfns:
                        with zf.open(xfn) as f:
                            et = lxml.etree.iterparse(f)

                            for action, element in et:
                                if not (
                                    element.tag == "Transaction" and action == "end"
                                ):
                                    continue

                                operation = element.attrib["operationCode"]
                                assert operation in ("Insert", "Delete")

                                if operation == "Delete":
                                    tms = element.findall(
                                        "TradeMarkTransactionDelete/TradeMark"
                                    )
                                    assert len(tms) == 1
                                    row = extract(tms[0], mp["delete"])
                                    row = {
                                        k: json.dumps(v, ensure_ascii=False)
                                        if isinstance(v, (dict, list))
                                        else v
                                        for k, v in row.items()
                                    }
                                    cd.writerow(row)
                                else:
                                    tms = element.findall(
                                        TM_PATH,
                                    )
                                    assert len(tms) == 1
                                    row = extract(tms[0], mp["insert"])
                                    row = {
                                        k: json.dumps(v, ensure_ascii=False)
                                        if isinstance(v, (dict, list))
                                        else v
                                        for k, v in row.items()
                                    }
                                    ci.writerow(row)

                                element.clear()


if __name__ == "__main__":
    main(".")
