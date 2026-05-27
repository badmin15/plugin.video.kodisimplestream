![Version](https://img.shields.io/github/v/tag/Kecerim24/plugin.video.kodisimplestream?label=version&logo=github)
![License](https://img.shields.io/github/license/Kecerim24/plugin.video.kodisimplestream)

# KodiSimpleStream - Kodi Plugin pro Webshare.cz

KodiSimpleStream je jednoduchý Kodi plugin, který umí vyhledávat a přehrávat videa z [Webshare.cz](https://webshare.cz)

### Instalace
1. Stáhněte si zip [nejnovější verze repozitáře](https://github.com/Kecerim24/repository.kecerim/releases/latest)
2. Nainstalujte plugin přes Správce doplňků v Kodi:
   - Přejděte do Doplňků
   - Klikněte na ikonu instalátoru balíčků
   - Vyberte "Instalovat ze souboru zip"
   - Zvolte stažený zip soubor
3. Jděte do Instalovat z repozitáře:
   - Vyberte kecerim's repo > doplňky videí > kodisimplestream
### Nebo
1. Přidejte si zdroj repozitáře do Správce souborů:
   - Přejděte do Správce souborů
   - Klikněte na "Přidat zdroj"
   - Do pole "Cesta k médiu" zadejte: https://kecerim24.github.io/repository.kecerim/
   - Pojmenujte zdroj (např. "Kecerim Repo")
2. Nainstalujte repozitář:
   - Přejděte do Doplňků
   - Klikněte na ikonu instalátoru balíčků
   - Vyberte "Instalovat ze souboru zip"
   - Najděte přidaný zdroj a vyberte repository.kecerim-x.x.x.zip
3. Nainstalujte plugin:
   - Jděte do "Instalovat z repozitáře"
   - Vyberte kecerim's repo > doplňky videí > kodisimplestream

### Konfigurace
1. Po instalaci přejděte do nastavení pluginu
2. Zadejte své uživatelské jméno a heslo do Webshare.cz

### Použití
1. Spusťte plugin z vašich Kodi doplňků
2. Použijte vyhledávací funkci pro nalezení videí (hodně možností že?)
3. Vyberte video pro spuštění přehrávání

### Požadavky
- Kodi 19.0 (Matrix) nebo novější (testoval jsem jen na Kodi 21)
- Aktivní účet na Webshare.cz

### Podpora
Pokud narazíte na problémy nebo máte otázky:
- Prohlédněte si [Issues](https://github.com/Kecerim24/plugin.video.kodisimplestream/issues)
- Vytvořte nový problém, pokud váš problém ještě nebyl nahlášen

Máte-li nápad na vylepšení doplňku, neváhejte ho sdílet v sekci Issues nebo rovnou přispět vlastním kódem prostřednictvím Pull requestu (pomoc bych velmi ocenil, jelikož to je můj první addon pro Kodi). Veškeré návrhy na zlepšení jsou vítány!

### TMDb Helper integrace
1. Zkopírujte soubor `docs/tmdbhelper/kodisimplestream.json` do:
   `userdata/addon_data/plugin.video.themoviedb.helper/players/kodisimplestream.json`
2. V TMDb Helper otevřete nastavení přehrávačů a povolte/vyberte `KodiSimpleStream`.
3. TMDb Helper pak při kliknutí na film/epizodu zavolá trasu:
   `plugin://plugin.video.kodisimplestream/?action=tmdbh_play...`

Nová nastavení addonu (sekce **TMDb Helper**):
- **Auto-play best source** – automaticky přehraje nejlépe skórovaný zdroj.
- **Auto-play minimum score** – minimální skóre, od kterého dojde k auto-play.
- **Maximum ranked results** – omezení počtu kandidátů v seznamu.
- **Preferred quality mode** – jemné řazení kvality (`1080p_or_best`, `720p_or_best`, `highest`).
- **Show debug scores in labels and logs** – zobrazí skóre i v názvech položek a logu.

Poznámka: přesnost párování závisí na kvalitě názvů souborů na Webshare a kvalitě metadat předaných z TMDb Helper.
