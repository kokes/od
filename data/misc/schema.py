from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Integer, Text

meta = MetaData()
"IČO", "Obchodní jméno", "Sídlo", "Stát", "Odsouzeni"


schema = [
    Table(
        "odsouzene_po",
        meta,
        Column("ico", Integer, nullable=True, index=True),
        Column("obchodni_jmeno", Text, nullable=False),
        Column("sidlo", Text, nullable=True),
        Column("stat", Text, nullable=False),
        Column("odsouzeni", Text, nullable=False),
    )
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
