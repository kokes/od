from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import Date, SmallInteger, Text

meta = MetaData()

schema = [
    Table(
        "psp",  # TODO: prejmenovat
        meta,
        Column("rok", SmallInteger, nullable=False),
        Column("datum", Date, nullable=True),
        Column("schuze", SmallInteger, nullable=False),
        Column("soubor", Text, nullable=False),
        Column("autor", Text, nullable=True),
        Column("funkce", Text, nullable=True),
        Column("tema", Text, nullable=True),
        Column("text", Text, nullable=False),
    )
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
