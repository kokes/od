from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import BigInteger, Date, Integer, Text

meta = MetaData()


schema = [
    Table(
        "addresses",
        meta,
        Column("_id", Integer, nullable=False, primary_key=True),
        Column("node_id", BigInteger, nullable=False),
        Column("address", Text, nullable=True),
        Column("name", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=False, index=False),
        Column("valid_until", Text, nullable=False),
        Column("note", Text, nullable=True),
    ),
    Table(
        "entities",
        meta,
        Column("_id", Integer, nullable=False, primary_key=True),
        Column("node_id", BigInteger, nullable=False),
        Column("name", Text, nullable=True),
        Column("original_name", Text, nullable=True),
        Column("former_name", Text, nullable=True),
        Column("jurisdiction", Text, nullable=True),
        Column("jurisdiction_description", Text, nullable=True),
        Column("company_type", Text, nullable=True),
        Column("address", Text, nullable=True),
        Column("internal_id", Text, nullable=True),
        Column("incorporation_date", Date, nullable=True),
        Column("inactivation_date", Date, nullable=True),
        Column("struck_off_date", Date, nullable=True),
        Column("dorm_date", Date, nullable=True),
        Column("status", Text, nullable=True),
        Column("service_provider", Text, nullable=True),
        Column("ibcRUC", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("sourceID", Text, nullable=False),
        Column("valid_until", Text, nullable=False),
        Column("note", Text, nullable=True),
    ),
    Table(
        "intermediaries",
        meta,
        Column("_id", Integer, nullable=False, primary_key=True),
        Column("node_id", BigInteger, nullable=False),
        Column("name", Text, nullable=True),
        Column("status", Text, nullable=True),
        Column("internal_id", Text, nullable=True),
        Column("address", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=False),
        Column("valid_until", Text, nullable=False),
        Column("note", Text, nullable=True),
    ),
    Table(
        "officers",
        meta,
        Column("_id", Integer, nullable=False, primary_key=True),
        Column("node_id", BigInteger, nullable=False),
        Column("name", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=False),
        Column("valid_until", Text, nullable=False),
        Column("note", Text, nullable=True),
    ),
    Table(
        "others",
        meta,
        Column("_id", Integer, nullable=False, primary_key=True),
        Column("node_id", BigInteger, nullable=False),
        Column("name", Text, nullable=False),
        Column("type", Text, nullable=True),
        Column("incorporation_date", Date, nullable=True),
        Column("struck_off_date", Date, nullable=True),
        Column("closed_date", Date, nullable=True),
        Column("jurisdiction", Text, nullable=True),
        Column("jurisdiction_description", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=False),
        Column("valid_until", Text, nullable=False),
        Column("note", Text, nullable=True),
    ),
    Table(
        "relationships",
        meta,
        Column("_id", Integer, nullable=True),
        Column("_start", Text, nullable=False),
        Column("_end", Text, nullable=False),
        Column("_type", Text, nullable=False),
        Column("link", Text, nullable=True),
        Column("status", Text, nullable=True),
        Column("start_date", Text, nullable=True),
        Column("end_date", Text, nullable=True),
        Column("sourceID", Text, nullable=True),
    ),
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
