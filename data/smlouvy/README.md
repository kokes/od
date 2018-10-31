# Smlouvy
Různé exporty smluv se na webech úřadů objevovaly delší dobu, ale až s příchodem léta 2016 a zákonem o tzv. registru smluv se vše změnilo. Smlouvy jsou nyní na jednom místě, na webu [smlouvy.gov.cz](http://smlouvy.gov.cz) a je možné stahovat si bulkové exporty.

Kód zde obstarává stahování čerstvých dat (kontroluje se otisk souboru vůči vzdáleném serveru a případně se data aktualizují), parsování a nahrávání do databáze. Výsledkem jsou dvě tabulky - jedna se seznamem smluv v daný měsíc a jedna s přehledem dodavatelů a poskytovatelů.

V datech je spousta chyb, takže najdete nesmyslné částky, nesmyslné implicitní daně z přidané hodnoty, chyby v identifikátorech firem atd. Bohužel to všichni víme, včetně provozovatelů registru, ale za uplynulé roky s tím nikdo nic moc neudělal.
