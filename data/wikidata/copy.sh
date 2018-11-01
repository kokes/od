psql < schema.sql
cat politici.csv | psql -c 'copy wikidata.politici from stdin csv header'
