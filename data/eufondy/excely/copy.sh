cat data/operace_2007_2013.csv | psql -c 'copy eufondy.dotace_0713 from stdin csv header'
cat data/operace_2014_2020.csv | psql -c 'copy eufondy.dotace_1420 from stdin csv header'
