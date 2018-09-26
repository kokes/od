BEGIN;
DROP TABLE IF EXISTS psp_typ_organu CASCADE;
CREATE TABLE psp_typ_organu (
	"id_typ_org" int unique not null,
	"typ_id_typ_org" int, -- REFERENCES psp_typ_organu(id_typ_org)
	"nazev_typ_org_cz" varchar,
	"nazev_typ_org_en" varchar,
	"typ_org_obecny" int, -- REFERENCES psp_typ_organu(id_typ_org)
	"priorita" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_typ_funkce CASCADE;
CREATE TABLE psp_typ_funkce (
	"id_typ_funkce" int unique not null,
	"id_typ_org" int, -- REFERENCES psp_typ_organu(id_typ_org)
	"typ_funkce_cz" varchar,
	"typ_funkce_en" varchar,
	"priorita" int,
	"typ_funkce_obecny" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_organy CASCADE;
CREATE TABLE psp_organy (
	"id_organ" int unique not null,
	"organ_id_organ" int,
	"id_typ_organu" int, -- REFERENCES psp_typ_organu(id_typ_org)
	"zkratka" varchar,
	"nazev_organu_cz" varchar,
	"nazev_organu_en" varchar,
	"od_organ" date,
	"do_organ" date,
	"priorita" int,
	"cl_organ_base" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_funkce CASCADE;
CREATE TABLE psp_funkce (
	"id_funkce" int unique not null,
	"id_organ" int, -- REFERENCES psp_organy(id_organ)
	"id_typ_funkce" int, -- REFERENCES psp_typ_funkce(id_typ_funkce)
	"nazev_funkce_cz" varchar,
	"priorita" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_osoby CASCADE;
CREATE TABLE psp_osoby (
	"id_osoba" int unique not null,
	"pred" varchar,
	"prijmeni" varchar,
	"jmeno" varchar,
	"za" varchar,
	"narozeni" date,
	"pohlavi" varchar,
	"zmena" date,
	"umrti" date,
	"x" varchar
);

DROP TABLE IF EXISTS psp_zarazeni CASCADE;
CREATE TABLE psp_zarazeni (
	"id_osoba" int, -- REFERENCES psp_osoby(id_osoba)
	"id_of" int, -- dve ruzne reference podle hodnoty `cl_funkce`
	"cl_funkce" int,
	"od_o" varchar, -- TODO: jsou tam i hodiny, je to takovy pseudoformat
	"do_o" varchar, -- TODO: jsou tam i hodiny, je to takovy pseudoformat
	"od_f" date,
	"do_f" date,
	"x" varchar
);

DROP TABLE IF EXISTS psp_poslanec CASCADE;
CREATE TABLE psp_poslanec (
	"id_poslanec" int unique not null,
	"id_osoba" int, -- REFERENCES psp_osoby(id_osoba)
	"id_kraj" int, -- REFERENCES psp_organy(id_organ)
	"id_kandidatka" int, -- REFERENCES psp_organy(id_organ)
	"id_obdobi" int, -- REFERENCES psp_organy(id_organ)
	"web" varchar,
	"ulice" varchar,
	"obec" varchar,
	"psc" varchar,
	"email" varchar,
	"telefon" varchar,
	"fax" varchar,
	"psp_telefon" varchar,
	"facebook" varchar,
	"foto" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_pkgps CASCADE;
CREATE TABLE psp_pkgps (
	"id_poslanec" int, -- REFERENCES psp_poslanec(id_poslanec)
	"adresa" varchar,
	"sirka" numeric(9, 2),
	"delka" numeric(9, 2),
	"x" varchar
);
COMMIT;
