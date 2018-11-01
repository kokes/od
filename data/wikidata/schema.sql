CREATE SCHEMA IF NOT EXISTS wikidata;
DROP TABLE IF EXISTS wikidata.politici;
CREATE TABLE IF NOT EXISTS wikidata.politici (
	wikidata_id varchar,
	jmeno_prijmeni varchar,
	datum_narozeni date
);
