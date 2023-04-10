import csv
import os
from urllib.request import urlopen
from urllib.request import urlretrieve
import os
import zipfile
from io import TextIOWrapper
from tempfile import TemporaryDirectory
from tqdm import tqdm

import pyproj

from shapely.geometry import Point
from shapely.ops import transform

# RSS feed for data
URL = "https://services.cuzk.cz/atom-index/RUIAN-CSV-ADR-ST/5514"

# https://www.cuzk.cz/Uvod/Produkty-a-sluzby/RUIAN/2-Poskytovani-udaju-RUIAN-ISUI-VDP/Dopady-zmeny-zakona-c-51-2020-Sb/Adresni-mista-CSV_atributy.aspx
COLS = {
    'Kód ADM': 'kod_adm',
    'Kód obce': 'kod_obce',
    'Název obce': 'nazev_obce',
    'Kód MOMC': 'kod_momc',
    'Název MOMC':'nazev_momc',
    'Kód obvodu Prahy':'kod_obvodu_prahy',
    'Název obvodu Prahy':'nazev_obvodu_prahy',
    'Kód části obce':'kod_casti_obce',
    'Název části obce':'nazev_casti_obce',
    'Kód ulice':'kod_ulice', 
    'Název ulice':'nazev_ulice', 
    'Typ SO':'typ_so', 
    'Číslo domovní':'cislo_domovni', 
    'Číslo orientační':'cislo_orientacni', 
    'Znak čísla orientačního':'znak_cisla_orientacniho', 
    'PSČ':'psc', 
    'Souřadnice Y':'souradnice_y', 
    'Souřadnice X':'souradnice_x', 
    'Platí Od':'plati_od',
    'GPS souřadnice':'gps_souradnice',
}



def read_compressed():
    response = urlopen(URL)
    burl=response.read().decode("utf8").split('<a href="')[-1].split('">')[0] #link to file from RSS feed
    print('Stahuji soubor ',burl)
    
    with TemporaryDirectory() as tdir:
        tfn = os.path.join(tdir, "tmp.zip")
        urlretrieve(burl, tfn)
        with zipfile.ZipFile(tfn) as zf:
            for f in tqdm(zf.namelist()):
                with zf.open(f, 'r') as infile:
                    yield TextIOWrapper(infile, "cp1250", errors="ignore")

# @contextmanager
def read_compressed_local():
    tfn = 'E://GitHub/ruian/data/RUIAN-CSV-ADR-ST.zip'
    with zipfile.ZipFile(tfn) as zf:
        for f in tqdm(zf.namelist()):
            with zf.open(f, 'r') as infile:
                yield TextIOWrapper(infile, "cp1250", errors="ignore")

    

def main(outdir: str, partial: bool = False):
    
    wgs84 = pyproj.CRS('EPSG:4326')
    jtsk = pyproj.CRS('EPSG:5514')

    project = pyproj.Transformer.from_crs( jtsk,wgs84, always_xy=True).transform

    
    ofn = os.path.join(outdir, "ruian.csv")

    with open(ofn, 'w', newline='', encoding='utf-8') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(list(COLS.values()))
        i=0
        for f in read_compressed():
            i+=1
            if partial and i > 10:
                    break 
            cr = csv.DictReader(f,delimiter=';')
            for row in cr:
                
                if (row['Souřadnice Y']!=''):
                        # coordinates in RUIAN and S-JTSK system have negative values
                        ruain_pt = Point(float(row['Souřadnice Y'])*-1, float(row['Souřadnice X'])*-1)
                        utm_point = transform(project, ruain_pt)
                        row['GPS souřadnice']=utm_point
                else:
                    row['GPS souřadnice']=''
                
                writer.writerow(list(row.values()))

if __name__ == "__main__":
    main(".")           
