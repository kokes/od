# Otevřená data Ministerstva spravedlnosti

Ministerstvo spravedlnosti nabízí otevřená data, konkrétně [veřejný rejstřík](https://dataor.justice.cz). Místní skripty mají za cíl tato data zpracovat do relační formy.

- Stačí pustit skript `main.py`, který data stáhne a pomocí schématu (definované v `xml_schema.json`) konvertuje na CSV data.
- Pokud chce člověk data nahrát do PostgreSQL, slouží tomu `schema.py` pro inicializaci tabulek v rámci schématu `justice`. Celé je to ale orchestrované přes rootové `main.py`, tady je automatizován jen export do CSV

Implementační detaily:

- Na portálu MSp není seznam souborů ke stažení, používáme neveřejné API, které seznam souborů obsahuje. Časem by mělo dojít k nápravě.
- Data na webu jsou i v CSV, ale tato CSV jsou prakticky nepoužitelná.
- Zaniklé subjekty jsou prozatím nezpracované, protože způsob jejich exportu je naprosto nepraktický.
