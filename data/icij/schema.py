from typing import Text
from sqlalchemy import (
    Table,
    Column,
    MetaData,
)
from sqlalchemy.sql.sqltypes import BigInteger, Integer, Numeric, Text

meta = MetaData()

# TODO(PR): black etc.

schema = [
    Table(
        "addresses",
        meta,
        Column("_id", Text, nullable=True),
        Column("node_id", Text, nullable=True),
        Column("address", Text, nullable=True),
        Column("name", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=True),
        Column("valid_until", Text, nullable=True),
        Column("note", Text, nullable=True),
    ),
    Table(
        "entities",
        meta,
        Column("_id", Text, nullable=True),
        Column("node_id", Text, nullable=True),
        Column("name", Text, nullable=True),
        Column("original_name", Text, nullable=True),
        Column("former_name", Text, nullable=True),
        Column("jurisdiction", Text, nullable=True),
        Column("jurisdiction_description", Text, nullable=True),
        Column("company_type", Text, nullable=True),
        Column("address", Text, nullable=True),
        Column("internal_id", Text, nullable=True),
        Column("incorporation_date", Text, nullable=True),
        Column("inactivation_date", Text, nullable=True),
        Column("struck_off_date", Text, nullable=True),
        Column("dorm_date", Text, nullable=True),
        Column("status", Text, nullable=True),
        Column("service_provider", Text, nullable=True),
        Column("ibcRUC", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("sourceID", Text, nullable=True),
        Column("valid_until", Text, nullable=True),
        Column("note", Text, nullable=True),
    ),
    Table(
        "intermediaries",
        meta,
        Column("_id", Text, nullable=True),
        Column("node_id", Text, nullable=True),
        Column("name", Text, nullable=True),
        Column("status", Text, nullable=True),
        Column("internal_id", Text, nullable=True),
        Column("address", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=True),
        Column("valid_until", Text, nullable=True),
        Column("note", Text, nullable=True),
    ),
    Table(
        "officers",
        meta,
        Column("_id", Text, nullable=True),
        Column("node_id", Text, nullable=True),
        Column("name", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=True),
        Column("valid_until", Text, nullable=True),
        Column("note", Text, nullable=True),
    ),
    Table(
        "others",
        meta,
        Column("_id", Text, nullable=True),
        Column("node_id", Text, nullable=True),
        Column("name", Text, nullable=True),
        Column("type", Text, nullable=True),
        Column("incorporation_date", Text, nullable=True),
        Column("struck_off_date", Text, nullable=True),
        Column("closed_date", Text, nullable=True),
        Column("jurisdiction", Text, nullable=True),
        Column("jurisdiction_description", Text, nullable=True),
        Column("countries", Text, nullable=True),
        Column("country_codes", Text, nullable=True),
        Column("sourceID", Text, nullable=True),
        Column("valid_until", Text, nullable=True),
        Column("note", Text, nullable=True),
    ),
    Table(
        "relationships",
        meta,
        Column("_id", Text, nullable=True),
        Column("_start", Text, nullable=True),
        Column("_end", Text, nullable=True),
        Column("_type", Text, nullable=True),
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
