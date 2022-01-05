from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import JSON, BigInteger, Date, Integer, Numeric, Text

meta = MetaData()

schema = [
    Table(
        "opendata_2014_2020",
        meta,
        Column("id", BigInteger, nullable=False),
        Column("id_vyzva", BigInteger, nullable=False),
        Column("kod", Text, nullable=False),
        Column("naz", Text, nullable=False),
        Column("nazeva", Text, nullable=True),
        Column("popis", Text, nullable=True),
        Column("problem", Text, nullable=True),
        Column("cil", Text, nullable=True),
        Column("datum_zahajeni", Date, nullable=True),
        Column("datum_ukonceni_predp", Date, nullable=False),
        Column("datum_ukonceni_skut", Date, nullable=True),
        Column("suk", Text, nullable=False),
        Column("zadatel_nazev", Text, nullable=False),
        Column("zadatel_ico", BigInteger, nullable=True),
        Column("zadatel_pravni_forma", Text, nullable=False),
        Column("zadatel_adresa", JSON, nullable=False),
        Column("cile_projektu", BigInteger, nullable=False),
        Column("financovani_czv", Numeric(18, 2), nullable=False),
        Column("financovani_eu", Numeric(18, 2), nullable=False),
        Column("financovani_cnv", Numeric(18, 2), nullable=True),
        Column("financovani_sn", Numeric(18, 2), nullable=True),
        Column("financovani_s", Numeric(18, 2), nullable=True),
        Column("financovani_esif", Numeric(18, 2), nullable=False),
        Column("financovani_cv", Numeric(18, 2), nullable=False),
        Column("cilove_skupiny", Text),
    ),
    Table(
        "prehled_2017_2013",
        meta,
        Column("prijemce", Text, nullable=True),
        Column("ico", Integer, nullable=True, index=True),
        Column("projekt", Text, nullable=False),
        Column("operacni_program", Text, nullable=False),
        Column("fond_eu", Text, nullable=False),  # -- TODO: enum
        Column("datum_alokace", Date, nullable=False),
        Column("castka_alokovana", Numeric(14, 2), nullable=False),
        Column("datum_platby", Date, nullable=True),
        Column("castka_proplacena", Numeric(14, 2), nullable=False),
        Column("stav", Text),  # TODO: enum
    ),
    Table(
        "prehled_2014_2020",
        meta,
        Column("nazev_programu", Text, nullable=True),
        Column("nazev_prioritni_osy", Text, nullable=True),
        Column("registracni_cislo_operace", Text, nullable=True),
        Column("nazev_projektu_cz", Text, nullable=True),
        Column("shrnuti_operace", Text, nullable=True),
        Column("nazev_subjektu", Text, nullable=True),
        Column("ico", Integer, nullable=True, index=True),
        Column("pravni_forma", Text, nullable=True),
        Column("psc_prijemce", Integer, nullable=True),
        Column("skutecne_zahajeni", Date, nullable=True),
        Column("predpokladane_ukonceni", Date, nullable=True),
        Column("skutecne_ukonceni", Date, nullable=True),
        Column("nazev_stavu", Text, nullable=True),
        Column("misto_realizace_nazev_nuts_1", Text, nullable=True),
        Column("misto_realizace_kod_nuts_3", Text, nullable=True),
        Column("misto_realizace_nazev_nuts_3", Text, nullable=True),
        Column("oblast_intervence_kod", Text, nullable=True),
        Column("oblast_intervence_nazev", Text, nullable=True),
        Column("fond", Text, nullable=True),
        Column("mira_spolufinancovani_z_esi_fondu", Numeric(3, 2)),
        Column("podpora_czk", Numeric(14, 2)),
        Column("podpora_prispevek_unie_czk", Numeric(14, 2)),
        Column("podpora_narodni_verejne_zdroje_czk", Numeric(14, 2)),
        Column("podpora_narodni_soukrome_zdroje_czk", Numeric(14, 2)),
        Column("vyuctovano_czk", Numeric(14, 2)),
        Column("vyuctovano_prispevek_unie_czk", Numeric(14, 2)),
        Column("vyuctovano_narodni_verejne_zdroje_czk", Numeric(14, 2)),
        Column("vyuctovano_narodni_soukrome_zdroje_czk", Numeric(14, 2)),
    ),
]

if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
