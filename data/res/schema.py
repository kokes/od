from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, Text

meta = MetaData()

schema = [
    Table(
        # https://opendata.czso.cz/data/od_org03/res_data-metadata.json
        "subjekty",
        meta,
        Column(
            "ico",
            Integer,
            nullable=False,
            primary_key=True,
            autoincrement=False,
            comment="Identifikační číslo",
        ),
        Column(
            "okres_lau",
            Text,
            nullable=True,
            comment="Kód okresu sídla (dle CZ-NUTS) dle číselníku ČSÚ (109)",
        ),
        Column(
            "datum_vznik",
            Date,
            nullable=True,
            comment="Datum vzniku ve formátu YYYY-MM-DD",
        ),
        Column(
            "datum_zanik",
            Date,
            nullable=True,
            comment="Datum zániku ve formátu YYYY-MM-DD",
        ),
        Column(
            "zpusob_zanik",
            Text,
            nullable=True,
            comment="Způsob zániku dle číselníku ČSÚ (572)",
        ),
        Column(
            "datum_aktualizace",
            Date,
            nullable=True,
            comment="Datum aktualizace ve formátu YYYY-MM-DD",
        ),
        Column(
            "pravni_forma",
            Text,
            nullable=True,
            comment="Právní forma (statistická) dle číselníku ČSÚ (56)",
        ),
        Column(
            "pravni_forma_ros",
            Text,
            nullable=True,
            comment="Právní forma (registr osob) dle číselníku ČSÚ (149)",
        ),
        Column(
            "kategorie_zamestnanci",
            Text,
            nullable=True,
            comment="Kategorie dle počtu pracovníků dle číselníku ČSÚ (579)",
        ),
        Column(
            "nace",
            Text,
            nullable=True,
            comment="Převažující činnost (statistická) dle klasifikace ČSÚ (80004)",
        ),
        Column(
            "ic_zuj",
            Text,
            nullable=True,
            comment="Identifikační číslo základní územní jednotky sídla organizace dle",
        ),
        # číselníku ČSÚ (51)
        Column(
            "firma",
            Text,
            nullable=True,
            comment="Firma, název (jméno)",
        ),
        Column(
            "esa2010",
            Text,
            nullable=True,
            comment="Kód institucionálního sektoru (ESA2010) dle číselníku ČSÚ (5161)",
        ),
        Column(
            "adresni_misto",
            Text,
            nullable=True,
            comment="Kód adresního místa dle ISUI (ČÚZK)",
        ),
        Column(
            "adresa",
            Text,
            nullable=True,
            comment="Text adresy (pro místa s chybějícím KODADM)",
        ),
        Column(
            "psc",
            Text,
            nullable=True,
            comment="Adresa sídla dle KODADM: PSČ",
        ),
        Column(
            "obec",
            Text,
            nullable=True,
            comment="Adresa sídla dle KODADM: obec",
        ),
        Column(
            "cast_obce",
            Text,
            nullable=True,
            comment="Adresa sídla dle KODADM: část obce",
        ),
        Column(
            "ulice",
            Text,
            nullable=True,
            comment="Adresa sídla dle KODADM: ulice",
        ),
        Column(
            "typ_cislo_domovni",
            Text,
            nullable=True,
            comment="Typ čísla domovního dle číselníku ČSÚ (73)",
        ),
        Column(
            "cislo_domovni",
            Text,
            nullable=True,
            comment="Adresa sídla dle KODADM: číslo domovní",
        ),
        Column(
            "cislo_orientacni",
            Text,
            nullable=True,
            comment="Adresa sídla dle KODADM: číslo orientační",
        ),
        Column(
            "datum_platnost",
            Date,
            nullable=False,
            comment="Datum platnosti dat ve formátu YYYY-MM-DD",
        ),
        Column(
            "priznak",
            Text,
            nullable=True,
            comment="Vyjadřuje změnu oproti minulému stavu: P = přírůstek záznamu oproti",
        ),
        # minulému stavu (může být i znovuobnovení IČO po více než 48 měsících,
        # např. IČO zaniklo v 2015-07 a znovu obnovilo činnost 2021-07-18 =>
        # dostane v dávce k 31.7.2021 příznak P, neboť z výstupů vypadl již
        # v červenci 2019), Z = změna v záznamu oproti minulému stavu
    ),
    Table(
        # https://opendata.czso.cz/data/od_org03/res_pf_nace-metadata.json
        "nace",
        meta,
        Column(
            "ico",
            Integer,
            nullable=False,
            comment="Identifikační číslo",
        ),
        Column(
            "zdroj_udaj",
            Text,
            nullable=True,
            comment="Zdroj údaje dle číselníku ČSÚ (564)",
        ),
        Column(
            "kod_ciselnik",
            Text,
            nullable=True,
            comment="Kód číselníku",
        ),
        Column(
            "hodnota",
            Text,
            nullable=True,
            comment="Kód atributu",
        ),
        Column(
            "datum_platnost",
            Date,
            nullable=False,
            comment="Datum platnosti dat ve formátu YYYY-MM-DD",
        ),
        Column(
            "datum_aktualizace",
            Date,
            nullable=True,
            comment="Datum aktualizace záznamu ve formátu YYYY-MM-DD",
        ),
        Column(
            "priznak",
            Text,
            nullable=True,
            comment="Vyjadřuje změnu oproti minulému stavu: P = přírůstek záznamu",
        ),
        # oproti minulému stavu (může být i znovuobnovení IČO po více než
        # 48 měsících, např. IČO zaniklo v 2015-07 a znovu obnovilo
        # činnost 2021-07-18 => dostane v dávce k 31.7.2021 příznak P,
        # neboť z výstupů vypadl již v červenci 2019), Z = změna v
        # záznamu oproti minulému stavu
    ),
]


if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
