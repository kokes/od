import csv
import gzip
import logging
import json
import os
from urllib.parse import urlparse
from urllib.request import urlretrieve


def remote_csv(url, cache_dir):
    filename = os.path.split(urlparse(url).path)[-1]
    local_path = os.path.join(cache_dir, filename)
    if not os.path.isfile(local_path):
        logging.info('Nemam %s (%s) lokalne, stahuju', filename, url)
        urlretrieve(url, local_path)

    with gzip.open(local_path, 'rt') as f:
        cr = csv.DictReader((line.replace('\0', '') for line in f))
        yield from cr


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    rdir = 'data/raw/'
    os.makedirs(rdir, exist_ok=True)
    with open('ciselnik.json') as f:
        csmp = json.load(f)

    csl = dict()

    logging.info('Nacitam ciselniky')
    for cs in csmp:
        for ln in remote_csv(cs['url'], rdir):
            csl[ln[cs['id']]] = ln[cs['nazev']]

    mapping = dict()
    logging.info('Nacitam prijemce pomoci (ICO)')

    for el in remote_csv('PrijemcePomoci.csv.gz', rdir):
        mapping[el['idPrijemce']] = int(
            el['ico']) if len(el['ico']) > 0 else None

    headers = {
        'Dotace': ['idDotace', 'idPrijemce', 'projektKod', 'podpisDatum', 'subjektRozliseniKod', 'ukonceniPlanovaneDatum', 'ukonceniSkutecneDatum', 'zahajeniPlanovaneDatum', 'zahajeniSkutecneDatum', 'zmenaSmlouvyIndikator', 'projektIdnetifikator', 'projektNazev', 'iriOperacniProgram', 'iriPodprogram', 'iriPriorita', 'iriOpatreni', 'iriPodopatreni', 'iriGrantoveSchema', 'iriProgramPodpora', 'iriTypCinnosti', 'iriProgram', 'dPlatnost', 'dtAktualizace'],
        'Rozhodnuti': ['idRozhodnuti', 'idDotace', 'castkaPozadovana', 'castkaRozhodnuta', 'iriPoskytovatelDotace', 'iriCleneniFinancnichProstredku', 'iriFinancniZdroj', 'rokRozhodnuti', 'investiceIndikator', 'navratnostIndikator', 'refundaceIndikator', 'dPlatnost', 'dtAktualizace'],
        'RozpoctoveObdobi': ['idObdobi', 'idRozhodnuti', 'castkaCerpana', 'castkaUvolnena', 'castkaVracena', 'castkaSpotrebovana', 'rozpoctoveObdobi', 'vyporadaniKod', 'iriDotacniTitul', 'iriUcelovyZnak', 'dPlatnost', 'dtAktualizace'],
    }

    for ds, exphd in headers.items():
        logging.info('Nacitam %s', ds)
        with open('data/{}.csv'.format(ds), 'w') as fw:
            cw = csv.DictWriter(fw, fieldnames=exphd)
            cw.writeheader()

            for ln in remote_csv(f'{ds}.csv.gz', rdir):
                # vypln info z ciselniku
                for j, el in enumerate(ln):
                    if el.startswith('http://'):
                        # tohle proste spadne, kdyz bude chybet klasifikator
                        ln[j] = csl[el]

                if ds == 'Dotace':
                    ln['idPrijemce'] = mapping[ln['idPrijemce']]  # idPrijemce -> ico
                # assert ln[3].endswith('T00:00:00.000Z') # v krajnich pripadech
                # tam je cas, ale v jednom z milionu
                # ln[3] = ln[3][:10] # z podpisDatum nas zajima datum, ne cas

                cw.writerow(ln)
