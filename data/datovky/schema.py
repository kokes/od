from sqlalchemy import (
    Table,
    Column,
    MetaData,
    JSON,
    Boolean,
    Text,
    SmallInteger,
    Integer,
)

meta = MetaData()

schema = [
    Table(
        "datovky",
        meta,
        Column("id", Text, unique=True, nullable=False),
        Column("type", Text, nullable=False),
        Column("subtype", SmallInteger, nullable=False),
        Column("firstName", Text, nullable=True),
        Column("lastName", Text, nullable=True),
        Column("middleName", Text, nullable=True),
        Column("tradeName", Text, nullable=True),
        Column("ico", Integer, nullable=True, index=True),
        Column("address", JSON, nullable=True),
        Column("pdz", Boolean, nullable=False),
        Column("ovm", Boolean, nullable=False),
        Column("hierarchy", JSON, nullable=False),
        Column("idOVM", Integer, nullable=True),
    )
]

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
