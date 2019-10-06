create schema if not exists eufondy;

drop table if exists eufondy.projekty;
create table eufondy.projekty (
    id bigint not null,
    id_vyzva bigint not null,
    kod varchar not null,
    naz varchar not null,
    nazeva varchar,
    popis varchar,
    problem varchar,
    cil varchar,
    datum_zahajeni date,
    datum_ukonceni_predp date not null,
    datum_ukonceni_skut date,
    suk varchar not null,
    zadatel_nazev varchar not null,
    zadatel_ico bigint,
    zadatel_pravni_forma varchar not null,
    zadatel_adresa jsonb not null,
    cile_projektu bigint not null,
    financovani_czv decimal(18,2) not null,
    financovani_eu decimal(18,2) not null,
    financovani_cnv decimal(18,2),
    financovani_sn decimal(18,2),
    financovani_s decimal(18,2),
    financovani_esif decimal(18,2) not null,
    financovani_cv decimal(18,2) not null,
    cilove_skupiny varchar
);
