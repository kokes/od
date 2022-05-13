from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Integer,
    MetaData,
    SmallInteger,
    Table,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "datovky",
        meta,
        Column("id", Text, unique=True, nullable=False),
        Column("type", Text, nullable=False),
        Column("subtype", SmallInteger, nullable=False),
        Column("first_name", Text, nullable=True),
        Column("last_name", Text, nullable=True),
        Column("middle_name", Text, nullable=True),
        Column("trade_name", Text, nullable=True),
        Column("ico", Integer, nullable=True, index=True),
        Column("address", JSON, nullable=True),
        Column("pdz", Boolean, nullable=False),
        Column("ovm", Boolean, nullable=False),
        Column("hierarchy", JSON, nullable=False),
        Column("id_ovm", Integer, nullable=True),
    )
]

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
