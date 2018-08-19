drop table if exists od.ares_res;
create table if not exists od.ares_res (
	ico int not null primary key,
	aktualizace_db date not null,
	datum_vypisu date not null,
	nazev varchar,
	pravni_forma_id int,
	pravni_forma_nazev varchar,
	datum_vzniku date not null,
	datum_zaniku date,
	sidlo json,
	stat_udaje json,
	nace json
);

drop table if exists od.ares_or_udaje cascade;
create table od.ares_or_udaje (
	ico int not null primary key,
	aktualizace_db date,
	datum_vypisu date,
	platnost_od date,
	datum_zapisu date,
	stav_subjektu varchar
);

drop table if exists od.ares_or_nazvy;
create table od.ares_or_nazvy (
	ico int not null references od.ares_or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	nazev varchar
);
create index ares_or_nazvy_ico_idx on od.ares_or_nazvy(ico);

drop table if exists od.ares_or_pravni_formy;
create table od.ares_or_pravni_formy (
	ico int not null references od.ares_or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	kpf int,
	npf varchar,
	pfo varchar,
	tzu varchar
);
create index ares_or_pravni_formy_ico_idx on od.ares_or_pravni_formy(ico);

drop table if exists od.ares_or_sidla;
create table od.ares_or_sidla (
	ico int not null references od.ares_or_udaje(ico) on delete cascade,
	dod date,
	ddo date,
	ulice varchar,
	obec varchar,
	stat varchar,
	psc varchar
);
create index ares_or_sidla_ico_idx on od.ares_or_sidla(ico);

drop table if exists od.ares_or_angos_fo;
create table od.ares_or_angos_fo (
	ico int not null references od.ares_or_udaje(ico) on delete cascade,
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
	datum_narozeni date
);
create index ares_or_angos_fo_ico_idx on od.ares_or_angos_fo(ico);

drop table if exists od.ares_or_angos_po;
create table od.ares_or_angos_po (
	ico int not null references od.ares_or_udaje(ico) on delete cascade,
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
	stat varchar
);
create index ares_or_angos_po_ico_idx on od.ares_or_angos_po(ico);
create index ares_or_angos_po_ico_ang_idx on od.ares_or_angos_po(ico_ang);
