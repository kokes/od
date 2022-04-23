from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Boolean, Integer, Numeric, SmallInteger, Text

meta = MetaData()

schema = [
    Table(
        "pobidky",
        meta,
        Column("cislo", SmallInteger, nullable=False),
        Column("firma", Text, nullable=True),
        Column("ico", Text, nullable=True, index=True),
        Column("sektor", Text, nullable=True),
        Column("nace", Text, nullable=True),
        Column("druh", Text, nullable=True),
        Column("zeme_skupina", Text, nullable=True),
        Column("zeme_zadatel", Text, nullable=True),
        Column("inv_eur", Numeric(22, 16), nullable=True),
        Column("inv_usd", Numeric(22, 16), nullable=True),
        Column("inv_czk", Numeric(22, 16), nullable=True),
        Column("nova_mista", Integer, nullable=True),
        Column("pod_dane", Text, nullable=True),
        Column("pob_mista", Text, nullable=True),
        Column("pob_rekv", Text, nullable=True),
        Column("pob_pozem", Text, nullable=True),
        Column("pob_kap", Text, nullable=True),
        Column("mira_podpory", Text, nullable=True),
        Column("strop", Text, nullable=True),
        Column("okres", Text, nullable=True),
        Column("kraj", Text, nullable=True),
        Column("region_nuts", Text, nullable=True),
        Column("podani", Text, nullable=True),
        Column("rozh_den", SmallInteger, nullable=True),
        Column("rozh_mesic", SmallInteger, nullable=True),
        Column("rozh_rok", SmallInteger, nullable=True),
        Column("msp", Boolean, nullable=True),
        Column("zruseno", Boolean, nullable=True),
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
