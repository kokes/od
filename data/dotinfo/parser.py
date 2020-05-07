import csv
import codecs
import os
import ssl
import zipfile
from datetime import datetime
from urllib.request import urlretrieve


header = {
    'Evidenční číslo dotace': 'evidencni_cislo_dotace',
    'Identifikator dotace': 'identifikator_dotace',
    'Název dotace': 'nazev_dotace',
    'Účastník': 'ucastnik',
    'IČ účastníka': 'ic_ucastnika',
    ' Účel dotace ': 'ucel_dotace',
    'Poskytovatel dotace': 'poskytovatel_dotace',
    'IČ poskytovatele': 'ic_poskytovatele',
    'Částka požadovaná': 'castka_pozadovana',
    'Částka schválená': 'castka_schvalne',
    'Datum poskytnutí dotace': 'datum_poskytnuti',
}


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    ssl._create_default_https_context = ssl._create_unverified_context
    if not os.path.isfile('data/raw.zip'):
        urlretrieve('https://data.mfcr.cz/sites/default/files/DotInfo_report_29_01_2020.zip', 'data/raw.zip')

    with zipfile.ZipFile('data/raw.zip') as zf, zf.open('DotInfo_report_29_01_2020.csv') as f, open('data/dotace.csv', 'w', encoding='utf8') as fw:
        ut = codecs.iterdecode(f, encoding='cp1250')
        cr = csv.DictReader(ut, delimiter=';')
        cw = csv.DictWriter(fw, fieldnames=header.values())
        cw.writeheader()
        exphd = set(header.keys())
        for j, row in enumerate(cr):
            if j == 0:
                rem = set(row.keys()) - exphd
                if rem:
                    print('vynechavame sloupce: ', rem)

            row = {k: None if v == 'NULL' else v for k, v in row.items()}
            remapped = {header[k]: v for k, v in row.items() if k in header}
            
            if remapped['datum_poskytnuti']:
                try:
                    datetime.fromisoformat(remapped['datum_poskytnuti'])
                except ValueError:
                    print('nevalidni datum', remapped['datum_poskytnuti'])
                    remapped['datum_poskytnuti'] = None
            
            if remapped['ic_ucastnika'] and not remapped['ic_ucastnika'].isdigit():
                print('nevalidni ICO', remapped['ic_ucastnika'])
                remapped['ic_ucastnika'] = None

            if remapped['ic_poskytovatele'] and not remapped['ic_poskytovatele'].isdigit():
                print('nevalidni ICO', remapped['ic_poskytovatele'])
                remapped['ic_poskytovatele'] = None

            cw.writerow(remapped)
