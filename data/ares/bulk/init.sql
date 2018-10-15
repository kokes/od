drop table if exists ares.vreo_firmy;
create table ares.vreo_firmy(
    zdroj varchar not null,
	aktualizace_db date not null,
	datum_vypisu date not null,
	cas_vypisu time not null,
	typ_vypisu varchar not null,
	rejstrik varchar,
	ico int not null, -- TODO: primary key po deduplikaci
	obchodni_firma varchar,
	datum_zapisu date not null,
	datum_vymazu date,
	sidlo json
);

drop table if exists ares.vreo_fosoby;
create table ares.vreo_fosoby(
	ico int not null,
	nazev_organu varchar,
	datum_zapisu date not null,
	datum_vymazu date,
	nazev_funkce varchar,
	jmeno varchar,
	prijmeni varchar,
	titul_pred varchar,
	titul_za varchar,
	adresa json,
	bydliste json
);
