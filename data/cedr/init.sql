drop table if exists od.cedr_dotace; create table od.cedr_dotace (
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

drop table if exists od.cedr_rozhodnuti; create table od.cedr_rozhodnuti (
	idRozhodnuti char(40) primary key,
	idDotace char(40),
	castkaPozadovana numeric(14, 2),
	castkaRozhodnuta numeric(14, 2),
	iriPoskytovatelDotace varchar,
	iriCleneniFinancnichProstredku varchar,
	iriFinancniZdroj varchar,
	rokRozhodnuti varchar,
	investiceIndikator bool,
	navratnostIndikator bool,
	refundaceIndikator bool,
	dPlatnost timestamp,
	dtAktualizace timestamp
);

drop table if exists od.cedr_rozpoctoveobdobi; create table od.cedr_rozpoctoveobdobi (
	idObdobi char(40) primary key,
	idRozhodnuti char(40),
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

-- TODO: indexy po copy - dotace(idprijemce) a rozhodnuti(iddotace)