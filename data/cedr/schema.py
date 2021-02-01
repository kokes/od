from sqlalchemy import (
    Table,
    Column,
    MetaData,
    Text,
    Integer,
    Boolean,
    String,
    DateTime,
    SmallInteger,
    Numeric,
    ForeignKey,
    Integer,
)

meta = MetaData()

schema = [
    Table(
        "dotace",
        meta,
        Column("idDotace", String(40), primary_key=True),
        Column(
            "idPrijemce", Integer, nullable=True, index=True
        ),  #  -- TODO: not null nemuzem, co?
        # TODO: projit vsechny, jestli fakt musej bejt nullable
        Column("projektKod", Text, nullable=True),
        Column("podpisDatum", DateTime, nullable=True),
        Column("subjektRozliseniKod", Text, nullable=True),
        Column("ukonceniPlanovaneDatum", DateTime, nullable=True),
        Column("ukonceniSkutecneDatum", DateTime, nullable=True),
        Column("zahajeniPlanovaneDatum", DateTime, nullable=True),
        Column("zahajeniSkutecneDatum", DateTime, nullable=True),
        Column("zmenaSmlouvyIndikator", Boolean, nullable=True),
        Column("projektIdentifikator", Text, nullable=True),
        Column("projektNazev", Text, nullable=True),
        Column("iriOperacniProgram", Text, nullable=True),
        Column("iriPodprogram", Text, nullable=True),
        Column("iriPriorita", Text, nullable=True),
        Column("iriOpatreni", Text, nullable=True),
        Column("iriPodopatreni", Text, nullable=True),
        Column("iriGrantoveSchema", Text, nullable=True),
        Column("iriProgramPodpora", Text, nullable=True),
        Column("iriTypCinnosti", Text, nullable=True),
        Column("iriProgram", Text, nullable=True),
        Column("dPlatnost", DateTime, nullable=True),
        Column("dtAktualizace", DateTime, nullable=True),
    ),
    Table(
        "rozhodnuti",
        meta,
        Column("idRozhodnuti", String(40), primary_key=True),
        Column("idDotace", ForeignKey("dotace.idDotace"), index=True),
        Column("castkaPozadovana", Numeric(14, 2)),
        Column("castkaRozhodnuta", Numeric(14, 2)),
        Column("iriPoskytovatelDotace", Text, nullable=True),
        Column("iriCleneniFinancnichProstredku", Text, nullable=True),
        Column("iriFinancniZdroj", Text, nullable=True),
        Column("rokRozhodnuti", SmallInteger, nullable=True),
        Column("investiceIndikator", Boolean, nullable=True),
        Column("navratnostIndikator", Boolean, nullable=True),
        Column("refundaceIndikator", Boolean, nullable=True),
        Column("dPlatnost", DateTime, nullable=True),
        Column("dtAktualizace", DateTime, nullable=True),
    ),
    Table(
        "rozpoctoveobdobi",
        meta,
        Column("idObdobi", String(40), primary_key=True),
        Column("idRozhodnuti", ForeignKey("rozhodnuti.idRozhodnuti"), index=True),
        Column("castkaCerpana", Numeric(14, 2), nullable=True),
        Column("castkaUvolnena", Numeric(14, 2), nullable=True),
        Column("castkaVracena", Numeric(14, 2), nullable=True),
        Column("castkaSpotrebovana", Numeric(14, 2), nullable=True),
        Column("rozpoctoveObdobi", SmallInteger, nullable=True),
        Column("vyporadaniKod", Text, nullable=True),
        Column("iriDotacniTitul", Text, nullable=True),
        Column("iriUcelovyZnak", Text, nullable=True),
        Column("dPlatnost", DateTime, nullable=True),
        Column("dtAktualizace", DateTime, nullable=True),
    ),
]

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.schema import CreateTable

    engine = create_engine("sqlite:///:memory:")
    for table in schema:
        print(f"-- {table.name} as created in SQLite")
        print(CreateTable(table).compile(engine))
