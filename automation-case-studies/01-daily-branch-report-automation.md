# Case Study 01 — Daily Branch Report Automation

## Účel případové studie

Cílem případové studie je navrhnout jednoduchý, bezpečný a opakovatelný proces pro automatickou přípravu denního reportu návštěvnosti poboček.

Případová studie ukazuje schopnost:
- převést ruční datový proces do automatizovaného workflow;
- určit vhodný trigger;
- rozdělit proces na samostatné tasky;
- definovat pořadí a závislosti kroků;
- pracovat s chybějícími, opožděnými a opravenými vstupy;
- zabránit duplicitnímu zpracování;
- bezpečně publikovat výstup pro Power BI;
- zaznamenat výsledek procesu do logu.

Nejde o implementaci konkrétního automatizačního nástroje. Výstupem je koncepční návrh, který bude možné později realizovat například pomocí Pythonu a Windows Task Scheduleru.

---

## Business kontext

Společnost provozuje několik poboček. Každá pobočka jednou denně ručně exportuje CSV soubor s údaji o své návštěvnosti.

Management potřebuje každý den aktualizovaný Power BI report, ve kterém může sledovat:
- celkovou návštěvnost;
- návštěvnost jednotlivých poboček;
- vývoj návštěvnosti v čase;
- porovnání výsledků mezi pobočkami;
- úplnost dat zahrnutých do reportu.

Ruční odesílání může vést k opožděnému doručení, chybějícím vstupům nebo opakovanému zaslání opravené verze. Proces proto nesmí předpokládat, že všechny soubory vždy dorazí správně a ve stejný čas.

---

## Datové zdroje

Vstupem jsou denní CSV soubory odesílané jednotlivými pobočkami.

Každý soubor musí obsahovat minimálně:
- identifikátor nebo název pobočky;
- datum, ke kterému data patří;
- sledované hodnoty návštěvnosti;
- povinné sloupce definované datovým schématem.

Přesné názvy sloupců a metriky nejsou součástí tohoto koncepčního návrhu.

---

## Jmenná konvence

Pro vstupní soubory bude použita jednotná jmenná konvence:

```text
visits_<branch>_<business_date>_v<version>.csv
```

Příklady:

```text
visits_plzen_2026-09-11_v01.csv
visits_praha_2026-09-11_v01.csv
visits_brno_2026-09-11_v02.csv
```

Z názvu souboru lze určit:
- zdrojovou pobočku;
- business datum, ke kterému data patří;
- verzi souboru.

**Business datum** označuje den, ke kterému se data vztahují. Nemusí být totožné s datem, kdy byl soubor doručen nebo zpracován.

---

## Business pravidla automatizace

### Kompletní vstupy

Jakmile dorazí validní soubory ze všech očekávaných poboček, může se zpracování spustit okamžitě.

Výsledný stav procesu bude:
```text
SUCCESS
```

### Chybějící vstupy v 06:00

Pokud v 06:00 některý očekávaný soubor chybí, proces se nezastaví. Zpracuje dostupná data a vytvoří report ve stavu:
```text
WARNING
```

Report musí obsahovat informaci, že data nejsou kompletní, a uvést chybějící pobočky.

### Soubor doručený mezi 06:00 a 07:00

Pokud chybějící soubor dorazí nejpozději v 07:00, proces se spustí znovu.

Po úspěšné validaci se:
- zahrnou nově doručená data;
- znovu vytvoří celý výstup;
- původní neúplný report nahradí kompletní verzí;
- stav procesu změní na `SUCCESS`;
- změna zaznamená do logu.

### Soubor doručený po 07:00

Soubor doručený po 07:00 se zařadí do následujícího zpracování. Stále si zachová původní business datum, aby nebyl nesprávně vykázán jako návštěvnost následujícího dne.

Pozdější zpracování představuje opravu nebo doplnění historických dat.

---

## Trigger procesu

Hlavním spouštěčem bude událostní trigger:
```text
doručení posledního souboru
→ kontrola názvu a obsahu
→ kontrola úplnosti očekávaných vstupů
→ případné spuštění zpracování
```

Událostní trigger bude doplněn časovou kontrolou v 06:00. Ta zajistí, že proces proběhne i tehdy, pokud některá pobočka svůj soubor neodešle.

Navržené řešení kombinuje:
- událostní spuštění po doručení vstupů;
- časovou kontrolu v 06:00;
- dodatečné zpracování souborů doručených do 07:00.

---

## Navržený datový proces
```text
doručení souboru
→ kontrola názvu, pobočky, data a verze
→ validace struktury a obsahu
→ registrace validního vstupu
→ kontrola úplnosti očekávaných souborů
→ výběr poslední validní verze každého vstupu
→ spojení dostupných dat
→ vytvoření dočasného výstupu
→ závěrečná validace výsledku
→ bezpečné nahrazení CSV souboru pro Power BI
→ archivace předchozího výstupu
→ zápis konečného stavu do logu
```

---

## Navržené tasky

### Task 1 — Detekce nového souboru

Proces zjistí, že do vstupní složky dorazil nový CSV soubor. Výstupem tasku je cesta k souboru a čas jeho přijetí.

### Task 2 — Kontrola názvu souboru

Název se porovná s definovanou jmennou konvencí. Kontroluje se pobočka, business datum, verze a přípona souboru.

### Task 3 — Validace vstupu

Soubor se otevře a ověří se jeho technická použitelnost.

Kontrola může zahrnovat:
- přítomnost povinných sloupců;
- správné datové typy;
- povinné hodnoty;
- platnost identifikátoru pobočky;
- soulad business data s názvem souboru;
- duplicity;
- základní logickou správnost hodnot.

### Task 4 — Registrace vstupu

Validní soubor se zaeviduje společně s pobočkou, business datem, verzí, časem přijetí a výsledkem validace.

### Task 5 — Kontrola úplnosti

Seznam doručených validních souborů se porovná se seznamem očekávaných poboček pro konkrétní business datum.

### Task 6 — Výběr aktivních verzí

Pro každou pobočku a business datum se vybere poslední validní verze. Starší verze zůstávají v archivu, ale nevstupují současně do stejného výpočtu.

### Task 7 — Spojení a transformace

Vybrané soubory se spojí do jednotného datasetu a provedou se požadované transformace.

### Task 8 — Vytvoření dočasného výstupu

Nový výstup se nejprve uloží pod dočasným názvem. Aktivní soubor používaný Power BI se během výpočtu nemění.

### Task 9 — Závěrečná validace

Před publikací se ověří například:
- existence výsledného souboru;
- přítomnost očekávaných sloupců;
- počet zpracovaných poboček;
- počet výsledných řádků;
- absence nepovolených duplicit;
- konečný stav `SUCCESS` nebo `WARNING`.

### Task 10 — Publikace výstupu

Po úspěšné validaci dočasný soubor jedním krokem nahradí předchozí aktivní výstup.

### Task 11 — Archivace a logování

Předchozí správný výstup se uloží do archivu a výsledek běhu se zapíše do logu.

---

## Závislosti mezi tasky

Každý další krok může začít pouze po úspěšném dokončení potřebného předchozího kroku.
```text
detekce souboru
→ kontrola názvu
→ validace vstupu
→ registrace vstupu
→ kontrola úplnosti
→ výběr aktivních verzí
→ spojení a transformace
→ dočasný výstup
→ závěrečná validace
→ publikace
→ archivace a logování
```

Nevalidní soubor nesmí pokračovat do transformačního kroku. Chybějící soubor však podle zvoleného business pravidla nezastaví zpracování ostatních validních vstupů.

---

## Práce s opravenými verzemi

Pobočka může původní soubor opravit a odeslat znovu.

```text
visits_brno_2026-09-11_v01.csv
visits_brno_2026-09-11_v02.csv
```

Platí následující pravidla:
- nová verze se vždy nejprve validuje;
- poslední validní verze se označí jako aktivní;
- předchozí verze se označí jako nahrazená;
- do výpočtu vstupuje pouze jedna aktivní verze;
- historie verzí zůstane zachována;
- nevalidní nová verze nenahradí starší validní verzi.

Příklad:

```text
v01 → validní → ACTIVE
v02 → nevalidní → REJECTED

výsledek
→ nadále se použije v01
→ proces zaznamená WARNING
```

---

## Ochrana před duplicitami

Proces nesmí automaticky připojit všechny nalezené soubory. Pro kombinaci pobočky a business data použije pouze jednu aktivní validní verzi.

Opakované spuštění nad stejnými vstupy musí vytvořit stejný výsledek bez přidání duplicit. Tato vlastnost se označuje jako **idempotence**.

```text
stejné vstupy
→ opakované spuštění
→ stejný výsledek
```

---

## Stavy procesu

### SUCCESS:
- všechny očekávané vstupy jsou dostupné;
- použité soubory prošly validací;
- výsledný soubor byl úspěšně vytvořen a publikován.

### WARNING:
- některý očekávaný vstup chybí;
- byla odmítnuta nevalidní opravná verze;
- proces mohl pokračovat nad dostupnými validními daty;
- report musí jasně informovat o omezení dat.

### FAILED:
- nelze vytvořit použitelný výstup;
- selhala kritická transformace;
- neprošla závěrečná validace;
- nový výstup nebyl publikován.

Při stavu `FAILED` zůstane pro Power BI dostupný poslední správný výstup.

---

## Bezpečná publikace

Výsledný soubor pro Power BI bude mít stabilní cestu a název:

```text
output/daily_branch_visits.csv
```

Nová data se nesmí zapisovat přímo do tohoto souboru řádek po řádku. Power BI by mohl během zápisu načíst neúplný obsah.

Bezpečný postup:
```text
vytvořit dočasný soubor
→ ověřit jeho strukturu a obsah
→ archivovat předchozí výstup
→ jedním krokem nahradit aktivní soubor
```

Příklady archivních výstupů:
```text
archive/daily_branch_visits_2026-09-11_0600.csv
archive/daily_branch_visits_2026-09-11_0645.csv
```

---

## Informace v Power BI reportu

Report musí vedle business výsledků obsahovat také informaci o aktuálnosti a úplnosti dat.

Doporučené provozní údaje:
- business datum;
- čas poslední aktualizace;
- stav aktualizace;
- počet očekávaných poboček;
- počet zahrnutých poboček;
- seznam chybějících poboček.

Při stavu `WARNING` nesmí report působit jako kompletní výsledek.

---

## Logování

Každé spuštění procesu se zaznamená do logu.

Log má obsahovat minimálně:
- jedinečný identifikátor běhu;
- datum a čas zahájení;
- datum a čas dokončení;
- zpracovávané business datum;
- seznam očekávaných vstupů;
- seznam skutečně doručených vstupů;
- použité verze souborů;
- výsledek validačních kontrol;
- počet zpracovaných a odmítnutých záznamů;
- cestu k publikovanému výstupu;
- konečný stav `SUCCESS`, `WARNING` nebo `FAILED`;
- stručný popis případné chyby nebo omezení.

Automatické e-mailové nebo jiné upozornění zatím není součástí návrhu. Chyby a varování jsou evidovány v logu a zobrazeny v reportu.

---

## Rozhodovací logika

```text
Dorazil nový soubor?
→ ne: čekat na další událost nebo kontrolu v 06:00
→ ano: zkontrolovat název a obsah

Je soubor validní?
→ ne: označit REJECTED a zachovat předchozí validní verzi
→ ano: zaregistrovat jako dostupný vstup

Jsou dostupné všechny očekávané pobočky?
→ ano: vytvořit kompletní výstup se stavem SUCCESS
→ ne a je 06:00: vytvořit neúplný výstup se stavem WARNING
→ ne a ještě není 06:00: čekat

Dorazil chybějící validní soubor do 07:00?
→ ano: přepočítat celý výstup
→ ne: zařadit jej do pozdějšího zpracování podle business data
```

---

## Navržené řešení

Výsledný proces kombinuje událostní a časové řízení.

Událostní část umožňuje spustit zpracování okamžitě po doručení všech potřebných souborů. Časová kontrola v 06:00 zajišťuje, že report vznikne i při neúplných vstupech. Hodinové toleranční okno umožňuje začlenit opožděná data bez čekání na další den.

Proces nepovažuje nejnovější soubor automaticky za správný. Každá nová verze musí projít validací. Výstup se publikuje až po závěrečné kontrole a opakované spuštění nesmí vytvořit duplicitní data.

Navržený přístup podporuje:
- pravidelnou dostupnost reportu;
- transparentní práci s neúplnými daty;
- bezpečné opravy vstupů;
- dohledatelnost jednotlivých běhů;
- ochranu posledního správného výstupu;
- pozdější rozšíření o monitoring a automatická upozornění.

---

## Hranice případové studie

Případová studie je koncepčním návrhem automatizovaného procesu.

Nezahrnuje:
- hotový Python skript;
- konfiguraci Windows Task Scheduleru;
- konkrétní implementaci sledování složky;
- automatické obnovení Power BI Service;
- odesílání e-mailových upozornění;
- produkční správu přístupových údajů;
- kompletní monitoring a alerting.

Tyto části mohou být doplněny v následujících praktických lekcích automatizace.

---

## Shrnutí

```text
vstup
→ denní CSV soubory poboček

trigger
→ doručení souboru + časová kontrola v 06:00

tolerance
→ opravené nebo chybějící soubory lze doplnit do 07:00

validace
→ název, pobočka, datum, verze, struktura a obsah

zpracování
→ pouze poslední validní verze každého vstupu

výstup
→ stabilní CSV soubor pro Power BI

bezpečnost publikace
→ dočasný soubor, kontrola a následné nahrazení

provozní stav
→ SUCCESS, WARNING nebo FAILED

dohledatelnost
→ archiv verzí a log každého spuštění
```