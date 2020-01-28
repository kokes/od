CREATE SCHEMA IF NOT EXISTS iissp;
CREATE TABLE iissp.ucetni_jednotky (
       ico int not null,
       start_date date not null,
       end_date date not null,
       ucjed_nazev text, -- fakt to tam obcas chybi
       dic text,
       adresa text not null,
       nuts_id text not null,
       zrizovatel_ico int,
       cofog_id smallint, -- nullif == 0?
       isektor_id smallint, -- nullif == 0?
       kapitola_id smallint, -- nullif == 0?
       nace_id int not null,
       druhuj_id smallint not null,
       poddruhuj_id smallint not null,
       konecplat date,
       forma_id smallint not null,
       katobyv_id smallint not null,
       obec text,
       kraj text not null,
       stat_id smallint,
       zdrojfin_id smallint,
       druhrizeni_id smallint,
       veduc_id smallint not null,
       zuj int,
       sidlo text,
       zpodm_id smallint,
       kod_pou text,
       typorg_id smallint,
       pocob int,
       ulice text,
       kod_rp text,
       datumakt date not null,
       aktorg_id smallint,
       datumvzniku date not null,
       psc text
);