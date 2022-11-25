from sqlalchemy import Column, ForeignKey, MetaData, Table
from sqlalchemy.sql.sqltypes import (
    Boolean,
    Date,
    DateTime,
    Integer,
    SmallInteger,
    String,
    Text,
    Time,
)

meta = MetaData()

schema = [
    Table(
        "poslanci_typ_organu",
        meta,
        Column(
            "id_typ_org",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor typu orgánu",
        ),
        Column(
            "typ_id_typ_org",
            SmallInteger,
            nullable=True,
            comment="Identifikátor nadřazeného typu orgánu "
            "(typ_organu:id_typ_org), pokud je ",
        ),
        Column(
            "nazev_typ_org_cz",
            Text,
            nullable=False,
            comment="Název typu orgánu v češtině",
        ),
        Column(
            "nazev_typ_org_en",
            Text,
            nullable=True,
            comment="Název typu orgánu v angličtině",
        ),
        Column(
            "typ_org_obecny",
            SmallInteger,
            nullable=True,
            comment="Obecný typ orgánu, pokud je vyplněný, odpovídá záznamu v "
            "typ_organu:id_typ_org. Pomocí tohoto sloupce lze najít např. všechny "
            "výbory v různých typech zastupitelských sborů.",
        ),
        Column("priorita", SmallInteger, nullable=True, comment="Priorita při výpisu"),
    ),
    Table(
        "poslanci_typ_funkce",
        meta,
        Column(
            "id_typ_funkce",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor typu funkce",
        ),
        Column(
            "id_typ_org",
            ForeignKey("poslanci_typ_organu.id_typ_org"),
            nullable=False,
            comment="Identifikátor typu orgánu, viz typ_organu:id_typ_org",
        ),
        Column(
            "typ_funkce_cz", Text, nullable=False, comment="Název typu funkce v češtině"
        ),
        Column(
            "typ_funkce_en",
            Text,
            nullable=True,
            comment="Název typu funkce v angličtině",
        ),
        Column("priorita", SmallInteger, nullable=False, comment="Priorita při výpisu"),
        Column(
            "typ_funkce_obecny",
            SmallInteger,
            nullable=True,
            comment="Obecný typ funkce, 1 - předseda, 2 - místopředseda, "
            "3 - ověřovatel, jiné hodnoty se nepoužívají.",
        ),
    ),
    Table(
        "poslanci_organy",
        meta,
        Column(
            "id_organ",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor orgánu",
        ),
        Column(
            "organ_id_organ",
            SmallInteger,
            nullable=True,
            comment="Identifikátor nadřazeného orgánu, viz organy:id_organ",
        ),
        Column(
            "id_typ_organu",
            SmallInteger,
            nullable=False,
            comment="Typ orgánu, viz typ_organu:id_typ_organu",
        ),
        Column(
            "zkratka",
            Text,
            nullable=False,
            comment="Zkratka orgánu, bez diakritiky, v některých připadech "
            "se zkratka při zobrazení nahrazuje jiným názvem",
        ),
        Column(
            "nazev_organu_cz", Text, nullable=False, comment="Název orgánu v češtině"
        ),
        Column(
            "nazev_organu_en", Text, nullable=True, comment="Název orgánu v angličtině"
        ),
        Column("od_organ", Date, nullable=True, comment="Ustavení orgánu"),
        Column("do_organ", Date, nullable=True, comment="Ukončení orgánu"),
        Column(
            "priorita", SmallInteger, nullable=True, comment="Priorita výpisu orgánů"
        ),
        Column(
            "cl_organ_base",
            Boolean,
            nullable=True,
            comment="Pokud je nastaveno na 1, pak při výpisu členů se nezobrazují "
            "záznamy v tabulkce zarazeni kde cl_funkce == 0. Toto chování odpovídá "
            "tomu, že v některých orgánech nejsou členové a teprve z nich se volí "
            "funkcionáři, ale přímo se volí do určité funkce.",
        ),
    ),
    Table(
        "poslanci_funkce",
        meta,
        Column(
            "id_funkce",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor funkce, používá se v zarazeni:id_fo",
        ),
        Column(
            "id_organ",
            ForeignKey("poslanci_organy.id_organ"),
            nullable=False,
            comment="Identifikátor orgánu, viz organy:id_organ",
        ),
        Column(
            "id_typ_funkce",
            ForeignKey("poslanci_typ_funkce.id_typ_funkce"),
            nullable=False,
            comment="Typ funkce, viz typ_funkce:id_typ_funkce",
        ),
        Column(
            "nazev_funkce_cz",
            Text,
            nullable=False,
            comment="Název funkce, pouze pro interní použití",
        ),
        Column("priorita", SmallInteger, nullable=False, comment="Priorita výpisu"),
    ),
    Table(
        "poslanci_osoby",
        meta,
        Column(
            "id_osoba",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor osoby",
        ),
        Column("pred", Text, nullable=True, comment="Titul pred jmenem"),
        Column(
            "prijmeni",
            Text,
            nullable=False,
            comment="Příjmení, v některých případech obsahuje i dodatek "
            'typu "st.", "ml."',
        ),
        Column("jmeno", Text, nullable=False, comment="Jméno"),
        Column("za", Text, nullable=True, comment="Titul za jménem"),
        Column("narozeni", Date, nullable=True, comment="Datum narození"),
        Column(
            "pohlavi",
            String(1),
            nullable=False,
            comment='Pohlaví, "M" jako muž, ostatní hodnoty žena',
        ),
        Column("zmena", Date, nullable=True, comment="Datum posledni změny"),
        Column("umrti", Date, nullable=True, comment="Datum úmrtí"),
    ),
    Table(
        "poslanci_zarazeni",
        meta,
        Column(
            "id_osoba",
            SmallInteger,
            nullable=False,
            comment="Identifikátor osoby, viz osoba:id_osoba",
        ),
        Column(
            "id_of",
            SmallInteger,
            nullable=False,
            comment="Identifikátor orgánu či funkce: pokud je zároveň nastaveno "
            "zarazeni:cl_funkce == 0, pak id_o odpovídá organy:id_organ, "
            "pokud cl_funkce == 1, pak odpovídá funkce:id_funkce.",
        ),
        Column(
            "cl_funkce",
            Boolean,
            nullable=False,
            comment="Status členství nebo funce: pokud je rovno 0, pak jde o "
            "členství, pokud 1, pak jde o funkci.",
        ),
        Column("od_o", DateTime, nullable=False, comment="Zařazení "),
        Column("do_o", DateTime, nullable=True, comment="Zařazení "),
        Column("od_f", Date, nullable=True, comment="Mandát "),
        Column("do_f", Date, nullable=True, comment="Mandát"),
    ),
    Table(
        "poslanci_poslanec",
        meta,
        Column(
            "id_poslanec",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor poslance",
        ),
        Column(
            "id_osoba",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Identifikátor osoby, viz osoba:id_osoba",
        ),
        Column(
            "id_kraj",
            SmallInteger,
            nullable=False,
            comment="Volební kraj, viz organy:id_organu",
        ),
        Column(
            "id_kandidatka",
            SmallInteger,
            nullable=False,
            comment="Volební strana/hnutí, viz org:id_organu, pouze odkazuje na "
            "stranu/hnutí, za kterou byl zvolen a nemusí mít souvislost s "
            "členstvím v poslaneckém klubu.",
        ),
        Column(
            "id_obdobi",
            SmallInteger,
            nullable=False,
            comment="Volební období, viz organy:id_organu",
        ),
        Column("web", Text, nullable=True, comment="URL vlastních stránek poslance"),
        Column(
            "ulice", Text, nullable=True, comment="Adresa regionální kanceláře, ulice."
        ),
        Column(
            "obec", Text, nullable=True, comment="Adresa regionální kanceláře, obec."
        ),
        Column("psc", Text, nullable=True, comment="Adresa regionální kanceláře, PSČ."),
        Column(
            "email",
            Text,
            nullable=False,
            comment="E-mailová adresa poslance, případně obecná posta@psp.cz.",
        ),
        Column(
            "telefon",
            Text,
            nullable=True,
            comment="Adresa regionální kanceláře, telefon.",
        ),
        Column("fax", Text, nullable=True, comment="Adresa regionální kanceláře, fax."),
        Column(
            "psp_telefon",
            Text,
            nullable=True,
            comment="Telefonní číslo do kanceláře v budovách PS.",
        ),
        Column("facebook", Text, nullable=True, comment="URL stránky služby Facebook."),
        Column(
            "foto",
            Boolean,
            nullable=True,
            comment="Pokud je rovno 1, pak existuje fotografie poslance.",
        ),
    ),
    Table(
        "poslanci_pkgps",
        meta,
        Column(
            "id_poslanec",
            ForeignKey("poslanci_poslanec.id_poslanec"),
            nullable=False,
            unique=True,
            comment="Identifikátor poslance, viz poslanec:id_poslanec",
        ),
        Column(
            "adresa",
            Text,
            nullable=False,
            comment="Adresa kanceláře, jednotlivé položky jsou odděleny středníkem",
        ),
        Column(
            "sirka",
            Text,
            nullable=False,
            comment="Severní šířka, WGS 84, formát GG.AABBCCC, GG = stupně, "
            "AA - minuty, BB - vteřiny, CCC - tisíciny vteřin",
        ),
        Column(
            "delka",
            Text,
            nullable=False,
            comment="Východní délka, WGS 84, formát GG.AABBCCC, GG = stupně, "
            "AA - minuty, BB - vteřiny, CCC - tisíciny vteřin",
        ),
    ),
    Table(
        "poslanci_osoba_extra",
        meta,
        Column(
            "id_osoba",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Identifikátor osoby, viz osoba:id_osoba",
        ),
        Column(
            "id_org",
            SmallInteger,
            nullable=False,
            comment="Identifikátor orgánu, viz org:id_org",
        ),
        Column("typ", SmallInteger, nullable=False, comment="Typ záznamu, viz výše."),
        Column(
            "obvod",
            SmallInteger,
            nullable=False,
            comment="Je-li typ = 1, pak jde o číslo senátního obvodu",
        ),
        Column(
            "strana",
            Text,
            nullable=False,
            comment="Je-li typ = 1, pak jde o název volební strany/hnutí či "
            "označení nezávislého kandidáta",
        ),
        Column(
            "id_external",
            SmallInteger,
            nullable=False,
            comment="Je-li typ = 1, pak je to identifikátor senátora na senat.cz",
        ),
    ),
    Table(
        "hlasovani_hl_hlasovani",
        meta,
        Column(
            "id_hlasovani",
            Integer,
            nullable=False,
            unique=True,
            comment="Identifikátor hlasování",
        ),
        Column(
            "id_organ",
            ForeignKey("poslanci_organy.id_organ"),
            nullable=False,
            comment="Identifikátor orgánu, viz organy:id_organ",
        ),
        Column("schuze", SmallInteger, nullable=False, comment="Číslo schůze"),
        Column("cislo", SmallInteger, nullable=False, comment="Číslo hlasování"),
        Column(
            "bod",
            SmallInteger,
            nullable=True,
            comment="Bod pořadu schůze; je-li menší než 1, pak jde o procedurální "
            "hlasování nebo o hlasování k bodům, které v době hlasování "
            "neměly přiděleno číslo.",
        ),
        Column("datum", Date, nullable=False, comment="Datum hlasování"),
        Column("čas", Time, nullable=False, comment="Čas hlasování"),
        Column("pro", SmallInteger, nullable=False, comment="Počet hlasujících pro"),
        Column(
            "proti", SmallInteger, nullable=False, comment="Počet hlasujících proti"
        ),
        Column(
            "zdrzel",
            SmallInteger,
            nullable=False,
            comment="Počet hlasujících zdržel se, tj. stiskl tlačítko X",
        ),
        Column(
            "nehlasoval",
            SmallInteger,
            nullable=True,
            comment="Počet přihlášených, kteří nestiskli žádné tlačítko",
        ),
        Column(
            "prihlaseno",
            SmallInteger,
            nullable=False,
            comment="Počet přihlášených poslanců",
        ),
        Column(
            "kvorum",
            SmallInteger,
            nullable=False,
            comment="Kvórum, nejmenší počet hlasů k přijetí návrhu",
        ),
        Column(
            "druh_hlasovani",
            String(1),
            nullable=False,
            comment="Druh hlasování: N - normální, R - ruční (nejsou známy "
            "hlasování jednotlivých poslanců)",
        ),
        Column(
            "vysledek",
            String(1),
            nullable=False,
            comment="Výsledek: A - přijato, R - zamítnuto, jinak zmatečné hlasování",
        ),
        Column(
            "nazev_dlouhy", Text, nullable=True, comment="Dlouhý název bodu hlasování"
        ),
        Column(
            "nazev_kratky", Text, nullable=True, comment="Krátký název bodu hlasování"
        ),
    ),
    Table(
        "hlasovani_hl_poslanec",
        meta,
        Column(
            "id_poslanec",
            ForeignKey("poslanci_poslanec.id_poslanec"),
            nullable=False,
            comment="Identifikátor poslance, viz poslanec:id_poslanec",
        ),
        Column(
            "id_hlasovani",
            ForeignKey("hlasovani_hl_hlasovani.id_hlasovani"),
            nullable=False,
            comment="Identifikátor hlasování, viz hl_hlasovani:id_hlasovani",
        ),
        Column(
            "vysledek",
            String(1),
            nullable=False,
            comment="Hlasování jednotlivého poslance. A - ano, B nebo N - ne, "
            "C - zdržel se (stiskl tlačítko X), F - nehlasoval (byl přihlášen, "
            "ale nestiskl žádné tlačítko), @ - nepřihlášen, M - omluven, "
            "W - hlasování před složením slibu poslance, K - zdržel se/nehlasoval. "
            "Viz úvodní vysvětlení zpracování výsledků hlasování.",
        ),
    ),
    Table(
        "hlasovani_omluvy",
        meta,
        Column(
            "id_organ",
            ForeignKey("poslanci_organy.id_organ"),
            nullable=False,
            comment="Identifikátor volebního období, viz organy:id_organ",
        ),
        Column(
            "id_poslanec",
            ForeignKey("poslanci_poslanec.id_poslanec"),
            nullable=False,
            comment="Identifikátor poslance, viz poslanec:id_poslanec",
        ),
        Column("den", Date, nullable=False, comment="Datum omluvy"),
        Column("od", Time, nullable=True, comment="Čas začátku omluvy, pokud je "),
        Column("do", Time, nullable=True, comment="Čas konce omluvy, pokud je "),
    ),
    Table(
        "hlasovani_hl_check",
        meta,
        Column(
            "id_hlasovani",
            ForeignKey("hlasovani_hl_hlasovani.id_hlasovani"),
            nullable=False,
            comment="Identifikátor hlasování, viz hl_hlasovani:id_hlasovani, "
            "které bylo zpochybněno.",
        ),
        Column(
            "turn",
            SmallInteger,
            nullable=False,
            comment="Číslo stenozáznamu, ve kterém je první zmínka o "
            "zpochybnění hlasování.",
        ),
        Column(
            "mode",
            SmallInteger,
            nullable=False,
            comment="Typ zpochybnění: 0 - žádost o opakování hlasování - v tomto "
            "případě se o této žádosti neprodleně hlasuje a teprve je-li tato "
            "žádost přijata, je hlasování opakováno; 1 - pouze sdělení pro "
            "stenozáznam, není požadováno opakování hlasování.",
        ),
        Column(
            "id_h2",
            Integer,
            nullable=True,
            comment="Identifikátor hlasování o žádosti o opakování hlasování, "
            "viz hl_hlasovani:id_hlasovani. Zaznamenává se poslední takové, "
            "které nebylo zpochybněno.",
        ),
        Column(
            "id_h3",
            Integer,
            nullable=True,
            comment="Identifikátor opakovaného hlasování, viz "
            "hl_hlasovani:id_hlasovani a hl_check:id_hlasovani. "
            "Zaznamenává se poslední takové, které nebylo zpochybněno.",
        ),
    ),
    Table(
        "hlasovani_hl_zposlanec",
        meta,
        Column(
            "id_hlasovani",
            Integer,
            nullable=False,
            comment="Identifikátor hlasování, viz hl_hlasovani:id_hlasovani a "
            "hl_check:id_hlasovani, které bylo zpochybněno.",
        ),
        Column(
            "id_osoba",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Identifikátor poslance, který zpochybnil hlasování; "
            "viz osoby:id_osoba.",
        ),
        Column(
            "mode",
            SmallInteger,
            nullable=False,
            comment="Typ zpochybnění, viz hl_check:mode.",
        ),
    ),
    Table(
        "hlasovani_hl_vazby",
        meta,
        Column(
            "id_hlasovani",
            Integer,
            nullable=False,
            comment="Identifikátor hlasování, viz hl_hlasovani:id_hlasovani",
        ),
        Column("turn", SmallInteger, nullable=False, comment="Číslo stenozáznamu"),
        Column(
            "typ",
            SmallInteger,
            nullable=False,
            comment="Typ vazby: 0 - hlasování je v textu explicitně zmíněno a "
            "lze tedy vytvořit odkaz přímo na začátek hlasování, 1 - hlasování "
            "není v textu explicitně zmíněno, odkaz lze vytvořit pouze na "
            "stenozáznam jako celek.",
        ),
    ),
    Table(
        "hlasovani_zmatecne",
        meta,
        Column(
            "id_hlasovani",
            Integer,
            nullable=False,
            comment="Identifikátor hlasování, viz hl_hlasovani:id_hlasovani",
        ),
    ),
    Table(
        "tisky_druh_tisku",
        meta,
        Column(
            "id_druh",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor druhu tisku",
        ),
        Column(
            "druh_t",
            String(1),
            nullable=False,
            comment='Typ druhu tisku: T - "hlavní tisk", Z - "následný tisk", '
            "X - historické druhy tisků",
        ),
        Column("nazev_druh", Text, nullable=False, comment="Název druhu tisku"),
    ),
    Table(
        "tisky_typ_zakon",
        meta,
        Column(
            "id_navrh",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor typu navrhovatele",
        ),
        Column(
            "druh_navrhovatele",
            Text,
            nullable=False,
            unique=True,
            comment="Popis typu navrhovatele",
        ),
    ),
    Table(
        "tisky_typ_stavu",
        meta,
        Column(
            "id_typ",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor typu stavu projednávání tisku",
        ),
        Column("popis_stavu", Text, nullable=True, comment="Název typu stavu"),
    ),
    Table(
        "tisky_stavy",
        meta,
        Column(
            "id_stav",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor stavu",
        ),
        Column(
            "id_typ",
            ForeignKey("tisky_typ_stavu.id_typ"),
            nullable=False,
            comment="Typ druhu stavu,typ_stavu:id_typ",
        ),
        Column(
            "id_druh",
            ForeignKey("tisky_druh_tisku.id_druh"),
            nullable=False,
            comment="Typ druhu tisku, druh_tisku:id_druh",
        ),
        Column(
            "popis",
            Text,
            nullable=True,
            comment="Popis stavu, případně informace k dalšímu projednávání",
        ),
        Column(
            "lhuta",
            SmallInteger,
            nullable=True,
            comment="Počet dní k možnému dalšímu postupu v projednávání tisku, "
            "viz stavy:lhuta_where",
        ),
        Column(
            "lhuta_where",
            SmallInteger,
            nullable=True,
            comment="Identifikátor přechodu, od něhož se bude počítat lhůta k "
            "dalšímu možnému postupu v projednávání tisku (viz prechody:id_prechod "
            "a stavy:lhuta). Výpočet není nutno provádět, je prováděn automaticky "
            "u každého tisku, viz tisk:dal. Navíc, pro některé stavy se použijí "
            "speciální vyjímky a lhůta může záviset na více údajích, viz tabulka hist.",
        ),
    ),
    Table(
        "tisky_typ_akce",
        meta,
        Column(
            "id_akce",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor typu přechodu",
        ),
        Column("popis_akce", Text, nullable=False, comment="Název typu přechodu"),
    ),
    Table(
        "tisky_prechody",
        meta,
        Column(
            "id_prechod",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor přechodu",
        ),
        Column(
            "odkud",
            ForeignKey("tisky_stavy.id_stav"),
            nullable=False,
            comment="Výchozí stav, viz stavy:id_stav",
        ),
        Column(
            "kam",
            ForeignKey("tisky_stavy.id_stav"),
            nullable=False,
            comment="Koncový stav, viz stavy:id_stav",
        ),
        Column(
            "id_akce",
            SmallInteger,
            nullable=False,
            comment="Typ akce, viz typ_prechodu:id_akce",
        ),
        Column(
            "typ_prechodu",
            SmallInteger,
            nullable=False,
            comment="Typ přechodu; 1 - dle aktuálního jednacího řádu, 2 - staré "
            "jednací řády, 3 - vyjímky a speciální přechody",
        ),
    ),
    Table(
        "tisky_tisky",
        meta,
        Column(
            "id_tisk",
            Integer,
            nullable=False,
            unique=True,
            comment="Identifikátor tisku",
        ),
        Column(
            "id_druh",
            ForeignKey("tisky_druh_tisku.id_druh"),
            nullable=False,
            comment="Druh tisku, viz druh_tisku:id_druh",
        ),
        Column(
            "id_stav",
            SmallInteger,
            nullable=False,
            comment="Stav tisku, viz stavy:id_stav. Tisk je projednaný, pokud je u "
            "tisky:id_stav = stavy:id_stav a stavy:id_typ == 6, stav tisku odpovídá "
            "výstupnímu stavu posledního přechodu v historii projednávání, "
            "viz tabulka hist.",
        ),
        Column(
            "ct",
            SmallInteger,
            nullable=False,
            comment="Číslo tisku, resp. část reference tisku. Pokud je tisk:id_druh "
            "in (41,45,46,47), pak do reference k číslu tisku patří i -E.",
        ),
        Column(
            "cislo_za",
            SmallInteger,
            nullable=False,
            comment='Číslo "za lomítkem", resp. část reference tisku. Obvykle '
            "je rovno 0, v jiných hodnotách se zpravidla jedná o opravené/přepracované "
            "verze dokumentu. Zobrazuje se u tisků od poloviny 1. volebního období "
            "PS, 1993-1996, viz výše.",
        ),
        Column(
            "id_navrh",
            SmallInteger,
            nullable=True,
            comment="Typ navrhovatele, viz typ_zakon:id_typ, vyplněno pouze "
            "je-li tisky:id_druh = 2 (nevládní návrhy zákonů).",
        ),
        Column(
            "id_org",
            SmallInteger,
            nullable=True,
            comment="Orgán navrhovatele, viz organy:id_org. Vyplněno pouze "
            "pokud navrhovatelem je instituce či orgán.",
        ),
        Column(
            "id_org_obd",
            SmallInteger,
            nullable=False,
            comment="Volební období, viz organy:id_org.",
        ),
        Column(
            "id_osoba",
            Integer,
            nullable=True,
            comment="Navrhovatel či jeho zástupce, viz osoba:id_osoba. Pokud je více "
            "navrhovatelů, pak záznamy o nich jsou uloženy v tabulce predkladatel.",
        ),
        Column(
            "navrhovatel",
            Text,
            nullable=True,
            comment="Textový popis navrhovatele. Používá se k doplnění navrhovatele, "
            "resp. jeho zástupce, který vychází z typu tisku a druhu navrhovatele, "
            "viz tisky:id_druh a tisky:id_navrh, případně u skupiny poslanců ze "
            "seznamu předkladatelů, viz tabulka predkladatel.",
        ),
        Column(
            "nazev_tisku",
            Text,
            nullable=False,
            comment="Zkrácený název sněmovního tisku.",
        ),
        Column(
            "predlozeno", DateTime, nullable=True, comment="Datum předložení tisku."
        ),
        Column(
            "rozeslano",
            DateTime,
            nullable=True,
            comment="Datum rozeslání tisku poslancům. Od prosince 2011 se používá "
            "tisky:roz (určení rozeslání poslancům v elektronické verzi s "
            "přesností na minuty).",
        ),
        Column(
            "dal",
            DateTime,
            nullable=True,
            comment="Pokud je vyplněno, určuje nejbližší možný začátek dalšího "
            "projednávání tisku, jak plyne z lhůt jednacího řádu, "
            "viz např. tabulka stavy.",
        ),
        Column(
            "tech_nos_dat",
            Date,
            nullable=True,
            comment="Datum zpřístupnění elektronické verze sněmovního tisku, "
            "od prosince 2011 nepoužíváno.",
        ),
        Column(
            "uplny_nazev_tisku",
            Text,
            nullable=True,
            comment="Úplný název sněmovního tisku, X > 1340.",
        ),
        Column(
            "zm_lhuty",
            Text,
            nullable=True,
            comment="Příznak změny lhůty k projednání výbory. 1 - zkrácení, "
            "2 - prodloužení, viz též tisky:lhuta.",
        ),
        Column(
            "lhuta",
            SmallInteger,
            nullable=True,
            comment="Změna lhůty k projednání výbory, viz tisky:zm_lhuty.",
        ),
        Column(
            "rj",
            Boolean,
            nullable=True,
            comment="Příznak navržení k projednání dle paragrafu 90, odst. 2 "
            '("rychlé jednání"), které navrhuje předkladatel a Sněmovna to '
            "potvrzuje v prvém čtení. V bodech pořadu schůze je tento příznak "
            "v případech potřeby zkopírován, viz tabulka i_bod_schuze.",
        ),
        Column(
            "t_url",
            Text,
            nullable=True,
            comment="URL k textu sněmovního tisku, pokud není vyplněno, "
            "vytváří se dle vzoru.",
        ),
        Column(
            "is_eu",
            Boolean,
            nullable=True,
            comment="Příznak vztahu sněmovního tisku k členství v EU.",
        ),
        Column(
            "roz",
            DateTime,
            nullable=True,
            comment="Datum rozeslání sněmovního tisku, používáno od prosince 2011. "
            "Rozesláním se rozumí zveřejněním v elektronické podobě.",
        ),
        Column(
            "is_sdv",
            Boolean,
            nullable=True,
            comment="Příznak spojení projednávání sněmovního tisku s důvěrou vládě.",
        ),
        Column(
            "status",
            SmallInteger,
            nullable=True,
            comment="Pokud je vyplněno, pak uchovává status sněmovního tisku; "
            "1 nebo 2: revokováno.",
        ),
    ),
    Table(
        "tisky_hist",
        meta,
        Column(
            "id_hist",
            Integer,
            nullable=False,
            unique=True,
            comment="Identifikátor kroku v historii projednávání",
        ),
        Column(
            "id_tisk",
            Integer,  # nemuzem pouzit FK, protoze nektery tisky nejsou v tisky.tisky
            nullable=False,
            comment="Identifikátor sněmovního tisku, viz tisky:id_tisk",
        ),
        Column(
            "datum",
            DateTime,
            nullable=True,
            comment="Datum a čas kroku; pokud je údaj hodina roven nule, pak se "
            "zobrazuje pouze den, bez časové specifikace.",
        ),
        Column(
            "id_hlas",
            ForeignKey("hlasovani_hl_hlasovani.id_hlasovani"),
            nullable=True,
            comment="Identifikátor hlasování, viz hl_hlasovani:id_hlasovani",
        ),
        Column(
            "id_prechod",
            ForeignKey("tisky_prechody.id_prechod"),
            nullable=False,
            comment="Identifikátor přechodu, viz prechody:id_prechod",
        ),
        Column(
            "id_bod",
            Integer,
            nullable=True,
            comment="Identifikátor bodu pořadu schůze, viz i_bod_schuze:id_bod, "
            "kde i_bod_schuze:pozvanka is null.",
        ),
        Column(
            "schuze",
            SmallInteger,
            nullable=True,
            comment="Číslo schůze, na které bylo projednáváno.",
        ),
        Column("usnes_ps", SmallInteger, nullable=True, comment="Číslo usnesení PS."),
        Column(
            "orgv_id_posl",
            ForeignKey("poslanci_poslanec.id_poslanec"),
            nullable=True,
            comment="Zpravodaj k tisku určený organizačním výborem, viz "
            "poslanec:id_poslanec.",
        ),
        Column(
            "ps_id_posl",
            ForeignKey("poslanci_poslanec.id_poslanec"),
            nullable=True,
            comment="Zpravodaj k tisku určený předsedou sněmovny, viz "
            "poslanec:id_poslanec.",
        ),
        Column(
            "orgv_p_usn",
            SmallInteger,
            nullable=True,
            comment="Číslo usnesení organizačního výboru nebo číslo "
            "rozhodnutí předsedy sněmovny.",
        ),
        Column(
            "zaver_publik",
            Date,
            nullable=True,
            comment="Datum vydání Sbírky, viz další.",
        ),
        Column(
            "zaver_sb_castka",
            SmallInteger,
            nullable=True,
            comment="Číslo částky Sbírky.",
        ),
        Column(
            "zaver_sb_cislo",
            Text,
            nullable=True,
            comment="Čislo ve Sbírce, číslo za lomítkem se vezme jako část "
            "rok z hist:datum.",
        ),
        Column("poznamka", Text, nullable=True, comment="Poznámka ke kroku."),
    ),
    Table(
        "tisky_hist_vybory",
        meta,
        Column(
            "id_tisku",
            ForeignKey("tisky_tisky.id_tisk"),
            nullable=False,
            comment="Identifikátor tisku, viz tisky:id_tisk",
        ),
        Column(
            "id_organ",
            ForeignKey("poslanci_organy.id_organ"),
            nullable=False,
            comment="Identifikátor orgánu, viz organ:id_organ",
        ),
        Column(
            "typ",
            SmallInteger,
            nullable=False,
            comment="Typ vazby: 1 - navrženo k přikázání, 2 - přikázáno, "
            "3 - projednáno iniciativně",
        ),
        Column(
            "id_hist",
            ForeignKey("tisky_hist.id_hist"),
            nullable=False,
            comment="Identifikátor kroku, viz hist:id_hist, ke kterému se "
            "přikázání vztahují.",
        ),
        Column(
            "id_posl",
            Integer,  # nejde pouzit FK, protoze jsou tu nesmysly
            nullable=True,
            comment="Identifikátor zpravodaje výboru k tisku, viz poslanec:id_poslanec",
        ),
        Column("poradi", SmallInteger, nullable=True, comment="Pořadí orgánů"),
    ),
    Table(
        "tisky_vysledek",
        meta,
        Column(
            "id_vysledek",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor druhu výsledku",
        ),
        Column(
            "druh_vysledek",
            Text,
            nullable=False,
            unique=True,
            comment="Popis druhu výsledku",
        ),
    ),
    Table(
        "tisky_tisky_za",
        meta,
        Column(
            "id_tisk",
            ForeignKey("tisky_tisky.id_tisk"),
            nullable=False,
            comment="Identifikátor sněmovního tisku, viz tisky:id_tisk",
        ),
        Column(
            "cislo_za",
            SmallInteger,
            nullable=False,
            comment='"Číslo za lomítkem" v referenci sněmovního tisku. Pokud je '
            "menší než nula, pak se pro zápis použije: -1 = Z, -2 = Z1, -3 = Z2. "
            "Viz též tisky_za:cislo_za_post.",
        ),
        Column(
            "id_hist",
            Integer,
            nullable=False,
            comment="Identifikátor kroku projednávání tisku, ke kterému se tisk "
            "vztahuje nebo po kterém byl tisk rozeslán, viz hist:id_hist a "
            "případně hist_vybory:id_hist",
        ),
        Column(
            "id_druh",
            ForeignKey("tisky_druh_tisku.id_druh"),
            nullable=False,
            comment="Typ sněmovního tisku, viz druh_tisku:id_druh",
        ),
        Column(
            "nazev_za",
            Text,
            nullable=False,
            comment="Zkrácený název tisku, obvykle je tvořen pomocí šablony.",
        ),
        Column(
            "uplny_nazev_za",
            Text,
            nullable=False,
            comment="Úplný název tisku, X > 1340.",
        ),
        Column(
            "rozeslano",
            DateTime,
            nullable=True,
            comment="Čas rozeslání sněmovního tisku, od prosince 2011 se používá "
            "tisky_za:roz, podobně jako tisky:roz.",
        ),
        Column(
            "id_org",
            SmallInteger,
            nullable=True,
            comment="Identifikátor orgnánu původce tisku, viz organy:id_organ a "
            "případně hist_vybory:id_org",
        ),
        Column(
            "usn_vybor",
            SmallInteger,
            nullable=True,
            comment="Číslo usnesení orgánu (výboru, komise), které tvoří sněmovní tisk",
        ),
        Column(
            "id_posl",
            ForeignKey("poslanci_poslanec.id_poslanec"),
            nullable=True,
            comment="Identifikátor zpravodaje k tisku, viz poslanec:id_poslanec",
        ),
        Column(
            "t_url",
            Text,
            nullable=True,
            comment="URL k dokumentu tisku, pokud není uvededno, pak se URL "
            "vytvoří pomocí šablony.",
        ),
        Column(
            "id_vysledek",
            ForeignKey("tisky_vysledek.id_vysledek"),
            nullable=True,
            comment="Identifikátor druhu výsledku, viz vysledek:id_vysledek, pouze "
            "pro určité druhy sněmovního tisku",
        ),
        Column(
            "cislo_za_post",
            SmallInteger,
            nullable=True,
            comment="Část reference sněmovního tisku, pokud je vyplněno, použije se "
            'za "číslo za lomítkem": 1 = a (tj. reference pak může být 123/1a).',
        ),
        Column(
            "sort_it",
            SmallInteger,
            nullable=True,
            comment="Pořadí sněmovního tisku v řadě následných tisků: následné tisky "
            "by se měly ve výpisu řadit nejdříve podle tisky_za:sort_it, pak podle "
            "tisky_za:cislo_za a podle tisky_za:cislo_za_post",
        ),
        Column(
            "roz",
            DateTime,
            nullable=True,
            comment="Čas rozeslání tisku, používáno od prosince 2011.",
        ),
        Column(
            "status",
            SmallInteger,
            nullable=True,
            comment="Stav sněmovního tisku, popis viz tisky:status.",
        ),
    ),
    Table(
        "tisky_predkladatel",
        meta,
        Column(
            "id_tisk",
            Integer,  # opet nejde pouzit FK
            nullable=False,
            comment="Identifikátor sněmovního tisku, viz tisky:id_tisk",
        ),
        Column(
            "id_osoba",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Předkladatel nebo jeho zástupce, viz osoba:id_osoba.",
        ),
        Column(
            "poradi", SmallInteger, nullable=False, comment="Pořadí osoby v seznamu."
        ),
        Column(
            "typ",
            SmallInteger,
            nullable=False,
            comment="Typ záznamu: 0 - předkladatel, 1 - jako předkladatel se "
            "připojil později.",
        ),
    ),
    Table(
        "tisky_navrh_podpis",
        meta,
        Column(
            "id_tisk",
            ForeignKey("tisky_tisky.id_tisk"),
            nullable=False,
            comment="Identifikátor sněmovního tisku, viz tisky:id_tisk",
        ),
        Column(
            "id_osoba",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Předkladatel nebo jeho zástupce, viz osoba:id_osoba.",
        ),
        Column(
            "stav",
            SmallInteger,
            nullable=False,
            comment="Typ záznamu: 1 - připojil podpis, 10 - vzal podpis zpět.",
        ),
        Column("datum", Date, nullable=False, comment="Datum záznamu."),
    ),
    Table(
        "interp_uitypv",
        meta,
        Column(
            "id_ui_stav",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor typu výsledku projednávání ústní interpelace",
        ),
        Column(
            "nazev",
            Text,
            nullable=False,
            unique=True,
            comment="Název typu výsledku ústní interpelace",
        ),
        Column(
            "priorita",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Priorita výpisu typu výsledku",
        ),
    ),
    Table(
        "interp_los_interpelaci",
        meta,
        Column(
            "id_los",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor losování interpelací.",
        ),
        Column(
            "datum_los",
            Date,
            nullable=False,
            comment="Datum interpelací. Změnou jednacího řádu se losování interpelací "
            "přesunulo ze začátku schůze na den projednávání interpelací a "
            "tak tento datum již není používán.",
        ),
        Column(
            "typ_los",
            String(1),
            nullable=False,
            comment='Typ interpelací: "M" - na členy vlády, "P" - na předsedu vlády. '
            "Interpelace se projednávají v pořadí na předsedu vlády a "
            "pak na členy vlády.",
        ),
        Column(
            "cas_los",
            DateTime,
            nullable=True,
            comment="Čas losování interpelací, v současné době též "
            "datum projednávání interpelací.",
        ),
        Column(
            "id_schuze",
            SmallInteger,
            nullable=False,
            comment="Identifikátor schůze, viz i_schuze:id_schuze.",
        ),
        Column(
            "id_bod",
            Integer,
            nullable=False,
            comment="Identifikátor bodu schůze, viz i_bod_schuze:id_bod.",
        ),
        Column(
            "schuze",
            SmallInteger,
            nullable=False,
            comment="Číslo schůze, odvozeno od id_schuze.",
        ),
        Column(
            "id_org",
            ForeignKey("poslanci_organy.id_organ"),
            nullable=False,
            comment="Identifikátor volebního období, viz organy:id_org.",
        ),
    ),
    Table(
        "interp_poradi",
        meta,
        Column(
            "id_poradi",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor pořadí interpelací.",
        ),
        Column(
            "id_losovani",
            ForeignKey("interp_los_interpelaci.id_los"),
            nullable=False,
            comment="Identifikátor losování interpelací, viz los_interpelaci:id_los.",
        ),
        Column(
            "id_poslanec",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Identifikátor poslance, viz osoba:id_osoba.",
        ),
        Column(
            "id_ministr",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=False,
            comment="Identifikátor člena vlády, viz osoba:id_osoba.",
        ),
        Column("vec", Text, nullable=False, comment="Téma interpelace."),
        Column(
            "poradi_l",
            SmallInteger,
            nullable=False,
            comment="Pořadí interpelace, dáno losováním. V současné době se "
            "losují interpelace po skupinách dle priorit, viz poradi:priorita.",
        ),
        Column(
            "priorita",
            SmallInteger,
            nullable=True,
            comment="Priorita interpelace daná interpelovaným: před losováním "
            "interpelací označí interpelovaný prioritu interpelace a interpelace "
            "se pak losují postupně ve skupinách podle priorit, tak, aby se "
            "zamezilo stavu, kdy interpelace jednoho poslance by následovaly za sebou.",
        ),
        Column(
            "vec32", Text, nullable=True, comment="Zkrácený popis tématu interpelace."
        ),
    ),
    Table(
        "interp_ui_stav",
        meta,
        Column(
            "id_poradi",
            ForeignKey("interp_poradi.id_poradi"),
            nullable=False,
            unique=True,
            comment="Identifikátor přihlášky k interpelaci, viz poradi:id_poradi.",
        ),
        Column(
            "id_typ",
            ForeignKey("interp_uitypv.id_ui_stav"),
            nullable=False,
            comment="Typ výsledku projednávání interpelace, viz uitypv:id_ui_stav.",
        ),
        Column(
            "steno",
            SmallInteger,
            nullable=True,
            comment="Číslo stenozáznamu, ve kterém bylo zahájeno projednávání "
            "interpelace, pokud je větší než nula, viz vytváření odkazů na zdroje PS.",
        ),
    ),
    Table(
        "schuze_schuze",
        meta,
        Column(
            "id_schuze",
            SmallInteger,
            nullable=False,
            comment="Identifikátor schůze, není to primární klíč, je nutno "
            "používat i položku schuze:pozvanka. Záznamy schůzí stejného "
            "orgánu a stejného čísla (tj. schuze:id_org a schuze:schuze), "
            "mají stejné schuze:id_schuze a liší se pouze v schuze:pozvanka.",
        ),
        Column(
            "id_org",
            ForeignKey("poslanci_organy.id_organ"),
            nullable=False,
            comment="Identifikátor orgánu, viz org:id_org.",
        ),
        Column("schuze", SmallInteger, nullable=False, comment="Číslo schůze."),
        Column(
            "od_schuze",
            DateTime,
            nullable=False,
            comment="Předpokládaný začátek schůze; viz též tabulka schuze_stav",
        ),
        Column(
            "do_schuze",
            DateTime,
            nullable=True,
            comment="Konec schůze. V případě schuze:pozvanka == 1 se nevyplňuje.",
        ),
        Column(
            "aktualizace",
            DateTime,
            nullable=False,
            comment="Datum a čas poslední aktualizace.",
        ),
        Column(
            "pozvanka",
            SmallInteger,
            nullable=True,
            comment="Druh záznamu: null - schválený pořad, 1 - navržený pořad.",
        ),
    ),
    Table(
        "schuze_schuze_stav",
        meta,
        Column(
            "id_schuze",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor schůze, viz schuze:id_schuze.",
        ),
        Column(
            "stav",
            SmallInteger,
            nullable=False,
            comment="Stav schůze: 1 - OK, 2 - pořad schůze nebyl schválen "
            "a schůze byla ukončena.",
        ),
        Column(
            "typ",
            SmallInteger,
            nullable=True,
            comment="Typ schůze: 1 - řádná, 2 - mimořádná (navržená skupinou "
            "poslanců). Dle jednacího řádu nelze měnit navržený pořad "
            "mimořádné schůze.",
        ),
        Column(
            "text_dt",
            Text,
            nullable=True,
            comment="Zvláštní určení začátku schůze: pokud je vyplněno, "
            "použije se namísto schuze:od_schuze.",
        ),
        Column(
            "text_st",
            Text,
            nullable=True,
            comment="Text stavu schůze, obvykle informace o přerušení.",
        ),
        Column(
            "tm_line",
            Text,
            nullable=True,
            comment="Podobné jako schuze_stav:text_st, pouze psáno na začátku "
            "s velkým písmenem a ukončeno tečkou.",
        ),
    ),
    Table(
        "schuze_bod_stav",
        meta,
        Column(
            "id_bod_stav",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Typ stavu bodu schůze: typ 3 - neprojednatelný znamená vyřazen "
            "z pořadu či neprojednatelný z důvodu legislativního procesu.",
        ),
        Column("popis", Text, nullable=False, unique=True, comment="Popis stavu bodu."),
    ),
    Table(
        "schuze_bod_schuze",
        meta,
        Column(
            "id_bod",
            Integer,
            nullable=False,
            comment="Identifikátor bodu pořadu schůze, není to primární klíč, "
            "je nutno používat i položku bod_schuze:pozvanka. Záznamy se stejným "
            "id_bod odkazují na stejný bod, i když číslo bodu může být rozdílné "
            "(během schvalování pořadu schůze se pořadí bodů může změnit).",
        ),
        Column(
            "id_schuze",
            SmallInteger,
            nullable=False,
            comment="Identifikátor schůze, viz schuze:id_schuze a též schuze:pozvanka.",
        ),
        Column(
            "id_tisk",
            ForeignKey("tisky_tisky.id_tisk"),
            nullable=True,
            comment="Identifikátor tisku, pokud se bod k němu vztahuje. "
            "V tomto případě lze využít bod_schuze:uplny_kon.",
        ),
        Column(
            "id_typ",
            SmallInteger,
            nullable=True,
            comment="Typ bodu, resp. typ projednávání. Kromě bod_schuze:id_typ == 6, "
            "se jedná o typ stavu, viz stavy:id_typ a tabulka níže. Je-li "
            "bod_schuze:id_typ == 6, jedná se o jednotlivou odpověď na písemnou "
            "interpelaci a tento záznam se obykle nezobrazuje (navíc má stejné "
            "id_bodu jako bod odpovědi na písemné interpelace a může "
            "mít různé číslo bodu).",
        ),
        Column(
            "bod",
            SmallInteger,
            nullable=False,
            comment="Číslo bodu. Pokud je menší než jedna, pak se při výpisu "
            "číslo bodu nezobrazuje.",
        ),
        Column("uplny_naz", Text, nullable=True, comment="Úplný název bodu."),
        Column(
            "uplny_kon",
            Text,
            nullable=True,
            comment="Koncovka názvu bodu s identifikací čísla tisku nebo čísla "
            "sněmovního dokumentu, pokud jsou používány, viz "
            "bod_schuze:id_tisk a bod_schuze:id_sd.",
        ),
        Column(
            "poznamka",
            Text,
            nullable=True,
            comment="Poznámka k bodu - obvykle obsahuje informaci "
            "o pevném zařazení bodu.",
        ),
        Column(
            "id_bod_stav",
            SmallInteger,
            nullable=False,
            comment="Stav bodu pořadu, viz bod_stav:id_bod_stav. "
            "U bodů návrhu pořadu se nepoužije.",
        ),
        Column(
            "pozvanka",
            SmallInteger,
            nullable=True,
            comment="Rozlišení záznamu, viz schuze:pozvanka",
        ),
        Column(
            "rj",
            SmallInteger,
            nullable=True,
            comment="Režim dle par. 90, odst. 2 jednacího řádu.",
        ),
        Column("pozn2", Text, nullable=True, comment="Poznámka k bodu, zkrácený zápis"),
        Column(
            "druh_bodu",
            SmallInteger,
            nullable=True,
            comment="Druh bodu: 0 nebo null: normální, 1: odpovědi na ústní "
            "interpelace, 2: odpovědi na písemné interpelace, 3: volební bod",
        ),
        Column(
            "id_sd",
            SmallInteger,
            nullable=True,
            comment="Identifikátor sněmovního dokumentu, viz sd_dokument:id_dokument. "
            "Pokud není null, při výpisu se zobrazuje bod_schuze:uplny_kon.",
        ),
        Column(
            "zkratka", Text, nullable=True, comment="Zkrácený název bodu, neoficiální."
        ),
    ),
    Table(
        "steno_steno",
        meta,
        Column(
            "id_steno",
            Integer,
            nullable=False,
            unique=True,
            comment="Identifikátor stenozáznamu",
        ),
        Column(
            "id_org",
            SmallInteger,
            nullable=False,
            comment="Identifikátor orgánu stenozáznamu (v případě PS "
            "je to volební období), viz org:id_org.",
        ),
        Column("schuze", SmallInteger, nullable=False, comment="Číslo schůze."),
        Column(
            "turn",
            SmallInteger,
            nullable=False,
            comment="Číslo stenozáznamu (turn). Pokud číselná řada je neúplná, tj. "
            "obsahuje mezery, pak chybějící obsahují záznam z neveřejného jednání. "
            'V novějších volebních období se i v těchto případech "stenozáznamy" '
            "vytvářejí, ale obsahují pouze informaci o neveřejném jednání.",
        ),
        Column("od_steno", Date, nullable=False, comment="Datum začátku stenozáznamu."),
        Column(
            "jd",
            SmallInteger,
            nullable=False,
            comment="Číslo jednacího dne v rámci schůze (používá se např. při "
            "konstrukci URL na index stenozáznamu dle dnů).",
        ),
        Column(
            "od_t",
            SmallInteger,
            nullable=True,
            comment="Čas začátku stenozáznamu v minutách od začátku kalendářního dne; "
            "pokud je null či menší než nula, není známo. Tj. převod na čas "
            "typu H:M je pomocí H = div(od_t, 60), M = mod(od_t, 60).",
        ),
        Column(
            "do_t",
            SmallInteger,
            nullable=True,
            comment="Čas konce stenozáznamu v minutách od začátku kalendářního dne; "
            "pokud je null či menší než nula, není známo. V některých "
            "případech může být od_t == do_t; v některých případech může "
            "být i od_t > do_t -- platné pouze v případě, že během stena "
            "dojde k změně kalendářního dne (například 23:50 - 00:00).",
        ),
    ),
    Table(
        "steno_steno_bod",
        meta,
        Column(
            "id_steno",
            Integer,
            nullable=False,
            comment="Identifikátor stenozáznamu, viz steno:id_steno.",
        ),
        Column(
            "aname",
            SmallInteger,
            nullable=False,
            comment="Pozice v indexu jednacího dne.",
        ),
        Column(
            "id_bod",
            Integer,
            nullable=False,
            comment="Identifikace bodu pořadu schůze, viz bod_schuze:id_bod. Je-li ",
        ),
    ),
    Table(
        "steno_rec",
        meta,
        Column(
            "id_steno",
            Integer,
            nullable=False,
            comment="Identifikátor stenozáznamu, viz steno:id_steno.",
        ),
        Column(
            "id_osoba",
            Integer,
            nullable=False,
            comment="Identifikátor osoby, viz osoba:id_osoba.",
        ),
        Column(
            "aname",
            SmallInteger,
            nullable=False,
            comment="Identifikace vystoupení v rámci stenozáznamu.",
        ),
        Column(
            "id_bod",
            Integer,
            nullable=True,
            comment="Identifikátor bodu pořadu schůze, viz bod_schuze:id_bod. Je-li ",
        ),
        Column(
            "druh",
            SmallInteger,
            nullable=True,
            comment="Druh vystoupení řečníka: 0 či null - neznámo, 1 - nezpracováno, "
            "2 - předsedající (ověřeno), 3 - řečník (ověřeno), "
            "4 - předsedající, 5 - řečník.",
        ),
    ),
    Table(
        "dokumenty_sd_dokument",
        meta,
        Column(
            "id_dokument",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor sněmovního dokumentu",
        ),
        Column(
            "id_obdobi",
            SmallInteger,
            nullable=False,
            comment="Identifikátor volebního období, viz org:id_org",
        ),
        Column(
            "cislo", SmallInteger, nullable=False, comment="Číslo sněmovního dokumentu"
        ),
        Column(
            "typ",
            SmallInteger,
            nullable=False,
            comment="Typ sněmovního dokumentu, 12 - Podklady pro jednání PS, "
            "13 - Písemné pozměňovací návrhy",
        ),
        Column(
            "nazev",
            Text,
            nullable=True,
            comment="Název sněmovního dokumentu (u některých typů SD se nevyplňuje)",
        ),
        Column(
            "predkladatel",
            Text,
            nullable=True,
            comment="Předkladatel sněmovního dokumentu - textový popis "
            "(u některých typů SD se nevyplňuje)",
        ),
        Column(
            "ct",
            SmallInteger,
            nullable=True,
            comment="Číslo sněmovního tisku, ke kterému se sněmovní dokument vztahuje, "
            "ve stejném volebním období jako sněmovní dokument.",
        ),
        Column(
            "id_x",
            ForeignKey("poslanci_osoby.id_osoba"),
            nullable=True,
            comment="Doplňující informace: je-li typ = 12, pak je obsahem id_osoba "
            "(viz osoba:id_osoba) poslance, který dokument předkládá.",
        ),
        Column(
            "end",
            DateTime,
            nullable=False,
            comment="Ukončení editace sněmovního dokumentu (u některých "
            "typů zároveň čas zveřejnění)",
        ),
    ),
    Table(
        "sbirka_druh_predpisu",
        meta,
        Column(
            "id_dp",
            SmallInteger,
            nullable=False,
            unique=True,
            comment="Identifikátor druhu předpisu.",
        ),
        Column("nazev_druhu", Text, nullable=False, comment="Název druhu předpisu"),
        Column(
            "priorita",
            SmallInteger,
            nullable=True,
            comment="Priorita výpisu druhu předpisu.",
        ),
    ),
    Table(
        "sbirka_sbirka",
        meta,
        Column(
            "id_sbirka",
            SmallInteger,
            nullable=False,
            comment="Identifikátor položky ve Sbírce",
        ),
        Column(
            "cislo", SmallInteger, nullable=False, comment="Číslo položky ve Sbírce"
        ),
        Column("rok", SmallInteger, nullable=False, comment="Rok položky ve Sbírce"),
        Column(
            "id_dp",
            SmallInteger,
            nullable=True,
            comment="Druh předpisu, viz druh_predpisu:id_dp",
        ),
        Column(
            "id_tisk",
            ForeignKey("tisky_tisky.id_tisk"),
            nullable=True,
            comment="Identifikátor tisku, viz tisky:id_tisk; vazba na sněmovní tisk (",
        ),
        Column("datum", Date, nullable=False, comment="Datum vydání ve Sbírce"),
        Column("castka", SmallInteger, nullable=False, comment="Částka Sbírky"),
    ),
    Table(
        "sbirka_sb_pre",
        meta,
        Column(
            "id_tisk",
            Integer,  # opet nemuzem pouzit FK
            nullable=False,
            comment="Identifikátor tisku. Pokud je sb_pre:zdroj = 1, pak se jedná "
            "o sněmovní tisk, viz tisky:id_tisk, pokud zdroj = 2, pak jde o "
            "senátní tisk, viz se_tisk:id_tisk.",
        ),
        Column("cz", SmallInteger, nullable=False, comment=""),
        Column(
            "id_sbirka",
            SmallInteger,
            nullable=True,
            comment="Identifikátor předpisu. Pokud je hodnota ",
        ),
        Column(
            "typ",
            SmallInteger,
            nullable=False,
            comment="Typ změny: 31 - mění předpis, 32 - ruší předpis, 0 - žádná změna",
        ),
        Column(
            "zdroj",
            SmallInteger,
            nullable=False,
            comment="Zdroj tisku: 1 - sněmovní tisk, 2 - senátní tisk",
        ),
        Column(
            "xzdroj",
            SmallInteger,
            nullable=False,
            comment="Zdroj změny: 0 - dokument tisku, 1 - jiný způsob (např. navrženo "
            "v rozpravě, změna nenalezena a další)",
        ),
    ),
]


if __name__ == "__main__":
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    for table in schema:
        print(f"-- {table.name} as created in Postgres")

        print(CreateTable(table).compile(dialect=postgresql.dialect()))
