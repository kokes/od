cat data/pobidky.csv | psql -c 'truncate czechinvest.pobidky; copy czechinvest.pobidky from stdin csv header'
