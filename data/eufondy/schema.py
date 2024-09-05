from sqlalchemy import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import JSON, BigInteger, Date, Integer, Numeric, Text

meta = MetaData()

schema = [
    Table(
        "opendata_2014_2020",
        meta,
        Column("id", BigInteger, nullable=False),
        Column("id_vyzva", BigInteger, nullable=False),
        Column("kod", Text, nullable=False),
        Column("naz", Text, nullable=False),
        Column("nazeva", Text, nullable=True),
        Column("popis", Text, nullable=True),
        Column("problem", Text, nullable=True),
        Column("cil", Text, nullable=True),
        Column("datum_zahajeni", Date, nullable=True),
        Column("datum_ukonceni_predp", Date, nullable=False),
        Column("datum_ukonceni_skut", Date, nullable=True),
        Column("suk", Text, nullable=False),
        Column("zadatel_nazev", Text, nullable=False),
        Column("zadatel_ico", Integer, nullable=True),
        Column("zadatel_pravni_forma", Text, nullable=False),
        Column("zadatel_adresa", JSON, nullable=False),
        Column("cile_projektu", BigInteger, nullable=False),
        Column("financovani_czv", Numeric(18, 2), nullable=False),
        Column("financovani_eu", Numeric(18, 2), nullable=False),
        Column("financovani_cnv", Numeric(18, 2), nullable=True),
        Column("financovani_sn", Numeric(18, 2), nullable=True),
        Column("financovani_s", Numeric(18, 2), nullable=True),
        Column("financovani_esif", Numeric(18, 2), nullable=False),
        Column("financovani_cv", Numeric(18, 2), nullable=False),
        Column("cilove_skupiny", Text),
    ),
    Table(
        "prehled_2007_2013",
        meta,
        Column("prijemce", Text, nullable=False),
        Column("ico", Integer, nullable=True, index=True),
        Column("projekt", Text, nullable=False),
        Column("operacni_program", Text, nullable=False),
        Column("fond_eu", Text, nullable=False),  # -- TODO: enum
        Column("datum_alokace", Date, nullable=False),
        Column("castka_alokovana", Numeric(14, 2), nullable=False),
        Column("datum_platby", Date, nullable=True),
        Column("castka_proplacena", Numeric(14, 2), nullable=False),
        Column("stav", Text, nullable=False),  # TODO: enum
    ),
    Table(
        "prehled_2014_2020",
        meta,
        Column("nazev_programu", Text, nullable=False),
        Column("nazev_prioritni_osy", Text, nullable=False),
        Column("registracni_cislo_operace", Text, nullable=False),
        Column("nazev_projektu_cz", Text, nullable=False),
        Column("shrnuti_operace", Text, nullable=True),
        Column("nazev_subjektu", Text, nullable=False),
        Column("ico", Integer, nullable=True, index=True),
        Column("pravni_forma", Text, nullable=False),
        Column("psc_prijemce", Integer, nullable=True),
        Column("skutecne_zahajeni", Date, nullable=True),
        Column("predpokladane_ukonceni", Date, nullable=False),
        Column("skutecne_ukonceni", Date, nullable=True),
        Column("nazev_stavu", Text, nullable=False),
        Column("misto_realizace_nazev_nuts_1", Text, nullable=False),
        Column("misto_realizace_kod_nuts_3", Text, nullable=True),
        Column("misto_realizace_nazev_nuts_3", Text, nullable=True),
        Column("oblast_intervence_kod", Text, nullable=True),
        Column("oblast_intervence_nazev", Text, nullable=True),
        Column("fond", Text, nullable=False),
        Column("mira_spolufinancovani_z_esi_fondu", Numeric(3, 2), nullable=False),
        Column("podpora_czk", Numeric(14, 2), nullable=False),
        Column("podpora_prispevek_unie_czk", Numeric(14, 2), nullable=False),
        Column("podpora_narodni_verejne_zdroje_czk", Numeric(14, 2)),
        Column("podpora_narodni_soukrome_zdroje_czk", Numeric(14, 2), nullable=False),
        Column("vyuctovano_czk", Numeric(14, 2), nullable=False),
        Column("vyuctovano_prispevek_unie_czk", Numeric(14, 2), nullable=False),
        Column("vyuctovano_narodni_verejne_zdroje_czk", Numeric(14, 2), nullable=False),
        Column(
            "vyuctovano_narodni_soukrome_zdroje_czk", Numeric(14, 2), nullable=False
        ),
    ),
    Table(
        "prehled_2021_2027",
        meta,
        Column("cislo_programu", Text, nullable=False),
        Column("nazev_programu", Text, nullable=False),
        Column("cislo_priority", Text, nullable=False),
        Column("nazev_priority", Text, nullable=False),
        Column("cislo_specifickeho_cile", Text, nullable=False),
        Column("nazev_specifickeho_cile", Text, nullable=True),
        Column("fond", Text, nullable=False),
        Column("registracni_cislo_projektu", Text, nullable=False),
        Column("nazev_projektu", Text, nullable=False),
        Column("popis_projektu", Text, nullable=False),
        Column("cil_projektu", Text, nullable=False),
        Column("kod_stavu_projektu", Text, nullable=False),
        Column("stav_projektu", Text, nullable=False),
        Column("prijemce_nazev", Text, nullable=False),
        Column("ic_prijemce", Integer, nullable=True),
        Column("pravni_forma_prijemce", Text, nullable=False),
        Column("psc_prijemce", Text, nullable=True),
        Column(
            "skutecne_datum_zahajeni_fyzicke_realizace_projektu", Date, nullable=True
        ),
        Column(
            "predpokladane_datum_ukonceni_fyzicke_realizace_projektu",
            Date,
            nullable=True,
        ),
        Column(
            "skutecne_datum_ukonceni_fyzicke_realizace_projektu", Date, nullable=True
        ),
        Column("misto_realizace_kod_nuts_3", Text, nullable=False),
        Column("misto_realizace_nazev_nuts_3", Text, nullable=False),
        Column("oblast_intervence_kod", Text, nullable=True),
        Column("oblast_intervence_nazev", Text, nullable=True),
        Column("mira_spolufinancovani_ze_strany_unie", Numeric(3, 2), nullable=False),
        Column("celkove_naklady_na_operaci_czk", Numeric(16, 2), nullable=False),
        Column(
            "financni_prostredky_v_pravnich_aktech_celkove_zpusobile_vydaje_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_v_pravnich_aktech_prispevek_unie_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_v_pravnich_aktech_narodni_verejne_zdroje_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_v_pravnich_aktech_narodni_"
            "soukrome_zdroje_soukrome_zdroje_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_vyuctovane_v_zadostech_o_platbu_"
            "celkove_zpusobile_vydaje_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_vyuctovane_v_zadostech_o_platbu_prispevek_unie_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_vyuctovane_v_zadostech_o_platbu_"
            "narodni_verejne_zdroje_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "financni_prostredky_vyuctovane_v_zadostech_o_platbu_"
            "narodni_soukrome_zdroje_soukrome_zdroje_czk",
            Numeric(16, 2),
            nullable=True,
        ),
        Column("poradi_verejne_zakazky", Integer, nullable=False),
        Column("nazev_verejne_zakazky", Text, nullable=True),
        Column("stav_verejne_zakazky", Text, nullable=True),
        Column("typ_verejne_zakazky", Text, nullable=True),
        Column("nazev_dodavatele_verejne_zakazky", Text, nullable=True),
        Column("ic_dodavatele_verejne_zakazky", Integer, nullable=True),
        Column("poddodavatel", Text, nullable=False),
        Column("datum_zahajeni_zadavaciho_vyberoveho_rizeni", Date, nullable=True),
        Column("datum_podpisu_smlouvy_dodatku", Date, nullable=True),
        Column(
            "predpokladana_hodnota_verejne_zakazky_bez_dph",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "cena_verejne_zakazky_podle_smlouvy_dodatlu_bez_dph",
            Numeric(16, 2),
            nullable=True,
        ),
        Column(
            "skutecne_uhrazena_cena_vazici_se_k_projektu_bez_dph",
            Numeric(16, 2),
            nullable=True,
        ),
    ),
]

if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
