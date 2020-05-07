create schema if not exists dotinfo;
drop table if exists dotinfo.dotace;
create table dotinfo.dotace (
	evidencni_cislo_dotace varchar,
	identifikator_dotace varchar not null,
	nazev_dotace varchar,
	ucastnik varchar,
	ic_ucastnika int,
	ucel_dotace varchar,
	poskytovatel_dotace varchar,
	ic_poskytovatele int,
	castka_pozadovana numeric(14, 2), 
	castka_schvalena numeric(14, 2),
	datum_poskytnuti timestamp null
);

-- TODO: tohle chce pustit az po loadu
create index dotinfo_ic_uc_idx on dotinfo.dotace(ic_ucastnika);
create index dotinfo_ic_ps_idx on dotinfo.dotace(ic_poskytovatele);

