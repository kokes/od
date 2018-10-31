# ARES API

ARES již skoro dvacet let poskytuje API, které vám poskytne informace o takřka libovolném českém podniku. Nabízí řadu endpointů, které se liší povahou a zdrojem. Pro nás jsou relevantní tři endpointy.

- **RES** - registr ekonomických subjektů poskytuje *aktuální* informace o podniku, poskytuje údaje jako sídlo, datum vzniku (příp. i zániku), kategorii podniku, přibližný počet zaměstnanců nebo obor podnikání. **Od léta 2018 API již nevrací informace k podnikům, které jsou zaniklé více jak 4 roky.**
- **OR** - obchodní rejstřík je jeden z nejcennějších datasetů, krom informací o osobách spjatých s danou firmou nabízí i kompletní historii těchto údajů, podobně jako byste to získali na webu [justice.cz](https://justice.cz/) v tzv. úplném výpisu.
- **VREO** - nejnovější endpoint, který by měl poskytovat údaje z obchodního rejstříku jako otevřená data. Nabízí i bulkový export, chybí v něm ale údaje k datům narození, takže je málo použitelný.

Jelikož bulková data nejsou nejvhodnější, budeme muset stahovat z API. Předně si přečtěte [podmínky provozu](https://wwwinfo.mfcr.cz/ares/ares_podminky.html.cz), jejich porušení může vyústit v zabanovaní vaší IP adresy ze strany MFČR. Také mějte na paměti, že toto je jeden z mála datasetů, který závisí na databázi, vše ostatní jsme se snažili koncipovat tak, aby člověku ze skriptu vylezlo CSV, tady to úplně nešlo, protože pro potřeby stahování z API potřebujeme jistou koordinaci.

Máme zde několik nesourodých souborů, tak se podívejme, co nám nabízí:

- `init.sql` - inicializace databáze pro potřeby uložení *naparsovaných* dat
- `init_raw.sql` - inicializace databáze pro potřeby uložení *surových* dat z API, tedy XML
- `nova_ic.py` - MFČR vydává seznam změnových souborů, resp. seznam IČO, pro které se změnily údaje v rejstřících. My můžeme stahovat tyto soubory a přidávat nová IČO do databáze, abychom pro ně stáhli nové údaje z API.
- `dl.py` - **hlavní skript** na stahování dat, nedělá ale vesměs nic podstatného. Nahlíží do databáze a stahuje údaje pro ty firmy, pro které ještě žádné údaje nemáme. Až budete spokojeni s rozsahem dat ve vaší databázi, můžete upravit SQL dotaz, aby místo stahování nových dat aktualizoval ta stará (ideálně seřazená podle data modifikace).
- `res.py` - načítá surová data pro RES a parsuje je do CSV
- `or.py` - to stejné jako `res.py`, ale pro obchodní rejstřík. Tento skript generuje celou řadu souborů, protože datový model obchodního rejstříku, zvlášť když máme historizovaná data, je celkem košatý.
- `copy.sh` - kopíruje data z CSV do databáze
- `postcopy.sql` -  přidává několik indexů do naparsovaných dat, nejdůležitější je index na jmény u angažovaných osob a několik indexů nad IČO pro rychlé joiny nejen v rámci ARES dat, ale napříč datasety

Je důležité poznamenat, že stahovací skript závisí na tom, že máte v databázi dostatek IČO podniků. Jedním ze zdrojů těchto dat jsou zmíněné změnové soubory, tím ale získáte jen relativně malý subset dat. Lepší zdroj dat jsou otevřená data ARES (která obecně nechceme používat, ale pro tuto chvíli se nám hodí), kde je mj. [seznam IČO](https://wwwinfo.mfcr.cz/ares/ares_opendata.html.cz), pro které byl export udělán. Když jej importujete do `ares.raw` tabulky, budete moci pustit stahovací skript a získat data pro značnou část obchodního rejstříku.

V tuto chvíli je tato sada skriptů poněkud křehká, ale perfektně funkční. Časem se nám snad podaří tuto část učesat, aby se lépe používala širší veřejnosti.
