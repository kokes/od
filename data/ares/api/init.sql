drop table if exists ares.res;
create table if not exists ares.res (
	ico int not null primary key,
	aktualizace_db date not null,
	datum_vypisu date not null,
	nazev varchar,
	pravni_forma_id int,
	pravni_forma_nazev varchar,
	datum_vzniku date not null,
	datum_zaniku date,
	sidlo_nazev_obce varchar,
	sidlo_nazev_casti_obce varchar,
	sidlo_ulice varchar,
	sidlo_cislo_domovni int,
	sidlo_typ_cislo_domovni int,
	sidlo_cislo_orientacni varchar,
	sidlo_psc int,
	zuj_nzuj varchar,
	zuj_nuts4 varchar,
	zuj_nazev_nuts4 varchar,
	esa2010 int,
	esa2010t varchar,
	kpp varchar,
	nace varchar[] -- nemuze byt int, je tam G apod.
);
create extension pg_trgm;
create index res_nazev_trgm ON ares.res using gist (nazev gist_trgm_ops);

drop table if exists ares.or_udaje cascade;
create table ares.or_udaje (
	ico int not null primary key,
	aktualizace_db date,
	datum_vypisu date,
	platnost_od date,
	datum_zapisu date,
	stav_subjektu varchar
);

drop table if exists ares.or_nazvy;
create table ares.or_nazvy (
	ico int not null references ares.or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	nazev varchar
);
create index ares_or_nazvy_ico_idx on ares.or_nazvy(ico);

drop table if exists ares.or_pravni_formy;
create table ares.or_pravni_formy (
	ico int not null references ares.or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	kpf int,
	npf varchar,
	pfo varchar,
	tzu varchar
);
create index ares_or_pravni_formy_ico_idx on ares.or_pravni_formy(ico);

drop table if exists ares.or_sidla;
create table ares.or_sidla (
	ico int not null references ares.or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	ulice varchar,
	obec varchar,
	stat varchar,
	psc varchar
);
create index ares_or_sidla_ico_idx on ares.or_sidla(ico);

drop table if exists ares.or_angos_fo;
create table ares.or_angos_fo (
	ico int not null references ares.or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	nazev_ang varchar,
	kategorie_ang int,
	funkce varchar,
	clenstvi_zacatek date,
	clenstvi_konec date,
	funkce_zacatek date,
	funkce_konec date,

	titul_pred varchar,
	titul_za varchar,
	jmeno varchar,
	prijmeni varchar,
	datum_narozeni date,
	bydliste jsonb
);
create index ares_or_angos_fo_ico_idx on ares.or_angos_fo(ico);

drop table if exists ares.or_angos_po;
create table ares.or_angos_po (
	ico int not null references ares.or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	nazev_ang varchar,
	kategorie_ang int,
	funkce varchar,
	clenstvi_zacatek date,
	clenstvi_konec date,
	funkce_zacatek date,
	funkce_konec date,

	ico_ang int,
	izo_ang varchar,
	nazev varchar,
	pravni_forma varchar,
	stat varchar,
	sidlo jsonb
);
create index ares_or_angos_po_ico_idx on ares.or_angos_po(ico);
create index ares_or_angos_po_ico_ang_idx on ares.or_angos_po(ico_ang);
