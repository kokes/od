cat data/Dotace.csv | psql -c 'copy cedr.dotace from stdin csv header'
cat data/Rozhodnuti.csv | psql -c 'copy cedr.rozhodnuti from stdin csv header'
cat data/RozpoctoveObdobi.csv | psql -c 'copy cedr.rozpoctoveobdobi from stdin csv header'
