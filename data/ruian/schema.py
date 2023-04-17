from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, Numeric, Text

meta = MetaData()

schema = [
    Table(
        "adresni_mista",
        meta,
        Column(
            "kod_adm",
            Integer,
            nullable=False,
            primary_key=True,
            autoincrement=False,
            comment="Kód adresního místa vedeného v Informačním"
            " systému územní identifikace (ISÚI).",
        ),
        Column(
            "kod_obce",
            Integer,
            nullable=False,
            comment="Kód obce vedené v ISÚI, ze které jsou vypsána všechna"
            " adresní místa.",
        ),
        Column(
            "nazev_obce",
            Text,
            nullable=False,
            comment="Název obce, ze které jsou vypsána všechna adresní místa.",
        ),
        Column(
            "kod_momc",
            Integer,
            nullable=True,
            comment="Kód městského obvodu/městské části, který je vyplněn"
            " pouze v případě členěných statutárních měst.",
        ),
        Column(
            "nazev_momc",
            Text,
            nullable=True,
            comment="Název městského obvodu/městské části, který je vyplněn"
            " pouze v případě členěných statutárních měst.",
        ),
        Column(
            "kod_obvodu_prahy",
            Text,
            nullable=True,
            comment="Kód obvodu Prahy, který je vyplněn pouze v případě"
            " Hlavního města Prahy.",
        ),
        Column(
            "nazev_obvodu_prahy",
            Text,
            nullable=True,
            comment="Název obvodu Prahy, který je vyplněn pouze v případě"
            " Hlavního města Prahy.",
        ),
        Column(
            "kod_casti_obce",
            Integer,
            nullable=True,
            comment="Kód části obce v rámci nadřazené obce, ve které je"
            " číslován stavební objekt.",
        ),
        Column(
            "nazev_casti_obce",
            Text,
            nullable=True,
            comment="Název části obce v rámci nadřazené obce, ve které je"
            " číslován stavební  objekt.",
        ),
        Column(
            "kod_ulice",
            Integer,
            nullable=True,
            comment="Kód ulice, která je navázána na adresní místo."
            " Může být vyplněn pouze u obcí, které mají zavedenu uliční síť.",
        ),
        Column(
            "nazev_ulice",
            Text,
            nullable=True,
            comment="Název ulice, která je navázána na adresní místo."
            " Může být vyplněn pouze u obcí, které mají zavedenu uliční síť.",
        ),
        Column(
            "typ_so",
            Text,
            nullable=True,
            comment="Typ stavebního objektu, může nabývat hodnot:"
            " č.p.- číslo popisné stavebního objektu,"
            " č.ev.- číslo evidenční stavebního objektu",
        ),
        Column(
            "cislo_domovni",
            Integer,
            nullable=True,
            comment="Číslo popisné nebo číslo evidenční, podle rozlišeného typu SO.",
        ),
        Column(
            "cislo_orientacni",
            Integer,
            nullable=True,
            comment="Číslo orientační, slouží k orientaci v rámci nadřazené ulice.",
        ),
        Column(
            "znak_cisla_orientacniho",
            Text,
            nullable=True,
            comment="Znak čísla orientačního, uveden v případě,"
            " že je znak k orientačnímu číslu přidělen.",
        ),
        Column("psc", Integer, nullable=True, comment="Poštovní směrovací číslo."),
        Column(
            "souradnice_y",
            Numeric(18, 2),
            nullable=True,
            comment="Souřadnice Y definičního bodu adresního místa v systému S-JTSK"
            " (systém jednotné trigonometrické sítě katastrální), uvedené v [m].",
        ),
        Column(
            "souradnice_x",
            Numeric(18, 2),
            nullable=True,
            comment="Souřadnice X definičního bodu adresního místa v systému S-JTSK"
            " (systém jednotné trigonometrické sítě katastrální), uvedené v [m].",
        ),
        Column(
            "plati_od",
            Date,
            nullable=False,
            comment="Datum platnosti adresního místa ve tvaru RRRR-MM-DD."
            " Pokud je datum 1. 7. 2011, jedná se o adresní místo vzniklé"
            " při úvodní migraci dat",
        ),
        Column(
            "zemepisna_sirka",
            Numeric(18, 2),
            nullable=True,
            comment="Zeměpisná šířka převedená ze systému souřadnic S-JTSK",
        ),
        Column(
            "zemepisna_delka",
            Numeric(18, 2),
            nullable=True,
            comment="Zeměpisná délka převedená ze systému souřadnic S-JTSK",
        ),
    ),
]


if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
