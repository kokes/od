from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, Numeric, Text


meta = MetaData()

schema = [
    Table(
        "adreseni_mista",
        meta,
        Column("kod_adm", Integer, nullable=False,
               primary_key=True, autoincrement=False),
        Column("kod_obce", Integer, nullable=False),
        Column("nazev_obce", Text, nullable=False),
        Column("kod_momc", Integer, nullable=True),
        Column("nazev_momc", Text, nullable=True),
        Column("kod_obvodu_prahy", Text, nullable=True),
        Column("nazev_obvodu_prahy", Text, nullable=True),
        Column("kod_casti_obce", Integer, nullable=True),
        Column("nazev_casti_obce", Text, nullable=True),
        Column("kod_ulice", Integer, nullable=True),
        Column("nazev_ulice", Text, nullable=True),
        Column("typ_so", Text, nullable=True),
        Column("cislo_domovni", Integer, nullable=True),
        Column("cislo_orientacni", Integer, nullable=True),
        Column("znak_cisla_orientacniho", Text, nullable=True),
        Column("psc", Integer, nullable=True),
        Column("souradnice_y", Numeric(18, 2), nullable=True),
        Column("souradnice_x", Numeric(18, 2), nullable=True),
        Column("plati_od", Date, nullable=False),
        Column("zemepisna_sirka", Numeric(18, 2), nullable=True),
        Column("zemepisna_delka", Numeric(18, 2), nullable=True),
    ),

]


if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
