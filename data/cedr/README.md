# Centrální evidence dotací

[CEDR](http://cedr.mfcr.cz/cedr3internetv419/Default.aspx) je z hlediska transakcí jedním z nejhodnotnějších datasetů veřejné správy, protože nejen že popisuje nepřeberné množství finančních údajů, ale má sahá relativně dlouho do historie, až do roku 1999. Jde v sumě o biliony korun.

Tento informační systém byl dlouho značně nepoužitelný, pak konečně došlo k exportu dat, bylo to však ve veřejnosti nepřístupném formátu, před nedávnem došlo k exportu do CSV, s kterými pracujeme zde. Více informací naleznete v sekci [otevřených dat](http://cedr.mfcr.cz/cedr3internetv419/OpenData/DocumentationPage.aspx) na webu CEDR.

Několik převážně technických poznámek:

- Data jsou zabalená v 7zip, budete tedy potřebovat rozbalovací nástroj - můj skript s tím počítá a bohužel vypisuje spoustu informací na obrazovku během běhu - to se mi nepodařilo potlačit.
- Existují dva typy datový sad - samotné transakce a číselníky. Relativně komplexní popis vztahů naleznete [na straně 12 v dokumentaci](http://cedropendata.mfcr.cz/c3lod/C3_OpenData%20-%20datov%C3%A1%20sada%20IS%20CEDR%20III.pdf).
- Pro pohodlnost jsem denormalizoval všechny číselníky do transakcí. Obecně se jakékoliv úpravě dat v tomto repozitáři vyhýbám, ale zde mi to přišlo jako vhodné. Tady jsem neviděl výhody vločkovité normalizace, už takhle je zde spousta vztahů, navíc klíče jsou 160bitové, takže joiny nejsou nejrychlejší.
- V datasetu dotací jsem zmaterializoval IČO firem, protože vazební dataset, který by měl být exportem z ARES, má v sobě jen a pouze IČO. Není tedy důvod dělat join jen proto, abychom získali IČO.
- V datech není příliš mnoho metadat, málokterá dotace má nějaké informace o tom, k čemu vlastně slouží.
- Poskytovatelé dotací nejsou identifikovaní pomocí IČO, je jich ale relativně malý počet, takže by se tato informace dala ručně doplnit.
- Věnujte chvíli studiu vazebních tabulek, není to na první pohled příliš intuitivní, ale ve finále to dává smysl.
- V tomto skriptu zpracovávám jen několik tabulek, klidně přidávejte další, já pro ně neměl použití.
