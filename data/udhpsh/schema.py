from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import (
    BigInteger,
    Date,
    Integer,
    Numeric,
    SmallInteger,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "penizefo",
        meta,
        Column("rok", SmallInteger, nullable=False),
        Column("ico_prijemce", Integer, nullable=False),
        Column("nazev_prijemce", Text, nullable=False),
        Column("datum", Date, nullable=True),
        Column("castka", Numeric, nullable=True),
        Column("prijmeni", Text, nullable=False),
        Column("jmeno", Text, nullable=False),
        Column("titul_pred", Text, nullable=True),
        Column("titul_za", Text, nullable=True),
        Column("datum_narozeni", Date, nullable=False),
        Column("adresa_mesto", Text, nullable=True),
    ),
    Table(
        "penizepo",
        meta,
        Column("rok", SmallInteger, nullable=False),
        Column("ico_prijemce", Integer, nullable=False),
        Column("nazev_prijemce", Text, nullable=False),
        Column("datum", Date, nullable=True),
        Column("castka", Numeric, nullable=False),
        Column("ico_darce", Integer, nullable=True),
        Column("spolecnost", Text, nullable=False),
        Column("adresa_ulice", Text, nullable=True),
        Column("adresa_mesto", Text, nullable=True),
        Column("adresa_psc", BigInteger, nullable=True),
    ),
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
