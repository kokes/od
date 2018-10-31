# Poslanci a jiné veřejně činné osoby

PSP.cz nabízí vcelku unikátní seznam veřejně činných osob, včetně jejich zařazení (jak funkčním tak politickém) a jistých identifikujících údajů - zejm. data narození. Tyto údaje nám pak pomohou při prolinkování tohoto datasetu s Obchodním rejstříkem.

Jde o jeden z mála datasetů, kde nebudeme potřebovat Python ani žádný jiný programovací jazyk, data rovnou pošleme do databáze. Jde totiž o vesměs CSV, jen místo čárky máme rouru (pipe, `|`) a chybí hlavička. Schéma je ale na webu, takže jej můžeme naspecifikovat dopředu. Nestandardní je delimiter na konci každého řádku, takže ve schématu definujeme o sloupec navíc, nemá ale žádný praktický účel.

V praxi se s tím pracuje celkem snadno, je to prostě jen normalizovaný dataset. Jde se například dotázat na všechny poslance zvolené v roce 2017.

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
