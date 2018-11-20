# http://dotaceeu.cz/cs/Evropske-fondy-v-CR/Programove-obdobi-2007-2013/Cerpani-v-obdobi-2007-2013
# http://dotaceeu.cz/Dotace/media/SF/Informace%20o%20%c4%8derp%c3%a1n%c3%ad/Seznamy%20p%c5%99%c3%adjemc%c5%af%20(List%20of%20Beneficiaries)/2016/Seznam-prijemcu-05_2017.xlsx

# TODO: osetrit tady cesko-polsko veci
# TODO: přehled projektů pro 2007-2013? je tam víc info

import csv
import re

from openpyxl import load_workbook

wb = load_workbook('data/2007-2013/Seznam-prijemcu-05_2017.xlsx', read_only=True)
sh = wb.active

# TODO: nechcem strptime?
def predatuj(s):
    if s is None:
        return None
    
    d, m, y = map(int, s.split('.'))
    return f'{y}-{m:02d}-{d:02d}'

cws = re.compile('\s+')


with open('data/operace_2007_2013.csv', 'w', encoding='utf8') as fw:
    cw = csv.writer(fw)
    hd = ['prijemce', 'ico', 'projekt', 'operacni_program', 'fond_eu', 'datum_alokace', 'castka_alokovana', 'datum_platby', 'castka_proplacena', 'stav']
    cw.writerow(hd)
    for j, row in enumerate(sh.rows):
        dt = [j.value for j in row]
        assert len(dt) == 10
        if j == 0:
            assert dt[0] == 'LIST OF BENEFICIARIES \nSEZNAM PŘÍJEMCŮ PODPORY Z FONDŮ EU'
        elif j == 6:
            assert dt == [' Název příjemce', 'IČ', 'Název projektu', 'Operační \nprogram', 'Fond\nEU', 'Částka hrazená z fondů EU ', None, None, None, None]
        elif j == 7:
            assert dt == [None, None, None, None, None, 'Datum alokace', 'Alokovaná částka', 'Datum průběžné platby', 'Celková částka proplacená od začátku projektu', 'Stav']
        elif all([j is None for j in dt]):
            continue # predposledni radka
        elif dt[0] == 'Sestava vytvořena IS MSC2007':
            break # koncime
        
        if j < 8: continue
            
        dt = [cws.sub(' ', j.strip()) if isinstance(j, str) else j for j in dt] # cistime bile znaky
        
        # ICO
        if dt[1] is None:
            pass
        # OP ČR-Polsko má polský IČ, který potřebujem vyfiltrovat
        # bohužel nejsou nějak jednoznačně určené
        elif dt[3] == 'OP PS ČR-Polsko' and not dt[1].isdigit():
            dt[1] = None
        else:
            dt[1] = int(dt[1])
        
        dt[5] = predatuj(dt[5]) # datum alokace
        dt[7] = predatuj(dt[7]) # prubezna platba
        
        cw.writerow(dt)
