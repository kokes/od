# Volební data

Volební data přichází v několika formách, ta nejlépe zpracovatelná najdeme [v sekci otevřených dat](https://volby.cz/opendata/opendata.htm) na webu Českého statistického úřadu. Ačkoliv jde o otevřená data, není to jen o stažení dat a natažení do Excelu. Bohužel se formáty v čase trochu liší, občas jde jen o XML, někdy musíme do dat trochu šáhnout atd.

Právě z těchto důvodů se těmto datům explicitně věnujeme.

**Otevřená data ČSÚ nepokrývají všechny volby porevoluční České republiky a Československa, jde pouze o posledních 15 let.** Pokud vás tedy zajímají odpovědi na otázky typu "jaké byly nejtěsnější senátní volby," otevřená data ČSÚ vám v tom bohužel neposlouží.

## Volební registry

U každých voleb je sada datasetů, které uchovávají vždy trochu rozdílné informace, takže je třeba je zpracovávat separátně. V tomto adresáři se věnujeme _registrům_, které obsahují kompletní informace o výsledcích daných voleb, zpravidla na obecní úrovni (tj. ne okrskové). Často je nutné je propojit s číselníky, abychom získali informace o dimenzích.

Kód zde data stahuje i dál zpracovává. **Stahuje data ke všem volbám, pro které ČSÚ poskytuje otevřená data.** Po puštění skriptu tak budete moci analyzovat data k výsledkům prezidentských voleb, voleb do Senátu, Poslanecké sněmovny atd.

## Senátní data

Bohužel stále nemáme data za celou historii, takže pokud někde chceme dělat analytiku nad všema datama, musíme si je stáhnout přímo z webu ČSÚ. Nemám tu techniku moc rád, tak se ji snažim minimalizovat. Naštěstí jsem to potřeboval zatím jen pro Senát, kde těch dat není moc. Je tu tedy `senat.py`, které stáhne všechny senátní volby do ad-hoc CSV. Jeho databázové schéma je v komentáři v kódu, není to nijak napojené na jakoukoliv automatizaci v tomto repu.
