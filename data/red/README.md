# Centrální registr dotací

[IS ReD](https://red.financnisprava.cz/), dříve znám jako [CEDR](http://cedr.mfcr.cz/cedr3internetv419/Default.aspx), je z
hlediska transakcí jedním z nejhodnotnějších datasetů veřejné správy, protože nejen že popisuje nepřeberné množství
finančních údajů, ale má sahá relativně dlouho do historie, až do roku 1999. Jde v sumě o biliony korun.

Tento informační systém byl dlouho značně nepoužitelný, pak konečně došlo k exportu dat, bylo to však ve veřejnosti nepřístupném formátu, před nedávnem došlo k exportu do CSV, s kterými pracujeme zde.

Jde o poměrně komplexní sadu tabulek, je třeba se seznámit s jejich vztahy.

![diagram vztahů](https://red.financnisprava.cz/assets/images/opendata/ReDOpenData_Diagram.png)

Několik převážně technických poznámek:

- V datech není příliš mnoho metadat, málokterá dotace má nějaké informace o tom, k čemu vlastně slouží.
- Poskytovatelé dotací nejsou identifikovaní pomocí IČO, je jich ale relativně malý počet, takže by se tato informace dala ručně doplnit.
- Věnujte chvíli studiu vazebních tabulek, není to na první pohled příliš intuitivní, ale ve finále to dává smysl.
- V tomto skriptu zpracovávám jen několik tabulek, klidně přidávejte další, já pro ně neměl použití.
