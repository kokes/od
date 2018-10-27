cat data/Dotace.csv | psql -c 'delete from cedr.dotace; copy cedr.dotace from stdin csv header'
cat data/Rozhodnuti.csv | psql -c 'delete from cedr.rozhodnuti; copy cedr.rozhodnuti from stdin csv header'
cat data/RozpoctoveObdobi.csv | psql -c 'delete from cedr.rozpoctoveobdobi; copy cedr.rozpoctoveobdobi from stdin csv header'
