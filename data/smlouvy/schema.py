from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import (
    Boolean,
    Date,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "smlouvy",
        meta,
        Column("zdroj", String(7), nullable=False),  # 2018-07
        Column(
            "id_verze", Integer, nullable=False, primary_key=True, autoincrement=False
        ),
        Column("id_smlouvy", Integer, nullable=False),
        Column("odkaz", Text, nullable=False),  # TODO: redundantni?
        Column("cas_zverejneni", DateTime, nullable=False),
        Column("predmet", Text, nullable=True),
        Column("datum_uzavreni", Date, nullable=False),
        Column("cislo_smlouvy", Text, nullable=True),
        Column("schvalil", Text, nullable=True),
        Column("hodnota_bez_dph", Numeric(18, 2)),
        Column("hodnota_s_dph", Numeric(18, 2)),
        Column("platny_zaznam", Boolean, nullable=False),
    ),
    Table(
        "ucastnici",
        meta,
        Column("zdroj", String(7), nullable=False),  # 2018-07
        # TODO: on delete cascade? nebo budem mazat podle zdroje?
        Column(
            "smlouva", Integer, nullable=False
        ),  # TODO: ForeignKey("smlouvy.id_verze"), odstraneno kvuli --partial
        Column("subjekt", Boolean, nullable=False),
        Column("ds", Text, nullable=True),  # TODO: char? datovka
        Column("nazev", Text, nullable=True),
        Column("ico_raw", Text, nullable=True),
        Column("ico", Integer, nullable=True, index=True),
        Column("adresa", Text, nullable=True),
        Column("utvar", Text, nullable=True),
        Column("platce", Boolean, nullable=True),
        Column("prijemce", Boolean),
    ),
]


if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
