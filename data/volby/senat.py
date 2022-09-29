import csv
import os
from urllib.parse import quote_plus, urljoin
from urllib.request import Request, urlopen

import lxml.html
from tqdm import tqdm

# db schema
# cat senat_kandidati.csv | psql -c "COPY volby.senat_kandidati_vse FROM stdin CSV HEADER"
# CREATE TABLE volby.senat_kandidati_vse (
#     rok int not null,
#     obvod text not null,
#     datum text not null,
#     jmeno text not null,
#     navrhujici_strana text not null,
#     hlasy_k1 int not null,
#     hlasy_k2 int,
#     procenta_k1 decimal(5, 2) not null,
#     procenta_k2 decimal(5, 2)
# )

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def gurl(url):
    fn = "cache/%s.html" % quote_plus(url)
    if os.path.isfile(fn):
        with open(fn, "rt") as f:
            dt = f.read()
        return dt

    os.makedirs("cache", exist_ok=True)
    req = Request(url, headers={"User-Agent": ua})
    with urlopen(req) as r, open(fn, "wb") as f:
        dt = r.read()
        f.write(dt)

    return dt.decode("utf-8")


burl = "https://volby.cz/"
dt = lxml.html.fromstring(gurl(burl))

lnk = [
    j for j in dt.cssselect("a") if "pls/senat" in j.attrib["href"] and j.text.isdigit()
]

volby = ", ".join(j.text for j in lnk)
print(f"mame tyto volby: {volby}")


fln = []
for ln in lnk:
    bu = urljoin(burl, ln.attrib["href"])
    dt = lxml.html.fromstring(gurl(bu))

    vs = [j for j in dt.cssselect("a") if j.text == "Výsledky hlasování"]
    if len(vs) == 1:
        fln.append(urljoin(burl, ln.attrib["href"]))
        continue

    # doplnovaci volby

    fln.extend(
        [urljoin(bu, ll.attrib["href"]) for ll in dt.cssselect("div#tlacitka a")]
    )


with open("senat_kandidati.csv", "wt") as fw:
    cw = csv.writer(fw)
    cw.writerow(["rok", "obvod", "datum", "jmeno", "navrhujici_strana", "hlasy_k1", "hlasy_k2", "procenta_k1", "procenta_k2"])
    for ln in tqdm(fln):
        dt = lxml.html.fromstring(gurl(ln))

        vs = [j for j in dt.cssselect("a") if j.text == "Výsledky hlasování"]
        assert len(vs) == 1, ln
        vs = urljoin(bu, vs[0].attrib["href"])

        dt = lxml.html.fromstring(gurl(vs))

        for vl in dt.cssselect("td.cislo a"):
            nu = urljoin(bu, vl.attrib["href"])
            vld = lxml.html.fromstring(gurl(nu))

            rok = vld.cssselect("p.drobek a")[1].text.split(" ")[1]
            obv = vld.cssselect("h3")[0].text.strip()[7:]

            tt = vld.cssselect("h1")[0].text.strip()
            dat = tt[tt.index(" dne") + 5 :]  # datum prvniho kola

            jmena = [
                j.text.replace("\xa0", " ")
                for j in vld.cssselect('td[headers="s2a1 s2b2"]')
            ]
            # TODO: abstrahuj tyhle vytahovacky
            k1 = [
                int(j.text.replace("\xa0", "").replace(",", "."))
                if j.text != "X" else None
                for j in vld.cssselect('td[headers="s2a5 s2b3"]')
            ]
            k2 = [
                int(j.text.replace("\xa0", "").replace(",", "."))
                if j.text != "X" else None
                for j in vld.cssselect('td[headers="s2a5 s2b4"]')
            ]
            p1 = [
                float(j.text.replace("\xa0", "").replace(",", "."))
                if j.text != "X" else None
                for j in vld.cssselect('td[headers="s2a6 s2b5"]')
            ]
            p2 = [
                float(j.text.replace("\xa0", "").replace(",", "."))
                if j.text != "X" else None
                for j in vld.cssselect('td[headers="s2a6 s2b6"]')
            ]
            navrstrana = [j.text for j in vld.cssselect('td[headers="s2a3"]')]

            assert len(jmena) == len(navrstrana) == len(k1) == len(k2) == len(p1) == len(p2)
            
            nr = len(jmena)
            for j in range(nr):
                cw.writerow([
                    rok, obv, dat,
                    jmena[j], navrstrana[j], k1[j], k2[j], p1[j], p2[j],
                ])
