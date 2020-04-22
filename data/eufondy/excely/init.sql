create schema if not exists eufondy;
drop table if exists eufondy.dotace_0713;
create table eufondy.dotace_0713 (
	prijemce varchar,
	ico int,
	projekt varchar not null,
	operacni_program varchar not null,
	fond_eu varchar not null, -- TODO: enum
	datum_alokace date not null,
	castka_alokovana numeric(14, 2) not null,
	datum_platby date,
	castka_proplacena numeric(14, 2) not null,
	stav varchar -- TODO: enum
);

drop table if exists eufondy.dotace_1420;
create table eufondy.dotace_1420 (
 	nazev_programu varchar,
 	nazev_prioritni_osy varchar,
 	registracni_cislo_operace varchar,
 	nazev_projektu_cz varchar,
 	shrnuti_operace varchar,
 	nazev_subjektu varchar,
 	ico int,
 	pravni_forma varchar,
 	psc_prijemce int,
 	skutecne_zahajeni date,
 	predpokladane_ukonceni date,
 	skutecne_ukonceni date,
 	nazev_stavu varchar,
 	misto_realizace_nazev_nuts_1 varchar,
 	misto_realizace_kod_nuts_3 varchar,
 	misto_realizace_nazev_nuts_3 varchar,
 	oblast_intervence_kod varchar,
 	oblast_intervence_nazev varchar,
 	fond varchar,
 	mira_spolufinancovani_z_esi_fondu numeric(3, 2),
 	podpora_czk numeric(14, 2),
 	podpora_prispevek_unie_czk numeric(14, 2),
 	podpora_narodni_verejne_zdroje_czk numeric(14, 2),
 	podpora_narodni_soukrome_zdroje_czk numeric(14, 2),
 	vyuctovano_czk numeric(14, 2),
 	vyuctovano_prispevek_unie_czk numeric(14, 2),
 	vyuctovano_narodni_verejne_zdroje_czk numeric(14, 2),
 	vyuctovano_narodni_soukrome_zdroje_czk numeric(14, 2)
)
