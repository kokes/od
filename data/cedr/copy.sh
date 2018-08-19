cat data/Dotace.csv | psql -c 'copy od.cedr_dotace from stdin csv header'
cat data/Rozhodnuti.csv | psql -c 'copy od.cedr_rozhodnuti from stdin csv header'
cat data/RozpoctoveObdobi.csv | psql -c 'copy od.cedr_rozpoctoveobdobi from stdin csv header'