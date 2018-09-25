# Poslanci a jiné veřejně činné osoby

Zpracování informací o poslancích a jiných veřejných činitelích. Jde se například dotázat na všechny poslance zvolené v roce 2017.

```
SELECT
    *
FROM
    psp_osoby os
    INNER JOIN psp_zarazeni za USING (id_osoba)
    INNER JOIN psp_organy org ON org.id_organ = za.id_of
WHERE
	za.cl_funkce = 0
    AND org.zkratka = 'PSP8'
```

Data pro zpracování ke stažení [na webu PSP](https://www.psp.cz/sqw/hp.sqw?k=1300).
