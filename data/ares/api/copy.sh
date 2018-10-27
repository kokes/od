cat data/csv/res.csv | psql -c 'delete from ares.res; copy ares.res from stdin csv header'
cat data/csv/res_nace.csv | psql -c 'delete from ares.res_nace; copy ares.res_nace from stdin csv header'

psql -c 'alter table ares.or_angos_fo drop column if exists jmeno_prijmeni' # lower(jmeno || prijmeni) kvuli indexu
cat data/csv/udaje.csv | psql -c 'delete from ares.or_udaje; copy ares.or_udaje from stdin csv header'
cat data/csv/nazvy.csv | psql -c 'delete from ares.or_nazvy; copy ares.or_nazvy from stdin csv header'
cat data/csv/pravni_formy.csv | psql -c 'delete from ares.or_pravni_formy; copy ares.or_pravni_formy from stdin csv header'
cat data/csv/sidla.csv | psql -c 'delete from ares.or_sidla; copy ares.or_sidla from stdin csv header'
cat data/csv/angos_fo.csv | psql -c 'delete from ares.or_angos_fo; copy ares.or_angos_fo from stdin csv header'
cat data/csv/angos_po.csv | psql -c 'delete from ares.or_angos_po; copy ares.or_angos_po from stdin csv header'
