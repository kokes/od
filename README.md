# Česká otevřená data

Cílem tohoto repozitáře je sjednotit přístup k otevřeným datům, které se týkají finančních výdajů státu. Jde nám o shromáždění dat v konzistentním formátu a přidání číselníků, které rozklíčují vztahy státu a firem, případně organizačních složek státu.

Před několika lety se stát začal víc a víc otevírat vůči veřejnosti, ale často tak činil pouze formálně. Do veřejné sféry se dostala data, ale často ve formátech špatně zpracovatelných, s chybami, případně obojí. Komunitě tak často trvalo dlouhou dobu, než data zpracovala, na některé datasety se vůbec nedostalo.

I když proběhlo samotné zpracování, často se nedostalo na klíčovou část - fúzi jednotlivých datasetů, aby se na veřejnost dostaly předem neznámé skutečnosti. I to je jeden z účelů této práce.

Ačkoliv se tu nenachází příliš mnoho kódu, věřte, že tato práce stojí na letech námahy a komunikace s úřady, na nekonečných diskusích s lidmi ze všech sfér státní správy i soukromých účastníků. I přes tyto nástrahy se nám za ta léta podařilo vytvořit dialog mezi uživateli a poskytovateli dat a jen doufáme, že se nám podaří jej udržet.

## Doménová znalost a kvalita dat

Než se dostaneme k datasetům samotným, je třeba zmínit klíčový předpoklad pro správnou interpretaci dat, tím je doménová znalost, tedy pochopení dané problematiky na věcné úrovni, ne pouhé technické zpracování dat.

Člověk musí pochopit, proč je něco v CEDR a ne v DotInfo a naopak. Většina dat obsahuje jisté informace o platnosti dat, datum podpisu není to samé jako datum čerpání. Když pak člověk informace páruje např. s obchodním rejstříkem, jsou tyto atribuce klíčové.

Je tu též věcný překryv, kdy dotace by měly mít sepsané smlouvy a pokud byly uzavřeny v určitou dobu, budu i v registru smluv (ale nemusí!).

V neposlední řadě jsou všechny datasety zatíženy jistou chybovostí. Neznamená to, že bychom měli rezignovat na jisté analýzy, spíš že bychom měli být extrémně opatrní v tom, co z dat vyčteme.

## Formát dat

Při zpracování dat se řídíme jedním hlavním principem - snažíme se neměnit strukturu dat nad nezbytnou mez. To znamená, že bereme všechny sloupce ze zdrojových datasetů, až na extrémní případy neměníme obsah dat (i tak jen kvůli párování dat - tedy IČO).

Jde nám o to, aby člověk mohl vždy dohledat primární zdroj, což se mu v případě naší manipulaci s daty nepodaří.

I přes naši značnou snahu se může stát, že při našem zpracování dat něco změníme či smažeme. Jakoukoliv takovouto chybu nám prosím hlašte, pokusíme se ji opravit v co možná nejkratším termínu. Je důležité zdůraznit, že **nejsme autory žádných těchto dat, pouze je zpřístupňujeme veřejnosti**.

## Datasety

Plánujeme zde zapojit dva typy datasetů - transakční a klasifikační, byť toto rozdělení není čisté, budou zde jisté překryvy.

TODO: přidat odkazy na README v podslozkach

- **CEDR** - centrální evidence dotací je jeden z větších datasetů, obsahuje dotace pro soukromé i veřejné subjekty a tento dataset sahá až do roku 1999. Hlavní nevýhodou je absence metadat u velké části záznamů. Aktualizován je kvartálně.
- **Dotace EU** - mediálně asi nejpropíranější téma, dataset je až překvapivě přímočarý, jde o jednu tabulku, resp. dvě, jednu pro každé rozpočtové období. Dataset spadá pod MMR, aktualizován je měsíčně.
- **DotInfo** - třetí informační systém pro dotace, bohužel zatím není jasné, co je ve kterém. Puristicky vzato by Dotace EU měl být subset CEDRu a DotInfo by nemělo existovat. Bohužel je DotInfo do velké míry překryvem CEDR, ale ne úplným. Je též mnohem kratší, sahá jen do cca roku 2011 (TODO).
- **Veřejné zakázky** - shromáždění dat z několika systémů zadávání veřejných zakázek, pro nás doposud nejméně prostudovaný dataset, s ním budeme potřebovat nejvíce pomoci. Je asi nejvíce ošemetný co se týče rozklíčování složité struktury dat.
- **Registr smluv** - od léta 2016 mají veřejné subjekty povinnost zveřejňovat smlouvy nad 50 tisíc Kč hodnoty, tento revoluční zákon dramaticky zvýšil transparentnost veřejného utrácení. Zpřístupnil informace o výdajích mimo veřejné zakázky, ke všem výdajům též přidal samotné smlouvy, byť místy začerněné. Dataset patří pod MVČR a je aktualizován denně.
- **Monitor státní pokladny** - jeden z nejčitších datasetů státu nabízí pohled do vyúčtování jednotlivých subjektů státu, ať už jde o ministerstva nebo obce. Zatím dataset nemáme zpracovaný, plánujeme jej použít na obohacení informací o veřejných subjektech. (Např. u smlouvy na 1 miliardu člověk uvidí, kolik procent z ročního rozpočtu to je.)
- **ARES** - nechvalně známý administrativní rejstřík ekonomických subjektů nabízí vhled nejen do právnických subjektů Česka. Klíčové jsou základní informace o subjektech, možná využijeme i obchodní rejstřík. Nová otevřená data ARES nám bohužel moc platná nebudou, více v README (TODO). Tento dataset bude bohužel jediný, který nejde volně stáhnout najednou.

## Identifikace podniků
Jedním z hlavních zásahů do dat je nahrazení identifikace podniků našimi “vlastními” daty, konkrétně daty z ARES. Problémem je, že místo odkazování do ARES se každý z poskytovatelů dat snaží tvořit si vlastní databázi podniků a v oněch datech jsou často chyby. Z důvodu konzistence a kvality dat proto používáme většinou pouze IČO podniků a dál přebíráme informace z ARES.

## Účel repozitáře

TODO: přesunout výše
Najdete zde několik sad kódů, v tuto chvíli poněkud bez struktury a organizace. Časem snad vymyslíme nějakou koherentní orchestraci.

Účely skriptů budou zhruba následující:

1. Stažení dat - většinou jsou definované adresy, odkud se dají čerstvá data strojově stáhnout, občas je třeba ručního zásahu.
2. Konverze dat a prvotní čištění. V tuto chvíli se každý dataset bude nacházet v CSV, které pak člověk může nahrát prakticky kamkoliv, včetně Excelu.
3. Export dat z CSV do databáze, v našem případě PostgreSQL. Můžete si zvolit svoji vlastní, my jsme náš systém indexů, datových verifikací a dalších mechanismů postavili nad PostgreSQL.

Posledním aspektem je aktualizace dat. V tuto chvíli máme hotové jednorázové nalití všech dat, postupně promýšlíme, jak by se ideálně dal provádět update.

## Technologie
TODO
ETL v Python 3 s hrstkou balíků pro zpracování XML a XLS
PostgreSQL, volitelná
HTML/JS a tenký klient ve Flasku

