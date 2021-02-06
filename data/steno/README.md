# Stenoprotokoly

Stenoprotokoly jak jsou poskytované, nejsou příliš dobře zpracovatelné. Jde o HTML ve volné formě, je třeba to rozparsovat, nadetekovat kde kdo mluví, jak se stránkuje (řeč může být přes více stran), jaké je probírané téma atd. I takové drobnosti jako co je jméno a co je titul, nejsou úplně triviální.

Ve stenoprotokolech není odděleno jméno a funkce dané osoby (např. poslanec, senátor, ministr) a nejde jen říci, že poslední dvě slova tohoto kompozita je jméno, protože lidé mají prostřední jména, dvě příjmení, cizí jména atd. Proto máme soubor `pozice.txt`, kde je výčet všech možných funkcí, abychom je mohli správně detekovat. Jelikož nové stenoprotokoly stále přibývají, je třeba tento soubor doplňovat. Na konci běhu skriptu se ukáže seznam potenciálních přírůstků do těchto souborů - ukazuji seznam jmen, které skript možná špatně detekoval a jejichž funkce je možné třeba doplnit do pomocného souboru.

Skript v uvedené podobě používám už řadu let a pro potřeby tohoto repozitáře jsem jej rozšířil o podporu starších stenoprotokolů, některé vyložené staré jsem ale nezkoušel, je tu podpora jen pro poslední tři sněmovny.
