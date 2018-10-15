drop table if exists cedr.dotace; create table cedr.dotace (
	idDotace char(40) primary key,
	idPrijemce int, -- TODO: not null nemuzem, co?
	projektKod varchar,
	podpisDatum timestamp,
	subjektRozliseniKod varchar,
	ukonceniPlanovaneDatum timestamp,
	ukonceniSkutecneDatum timestamp,
	zahajeniPlanovaneDatum timestamp,
	zahajeniSkutecneDatum timestamp,
	zmenaSmlouvyIndikator bool,
	projektIdentifikator varchar,
	projektNazev varchar,
	iriOperacniProgram varchar,
	iriPodprogram varchar,
	iriPriorita varchar,
	iriOpatreni varchar,
	iriPodopatreni varchar,
	iriGrantoveSchema varchar,
	iriProgramPodpora varchar,
	iriTypCinnosti varchar,
	iriProgram varchar,
	dPlatnost timestamp,
	dtAktualizace timestamp
);

drop table if exists cedr.rozhodnuti; create table cedr.rozhodnuti (
	idRozhodnuti char(40) primary key,
	idDotace char(40) references cedr.dotace(idDotace),
	castkaPozadovana numeric(14, 2),
	castkaRozhodnuta numeric(14, 2),
	iriPoskytovatelDotace varchar,
	iriCleneniFinancnichProstredku varchar,
	iriFinancniZdroj varchar,
	rokRozhodnuti smallint,
	investiceIndikator bool,
	navratnostIndikator bool,
	refundaceIndikator bool,
	dPlatnost timestamp,
	dtAktualizace timestamp
);

drop table if exists cedr.rozpoctoveobdobi; create table cedr.rozpoctoveobdobi (
	idObdobi char(40) primary key,
	idRozhodnuti char(40) references cedr.rozhodnuti(idRozhodnuti),
	castkaCerpana numeric(14, 2),
	castkaUvolnena numeric(14, 2),
	castkaVracena numeric(14, 2),
	castkaSpotrebovana numeric(14, 2),
	rozpoctoveObdobi smallint,
	vyporadaniKod varchar,
	iriDotacniTitul varchar,
	iriUcelovyZnak varchar,
	dPlatnost timestamp,
	dtAktualizace timestamp
);

create index cedr_dotace_idprijemce_idx on cedr.dotace(idprijemce);
create index cedr_rozhodnuti_iddotace_idx on cedr.dotace(idprijemce);
create index cedr_rozpoctoveobdobi_idrozhodnuti_idx on cedr.rozpoctoveobdobi(idRozhodnuti);
