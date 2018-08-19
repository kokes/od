drop table if exists od.smlouvy cascade;
create table od.smlouvy (
  zdroj char(7), -- 2018-07
  id_verze int not null primary key,
  id_smlouvy int not null,
  odkaz varchar not null, -- TODO: redundantni?
  cas_zverejneni timestamptz not null,
  predmet varchar,
  datum_uzavreni date not null,
  cislo_smlouvy varchar,
  schvalil varchar,
  hodnota_bez_dph numeric(18, 2),
  hodnota_s_dph numeric(18, 2),
  platny_zaznam boolean
);

drop table if exists od.smlouvy_ucastnici;
create table od.smlouvy_ucastnici (
  zdroj char(7), -- 2018-07
  smlouva int not null references od.smlouvy(id_verze) on delete cascade,
  subjekt boolean not null,
  ds varchar, -- TODO: char? datovka
  nazev varchar,
  ico_raw varchar,
  ico int,
  adresa varchar,
  utvar varchar,
  platce boolean,
  prijemce boolean
);
create index smlouvy_ucastnici_ico_idx on od.smlouvy_ucastnici(ico);
