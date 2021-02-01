from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import Date, Text

meta = MetaData()

schema = [
    Table(
        "politici",
        meta,
        Column("wikidata_id", Text, nullable=False),
        Column("jmeno_prijmeni", Text, nullable=False),
        Column("datum_narozeni", Date, nullable=False),
    )
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
