BEGIN;
CREATE SCHEMA IF NOT EXISTS psp;
DROP TABLE IF EXISTS psp.poslanci_typ_organu CASCADE;
CREATE TABLE psp.poslanci_typ_organu (
	"id_typ_org" int unique not null,
	"typ_id_typ_org" int, -- REFERENCES psp.poslanci_typ_organu(id_typ_org)
	"nazev_typ_org_cz" varchar,
	"nazev_typ_org_en" varchar,
	"typ_org_obecny" int, -- REFERENCES psp.poslanci_typ_organu(id_typ_org)
	"priorita" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp.poslanci_typ_funkce CASCADE;
CREATE TABLE psp.poslanci_typ_funkce (
	"id_typ_funkce" int unique not null,
	"id_typ_org" int, -- REFERENCES psp.poslanci_typ_organu(id_typ_org)
	"typ_funkce_cz" varchar,
	"typ_funkce_en" varchar,
	"priorita" int,
	"typ_funkce_obecny" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp.poslanci_organy CASCADE;
CREATE TABLE psp.poslanci_organy (
	"id_organ" int unique not null,
	"organ_id_organ" int,
	"id_typ_organu" int, -- REFERENCES psp.poslanci_typ_organu(id_typ_org)
	"zkratka" varchar,
	"nazev_organu_cz" varchar,
	"nazev_organu_en" varchar,
	"od_organ" date,
	"do_organ" date,
	"priorita" int,
	"cl_organ_base" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp.poslanci_funkce CASCADE;
CREATE TABLE psp.poslanci_funkce (
	"id_funkce" int unique not null,
	"id_organ" int, -- REFERENCES psp.poslanci_organy(id_organ)
	"id_typ_funkce" int, -- REFERENCES psp.poslanci_typ_funkce(id_typ_funkce)
	"nazev_funkce_cz" varchar,
	"priorita" int,
	"x" varchar
);

DROP TABLE IF EXISTS psp.poslanci_osoby CASCADE;
CREATE TABLE psp.poslanci_osoby (
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

DROP TABLE IF EXISTS psp.poslanci_zarazeni CASCADE;
CREATE TABLE psp.poslanci_zarazeni (
	"id_osoba" int, -- REFERENCES psp.poslanci_osoby(id_osoba)
	"id_of" int, -- dve ruzne reference podle hodnoty `cl_funkce`
	"cl_funkce" int,
	"od_o" varchar, -- TODO: jsou tam i hodiny, je to takovy pseudoformat
	"do_o" varchar, -- TODO: jsou tam i hodiny, je to takovy pseudoformat
	"od_f" date,
	"do_f" date,
	"x" varchar
);

DROP TABLE IF EXISTS psp.poslanci_poslanec CASCADE;
CREATE TABLE psp.poslanci_poslanec (
	"id_poslanec" int unique not null,
	"id_osoba" int, -- REFERENCES psp.poslanci_osoby(id_osoba)
	"id_kraj" int, -- REFERENCES psp.poslanci_organy(id_organ)
	"id_kandidatka" int, -- REFERENCES psp.poslanci_organy(id_organ)
	"id_obdobi" int, -- REFERENCES psp.poslanci_organy(id_organ)
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

DROP TABLE IF EXISTS psp.poslanci_pkgps CASCADE;
CREATE TABLE psp.poslanci_pkgps (
	"id_poslanec" int, -- REFERENCES psp.poslanci_poslanec(id_poslanec)
	"adresa" varchar,
	"sirka" numeric(9, 2),
	"delka" numeric(9, 2),
	"x" varchar
);
COMMIT;

COMMENT ON COLUMN "psp"."poslanci_typ_organu"."id_typ_org" IS 'Identifikátor typu orgánu';
COMMENT ON COLUMN "psp"."poslanci_typ_organu"."typ_id_typ_org" IS 'Identifikátor nadřazeného typu orgánu (typ_organu:id_typ_org), pokud je null či nevyplněno, pak nemá nadřazený typ';
COMMENT ON COLUMN "psp"."poslanci_typ_organu"."nazev_typ_org_cz" IS 'Název typu orgánu v češtině';
COMMENT ON COLUMN "psp"."poslanci_typ_organu"."nazev_typ_org_en" IS 'Název typu orgánu v angličtině';
COMMENT ON COLUMN "psp"."poslanci_typ_organu"."typ_org_obecny" IS 'Obecný typ orgánu, pokud je vyplněný, odpovídá záznamu v typ_organu:id_typ_org. Pomocí tohoto sloupce lze najít např. všechny výbory v různých typech zastupitelských sborů.';
COMMENT ON COLUMN "psp"."poslanci_typ_organu"."priorita" IS 'Priorita při výpisu';
 
COMMENT ON COLUMN "psp"."poslanci_typ_funkce"."id_typ_funkce" IS 'Identifikátor typu funkce';
COMMENT ON COLUMN "psp"."poslanci_typ_funkce"."id_typ_org" IS 'Identifikátor typu orgánu, viz typ_organu:id_typ_org';
COMMENT ON COLUMN "psp"."poslanci_typ_funkce"."typ_funkce_cz" IS 'Název typu funkce v češtině';
COMMENT ON COLUMN "psp"."poslanci_typ_funkce"."typ_funkce_en" IS 'Název typu funkce v angličtině';
COMMENT ON COLUMN "psp"."poslanci_typ_funkce"."priorita" IS 'Priorita při výpisu';
COMMENT ON COLUMN "psp"."poslanci_typ_funkce"."typ_funkce_obecny" IS 'Obecný typ funkce, 1 - předseda, 2 - místopředseda, 3 - ověřovatel, jiné hodnoty se nepoužívají.';
 
COMMENT ON COLUMN "psp"."poslanci_funkce"."id_funkce" IS 'Identifikátor funkce, používá se v zarazeni:id_fo';
COMMENT ON COLUMN "psp"."poslanci_funkce"."id_organ" IS 'Identifikátor orgánu, viz organy:id_organ';
COMMENT ON COLUMN "psp"."poslanci_funkce"."id_typ_funkce" IS 'Typ funkce, viz typ_funkce:id_typ_funkce';
COMMENT ON COLUMN "psp"."poslanci_funkce"."nazev_funkce_cz" IS 'Název funkce, pouze pro interní použití';
COMMENT ON COLUMN "psp"."poslanci_funkce"."priorita" IS 'Priorita výpisu';
 
COMMENT ON COLUMN "psp"."poslanci_organy"."id_organ" IS 'Identifikátor orgánu';
COMMENT ON COLUMN "psp"."poslanci_organy"."organ_id_organ" IS 'Identifikátor nadřazeného orgánu, viz organy:id_organ';
COMMENT ON COLUMN "psp"."poslanci_organy"."id_typ_organu" IS 'Typ orgánu, viz typ_organu:id_typ_organu';
COMMENT ON COLUMN "psp"."poslanci_organy"."zkratka" IS 'Zkratka orgánu, bez diakritiky, v některých připadech se zkratka při zobrazení nahrazuje jiným názvem';
COMMENT ON COLUMN "psp"."poslanci_organy"."nazev_organu_cz" IS 'Název orgánu v češtině';
COMMENT ON COLUMN "psp"."poslanci_organy"."nazev_organu_en" IS 'Název orgánu v angličtině';
COMMENT ON COLUMN "psp"."poslanci_organy"."od_organ" IS 'Ustavení orgánu';
COMMENT ON COLUMN "psp"."poslanci_organy"."do_organ" IS 'Ukončení orgánu';
COMMENT ON COLUMN "psp"."poslanci_organy"."priorita" IS 'Priorita výpisu orgánů';
COMMENT ON COLUMN "psp"."poslanci_organy"."cl_organ_base" IS 'Pokud je nastaveno na 1, pak při výpisu členů se nezobrazují záznamy v tabulkce zarazeni kde cl_funkce == 0. Toto chování odpovídá tomu, že v některých orgánech nejsou členové a teprve z nich se volí funkcionáři, ale přímo se volí do určité funkce.';
 
COMMENT ON COLUMN "psp"."poslanci_osoby"."id_osoba" IS 'Identifikátor osoby';
COMMENT ON COLUMN "psp"."poslanci_osoby"."pred" IS 'Titul pred jmenem';
COMMENT ON COLUMN "psp"."poslanci_osoby"."jmeno" IS 'Jméno';
COMMENT ON COLUMN "psp"."poslanci_osoby"."prijmeni" IS 'Příjmení, v některých případech obsahuje i dodatek typu "st.", "ml."';
COMMENT ON COLUMN "psp"."poslanci_osoby"."za" IS 'Titul za jménem';
COMMENT ON COLUMN "psp"."poslanci_osoby"."narozeni" IS 'Datum narození, pokud neznámo, pak 1.1.1900.';
COMMENT ON COLUMN "psp"."poslanci_osoby"."pohlavi" IS 'Pohlaví, "M" jako muž, ostatní hodnoty žena';
COMMENT ON COLUMN "psp"."poslanci_osoby"."zmena" IS 'Datum posledni změny';
COMMENT ON COLUMN "psp"."poslanci_osoby"."umrti" IS 'Datum úmrtí';
 
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."id_osoba" IS 'Identifikátor osoby, viz osoba:id_osoba';
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."id_of" IS 'Identifikátor orgánu či funkce: pokud je zároveň nastaveno zarazeni:cl_funkce == 0, pak id_o odpovídá organy:id_organ, pokud cl_funkce == 1, pak odpovídá funkce:id_funkce.';
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."cl_funkce" IS 'Status členství nebo funce: pokud je rovno 0, pak jde o členství, pokud 1, pak jde o funkci.';
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."od_o" IS 'to hour)	Zařazení od';
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."do_o" IS 'to hour)	Zařazení do';
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."od_f" IS 'Mandát od. Nemusí být vyplněno a pokud je vyplněno, pak určuje datum vzniku mandátu a zarazeni:od_o obsahuje datum volby.';
COMMENT ON COLUMN "psp"."poslanci_zarazeni"."do_f" IS 'Mandát do. Nemusí být vyplněno a pokud je vyplněno, určuje datum konce mandátu a zarazeni:do_o obsahuje datum ukončení zařazení.';
 
COMMENT ON COLUMN "psp"."poslanci_poslanec"."id_poslanec" IS 'Identifikátor poslance';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."id_osoba" IS 'Identifikátor osoby, viz osoba:id_osoba';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."id_kraj" IS 'Volební kraj, viz organy:id_organu';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."id_kandidatka" IS 'Volební strana/hnutí, viz org:id_organu, pouze odkazuje na stranu/hnutí, za kterou byl zvolen a nemusí mít souvislost s členstvím v poslaneckém klubu.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."id_obdobi" IS 'Volební období, viz organy:id_organu';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."web" IS 'URL vlastních stránek poslance';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."ulice" IS 'Adresa regionální kanceláře, ulice.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."obec" IS 'Adresa regionální kanceláře, obec.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."psc" IS 'Adresa regionální kanceláře, PSČ.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."email" IS 'E-mailová adresa poslance, případně obecná posta@psp.cz.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."telefon" IS 'Adresa regionální kanceláře, telefon.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."fax" IS 'Adresa regionální kanceláře, fax.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."psp_telefon" IS 'Telefonní číslo do kanceláře v budovách PS.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."facebook" IS 'URL stránky služby Facebook.';
COMMENT ON COLUMN "psp"."poslanci_poslanec"."foto" IS 'Pokud je rovno 1, pak existuje fotografie poslance.';
 
COMMENT ON COLUMN "psp"."poslanci_pkgps"."id_poslanec" IS 'Identifikátor poslance, viz poslanec:id_poslanec';
COMMENT ON COLUMN "psp"."poslanci_pkgps"."adresa" IS 'Adresa kanceláře, jednotlivé položky jsou odděleny středníkem';
COMMENT ON COLUMN "psp"."poslanci_pkgps"."sirka" IS 'Severní šířka, WGS 84, formát GG.AABBCCC, GG = stupně, AA - minuty, BB - vteřiny, CCC - tisíciny vteřin';
COMMENT ON COLUMN "psp"."poslanci_pkgps"."delka" IS 'Východní délka, WGS 84, formát GG.AABBCCC, GG = stupně, AA - minuty, BB - vteřiny, CCC - tisíciny vteřin';
