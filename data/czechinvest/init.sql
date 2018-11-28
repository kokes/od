create schema if not exists czechinvest;

drop table if exists czechinvest.pobidky;
create table czechinvest.pobidky (
    cislo smallint not null,
    firma varchar,
    ico varchar,
    sektor varchar,
    nace varchar,
    druh varchar,
    zeme_skupina varchar,
    zeme_zadatel varchar,
    inv_eur decimal(22, 16),
    inv_usd decimal(22, 16),
    inv_czk decimal(22, 16),
    nova_mista int,
    pod_dane varchar,
    pob_mista varchar,
    pob_rekv varchar,
    pob_pozem varchar,
    pob_kap varchar,
    mira_podpory varchar,
    strop decimal(22, 16),
    okres varchar,
    kraj varchar,
    region_nuts varchar,
    podani varchar,
    rozh_den smallint,
    rozh_mesic smallint,
    rozh_rok smallint,
    msp bool,
    zruseno bool
);

create index czechinvest_pobidky_ico_idx on czechinvest.pobidky(ico);
