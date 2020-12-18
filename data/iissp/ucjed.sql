CREATE SCHEMA IF NOT EXISTS iissp;
DROP TABLE IF EXISTS iissp.ucetni_jednotky;
CREATE TABLE iissp.ucetni_jednotky (
       csuis_ucjed_id bigint not null,
       ico int not null,
       start_date date not null,
       end_date date not null,
       ucjed_nazev text, -- fakt to tam obcas chybi
       dic text,
       adresa text not null,
       nuts_id text,
       zrizovatel_id bigint, -- references(csuis_ucjed_id),
       cofog_id smallint, -- nullif == 0?
       isektor_id smallint, -- nullif == 0?
       kapitola_id smallint, -- nullif == 0?
       nace_id int,
       druhuj_id smallint,
       poddruhuj_id smallint,
       konecplat date,
       forma_id text, -- ma byt short/int, ale občas to má jiný hodnoty
       katobyv_id smallint not null,
       stat_id smallint,
       zdrojfin_id smallint,
       druhrizeni_id smallint,
       veduc_id smallint,
       zuj int,
       sidlo text,
       zpodm_id smallint,
       kod_pou text,
       typorg_id smallint,
       pocob int,
       ulice text,
       kod_rp text,
       datumakt date,
       aktorg_id smallint,
       datumvzniku date,
       psc text,
       pou_id int,
       orp_id int,
       zuj_id int
);
