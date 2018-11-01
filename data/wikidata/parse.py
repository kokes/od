import csv
import json
import re
from urllib.request import urlopen
from urllib.parse import quote

if __name__ == '__main__':
  url = 'https://query.wikidata.org/sparql?query={}&format=json'
  query = '''SELECT ?person ?personLabel ?date_of_birth WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "cs". }
    VALUES ?politician {wd:Q18941264 wd:Q19803234}
    ?person wdt:P39 ?politician.

    ?person wdt:P569 ?date_of_birth.
  }

  LIMIT 10000'''

  r = urlopen(url.format(quote(query)))
  dt = json.load(r)
  rr = re.compile(r'\s+\(.+\)')

  with open('politici.csv', 'w', encoding='utf8') as fw:
      cw = csv.writer(fw)
      cw.writerow(['wikidata', 'jmeno_prijmeni', 'datum_narozeni'])
      for el in dt['results']['bindings']:
          cw.writerow([
              el['person']['value'].rpartition('/')[-1],
              rr.sub('', el['personLabel']['value']),
              el['date_of_birth']['value'][:10],
          ])
