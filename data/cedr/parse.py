import subprocess
import shutil
import csv
import json
import os
from glob import glob

from tqdm import tqdm

def unpack(fn: str):
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')
    r = subprocess.run(['7z', 'x', '-otmp', fn])
    assert r.returncode == 0
    yield from glob('tmp/*.csv')
    if os.path.isdir('tmp'):
        shutil.rmtree('tmp')

if __name__ == '__main__':
    with open('ciselnik.json') as f:
        csmp = json.load(f)
    
    csl = dict()
    for cfn in glob('data/raw/ciselnik*.csv.7z'):
        for fn in unpack(cfn):
            with open(fn) as f:
                hd = next(f).strip()
                if hd not in csmp:
                    raise ValueError(f'{fn} nema ocekavanou hlavicku: "{hd}"')
                
                mp = csmp[hd]
                hd = hd.split(',')
                idn = hd.index(mp['id'])
                namen = hd.index(mp['nazev'])
                
                cr = csv.reader(f)
                for ln in cr:
                    csl[ln[idn]] = ln[namen]

    mapping = dict()
    for fn in unpack('data/raw/PrijemcePomoci.csv.7z'):
        with open(fn) as f:
            cr = csv.reader(f)
            hd = next(cr)
            assert hd[:2] == ['idPrijemce', 'ico'] # nic jineho nas nezajima

            for ln in cr:
                mapping[ln[0]] = int(ln[1]) if len(ln[1]) > 0 else None


    rdir = 'data/raw/'

    headers = {
        'Dotace': ['idDotace', 'idPrijemce', 'projektKod', 'podpisDatum', 'subjektRozliseniKod', 'ukonceniPlanovaneDatum', 'ukonceniSkutecneDatum', 'zahajeniPlanovaneDatum', 'zahajeniSkutecneDatum', 'zmenaSmlouvyIndikator', 'projektIdnetifikator', 'projektNazev', 'iriOperacniProgram', 'iriPodprogram', 'iriPriorita', 'iriOpatreni', 'iriPodopatreni', 'iriGrantoveSchema', 'iriProgramPodpora', 'iriTypCinnosti', 'iriProgram', 'dPlatnost', 'dtAktualizace'],
        'Rozhodnuti': ['idRozhodnuti', 'idDotace', 'castkaPozadovana', 'castkaRozhodnuta', 'iriPoskytovatelDotace', 'iriCleneniFinancnichProstredku', 'iriFinancniZdroj', 'rokRozhodnuti', 'investiceIndikator', 'navratnostIndikator', 'refundaceIndikator', 'dPlatnost', 'dtAktualizace'],
        'RozpoctoveObdobi': ['idObdobi', 'idRozhodnuti', 'castkaCerpana', 'castkaUvolnena', 'castkaVracena', 'castkaSpotrebovana', 'rozpoctoveObdobi', 'vyporadaniKod', 'iriDotacniTitul', 'iriUcelovyZnak', 'dPlatnost', 'dtAktualizace'],
    }

    for ds, exphd in headers.items():
        with open('data/{}.csv'.format(ds), 'w') as fw:
            cw = csv.writer(fw)
            cw.writerow(exphd)
            for fn in unpack(os.path.join(rdir, '{}.csv.7z'.format(ds))):
                with open(fn) as f:
                    cr = csv.reader(f)
                    hd = next(cr)
                    assert hd == exphd

                    for ln in cr:
                        # vypln info z ciselniku
                        for j, el in enumerate(ln):
                            if el.startswith('http://'):
                                ln[j] = csl[el] # tohle proste spadne, kdyz bude chybet klasifikator
                                
                        if ds == 'Dotace':
                            ln[1] = mapping[ln[1]] # idPrijemce -> ico
                        # assert ln[3].endswith('T00:00:00.000Z') # v krajnich pripadech tam je cas, ale v jednom z milionu
                        #ln[3] = ln[3][:10] # z podpisDatum nas zajima datum, ne cas

                        cw.writerow(ln)

