from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    Integer,
    MetaData,
    SmallInteger,
    Table,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "ucetni_jednotky",
        meta,
        Column("ucjed_id", Text, nullable=False),
        Column("csuis_ucjed_id", BigInteger, nullable=False),
        Column("ico", Integer, nullable=False, index=True),
        Column("start_date", Date, nullable=False),
        Column("end_date", Date, nullable=True),
        Column("nazev", Text, nullable=True),  # -- fakt to tam obcas chybi
        Column("dic", Text, nullable=False),
        Column("adresa", Text, nullable=False),
        Column("nuts_id", Text, nullable=True),
        Column(
            "zrizovatel_id", BigInteger, nullable=True
        ),  # -- references(csuis_ucjed_id),
        Column("zrizovatel_ico", Integer, nullable=True, index=True),
        Column("cofog_id", SmallInteger, nullable=False),  # -- nullif == 0?
        Column("isektor_id", SmallInteger, nullable=False),  # -- nullif == 0?
        Column("kapitola_id", SmallInteger, nullable=False),  # -- nullif == 0?
        Column("nace_id", Integer, nullable=False),
        Column("druhuj_id", SmallInteger, nullable=False),
        Column("poddruhuj_id", SmallInteger, nullable=False),
        Column("konecplat", Date, nullable=True),
        Column(
            "forma_id", Text, nullable=False
        ),  # -- ma byt short/int, ale občas to má jiný hodnoty
        Column("katobyv_id", SmallInteger, nullable=False),
        Column("stat_id", SmallInteger, nullable=True),
        Column("zdrojfin_id", SmallInteger, nullable=True),
        Column("druhrizeni_id", SmallInteger, nullable=True),
        Column("veduc_id", SmallInteger, nullable=False),
        Column("zuj", Integer, nullable=True),
        Column("sidlo", Text, nullable=True),
        Column("zpodm_id", SmallInteger, nullable=True),
        Column("kod_pou", Text, nullable=True),
        Column("typorg_id", SmallInteger, nullable=True),
        Column("pocob", Integer, nullable=False),
        Column("kraj", Text, nullable=True),
        Column("obec", Text, nullable=True),
        Column("ulice", Text, nullable=False),
        Column("kod_rp", Text, nullable=True),
        Column("datumakt", Date, nullable=True),
        Column("aktorg_id", SmallInteger, nullable=False),
        Column("datumvzniku", Date, nullable=True),
        Column("psc", Text, nullable=True),
        Column("pou_id", Integer, nullable=False),
        Column("orp_id", Integer, nullable=False),
        Column("zuj_id", Integer, nullable=True),
    )
]

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
