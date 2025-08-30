from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Date, Integer, Numeric, Text

meta = MetaData()

schema = [
    Table(
        "platby",
        meta,
        Column("rok", Integer, nullable=False),
        Column("datum", Date, nullable=True),
        Column("jmeno_nazev", Text, nullable=False),
        Column("obec", Text, nullable=True),
        Column("okres", Text, nullable=True),
        Column("fond_typ_podpory", Text, nullable=True),
        Column("opatreni", Text, nullable=True),
        Column("zdroje_cr", Numeric(12, 2), nullable=False),
        Column("zdroje_eu", Numeric(12, 2), nullable=False),
        Column("celkem_czk", Numeric(12, 2), nullable=False),
    ),
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
