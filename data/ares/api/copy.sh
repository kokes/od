cat data/csv/res.csv | psql -c 'copy od.ares_res from stdin csv header'

cat data/csv/udaje.csv | psql -c 'copy od.ares_or_udaje from stdin csv header'
cat data/csv/nazvy.csv | psql -c 'copy od.ares_or_nazvy from stdin csv header'
cat data/csv/pravni_formy.csv | psql -c 'copy od.ares_or_pravni_formy from stdin csv header'
cat data/csv/sidla.csv | psql -c 'copy od.ares_or_sidla from stdin csv header'
cat data/csv/angos_fo.csv | psql -c 'copy od.ares_or_angos_fo from stdin csv header'
cat data/csv/angos_po.csv | psql -c 'copy od.ares_or_angos_po from stdin csv header'
