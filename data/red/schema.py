from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    Table,
    Text,
)

meta = MetaData()


schema = [
    Table(
        "prijemce",
        meta,
        Column("id_prijemce", Text, nullable=False, primary_key=True),
        Column("ico", Integer, nullable=True, index=True),
        Column("obchodni_nazev", Text, nullable=True),
        Column("jmeno", Text, nullable=True),
        Column("prijmeni", Text, nullable=True),
        Column("rok_narozeni", Integer, nullable=True),
        Column("pravni_forma", Text, nullable=False),
        Column("stat", Text, nullable=False),
        Column("datum_aktualizace", DateTime, nullable=False),
    ),
    Table(
        "dotace",
        meta,
        Column("id_dotace", Text, nullable=False, primary_key=True),
        Column("id_prijemce", ForeignKey("prijemce.id_prijemce"), nullable=False),
        Column("kod", Text, nullable=True),
        Column("identifikator", Text, nullable=False),
        Column("nazev", Text, nullable=True),
        Column("podpis_datum", DateTime, nullable=False),
        Column("rozliseni_subjektu", Text, nullable=True),
        Column("zahajeni_planovane_datum", DateTime, nullable=True),
        Column("ukonceni_planovane_datum", DateTime, nullable=True),
        Column("zahajeni_skutecne_datum", DateTime, nullable=True),
        Column("ukonceni_skutecne_datum", DateTime, nullable=True),
        Column("zmena_smlouvy_indikator", Text, nullable=False),
        Column("operacni_program", Text, nullable=True),
        Column("podprogram", Text, nullable=True),
        Column("priorita", Text, nullable=True),
        Column("opatreni", Text, nullable=True),
        Column("podopatreni", Text, nullable=True),
        Column("grantove_schema", Text, nullable=True),
        Column("platnost_datum", DateTime, nullable=False),
        Column("datum_aktualizace", DateTime, nullable=True),
    ),
    Table(
        "rozhodnuti",
        meta,
        Column("id_rozhodnuti", Text, nullable=False, primary_key=True),
        Column("id_dotace", ForeignKey("dotace.id_dotace"), nullable=False),
        Column("etapa", Text, nullable=True),
        Column("castka_pozadovana", Numeric(14, 2), nullable=True),
        Column("castka_rozhodnuta", Numeric(14, 2), nullable=True),
        Column("rok_rozhodnuti", Integer, nullable=False),
        Column("investice_indikator", Text, nullable=False),
        Column("navratnost_indikator", Text, nullable=False),
        Column("refundace_indikator", Text, nullable=False),
        Column("dotace_poskytovatel", Text, nullable=False),
        Column("cleneni_financnich_prostredku", Text, nullable=False),
        Column("financni_zdroj", Text, nullable=False),
        Column("platnost_datum", Text, nullable=True),
        Column("datum_aktualizace", Text, nullable=False),
    ),
    Table(
        "rozpoctoveobdobi",
        meta,
        Column("id_rozpoctove_obdobi", Text, nullable=False, primary_key=True),
        Column("id_rozhodnuti", ForeignKey("rozhodnuti.id_rozhodnuti"), nullable=False),
        Column("castka_cerpana", Numeric(14, 2), nullable=True),
        Column("castka_uvolnena", Numeric(14, 2), nullable=True),
        Column("castka_vracena", Numeric(14, 2), nullable=True),
        Column("castka_spotrebovana", Numeric(14, 2), nullable=True),
        Column("obdobi", Text, nullable=False),
        Column("vyporadani_kod", Text, nullable=True),
        Column("dotacni_titul", Text, nullable=True),
        Column("ucelovy_znak", Text, nullable=True),
        Column("datum_aktualizace", Text, nullable=False),
    ),
]

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
