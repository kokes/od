CREATE SCHEMA IF NOT EXISTS justice;

DROP TABLE IF EXISTS justice.subjekty;
CREATE TABLE justice.subjekty (
	"ico" bigint not null unique primary key,
	"nazev" text not null,
	"datum_zapis" date not null,
	"datum_vymaz" date
);

DROP TABLE IF EXISTS justice."spisova_znacka";
CREATE TABLE justice."spisova_znacka"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"znacka" text,
	"soud_kod" text,
	"soud_nazev" text,
	"oddil" text,
	"vlozka" text
);
DROP TABLE IF EXISTS justice."nazev";
CREATE TABLE justice."nazev"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"udaj_typ" text,
	"nazev" text
);
DROP TABLE IF EXISTS justice."pravni_forma";
CREATE TABLE justice."pravni_forma"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"nazev" text,
	"zkratka" text
);
DROP TABLE IF EXISTS justice."predmet_podnikani";
CREATE TABLE justice."predmet_podnikani"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"kategorie" text,
	"text" text
);
DROP TABLE IF EXISTS justice."pocet_clenu";
CREATE TABLE justice."pocet_clenu"(
	"ico" text,
	"udaj_typ" text,
	"datum_zapis" date,
	"text" text,
	"datum_vymaz" date);
DROP TABLE IF EXISTS justice."zpusob_jednani";
CREATE TABLE justice."zpusob_jednani"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."ostatni_skutecnosti";
CREATE TABLE justice."ostatni_skutecnosti"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."zpusob_rizeni";
CREATE TABLE justice."zpusob_rizeni"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."akcie";
CREATE TABLE justice."akcie"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"podoba" text,
	"udaj_typ" text,
	"pocet" text,
	"hodnota_typ" text,
	"hodnota" decimal(12,2),
	"text" text
);
DROP TABLE IF EXISTS justice."vklady";
CREATE TABLE justice."vklady"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"typ" text,
	"vklad_typ" text,
	"vklad_hodnota" text, -- obcas tam je pitomost
	"text" text
);
DROP TABLE IF EXISTS justice."pravni_duvod_vymazu";
CREATE TABLE justice."pravni_duvod_vymazu"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."spolecny_text";
CREATE TABLE justice."spolecny_text"(
	"ico" text,
	"udaj_typ" text,
	"datum_zapis" date,
	"text" text,
	"datum_vymaz" date);
DROP TABLE IF EXISTS justice."exekuce";
CREATE TABLE justice."exekuce"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."pravni_forma_text";
CREATE TABLE justice."pravni_forma_text"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."nejvyssi_organ";
CREATE TABLE justice."nejvyssi_organ"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."vznik";
CREATE TABLE justice."vznik"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"datum_vznik" date);
DROP TABLE IF EXISTS justice."majetek";
CREATE TABLE justice."majetek"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."spolecnik_zastavni_pravo";
CREATE TABLE justice."spolecnik_zastavni_pravo"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"datum_vznik_prava" text, -- obcas tam je pitomost
	"text" text
);
DROP TABLE IF EXISTS justice."text_spravni_rada";
CREATE TABLE justice."text_spravni_rada"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."spolecnik_podil";
CREATE TABLE justice."spolecnik_podil"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"vklad_typ" text,
	"vklad_hodnota" text, -- obcas tam je pitomost
	"souhrn_typ" text,
	"souhrn_hodnota" text, -- obcas tam je pitomost
	"splaceni_typ" text,
	"splaceni_hodnota" text, -- obcas tam je pitomost
	"druh_podilu" text,
	"kmenovy_list" text
);
DROP TABLE IF EXISTS justice."sidlo";
CREATE TABLE justice."sidlo"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"udaj_typ" text,
	"stat" text,
	"adresa" text,
	"obec" text,
	"cast_obce" text,
	"ulice" text,
	"cislo_po" text,
	"cislo_or" text,
	"cislo_text" text,
	"psc" text,
	"okres" text
);
DROP TABLE IF EXISTS justice."konkurs_prohlaseni";
CREATE TABLE justice."konkurs_prohlaseni"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"datum_rozhodnuti" date,
	"spisova_znacka" text,
	"datum_vyveseni" date,
	"text" text
);
DROP TABLE IF EXISTS justice."konkurs_zruseni";
CREATE TABLE justice."konkurs_zruseni"(
	"ico" text,
	"hlavicka" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"text" text
);
DROP TABLE IF EXISTS justice."insolvencni_zapis";
CREATE TABLE justice."insolvencni_zapis"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"id" text,
	"aktivni" text,
	"key" text,
	"nazev" text,
	"ciselnik" text,
	"externi_kod" text,
	"text" text
);
DROP TABLE IF EXISTS justice."vyrovnani";
CREATE TABLE justice."vyrovnani"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"udaj_typ" text,
	"text" text
);
DROP TABLE IF EXISTS justice."angazovane_osoby";
CREATE TABLE justice."angazovane_osoby"(
	"ico" text,
	"datum_zapis" date,
	"datum_vymaz" date,
	"udaj_typ" text,
	"funkce" text,
	"funkce_od" date,
	"clenstvi_od" date,
	"clenstvi_do" date,
	"funkce_do" date,
	"jmeno" text,
	"prijmeni" text,
	"datum_narozeni" date,
	"nazev" text,
	"reg_Cislo" text,
	"titul_pred" text,
	"titul_za" text,
	"ico_angos" text,
	"euid" text,
	"adresa_stat" text,
	"adresa_obec" text,
	"adresa_cast_obce" text,
	"adresa_ulice" text,
	"adresa_cislo_po" text,
	"adresa_psc" text,
	"adresa_okres" text,
	"adresa_cislo_or" text,
	"adresa_adresa_text" text,
	"adresa_cislo_ev" text,
	"adresa_doplnujici_text" text,
	"adresa_cislo_text" text,
	"bydliste_stat" text,
	"bydliste_ulice" text,
	"bydliste_obec" text,
	"bydliste_psc" text,
	"bydliste_cast_obce" text,
	"bydliste_cislo_po" text,
	"bydliste_cislo_or" text,
	"bydliste_okres" text,
	"bydliste_cislo_ev" text,
	"bydliste_cislo_text" text,
	"bydliste_doplnujici_text" text
);