CREATE SCHEMA IF NOT EXISTS udhpsh;

CREATE TABLE udhpsh.penize_fo (
	rok smallint not null,
	ico_prijemce bigint not null,
	nazev_prijemce text not null,
	datum date,
	castka numeric,
	prijmeni text not null,
	jmeno text not null,
	titul_pred text,
	titul_za text,
	datum_narozeni date not null,
	adresa_mesto text
);

CREATE TABLE udhpsh.penize_po (
	rok smallint not null,
	ico_prijemce bigint not null,
	nazev_prijemce text not null,
	datum date,
	castka numeric not null,
	ico_darce bigint not null,
	spolecnost text not null,
	adresa_ulice text,
	adresa_mesto text,
	adresa_psc bigint
);
