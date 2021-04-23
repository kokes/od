# Česká otevřená data

Cílem tohoto repozitáře je sjednotit přístup k otevřeným datům, které se týkají finančních výdajů státu. Jde nám o shromáždění dat v konzistentním formátu a přidání číselníků, které rozklíčují vztahy státu a firem, případně organizačních složek státu.

Před několika lety se stát začal víc a víc otevírat vůči veřejnosti, ale často tak činil pouze formálně. Do veřejné sféry se dostala data, ale často ve formátech špatně zpracovatelných, s chybami, případně obojí. Komunitě tak často trvalo dlouhou dobu, než data zpracovala, na některé datasety se vůbec nedostalo.

I když proběhlo samotné zpracování, často se nedostalo na klíčovou část - fúzi jednotlivých datasetů, aby se na veřejnost dostaly předem neznámé skutečnosti. I to je jeden z účelů této práce.

Ačkoliv se tu nenachází příliš mnoho kódu, věřte, že tato práce stojí na letech námahy a komunikace s úřady, na nekonečných diskusích s lidmi ze všech sfér státní správy i soukromých účastníků. I přes tyto nástrahy se nám za ta léta podařilo vytvořit dialog mezi uživateli a poskytovateli dat a jen doufáme, že se nám podaří jej udržet.

## Účel repozitáře

Najdete zde několik sad kódů, v tuto chvíli nejsou nějak značně sešňerované, jde o spíše samostatné skripty, časem snad vymyslíme nějakou koherentní orchestraci.

Účely skriptů budou zhruba následující:

1. Stažení dat - většinou jsou definované adresy, odkud se dají čerstvá data strojově stáhnout, občas je třeba ručního zásahu (zejm. u evropských dotací od MMR).
2. Konverze dat a prvotní čištění. Po tomto kroku bude každý dataset v CSV, které pak člověk může nahrát prakticky kamkoliv, včetně Excelu.
3. Export dat z CSV do databáze, v našem případě PostgreSQL. Můžete si zvolit svoji vlastní, my jsme náš systém indexů, datových verifikací a dalších mechanismů postavili nad PostgreSQL.

Posledním aspektem je aktualizace dat. V tuto chvíli máme hotové jednorázové nalití všech dat, postupně promýšlíme, jak by se ideálně dal provádět update.

**Již v tuto chvíli ale funguje základní princip tohoto projektu - jakmile člověk dostane datasety do jednoho systému/databáze, může se dotazovat napříč - například seznam zakázek pro firmu, která splňuje nějaká kritéria na základě informací z ARES a je propojena s určitými politicky aktivními lidmi.**

## Lokální spuštění

Účelem projektu je, aby se dal snadno použít nejen autorem. Pro základní použití vám postačí Python (3.6+) a nic jiného. Stačí si nainstalovat pár základních závislostí a můžete data nahrát do CSV nebo i databáze - podporovaná je SQLite (vestavěná do Pythonu) nebo PostgreSQL.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 main.py --all --partial
```

Tato sekvence příkazů nainstaluje potřebné závislosti do virtuálního prostředí a zpracuje všechna data do CSV.

Selektivní zpracování jde udělat pomocí specifikace datasetu jako pozičního argumentu

```sh
python3 main.py --partial ares volby
```

A nahrání do databáze se řídí argumentem `--connstring`. Při specifikaci databáze proběhne vše - stažení dat, konverze do CSV a nahrání do databáze. Bez specifikace databáze skončíte u CSV.

```sh

python3 main.py --connstring sqlite:///soubor.db --partial ares volby
python3 main.py --connstring postgres://localhost/data --partial ares volby
```

### Spuštění v Docker kontejneru

Pokud si nechcete lokálne instalovat Python, můžete využít přiložený `Dockerfile`, vytvořit si Docker image a spustit vše v kontejneru.

Všechna generovaná data včetně stažených zdrojových souborů se zapisují do složky `/data` v kontejneru. Zpracované CSV výstupy najdete v `/data/csv`.

**Tvorba Docker image**
```sh
docker build -t kokes-od .
```

**Spuštění**
```sh
docker run -it --rm -v $PWD:/data/csv kokes-od --partial ares volby
```

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

- [**CEDR**](data/cedr) - centrální evidence dotací je jeden z větších datasetů, obsahuje dotace pro soukromé i veřejné subjekty a tento dataset sahá až do roku 1999. Hlavní nevýhodou je absence metadat u velké části záznamů. Aktualizován je kvartálně.
- [**Dotace EU**](data/eufondy) - mediálně asi nejpropíranější téma, dataset je až překvapivě přímočarý, jde o jednu tabulku, resp. dvě, jednu pro každé rozpočtové období. Dataset spadá pod MMR, aktualizován je měsíčně.
- [**DotInfo**](data/dotinfo) - třetí informační systém pro dotace, bohužel zatím není jasné, co je ve kterém. Puristicky vzato by Dotace EU měl být subset CEDRu a DotInfo by nemělo existovat. Bohužel je DotInfo do velké míry překryvem CEDR, ale ne úplným. Je též mnohem kratší, sahá jen do cca roku 2011.
- [**Veřejné zakázky**](data/zakazky) - shromáždění dat z několika systémů zadávání veřejných zakázek, pro nás doposud nejméně prostudovaný dataset, s ním budeme potřebovat nejvíce pomoci. Je asi nejvíce ošemetný co se týče rozklíčování složité struktury dat.
- [**Registr smluv**](data/smlouvy) - od léta 2016 mají veřejné subjekty povinnost zveřejňovat smlouvy nad 50 tisíc Kč hodnoty, tento revoluční zákon dramaticky zvýšil transparentnost veřejného utrácení. Zpřístupnil informace o výdajích mimo veřejné zakázky, ke všem výdajům též přidal samotné smlouvy, byť místy začerněné. Dataset patří pod MVČR a je aktualizován denně.
- **Monitor státní pokladny** - jeden z nejčitších datasetů státu nabízí pohled do vyúčtování jednotlivých subjektů státu, ať už jde o ministerstva nebo obce. Zatím dataset nemáme zpracovaný, plánujeme jej použít na obohacení informací o veřejných subjektech. (Např. u smlouvy na 1 miliardu člověk uvidí, kolik procent z ročního rozpočtu to je.)
- [**ARES**](data/ares) - nechvalně známý administrativní rejstřík ekonomických subjektů nabízí vhled nejen do právnických subjektů Česka. Klíčové jsou základní informace o subjektech, možná využijeme i obchodní rejstřík. Nová otevřená data ARES nám bohužel moc platná nebudou, více v README (TODO). Tento dataset bude bohužel jediný, který nejde volně stáhnout najednou.
- [**PSP**](data/psp) - Poslanecká sněmovna Parlamentu nabízí velmi zajímavé datasety pro další zpracování, u nás najdete dva hlavní - informace o osobách (a nejen poslancích, ale i senátorech nebo členech vlád) a zpracování stenoprotokolů.
- [**Volby**](data/volby) - statistický úřad již nějaký pátek nabízí otevřená data, se kterými se celkem snadno pracuje, ale nejsou připravené k analytice hned po stažení. Navíc se jejich formát měnil v čase, takže se snažíme toto unifikovat.
- [**Justice**](data/justice) - data od Ministerstva spravedlnosti obsahují informace o jednotlivých ekonomických subjektech, jde o export z veřejných rejstříků, jak jsou mj. dostupné na webu [Justice](http://justice.cz).
- [**SZIF**](data/szif) - data od [Státního zemědělského intervenčního fondu](https://www.szif.cz/irj/portal/szif/seznam-prijemcu-dotaci) obsahují informace o příjemcích dotací, včetně rozdělení na národní a evropské zdroje


## Identifikace podniků
Jedním z hlavních zásahů do dat je nahrazení identifikace podniků našimi “vlastními” daty, konkrétně daty z ARES. Problémem je, že místo odkazování do ARES se každý z poskytovatelů dat snaží tvořit si vlastní databázi podniků a v oněch datech jsou často chyby. Z důvodu konzistence a kvality dat proto používáme většinou pouze IČO podniků a dál přebíráme informace z ARES.
