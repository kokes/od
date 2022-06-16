from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import BigInteger, Integer, Numeric, Text

meta = MetaData()

schema = [
    Table(
        "zadatele",
        meta,
        Column(
            "id_prijemce",
            BigInteger,
            nullable=False,
            primary_key=True,
            autoincrement=False,
        ),
        Column("rok", Integer, nullable=False, primary_key=True, autoincrement=False),
        Column("jmeno_nazev", Text, nullable=True),
        Column("obec", Text, nullable=True),
        Column("okres", Text, nullable=True),
        Column("castka_bez_pvp", Numeric(12, 2), nullable=True),
    ),
    Table(
        "platby",
        meta,
        Column("id_prijemce", BigInteger, nullable=False),
        Column("rok", Integer, nullable=False),
        Column("fond_typ_podpory", Text, nullable=True),
        Column("opatreni", Text, nullable=True),
        Column("zdroje_cr", Numeric(12, 2), nullable=True),
        Column("zdroje_eu", Numeric(12, 2), nullable=True),
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
