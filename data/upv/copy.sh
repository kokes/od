cat data/inserts.csv | psql -c 'copy upv.inserts from stdin csv header'
cat data/deletes.csv | psql -c 'copy upv.deletes from stdin csv header'
