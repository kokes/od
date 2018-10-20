cat data/csv/res.csv | psql -c 'copy ares.res from stdin csv header'
cat data/csv/res_nace.csv | psql -c 'copy ares.res_nace from stdin csv header'

cat data/csv/udaje.csv | psql -c 'copy ares.or_udaje from stdin csv header'
cat data/csv/nazvy.csv | psql -c 'copy ares.or_nazvy from stdin csv header'
cat data/csv/pravni_formy.csv | psql -c 'copy ares.or_pravni_formy from stdin csv header'
cat data/csv/sidla.csv | psql -c 'copy ares.or_sidla from stdin csv header'
cat data/csv/angos_fo.csv | psql -c 'copy ares.or_angos_fo from stdin csv header'
cat data/csv/angos_po.csv | psql -c 'copy ares.or_angos_po from stdin csv header'
