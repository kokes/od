# Data z Poslanecké sněmovny

Tento dataset je velmi hodnotný a po zpracování dost rozsáhlý, je ale dodáván v ne úplně ideálním formátu. V rámci zpracování bylo třeba:

1. Přidat schéma, které jsme naparsovali z webu a dále rozšířili. (Předmět skriptu `01stahni_schema.py`, který již pouštět nemusíte.)
2. Stáhnout a rozbalit zip soubory, vygenerovat CSV, za běhu použít schéma z prvního bodu, vyčistit některá pole, překonvertovat na jednotný formát data (a času), změnit kódování z windows-1250 na UTF-8. To vše se děje v `02generuj_csv.py` - to je třeba pouštět, když chce člověk vytvořit/aktualizovat lokální data.
3. Vygenerovat SQL pro případné použití dat v databázi. Krom vytvoření tabulek jde i o mírné věci okolo - komentáře, indexy, čistku neplatných dat atd. Máte-li CSV, stačí pustit `03sql_schema.py` a výsledný SQL soubor pustit proti Postgres databázi, `psql < schema.sql`.

## Příklad práce s daty

```
SELECT
    *
FROM
    psp.poslanci_osoby os
    INNER JOIN psp.poslanci_zarazeni za USING (id_osoba)
    INNER JOIN psp.poslanci_organy org ON org.id_organ = za.id_of
WHERE
	za.cl_funkce = 0
    AND org.zkratka = 'PSP8'
```

## RAW data

Data pro zpracování ke stažení [na webu PSP](https://www.psp.cz/sqw/hp.sqw?k=1300).
