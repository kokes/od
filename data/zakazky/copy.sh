psql < init.sql
cat data/processed/etrziste/casti_vz.csv | psql -c 'copy zakazky.etrziste_casti_vz from stdin csv header;'
cat data/processed/etrziste/polozky_vz.csv | psql -c 'copy zakazky.etrziste_polozky_vz from stdin csv header;'
cat data/processed/etrziste/kriteria_vz.csv | psql -c 'copy zakazky.etrziste_kriteria_vz from stdin csv header;'
cat data/processed/etrziste/dodavatele.csv | psql -c 'copy zakazky.etrziste_dodavatele from stdin csv header;'
cat data/processed/etrziste/vz.csv | psql -c 'copy zakazky.etrziste_vz from stdin csv header;'
cat data/processed/vvz/casti_vz.csv | psql -c 'copy zakazky.vvz_casti_vz from stdin csv header;'
cat data/processed/vvz/vz.csv | psql -c 'copy zakazky.vvz_vz from stdin csv header;'
cat data/processed/zzvz/zadani_vz.csv | psql -c 'copy zakazky.zzvz_zadani_vz from stdin csv header;'
cat data/processed/zzvz/casti_vz.csv | psql -c 'copy zakazky.zzvz_casti_vz from stdin csv header;'
cat data/processed/zzvz/dodavatele.csv | psql -c 'copy zakazky.zzvz_dodavatele from stdin csv header;'
cat data/processed/zzvz/vz.csv | psql -c 'copy zakazky.zzvz_vz from stdin csv header;'
cat data/processed/zzvz/kriteria_vz.csv | psql -c 'copy zakazky.zzvz_kriteria_vz from stdin csv header;'
psql < postcopy.sql
