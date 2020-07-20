CREATE SCHEMA IF NOT EXISTS volby;
drop view if exists volby.kandidati;
drop table if exists volby.prezident_kandidati;

create table volby.prezident_kandidati (
    datum date,
    ckand smallint not null,
    jmeno varchar not null,
    prijmeni varchar not null,
    titulpred varchar,
    titulza varchar,
    vek smallint,
    povolani varchar,
    bydlisten varchar not null,
    bydlistek int not null,
    pstrana smallint not null,
    nstrana smallint not null,
    pohlavi smallint not null,
    platnost varchar,
    hlasy_k1 int not null,
    zvolen_k1 smallint not null,
    hlasy_k2 int not null,
    zvolen_k2 smallint not null
);

DROP TABLE IF EXISTS volby.prezident_strany;

CREATE TABLE volby.prezident_strany (
	datum date,
	NSTRANA smallint NOT NULL,
	NAZEV_STRN varchar NOT NULL,
	ZKRATKAN30 varchar NOT NULL,
	ZKRATKAN8 varchar NOT NULL
);

DROP TABLE IF EXISTS volby.prezident_okrsky;

CREATE TABLE volby.prezident_okrsky (
	datum date,
	TYP_FORM int NOT NULL,
	OPRAVA int NOT NULL,
	CHYBA int NOT NULL,
	OKRES int NOT NULL,
	OBEC int NOT NULL,
	OKRSEK int NOT NULL,
	KC_1 int NOT NULL,
	KOLO smallint NOT NULL,
	VOL_SEZNAM int NOT NULL,
	VYD_OBALKY int NOT NULL,
	ODEVZ_OBAL int NOT NULL,
	PL_HL_CELK int NOT NULL,
	KC_2 int NOT NULL,
	KC_3 int NOT NULL,
	KC_4 int NOT NULL,
	POSL_KAND smallint NOT NULL,
	KC_SUM int NOT NULL,
    HLASY int[] NOT NULL
);

drop table if exists volby.psp_kandidati;

create table volby.psp_kandidati (
    datum date,
    volkraj smallint not null,
    kstrana smallint not null,
    porcislo smallint not null,
    jmeno varchar not null,
    prijmeni varchar not null,
    titulpred varchar,
    titulza varchar,
    vek smallint,
    povolani varchar,
    bydlisten varchar,
    bydlistek int,
    pstrana smallint,
    nstrana smallint,
    platnost varchar,
    pochlasu int not null,
    pocproc numeric(5, 2),
    pocprocvse numeric(5, 2),
    mandat char(1),
    poradimand smallint,
    poradinahr smallint
);

drop table if exists volby.psp_strany;

create table volby.psp_strany (
    datum date,
    kstrana smallint not null,
    vstrana smallint not null,
    nazevcelk varchar not null,
    nazev_strk varchar not null,
    zkratkak30 varchar not null,
    zkratkak8 varchar not null,
    pocstrvko smallint not null,
    slozeni varchar not null,
    stavreg varchar not null,
    platnost varchar,
    plat_str varchar,
    pocmandat smallint,
    pocmandcr smallint,
    slozneplat varchar,
    nazevplny varchar
);

DROP TABLE IF EXISTS volby.psp_okrsky_hlasy;

CREATE TABLE volby.psp_okrsky_hlasy (
	datum date,
	ID_OKRSKY int,
	TYP_FORM int NOT NULL,
	OPRAVA int NOT NULL,
	CHYBA int NOT NULL,
	OKRES int NOT NULL,
	OBEC int NOT NULL,
	OKRSEK int NOT NULL,
	KC_1 int NOT NULL,
	KSTRANA int NOT NULL,
	POC_HLASU int NOT NULL,
	KC_2 int NOT NULL,
	KC_3 int NOT NULL,
	KC_4 int NOT NULL,
	POSL_KAND int NOT NULL,
	KC_SUM int NOT NULL,
    HLASY int[] NOT NULL
);

DROP TABLE IF EXISTS volby.psp_okrsky_prehled;

CREATE TABLE volby.psp_okrsky_prehled (
	datum date,
	ID_OKRSKY int,
	TYP_FORM int NOT NULL,
	OPRAVA int NOT NULL,
	CHYBA int NOT NULL,
	OKRES int NOT NULL,
	OBEC int NOT NULL,
	OKRSEK int NOT NULL,
	KC_1 int NOT NULL,
	KC_2 int NOT NULL,
	ZAKRSTRANA bit(60) NOT NULL,
	VOL_SEZNAM int NOT NULL,
	VYD_OBALKY int NOT NULL,
	ODEVZ_OBAL int NOT NULL,
	PL_HL_CELK int NOT NULL
);

drop table if exists volby.komunalni_vysledky_obce;

create table volby.komunalni_vysledky_obce (
    datum date,
    okres smallint not null,
    kodzastup int not null,
    nazevzast varchar not null,
    cobvodu smallint not null,
    por_str_hl smallint not null,
    ostrana smallint not null,
    vstrana smallint not null,
    nazevcelk varchar not null,
    zkratkao30 varchar not null,
    zkratkao8 varchar,
    pocstr_slo smallint not null,
    slozeni varchar not null,
    hlasy_str int,
    prochlstr numeric(5, 2),
    mand_str smallint
);

drop table if exists volby.komunalni_kandidati;

create table volby.komunalni_kandidati (
    datum date,
    okres smallint not null,
    kodzastup int not null,
    cobvodu smallint not null,
    por_str_hl smallint not null,
    ostrana smallint not null,
    porcislo smallint not null,
    jmeno varchar not null,
    prijmeni varchar not null,
    titulpred varchar,
    titulza varchar,
    vek smallint,
    povolani varchar,
    bydlisten varchar,
    pstrana smallint,
    nstrana smallint,
    platnost varchar,
    pochlasu int,
    pochl_pres int,
    pocprocvse numeric(5, 2),
    mandat char(1),
    poradimand smallint,
    poradinahr smallint
);

drop table if exists volby.komunalni_strany;

create table volby.komunalni_strany (
    datum date,
    vstrana smallint not null,
    nazevcelk varchar not null,
    nazev_strv varchar not null,
    zkratkav30 varchar not null,
    zkratkav8 varchar,
    pocstr_slo varchar not null,
    slozeni varchar not null,
    zkratka_of varchar,
    typvs varchar not null
);

drop table if exists volby.komunalni_obce;

create table volby.komunalni_obce (
    datum date,
    kraj varchar not null,
    okres smallint not null,
    typzastup smallint not null,
    druhzastup smallint not null,
    kodzastup int not null,
    nazevzast varchar not null,
    obec int not null,
    nazevobce varchar not null,
    orp varchar,
    cpou int not null,
    regurad int not null,
    obvody smallint not null,
    cobvodu smallint not null,
    mandaty smallint not null,
    pocobyv int not null,
    typduvodu smallint not null,
    pocet_vs smallint not null,
    stav_obce smallint not null
);

DROP TABLE IF EXISTS volby.komunalni_okrsky_prehled;

CREATE TABLE volby.komunalni_okrsky_prehled (
  datum date,
  ID_OKRSKY int NOT NULL,
  TYP_FORM smallint NOT NULL,
  OPRAVA smallint NOT NULL,
  CHYBA smallint NOT NULL,
  OKRES int NOT NULL,
  OBEC int NOT NULL,
  OKRSEK int NOT NULL,
  KC_1 int NOT NULL,
  TYPZASTUP smallint NOT NULL,
  COBVODU smallint NOT NULL,
  VOL_SEZNAM int NOT NULL,
  VYD_OBALKY int NOT NULL,
  ODEVZ_OBAL int NOT NULL,
  PL_HL_CELK int NOT NULL,
  POCET_VS smallint NOT NULL,
  POC_VS_HL smallint NOT NULL,
  KC_2 int NOT NULL,
  KODZASTUP int NOT NULL
);

DROP TABLE IF EXISTS volby.komunalni_okrsky_hlasy;

CREATE TABLE volby.komunalni_okrsky_hlasy (
  datum date,
  ID_OKRSKY int NOT NULL,
  TYP_FORM smallint NOT NULL,
  OPRAVA smallint NOT NULL,
  CHYBA smallint NOT NULL,
  OKRES int NOT NULL,
  OBEC int NOT NULL,
  OKRSEK int NOT NULL,
  KC_1 int NOT NULL,
  TYPZASTUP smallint NOT NULL,
  POR_STR_HL int NOT NULL,
  POC_HLASU int NOT NULL,
  KC_2 int NOT NULL,
  POSL_KAND smallint NOT NULL,
  KC_SUM int NOT NULL,
  HLASY int[] NOT NULL
);

drop table if exists volby.kraje_kandidati;

create table volby.kraje_kandidati (
    datum date,
    krzast smallint not null,
    kstrana smallint not null,
    porcislo varchar not null,
    jmeno varchar not null,
    prijmeni varchar not null,
    titulpred varchar,
    titulza varchar,
    vek smallint,
    povolani varchar,
    bydlisten varchar,
    bydlistek int,
    pstrana smallint,
    nstrana smallint,
    platnost varchar,
    pochlasu int not null,
    pocproc numeric(5, 2),
    pocprocvse numeric(5, 2),
    mandat char(1),
    poradimand smallint,
    poradinahr smallint,
    poradihahr smallint
);

drop table if exists volby.kraje_strany_cr;

create table volby.kraje_strany_cr (
    datum date,
    kstrana smallint not null,
    vstrana smallint not null,
    nazevcelk varchar not null,
    nazev_strk varchar not null,
    zkratkak30 varchar not null,
    zkratkak8 varchar not null,
    pocstrvko smallint not null,
    slozeni varchar not null,
    stavreg varchar not null,
    plat_str varchar,
    pocmandcr smallint not null,
    nazevplny varchar,
    platnost varchar,
    slozneplat varchar
);

drop table if exists volby.kraje_strany_kraje;

create table volby.kraje_strany_kraje (
    datum date,
    krzast smallint not null,
    kstrana smallint not null,
    vstrana smallint not null,
    nazevcelk varchar not null,
    nazev_strk varchar not null,
    zkratkak30 varchar not null,
    zkratkak8 varchar not null,
    pocstrvko smallint not null,
    slozeni varchar not null,
    stavreg smallint not null,
    plat_str varchar,
    platnost varchar,
    slozneplat varchar
);

DROP TABLE IF EXISTS volby.kraje_obce;

CREATE TABLE volby.kraje_obce (
    datum date NOT NULL,
    KRAJ int NOT NULL,
    OKRES int NOT NULL,
    CPOU int NOT NULL,
    ORP int,
    OBEC int NOT NULL,
    NAZEVOBCE varchar NOT NULL,
    KRZAST smallint NOT NULL,
    OBEC_PREZ int
);

DROP TABLE IF EXISTS volby.kraje_okrsky_prehled;

CREATE TABLE volby.kraje_okrsky_prehled (
	datum date,
	ID_OKRSKY smallint,
	TYP_FORM smallint NOT NULL,
	OPRAVA smallint NOT NULL,
	CHYBA smallint NOT NULL,
	OKRES smallint NOT NULL,
	OBEC int NOT NULL,
	OKRSEK int NOT NULL,
	KC_1 int NOT NULL,
	VOL_SEZNAM smallint NOT NULL,
	VYD_OBALKY smallint NOT NULL,
	ODEVZ_OBAL smallint NOT NULL,
	PL_HL_CELK smallint NOT NULL,
	KC_2 int NOT NULL,
	ZAKRSTRANA bit varying(100) NOT NULL
);

DROP TABLE IF EXISTS volby.kraje_okrsky_hlasy;

CREATE TABLE volby.kraje_okrsky_hlasy (
	datum date,
	ID_OKRSKY smallint,
	TYP_FORM smallint NOT NULL,
	OPRAVA smallint NOT NULL,
	CHYBA smallint NOT NULL,
	OKRES smallint NOT NULL,
	OBEC int NOT NULL,
	OKRSEK int NOT NULL,
	KC_1 int NOT NULL,
	KSTRANA smallint NOT NULL,
	POC_HLASU smallint NOT NULL,
	KC_2 int NOT NULL,
	KC_3 int NOT NULL,
	KC_4 int NOT NULL,
	KC_5 int NOT NULL,
	POSL_KAND smallint NOT NULL,
	KC_SUM int NOT NULL,
    HLASY int[] NOT NULL
);

drop table if exists volby.ep_kandidati;

create table volby.ep_kandidati (
    datum date,
    estrana smallint not null,
    porcislo smallint not null,
    jmeno varchar not null,
    prijmeni varchar not null,
    titulpred varchar,
    titulza varchar,
    vek smallint,
    statobcan varchar,
    povolani varchar,
    bydlisten varchar,
    bydlistek int,
    pstrana smallint,
    nstrana smallint,
    platnost varchar,
    pochlasu int,
    pocproc numeric(5, 2),
    pocprocvse numeric(5, 2),
    mandat char(1),
    poradimand smallint,
    poradinahr smallint
);

drop table if exists volby.ep_strany;

create table volby.ep_strany (
    datum date,
    estrana smallint not null,
    vstrana smallint not null,
    nazevcelk varchar not null,
    nazev_stre varchar not null,
    zkratkae30 varchar not null,
    zkratkae8 varchar not null,
    pocstrvko smallint not null,
    slozeni varchar not null,
    stavreg smallint not null,
    platnost smallint,
    plat_str char(1),
    slozneplat varchar(40),
    pocmandcr smallint not null,
    nazevplny varchar
);

DROP TABLE IF EXISTS volby.ep_okrsky_prehled;

CREATE TABLE volby.ep_okrsky_prehled (
  datum date,
  ID_OKRSKY smallint,
  TYP_FORM smallint NOT NULL,
  OPRAVA smallint,
  CHYBA smallint,
  OKRES int NOT NULL,
  OBEC int NOT NULL,
  OKRSEK int NOT NULL,
  KC_1 int,
  KC_2 int,
  ZAKRSTRANA bit varying(100),
  VOL_SEZNAM smallint NOT NULL,
  VYD_OBALKY smallint NOT NULL,
  ODEVZ_OBAL smallint NOT NULL,
  PL_HL_CELK smallint NOT NULL
);

DROP TABLE IF EXISTS volby.ep_okrsky_hlasy;

CREATE TABLE volby.ep_okrsky_hlasy (
  datum date,
  ID_OKRSKY smallint,
  TYP_FORM smallint NOT NULL,
  OPRAVA smallint,
  CHYBA smallint,
  OKRES int NOT NULL,
  OBEC int NOT NULL,
  OKRSEK int NOT NULL,
  KC_1 int,
  ESTRANA smallint NOT NULL,
  POC_HLASU int NOT NULL,
  KC_2 int,
  KC_3 int,
  KC_4 int,
  POSL_KAND smallint,
  KC_SUM int,
  HLASY int[] NOT NULL
);

drop table if exists volby.senat_kandidati;

create table volby.senat_kandidati (
    datum date,
    obvod smallint not null,
    ckand smallint not null,
    vstrana smallint not null,
    jmeno varchar not null,
    prijmeni varchar not null,
    titulpred varchar,
    titulza varchar,
    vek smallint,
    povolani varchar,
    bydlisten varchar not null,
    bydlistek int not null,
    pstrana smallint not null,
    nstrana smallint not null,
    platnost varchar,
    hlasy_k1 int not null,
    proc_k1 numeric(5, 2) not null,
    uriz_pr_k1 double precision not null,
    zvolen_k1 smallint not null,
    los_k1 smallint not null,
    hlasy_k2 int not null,
    proc_k2 numeric(5, 2) not null,
    uriz_pr_k2 double precision not null,
    zvolen_k2 smallint not null,
    los_k2 smallint not null,
    nazev_vs varchar not null
);

DROP TABLE IF EXISTS volby.senat_obvody;

CREATE TABLE volby.senat_obvody (
	datum date,
	OBVOD smallint NOT NULL,
	NAZEV_OBV varchar NOT NULL,
	OKRES varchar NOT NULL,
	PRVNI_VO varchar NOT NULL,
	PLATNOST varchar NOT NULL
);

DROP TABLE IF EXISTS volby.senat_okrsky;

CREATE TABLE volby.senat_okrsky (
	datum date,
	TYP_FORM smallint NOT NULL,
	OPRAVA smallint NOT NULL,
	CHYBA smallint NOT NULL,
	OBEC int NOT NULL,
	OKRSEK int NOT NULL,
	KC_1 smallint NOT NULL,
	OBVOD int NOT NULL,
	KOLO smallint NOT NULL,
	VOL_SEZNAM int NOT NULL,
	VYD_OBALKY int NOT NULL,
	ODEVZ_OBAL int NOT NULL,
	PL_HL_CELK int NOT NULL,
	KC_2 int NOT NULL,
	KC_3 int NOT NULL,
	KC_4 int NOT NULL,
	POSL_KAND smallint NOT NULL,
	KC_SUM int NOT NULL,
    HLASY int[] NOT NULL
);


create view volby.kandidati AS (
    SELECT
        'senat' AS volby,
        obvod || ' - ' || nazev_obv as obvod,
        datum,
        jmeno || ' ' || prijmeni AS jmeno,
        nazev_vs AS strana,
        vek,
        povolani,
        (zvolen_k1 = 1) OR (zvolen_k2 = 1) AS zvolen
    FROM
        volby.senat_kandidati
        INNER JOIN volby.senat_obvody USING(datum, obvod)

    UNION ALL

    SELECT
        'ep' AS volby,
        NULL AS obvod,
        datum,
        jmeno || ' ' || prijmeni as jmeno,
        nazevcelk AS strana,
        vek,
        povolani,
        mandat IN ('1', 'A') AS zvolen
    FROM
        volby.ep_kandidati
        INNER JOIN volby.ep_strany USING (datum, estrana)

    UNION ALL

    SELECT
        'obce' AS volby,
        NULL AS obvod, -- TODO
        kn.datum,
        jmeno || ' ' || prijmeni AS jmeno,
        nazevcelk AS strana,
        vek,
        povolani,
        mandat IN ('1', 'A') AS zvolen
    FROM
        volby.komunalni_kandidati kn
        INNER JOIN volby.komunalni_strany ks ON kn.nstrana = ks.vstrana
            AND kn.datum = ks.datum

    UNION ALL

    SELECT
        'kraje' AS volby,
        NULL AS obvod, -- TODO
        kn.datum,
        jmeno || ' ' || prijmeni AS jmeno,
        nazevcelk AS strana,
        vek,
        povolani,
        mandat IN ('1', 'A') as zvolen
    FROM
        volby.kraje_kandidati kn
        INNER JOIN volby.kraje_strany_cr ks ON kn.nstrana = ks.vstrana
            AND kn.datum = ks.datum

    UNION ALL

    SELECT
        'psp' AS volby,
        NULL AS obvod, -- TODO
        kn.datum,
        jmeno || ' ' || prijmeni AS jmeno,
        nazevcelk AS strana,
        vek,
        povolani,
        mandat IN ('1', 'A') AS zvolen
    FROM
        volby.psp_kandidati kn
        INNER JOIN volby.psp_strany ks ON ks.datum = kn.datum
            AND ks.vstrana = kn.nstrana

    UNION ALL

    SELECT
        'prezident' AS volby,
        NULL AS obvod,
        kn.datum,
        jmeno || ' ' || prijmeni AS jmeno,
        ps.nazev_strn as strana,
        vek,
        povolani,
        (zvolen_k1 = 1) OR (zvolen_k2 = 1) AS zvolen
    FROM
        volby.prezident_kandidati kn
        INNER JOIN volby.prezident_strany ps ON kn.nstrana = ps.nstrana
        AND kn.datum = ps.datum
);
