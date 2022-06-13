from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import JSON, Date, Integer, Text, Time

meta = MetaData()

schema = [
    Table(
        "firmy",
        meta,
        Column("zdroj", Text, nullable=False),
        Column("aktualizace_db", Date, nullable=False),
        Column("datum_vypisu", Date, nullable=False),
        Column("cas_vypisu", Time, nullable=False),
        Column("typ_vypisu", Text, nullable=False),
        Column("rejstrik", Text, nullable=True),
        Column("ico", Integer, nullable=False, primary_key=True),
        Column("obchodni_firma", Text, nullable=True),
        Column("datum_zapisu", Date, nullable=False),
        Column("datum_vymazu", Date, nullable=True),
        Column("sidlo", JSON, nullable=True),
    ),
    Table(
        "fosoby",
        meta,
        Column("ico", Integer, nullable=False, index=True),
        Column("nazev_organu", Text, nullable=True),
        Column("datum_zapisu", Date, nullable=False),
        Column("datum_vymazu", Date, nullable=True),
        Column("nazev_funkce", Text, nullable=True),
        Column("jmeno", Text, nullable=True),
        Column("prijmeni", Text, nullable=True),
        Column("titul_pred", Text, nullable=True),
        Column("titul_za", Text, nullable=True),
        Column("adresa", JSON, nullable=True),
        Column("bydliste", JSON, nullable=True),
    ),
    Table(
        "posoby",
        meta,
        Column("ico", Integer, nullable=False, index=True),
        Column("nazev_organu", Text, nullable=True),
        Column("datum_zapisu", Date, nullable=False),
        Column("datum_vymazu", Date, nullable=True),
        Column("nazev_funkce", Text, nullable=True),
        Column("obchodni_firma", Text, nullable=True),
        Column("ico_organ", Integer, nullable=True, index=True),
        Column("adresa", JSON, nullable=True),
    ),
]


if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))


# TODO: resolvnout tohle:
# -- kvuli duplikatu v ICO 64123561

# delete from ares.vreo_firmy t1 using
# ares.vreo_firmy t2 where t1.aktualizace_db < t2.aktualizace_db and t1.ico=t2.ico;

# alter table ares.vreo_firmy add primary key (ico);
