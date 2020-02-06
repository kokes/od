CREATE SCHEMA IF NOT EXISTS udhpsh;

drop table if exists udhpsh.penize_fo; -- TODO
CREATE TABLE udhpsh.penize_fo (
	rok smallint not null,
	ico_prijemce bigint not null,
	datum date,
	castka numeric,
	prijmeni text not null,
	jmeno text not null,
	titul_pred text,
	titul_za text,
	datum_narozeni date not null,
	adresa_mesto text
);

drop table if exists udhpsh.penize_po; -- TODO
CREATE TABLE udhpsh.penize_po (
	rok smallint not null,
	ico_prijemce bigint not null,
	datum date,
	castka numeric not null,
	ico_darce bigint not null,
	spolecnost text not null,
	adresa_ulice text,
	adresa_mesto text,
	adresa_psc bigint
);
