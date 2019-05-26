for fn in data/csv/*; do
	cat $fn | psql -c 'copy datovky from stdin csv header'
done
