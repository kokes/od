mkdir -p data/raw/

mkdir -p data/raw/zzvz
for rok in `seq 2016 2018`; do
	echo "zzvz: $rok"
	curl -s -k https://www.isvz.cz/ReportingSuite/Explorer/Download/Data/CSV/ZZVZ/$rok | gzip -c > data/raw/zzvz/$rok.csv.gz
done

mkdir -p data/raw/vvz
for rok in `seq 2006 2016`; do
	echo "vvz: $rok"
	curl -s -k https://www.isvz.cz/ReportingSuite/Explorer/Download/Data/CSV/VVZ/$rok | gzip -c > data/raw/vvz/$rok.csv.gz
done

mkdir -p data/raw/etrziste

for rok in `seq 2012 2017`; do
	echo "etrziste: $rok"
	curl -s -k https://www.isvz.cz/ReportingSuite/Explorer/Download/Data/CSV/etrziste/$rok | gzip -c > data/raw/etrziste/$rok.csv.gz
done

