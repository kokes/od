# Státní zemědělský intervenční fond

Státní zemědělský intervenční fond (SZIF) dlouhodobě vydává seznam příjemců dotací a některá jejich metadata. Roky tato data byla pouze ve formě nahlédnutí [na jejich webu](https://www.szif.cz/irj/portal/szif/seznam-prijemcu-dotaci), nově začali vydávat data i jako XML exporty.

Pro jejich zpracování do relační formy stačí pustit tento jeden Python skript.

Poznámky:
- v datech není žádný unikátní identifikátor přijemce, vytváříme si tedy jeden syntetický identifikátor
- v datech chybí IČO, takže pro další propojení s daty je třeba udělat vazbu přes název a okres, takto jdou propojit jen vyšší desítky procent příjemců
- jde tu pouze o data za rok 2018 a 2017, byť SZIF funguje o dost déle
- pozor na přechodné vnitrostátní podpory, které jsou hrazené z národních zdrojů, ty nejsou v přehledu žadatelů a nejsou ani v platbách ve sloupci `zdroje_cr`, více vizte web SZIF
- jde o první nástřel, mohou zde být jisté nedostatky

## Příklad užití

Jde o velmi volně relační konverzi, takže je třeba propojit data přes rok a identifikátor příjemce

```sql
SELECT
	*
FROM
	szif.zadatele inner join szif.platby using(rok, id_prijemce)
LIMIT 1000
```
