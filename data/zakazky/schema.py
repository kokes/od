from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import (
    Boolean,
    Date,
    JSON,
    DateTime,
    Integer,
    Numeric,
    SmallInteger,
    Text,
)

meta = MetaData()

schema = [
    Table(
        "verejna_zakazka",
        meta,
        Column("casova_znacka", DateTime, nullable=False),
        Column("identifikator_NIPEZ", Text, nullable=False, index=True),
        Column("identifikator_v_elektronickem_nastroji", Text, nullable=True),
        Column("identifikatory_v_elektronickem_nastroji", JSON, nullable=False),
        Column(
            "interniIdentifikatorVerejneZakazkyPridelenyZadavatelem",
            Text,
            nullable=True,
        ),
        Column("nazev_verejne_zakazky", Text, nullable=False),
        Column("predpokladana_hodnota_bez_DPH_v_CZK", Numeric(16, 2), nullable=True),
        Column("predpokladana_hodnota_bez_DPH", Numeric(16, 2), nullable=True),
        Column("predpokladana_hodnota_bez_DPH_mena", Text, nullable=True),
        Column(
            "predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH_v_CZK",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "predpokladana_hodnota_vsech_verejnych_zakazek_ktere_mohou_byt_zadany_na_zaklade_ramcove_dohody_bez_DPH_mena",
            Text,
            nullable=True,
        ),
        Column("druh_verejne_zakazky", Text, nullable=True),
        Column("vedlejsi_druhy_verejne_zakazky", JSON, nullable=False),
        Column("rezim_verejne_zakazky", Text, nullable=False),
        Column("rezim_dle_volby_zadavatele", Text, nullable=True),
        Column("predmet", JSON, nullable=False),
        Column(
            "oduvodneni_nerozdeleni_nadlimitni_verejne_zakazky_na_casti",
            Text,
            nullable=True,
        ),
        Column(
            "typ_verejne_zakazky_dle_vyse_predpokladane_hodnoty", Text, nullable=False
        ),
        Column("hodnoty_koncese", JSON, nullable=False),
        # TODO: splitni tohle do zvlast tabulky
        Column("casti_verejne_zakazky", JSON, nullable=False),
        Column("zadavaci_postupy", Text, nullable=False),
    ),
    Table(
        "dynamicky_nakupni_system",
        meta,
        Column("casova_znacka", DateTime, nullable=False),
        Column("identifikator_NIPEZ", Text, nullable=False, index=True),
        Column("identifikator_v_elektronickem_nastroji", Text, nullable=True),
        Column("identifikatory_v_elektronickem_nastroji", JSON, nullable=False),
        Column(
            "interni_identifikator_dynamickeho_nakupniho_systemu_prideleny_zadavatelem",
            Text,
            nullable=True,
        ),
        Column("evidencni_cislo_ve_Vestniku_verejnych_zakazek", Text, nullable=True),
        Column("nazev_dynamickeho_nakupniho_systemu", Text, nullable=False),
        Column(
            "predpokladana_hodnota_dynamickeho_nakupniho_systemu_bez_DPH_v_CZK",
            Numeric(16, 2),
            nullable=False,
        ),
        Column(
            "predpokladana_hodnota_dynamickeho_nakupniho_systemu_bez_DPH",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "predpokladana_hodnota_dynamickeho_nakupniho_systemu_bez_DPH_mena",
            Text,
            nullable=True,
        ),
        Column("predpokladana_hodnota_bude_uverejnena", Boolean, nullable=False),
        Column("url", Text, nullable=True),
        Column("druh_verejne_zakazky", Text, nullable=False),
        Column("rezim_verejne_zakazky", Text, nullable=False),
        Column("rezim_dle_volby_zadavatele", Text, nullable=True),
        Column(
            "zadavaci_postup_pro_zavedeni_dynamickeho_nakupniho_systemu",
            Text,
            nullable=False,
        ),
        Column(
            "predmet_verejne_zakazky_zadavany_v_dynamickem_nakupnim_systemu",
            JSON,
            nullable=False,
        ),
        Column("kriteria_kvalifikace", JSON, nullable=True),
        Column(
            "verejna_zakazka_je_alespon_castecne_financovana_z_prostredku_Evropske_unie",
            Boolean,
            nullable=True,
        ),
        Column("informace_o_financnich_prostredcich_EU", Text, nullable=False),
        Column("kategorie_dynamickeho_nakupniho_systemu", Text, nullable=False),
        Column("doba_trvani", Text, nullable=False),
        Column("vedlejsi_druhy_verejne_zakazky", JSON, nullable=False),
        Column(
            "dodavatele_zadajici_o_ucast_v_dynamickem_nakupnim_systemu",
            JSON,
            nullable=False,
        ),
        Column(
            "ucastnici_zarazeni_do_dynamickeho_nakupniho_systemu", JSON, nullable=False
        ),
        Column("kriterium_pro_hodnoceni_nabidek", JSON, nullable=False),
        Column(
            "informace_o_otevirani_podani_v_zadavacim_postupu_pro_zavedeni_dynamickeho_nakupniho_systemu",
            Text,
            nullable=False,
        ),
    ),
]

# -- TODO: foreign keys? composite primary keys?

if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
