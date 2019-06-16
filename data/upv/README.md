# Úřad průmyslového vlastnictví

První nástřel zpracování dat z [ÚPV](https://upv.cz). Jde o kompletní databázi ochranných známek, v době psaní (6/2019) jde o více jak 400 tisíc záznamů.

Pár upozornění:

- Jde pouze o [národní databázi](https://www.upv.cz/cs/sluzby-uradu/databaze-on-line/databaze-ochrannych-znamek/narodni-databaze.html), četné [mezinárodní databáze](https://www.upv.cz/cs/sluzby-uradu/databaze-on-line/databaze-ochrannych-znamek/zahranicni-databaze.html) (ve kterých jde hledat na webu ÚPV) zde nejsou.
- Zatím zpracováváme pouze text, v otevřených datech jsou i obrázky, které zatím neřešíme.
- Neřešíme inkrementy, v tuto chvíli jde o full dump, nějaký state management na to půjde celkem snadno naroubovat.


V rámci Postgres schématu jsem přidal i n-gramový index (nutno přidat [nativní rozšíření](https://www.postgresql.org/docs/current/pgtrgm.html)), který pak umožní dělat velmi efektivně dělat dotazy typu

```sql
SELECT
	mark_verbal_element <-> 'mercedes' AS dist,
	*
FROM upv.inserts
-- pro zrychleni top-k dotazů je dobre pridat `AND mark_verbal_element % 'pattern'`
WHERE mark_verbal_element IS NOT NULL
ORDER BY dist
LIMIT 100;
```
