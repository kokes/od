# ICIJ datasety

Tohle neni český dataset, ale je to s nimi úzce spjato. Jde o data z různých leaků, které zpracovávala organizace
[ICIJ](https://www.icij.org/) a šlo o kauzy jako jsou Panama Papers, Pandora Papers nebo Paradise Papers.

Konkrétně je databáze [ke stažení](https://offshoreleaks.icij.org/pages/database) a místní zpracování je na celkem
simplistické úrovni - jen nahrávám CSV do databáze. Chtěl jsem i konvertovat všechna data na nativní databázový typ,
ale ukázalo se, že zdrojová data jsou značně nečistá a místy nelze určit neambiguidní datum.

Vypadá to ale, že garbage je především v relationships.csv, zbytek vypadá celkem čistě. Tady jsou patterny z dat (x je číslo):

```
entities.csv
	incorporation_date: {'xx-JAN-xxxx', 'JAN xx, xxxx', 'xxxx-xx-xx'}
	inactivation_date: {'xx-JAN-xxxx'}
	struck_off_date: {'xx-JAN-xxxx'}
	dorm_date: {'xx-JAN-xxxx'}
others.csv
	incorporation_date: {'xx-JAN-xxxx'}
	closed_date: {'xx-JAN-xxxx'}
	struck_off_date: {'xx-JAN-xxxx'}
relationships.csv
	start_date: {'xx/xx/xxxx', 'xxx/xxxx', 'x/xx/xxxx', 'xxxx-xx-xx', 'xx-xx-xxxx', 'xx/x/xx', 'xx/x/xxxx', 'x/x/xx', 'xxxxxxxx', 'x/xx/xx', 'xx/xx.xxxx', 'xx.x.xxxx', 'x/x/xxxx', 'xx-JAN-xxxx', 'x.xx.xxxx', 'xx/xx-xxxx', 'xx-x-xx', 'xx/xx/xx', 'xx.xx/xxxx', 'xxxxxxx', 'xx-xxxxxx', 'xxxx', 'xx.xxx.xx', 'xx/xx/xxx', 'xx.xx.xxxx'}
	end_date: {'xx/xx/xx', 'xx-JAN-xxxx', 'x/xx/xx', 'xx/xx/xxxx', 'x/xx/xxxx', 'xxxx-xx-xx', 'xxxx', 'x/x/xxxx', 'xx/x/xxxx', 'xx.xx.xxxx'}
```