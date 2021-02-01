from sqlalchemy import Table, MetaData, Column
from sqlalchemy.sql.sqltypes import Date, Integer, Text, JSON


meta = MetaData()

schema = [
    Table(
        "deletes",
        meta,
        Column("application_number", Integer, nullable=False),
        Column("application_date", Date, nullable=False),
    ),
    Table(
        "inserts",
        meta,
        Column("application_number", Integer, nullable=False),
        Column("application_date", Date, nullable=False),
        Column("registration_number", Integer, nullable=True),
        Column("registration_date", Date, nullable=True),
        Column("expiry_date", Date, nullable=True),
        Column("current_status_code", Text, nullable=False),
        Column("kind_mark", Text, nullable=False),
        Column("mark_feature", Text, nullable=True),
        Column("mark_verbal_element", Text, nullable=True),
        Column("class_description", JSON, nullable=True),
    ),
]
# TODO: pridat nejak
# CREATE INDEX trgm_verbal_idx ON upv.inserts USING gist (mark_verbal_element gist_trgm_ops);

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
