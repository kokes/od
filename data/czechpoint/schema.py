from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import JSON, Boolean, Integer, SmallInteger, Text

meta = MetaData()

# TODO: komentare do schematu:
# https://www.czechpoint.cz/data/files/SOVM_datove_soubory.pdf
schema = [
    Table(
        "subjekty",
        meta,
        Column("zkratka", Text, nullable=False),
        Column("ico", Integer, nullable=True, index=True),
        Column("nazev", Text, nullable=True),
        Column("adresa_uradu", JSON, nullable=False),
        Column("email", JSON, nullable=True),
        Column("typ_subjektu", Text, nullable=False),
        Column("pravni_forma", Text, nullable=False),
        Column("primarni_ovm", Boolean, nullable=True),
        Column("id_ds", Text, nullable=False),
        Column("typ_ds", Text, nullable=True),
        Column("stav_ds", SmallInteger, nullable=False),
        Column("stav_subjektu", SmallInteger, nullable=False),
        Column("detail_subjektu", Text, nullable=False),
        Column("identifikator_ovm", Text, nullable=False),
        Column("kategorie_ovm", Text, nullable=True),  # TODO: array type?
    )
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
