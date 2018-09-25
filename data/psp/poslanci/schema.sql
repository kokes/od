DROP TABLE IF EXISTS psp_typ_organu;
CREATE TABLE psp_typ_organu (
	"id_typ_org" int,
	"typ_id_typ_org" int,
	"nazev_typ_org_cz" varchar,
	"nazev_typ_org_en" varchar,
	"typ_org_obecny" int,
	"priorita" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_typ_funkce;
CREATE TABLE psp_typ_funkce (
	"id_typ_funkce" int,
	"id_typ_org" int,
	"typ_funkce_cz" varchar,
	"typ_funkce_en" varchar,
	"priorita" int,
	"typ_funkce_obecny" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_funkce;
CREATE TABLE psp_funkce (
	"id_funkce" int,
	"id_organ" int,
	"id_typ_funkce" int,
	"nazev_funkce_cz" varchar,
	"priorita" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_organy;
CREATE TABLE psp_organy (
	"id_organ" int,
	"organ_id_organ" int,
	"id_typ_organu" int,
	"zkratka" varchar,
	"nazev_organu_cz" varchar,
	"nazev_organu_en" varchar,
	"od_organ" date,
	"do_organ" date,
	"priorita" int,
	"cl_organ_base" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp_osoby;
CREATE TABLE psp_osoby (
	"id_osoba" int,
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

DROP TABLE IF EXISTS psp_zarazeni;
CREATE TABLE psp_zarazeni (
	"id_osoba" int,
	"id_of" int,
	"cl_funkce" int,
	"od_o" varchar, -- TODO: jsou tam i hodiny, je to takovy pseudoformat
	"do_o" varchar, -- TODO: jsou tam i hodiny, je to takovy pseudoformat
	"od_f" date,
	"do_f" date,
	"x" varchar
);

DROP TABLE IF EXISTS psp_poslanec;
CREATE TABLE psp_poslanec (
	"id_poslanec" int,
	"id_osoba" int,
	"id_kraj" int,
	"id_kandidatka" int,
	"id_obdobi" int,
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

DROP TABLE IF EXISTS psp_pkgps;
CREATE TABLE psp_pkgps (
	"id_poslanec" int,
	"adresa" varchar,
	"sirka" varchar,
	"delka" varchar,
	"x" varchar
);
