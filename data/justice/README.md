# Otevřená data Ministerstva spravedlnosti

Ministerstvo spravedlnosti nabízí otevřená data, konkrétně [veřejný rejstřík](https://dataor.justice.cz). Místní skripty mají za cíl tato data zpracovat do relační formy.

- Stačí pustit skript `main.py`, který data stáhne a pomocí schématu (definované v `xml_schema.json`) konvertuje na CSV data.
- Pokud chce člověk data nahrát do PostgreSQL, slouží tomu `schema.py` pro inicializaci tabulek v rámci schématu `justice`. Celé je to ale orchestrované přes rootové `main.py`, tady je automatizován jen export do CSV

Implementační detaily:

- Na portálu MSp není seznam souborů ke stažení, používáme neveřejné API, které seznam souborů obsahuje. Časem by mělo dojít k nápravě.
- Data na webu jsou i v CSV, ale tato CSV jsou prakticky nepoužitelná.

## Zaniklé subjekty

V úplném výpisu jsou jen živé subjekty a pak entity smazané _v daný kalendářní rok_, takže teď (únor 2024) je v datasetech
o mnoho méně dat než bylo v prosinci. Pokud tedy potřebujete historické subjekty, je třeba stáhnout staré exporty.

Tyto exporty jsou nabízené, ale protože tohle je křehká (kvůli kvalitě linky MSp) a pomalá věc, není to default. Defaultně
se berou jen nejnovější exporty, je možné to ovlivnit přes enviromentální proměnnou `CURRENT_YEAR_ONLY=0`. Doporučuju
použít taky `CACHE_ENABLED=1`, abyste nebyli na pospas linkám MSp, ale aby se vám lokálně ukládala data, než vám to celé
doběhne (a tedy retry bude stahovat jen nikdy nestažená data). Cache je nutné vypnout, pokud chcete aktualizovat data.
