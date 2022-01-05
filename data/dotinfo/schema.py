from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import DateTime, Integer, Numeric, Text

meta = MetaData()

schema = [
    Table(
        "dotace",
        meta,
        Column("evidencni_cislo_dotace", Text, nullable=True),
        Column("identifikator_dotace", Text, nullable=False),
        Column("nazev_dotace", Text, nullable=False),
        Column("ucastnik", Text, nullable=False),
        Column("ic_ucastnika", Integer, nullable=False, index=True),
        Column("ucel_dotace", Text, nullable=True),
        Column("poskytovatel_dotace", Text, nullable=True),
        Column("ic_poskytovatele", Integer, nullable=True, index=True),
        Column("castka_pozadovana", Numeric(14, 2), nullable=True),
        Column("castka_schvalena", Numeric(14, 2), nullable=True),
        Column("datum_poskytnuti", DateTime, nullable=True),
    )
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
