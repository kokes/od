psql < init.sql

cat data/penizefo.csv | psql -c 'COPY udhpsh.penize_fo FROM STDIN CSV HEADER'
cat data/penizepo.csv | psql -c 'COPY udhpsh.penize_po FROM STDIN CSV HEADER'
