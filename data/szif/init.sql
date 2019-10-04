create schema if not exists szif;

create table szif.zadatele (
	id_prijemce bigint not null,
	rok int not null,
	jmeno_nazev varchar,
	obec varchar,
	okres varchar,
	castka_bez_pvp decimal(12,2)
);

create index szif_zadatele_pkey on szif.zadatele(id_prijemce, rok);

create table szif.platby (
	id_prijemce bigint not null,
	rok int not null,
	fond_typ_podpory varchar,
	opatreni varchar,
	zdroje_cr decimal(12, 2),
	zdroje_eu decimal(12, 2),
	celkem_czk decimal(12, 2) not null
);

create index szif_platby_pkey on szif.platby(id_prijemce, rok);