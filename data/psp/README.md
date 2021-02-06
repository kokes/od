# Data z Poslanecké sněmovny

Tento dataset je velmi hodnotný a po zpracování dost rozsáhlý, je ale dodáván v ne úplně ideálním formátu. V rámci zpracování bylo třeba:

1. Přidat schéma, které jsme naparsovali z webu a dále rozšířili.
2. Stáhnout a rozbalit zip soubory, vygenerovat CSV, za běhu použít schéma z prvního bodu, vyčistit některá pole, překonvertovat na jednotný formát data (a času), změnit kódování z windows-1250 na UTF-8. To vše se děje v `main.py` - to je třeba pouštět, když chce člověk vytvořit/aktualizovat lokální data.

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
