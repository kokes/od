# Státní zemědělský intervenční fond

Státní zemědělský intervenční fond (SZIF) dlouhodobě vydává seznam příjemců dotací a některá jejich metadata. Roky tato data byla pouze ve formě nahlédnutí [na jejich webu](https://www.szif.cz/irj/portal/szif/seznam-prijemcu-dotaci), nově začali vydávat data i jako XML exporty. Ještě nověji začli vydávat CSV exporty (ale jen pro novější roky).

Pro jejich zpracování do relační formy stačí pustit tento jeden Python skript.

Poznámky:
- ve starších datech není žádný unikátní identifikátor přijemce, vytváříme si tedy jeden syntetický identifikátor
- ve starších datech chybí IČO, takže pro další propojení s daty je třeba udělat vazbu přes název a okres, takto jdou propojit jen vyšší desítky procent příjemců
- pozor na přechodné vnitrostátní podpory, které jsou hrazené z národních zdrojů, ty nejsou v přehledu žadatelů a nejsou ani v platbách ve sloupci `zdroje_cr`, více vizte web SZIF
