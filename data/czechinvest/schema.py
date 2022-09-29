from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Boolean, Integer, Numeric, SmallInteger, Text

meta = MetaData()

schema = [
    Table(
        "pobidky",
        meta,
        Column("cislo", SmallInteger, nullable=False),
        Column("firma", Text, nullable=False),
        Column("ico", Text, nullable=False, index=True),
        Column("sektor", Text, nullable=False),
        Column("nace", Text, nullable=True),
        Column("druh", Text, nullable=False),
        Column("zeme_skupina", Text, nullable=True),
        Column("zeme_zadatel", Text, nullable=False),
        Column("inv_eur", Numeric(22, 16), nullable=False),
        Column("inv_usd", Numeric(22, 16), nullable=False),
        Column("inv_czk", Numeric(22, 16), nullable=False),
        Column("nova_mista", Integer, nullable=False),
        Column("pod_dane", Text, nullable=True),
        Column("pob_mista", Text, nullable=True),
        Column("pob_rekv", Text, nullable=True),
        Column("pob_pozem", Text, nullable=True),
        Column("pob_kap", Text, nullable=True),
        Column("mira_podpory", Text, nullable=False),
        Column("strop", Text, nullable=True),
        Column("okres", Text, nullable=False),
        Column("kraj", Text, nullable=False),
        Column("region_nuts", Text, nullable=True),
        Column("podani", Text, nullable=False),
        Column("rozh_den", SmallInteger, nullable=True),
        Column("rozh_mesic", SmallInteger, nullable=False),
        Column("rozh_rok", SmallInteger, nullable=False),
        Column("msp", Boolean, nullable=True),
        Column("zruseno", Boolean, nullable=False),
        Column("zduvodneni", Text, nullable=True),
        Column("bez_pobidek", Text, nullable=True),
        # TODO: to by melo byt Date, ale maj tam nekonzistentni data
        Column("prodlouzeni_lhuty", Text, nullable=True),
    )
]


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
