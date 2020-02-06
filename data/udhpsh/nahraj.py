import os
import json
import csv
from urllib.request import urlopen

indices = {
    '2017': 'https://zpravy.udhpsh.cz/export/vfz2017-index.json',
    '2018': 'https://zpravy.udhpsh.cz/zpravy/vfz2018.json'
}

mappings = {
    'penizefo': {
        'date': 'datum',
        'money': 'castka',
        'lastName': 'prijmeni',
        'firstName': 'jmeno',
        'titleBefore': 'titul_pred',
        'titleAfter': 'titul_za',
        'birthDate': 'datum_narozeni',
        'addrCity': 'adresa_mesto',
    },
    'penizepo': {
        'date': 'datum',
        'money': 'castka',
        'companyId': 'ico_darce',
        'company': 'spolecnost',
        'addrStreet': 'adresa_ulice',
        'addrCity': 'adresa_mesto',
        'addrZip': 'adresa_psc',
    }
}

if __name__ == '__main__':
    cdir = os.path.dirname(os.path.abspath(__file__))
    tdir = os.path.join(cdir, 'data')
    os.makedirs(tdir, exist_ok=True)

    for dataset, mapping in mappings.items():
        print(f'Nahravam dataset: {dataset}')
        with open(os.path.join(tdir, dataset + '.csv'), 'w', encoding='utf8') as fw:
            columns = ['rok', 'ico_prijemce'] + list(mapping.values())
            cw = csv.DictWriter(fw, fieldnames=columns)
            cw.writeheader()
            for year, index in indices.items():
                print(f'zpracovavam rok: {year}')
                r = urlopen(index)
                dt = json.load(r)

                for party in dt['parties']:
                    relfiles = [j['url'] for j in party['files']
                                if j['subject'] == dataset and j['format'] == 'json']
                    for relfile in relfiles:
                        for item in json.load(urlopen(relfile)):
                            row = {mapping[k]: v for k, v in item.items()}
                            cw.writerow({
                                **row,
                                'rok': year,
                                'ico_prijemce': party['ic']
                            })
