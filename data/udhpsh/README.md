# ÚDHPSH - Úřad pro dohled nad hospodařením politických stran a politických hnutí

zatim stahujem jen výroční zprávy a zprávy o financování volebních kampaní
https://www.udhpsh.cz/vyrocni-financni-zpravy-stran-a-hnuti

data jsou za 2017 a 2018, je to zatim vepsany do kodu, casem to mozna extrahujem do configu

nahravam to do postgresy dost drevackym zpusobem

```
psql < init.sql

cat data/penizefo.csv | psql -c 'COPY udhpsh.penize_fo FROM STDIN CSV HEADER'
cat data/penizepo.csv | psql -c 'COPY udhpsh.penize_po FROM STDIN CSV HEADER'
```