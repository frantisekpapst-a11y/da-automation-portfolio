# Automation Basics Cheatsheet

Praktický přehled základních principů automatizace datových procesů.

---

## 1. Co znamená automatizace

**Automation** neboli automatizace znamená, že předem připravený proces může proběhnout bez toho, aby člověk ručně prováděl každý jeho krok.

Ruční proces:

```text

analytik otevře VS Code

→ ručně spustí Python

→ zkontroluje výsledek

→ uloží CSV

→ otevře Power BI

→ obnoví report

```

Automatizovaný proces:

```text

nastane spouštěcí podmínka

→ spustí se Python skript

→ načtou se data

→ proběhne validace

→ vytvoří se výstup

→ výsledek se zapíše do logu

```

Automatizace neznamená pouze automatické spuštění skriptu. Proces musí také určit:

- zda jsou vstupy dostupné;

- zda jsou data použitelná;

- co udělat při chybě;

- zda se výstup skutečně vytvořil;

- jak zaznamenat konečný výsledek.

---

## 2. Trigger — spouštěč

**Trigger** je událost nebo podmínka, která zahájí proces.

### Časový trigger

```text

každý pracovní den v 06:00

→ spustit Python skript

```

### Událostní trigger

```text

do složky dorazí nový CSV soubor

→ spustit jeho zpracování

```

### Ruční trigger

```text

uživatel vybere Run workflow

→ spustit připravený proces

```

I ručně aktivovaný proces může být automatizovaný. Uživatel jej pouze zahájí, ale jednotlivé kroky potom proběhnou bez dalšího ručního zásahu.

### Trigger v SQL

Databázový trigger je konkrétní typ událostního spouštěče.

Může reagovat například na:

- `INSERT`;

- `UPDATE`;

- `DELETE`.

```text

INSERT do tabulky orders

→ SQL trigger

→ zápis do auditní tabulky

```

Pojem trigger má tedy stejný základní význam, ale konkrétní spouštěcí událost závisí na použitém prostředí.

---

## 3. Automation versus Scheduling

### Scheduling

**Scheduling** určuje, kdy se má proces spustit.

```text

každý den v 06:00

každé pondělí

první den v měsíci

```

### Automation

**Automation** určuje, co se má po spuštění samo provést.

```text

načíst API

→ validovat data

→ vypočítat výsledky

→ uložit CSV

→ zapsat stav do logu

```

### Spojení obou principů

```text

Windows Task Scheduler

→ určí čas spuštění

Python skript

→ automaticky provede datové kroky

```

Kalendářní připomínka není plná automatizace:

```text

v 06:00 upozorní analytika

→ analytik musí proces ručně spustit

```

---

## 4. Automation versus Orchestration

### Automation

Automatizace provede předem připravenou činnost bez ručního zásahu.

```text

načíst CSV

→ vyčistit data

→ vypočítat souhrn

→ uložit výsledek

```

### Orchestration

**Orchestration** koordinuje více samostatných úloh a jejich závislosti.

Řeší například:

- pořadí úloh;

- paralelní kroky;

- závislosti;

- reakci na chybu;

- podmínky pokračování;

- okamžik publikace výsledku.

```text

načtení SQL dat ──┐

                  ├─→ spojení → validace → publikace

načtení API dat ──┘

```

Jeden menší Python skript může obsahovat jak automatizační, tak jednoduchou orchestrační logiku. Pro složité podnikové procesy se používají specializované orchestrační platformy.

---

## 5. Pipeline

**Pipeline** je celý řízený datový proces od vstupu až po výstup.

Pipeline:

- má začátek a konec;

- obsahuje jednu nebo více úloh;

- určuje pořadí zpracování;

- pracuje se závislostmi;

- má výsledný stav úspěchu nebo selhání.

```text

načíst data

→ validovat data

→ transformovat data

→ vytvořit výstup

→ ověřit výstup

→ zaznamenat stav

```

---

## 6. Task — jednotka pipeline

**Task** je jedna konkrétní výkonná úloha uvnitř pipeline.

```text

Pipeline: aktualizace cenového reportu

Task 1 → načíst produkty z SQL

Task 2 → načíst kurzy z API

Task 3 → validovat produkty

Task 4 → validovat kurzy

Task 5 → přepočítat ceny

Task 6 → uložit výstup

Task 7 → zapsat konečný stav

```

Dobře navržený task má mít jasný:

- účel;

- vstup;

- výstup;

- stav úspěchu nebo chyby.

Názvy se mezi nástroji mohou lišit. Konkrétní platforma může používat například pojmy `task`, `activity`, `job` nebo `step`.

---

## 7. Dependency — závislost

**Dependency** určuje, že jedna úloha může začít až po dokončení jiné úlohy.

```text

načtení kurzů

→ přepočet cen do CZK

```

Výpočet ceny v CZK potřebuje dva vstupy:

```text

produkty z SQL ───────┐

                      ├─→ přepočet cen do CZK

směnné kurzy z API ───┘

```

Načtení produktů a načtení kurzů mohou proběhnout nezávisle nebo paralelně. Přepočet však musí počkat na oba výsledky.

Pokud povinný předchozí task selže, závislý task se zpravidla:

- nespustí;

- označí jako `SKIPPED`;

- nebo skončí řízenou chybou podle návrhu procesu.

---

## 8. Základní stavy procesu

### SUCCESS

Všechny povinné kroky byly úspěšně dokončeny.

### WARNING

Hlavní výstup vznikl, ale vyskytl se předem definovaný nekritický problém.

### FAILED

Chybí povinný vstup, selhala kritická kontrola nebo nevznikl důvěryhodný výstup.

### SKIPPED

Úloha se nespustila, protože:

- nebyla potřebná;

- nebyla splněna podmínka;

- selhal její povinný předchůdce.

Business pravidla musí předem určit, která chyba je kritická a která umožňuje pokračovat.

---

## 9. Fail fast

**Fail fast** znamená ukončit proces co nejdříve po zjištění kritické chyby.

```text

načtení vstupu

→ chybí povinný sloupec

→ okamžité ukončení

```

Proces nemá pokračovat do dalších výpočtů a vytvořit chybný report.

Typické kritické chyby:

- nedostupná povinná databáze;

- chybějící povinný soubor;

- chybějící klíčový sloupec;

- neplatný směnný kurz;

- chyba při zápisu;

- neúspěšná závěrečná validace.

Reakce:

```text

kritická chyba

→ zastavit závislé kroky

→ nepublikovat nový výstup

→ zapsat důvod chyby

→ označit proces jako FAILED

```

---

## 10. Idempotence

**Idempotence** znamená, že opakované spuštění procesu nad stejnými vstupy nezpůsobí nežádoucí změnu výsledného stavu.

### Neidempotentní zápis

```text

první spuštění

→ 1 000 řádků

druhé spuštění se stejnými daty

→ 2 000 řádků

```

Vznikly duplicity.

### Idempotentní zápis

```text

první spuštění

→ 1 000 řádků

druhé spuštění se stejnými daty

→ stále 1 000 správných řádků

```

Možné postupy:

- přepsat celý malý výstup;

- odstranit před novým zápisem data stejného období;

- aktualizovat existující záznamy;

- vkládat pouze nové záznamy;

- použít jednoznačný klíč;

- evidovat již zpracované vstupy.

### Opakovatelnost versus Idempotence

```text

Opakovatelnost

→ proces lze spustit znovu

Idempotence

→ opakované spuštění nepoškodí výsledný stav

```

---

## 11. Determinismus

**Deterministický proces** vytvoří při stejných vstupech a stejných pravidlech stejný výsledek.

```text

stejný vstup

+ stejný kód

+ stejná konfigurace

= stejný výsledek

```

Výsledek se může změnit například při použití:

- aktuálního data nebo času;

- aktuálních dat z API;

- náhodných hodnot;

- změněné konfigurace;

- změněného business pravidla;

- aktualizované databáze.

### Determinismus versus Idempotence

```text

Determinismus

→ stejné vstupy vytvoří stejné hodnoty

Idempotence

→ opakované spuštění nepoškodí cílový stav

```

Skript může být deterministický, ale ne idempotentní. Pokaždé například vypočítá stejný řádek, ale opakovaně jej připojí do cílové tabulky.

---

## 12. Reprodukovatelnost

**Reprodukovatelnost** znamená, že dokážeme proces znovu spustit za známých podmínek a vysvětlit vznik výsledku.

Potřebujeme znát například:

- použitý vstup;

- datum a čas načtení;

- verzi kódu;

- konfiguraci;

- transformační pravidla;

- počet vstupních a výstupních řádků;

- výsledek validace.

Základní metadata běhu:

```text

run_id

start_time

end_time

input_name

input_row_count

output_row_count

status

error_message

```

**Run ID** je jednoznačný identifikátor konkrétního spuštění procesu.

---

## 13. Rollback a zachování správného stavu

Při chybě není vždy potřeba vracet úplně celý proces do počátečního stavu. Cílem je především zachovat poslední známý správný stav.

### Chyba před zápisem

```text

načtení

→ validace selže

→ proces skončí

→ původní výstup zůstane beze změny

```

Žádný rollback není potřeba, protože se do cíle ještě nezapisovalo.

### Databázová transakce

```sql

BEGIN TRANSACTION;

-- změny v databázi

COMMIT;

```

Pokud operace selže:

```sql

ROLLBACK;

```

- `COMMIT` potvrdí změny;

- `ROLLBACK` zruší nepotvrzené změny v dané transakci.

### Bezpečný souborový výstup

```text

vytvořit dočasný soubor

→ validovat ho

→ po úspěchu nahradit oficiální výstup

```

Při chybě se nový soubor nepublikuje a poslední správná verze zůstane zachována.

### Více systémů

Pokud proces zapisuje do databáze, souboru a externí služby, jeden společný `ROLLBACK` obvykle nestačí. Mohou být potřeba samostatné kompenzační kroky.

---

## 14. Atomic publication — bezpečná publikace

**Atomic publication** znamená, že se nový výstup stane oficiálním až po úplném dokončení a ověření.

```text

1. načíst data

2. validovat vstupy

3. transformovat data

4. vytvořit pracovní výstup

5. validovat pracovní výstup

6. nahradit oficiální výstup

7. zapsat konečný stav

```

Při chybě:

```text

nový výstup

→ nepublikovat

poslední správný výstup

→ zachovat

```

Podobný princip lze použít v databázi:

```text

nová data

→ staging tabulka

→ validace

→ aktualizace cílové tabulky

```

---

## 15. Co je vhodné automatizovat

Proces je vhodným kandidátem, pokud:

- se pravidelně opakuje;

- používá podobně strukturované vstupy;

- má jasná pravidla;

- ruční provedení zabírá čas;

- při ruční práci vznikají chyby;

- výsledek je pravidelně potřebný;

- lze ověřit správné dokončení;

- existuje odpovědnost za případné selhání.

```text

každý den

→ stejné zdroje

→ stejné kontroly

→ stejné transformace

→ stejný typ výstupu

```

Automatizace nemusí být vhodná, pokud:

- jde o jednorázovou analýzu;

- vstup má pokaždé jinou strukturu;

- pravidla se stále mění;

- proces vyžaduje výrazný lidský úsudek;

- nelze definovat správný výsledek;

- náklady na automatizaci převýší přínos;

- automatické rozhodnutí představuje nepřiměřené riziko.

---

## 16. Human in the loop

**Human in the loop** znamená, že člověk zůstává součástí částečně automatizovaného procesu.

```text

automaticky

→ načíst data

→ validovat je

→ připravit výsledek

ručně

→ prověřit výjimky

→ schválit publikaci nebo rozhodnutí

```

Python může automaticky:

- vypočítat odchylku;

- označit neobvyklou hodnotu;

- připravit seznam ke kontrole.

Člověk může následně rozhodnout například o změně ceny, obchodním opatření nebo jiné významné business akci.

---

## 17. Kontrolní otázky před automatizací

### Business potřeba

1. Jaký problém má automatizace řešit?

2. Kdo potřebuje její výstup?

3. Jak často se proces opakuje?

4. Jak poznáme správný výsledek?

### Vstupy

1. Kde jsou data uložená?

2. Které vstupy jsou povinné?

3. Které vstupy jsou volitelné?

4. Kdy jsou zdroje dostupné?

5. Jak ověříme aktuálnost dat?

### Průběh

1. Jaké tasky proces obsahuje?

2. Které tasky mohou běžet paralelně?

3. Jaké jsou mezi nimi dependencies?

4. Co se má stát při selhání?

### Výstup

1. Má vzniknout soubor, databázová tabulka nebo datový model?

2. Budeme výstup přepisovat, nebo uchovávat historii?

3. Jak zabráníme duplicitám?

4. Jak zachováme poslední správnou verzi?

### Provoz

1. Co se zapíše do logu?

2. Kdo řeší chybu?

3. Lze proces bezpečně spustit znovu?

4. Jak uživatel pozná aktuálnost výsledku?

---

## 18. Základní návrh automatizovaného procesu

```text

Trigger

→ načtení vstupů

→ technická kontrola

→ datová validace

→ transformace

→ vytvoření pracovního výstupu

→ závěrečná validace

→ publikace

→ zápis konečného stavu

```

Chybová větev:

```text

kritická chyba

→ zastavit závislé úlohy

→ nepublikovat neplatný výstup

→ zachovat poslední správný stav

→ zapsat chybu

→ označit proces jako FAILED

```

---

## 19. Hlavní terminologie

- **Automation** – automatické provedení připraveného procesu;

- **Scheduling** – plánování času spuštění;

- **Trigger** – událost nebo podmínka zahajující proces;

- **Pipeline** – celý řízený datový tok;

- **Task** – jedna konkrétní úloha uvnitř pipeline;

- **Dependency** – závislost mezi úlohami;

- **Orchestration** – řízení pořadí, závislostí a chování úloh;

- **Idempotence** – bezpečné opakování bez poškození cílového stavu;

- **Determinismus** – stejné vstupy a pravidla vytvářejí stejný výsledek;

- **Reprodukovatelnost** – možnost proces zopakovat a vysvětlit jeho výsledek;

- **Fail fast** – ukončení procesu ihned po zjištění kritické chyby;

- **Rollback** – vrácení nepotvrzených databázových změn;

- **Commit** – potvrzení databázových změn;

- **Atomic publication** – zveřejnění výstupu až po úplném dokončení a kontrole;

- **Run ID** – jednoznačný identifikátor spuštění;

- **Human in the loop** – zapojení člověka do kontroly nebo rozhodnutí.

---

## 20. Jupyter Notebook versus Python skript

Jupyter Notebook i soubor `.py` používají Python, ale hodí se pro jiný způsob práce.

### Jupyter Notebook

Vhodný zejména pro:

- průzkum dat;
- postupnou analýzu;
- kombinaci kódu, výsledků a Markdown komentářů;
- prezentaci analytického postupu.

Notebook je stavové prostředí. Výsledek může záviset na pořadí, ve kterém byly buňky spuštěny.

### Python skript

Vhodný zejména pro:

- opakované zpracování;
- automatické spuštění bez obsluhy;
- pevně dané pořadí kroků;
- předvídatelný návratový stav.

V praxi se řešení často nejprve připraví a ověří v notebooku a stabilní proces se následně převede do skriptu.

---

## 21. Jednoduchá lokální automatizace

Základní architektura lokálního procesu může vypadat takto:

```text
Windows Task Scheduler
→ BAT soubor
→ Python skript
→ CSV a databáze
→ log
```

Jednotlivé části mají rozdílnou odpovědnost:

- **Windows Task Scheduler** určuje, kdy se proces spustí;
- **BAT soubor** připraví způsob spuštění a zavolá správný Python;
- **Python skript** provede načtení, validaci, transformaci a zápis;
- **databáze a soubor** uchovávají výsledky;
- **log** uchovává informace o průběhu a chybách.

Oddělení těchto odpovědností usnadňuje testování i hledání problému.

---

## 22. Windows Task Scheduler

**Windows Task Scheduler** neboli Plánovač úloh umožňuje spouštět programy podle nastaveného plánu.

### Základní části úlohy


- **General** určuje uživatelský účet a oprávnění;
- **Triggers** určují čas nebo událost spuštění;
- **Actions** určují, co se má spustit;
- **Conditions** stanovují další podmínky, například napájení nebo síť;
- **Settings** určují provozní chování úlohy.

### Praktická nastavení

Pro pravidelný lokální datový proces je obvykle vhodné:

- povolit ruční spuštění úlohy;
- spustit zmeškanou úlohu co nejdříve;
- nastavit maximální dobu běhu;
- při souběhu nespouštět novou instanci;
- nevyžadovat napájení ze sítě, pokud to není nutné;
- nevyžadovat síťové připojení pro čistě lokální proces.

Volba **Do not start a new instance** chrání proces před tím, aby současně běželo více jeho kopií.

Účet použitý Plánovačem musí mít přístup ke skriptu, vstupům, výstupům a databázi.

---

## 23. BAT soubor a běhové prostředí

**BAT soubor** je spouštěcí soubor systému Windows. V automatizaci může:

- nastavit pracovní složku;
- použít konkrétní Python interpreter;
- spustit Python skript;
- předat jeho návratový kód Plánovači úloh.

Pro automatické spouštění je bezpečnější používat úplné cesty. Proces potom není závislý na tom, ze které složky byl spuštěn.

### Virtuální prostředí

**Virtual environment** neboli virtuální prostředí odděluje Python a knihovny konkrétního projektu.

Plánovač nemá spoléhat na ruční aktivaci prostředí ve VS Code. BAT soubor proto přímo spouští Python uložený ve složce `.venv`.

### Závislosti

Automatizace vyžaduje také dostupné knihovny a systémové ovladače. Pro připojení Pythonu k SQL Serveru mohou být potřeba například:

- balíček `pyodbc` ve virtuálním prostředí;
- Microsoft ODBC Driver for SQL Server v operačním systému.

---

## 24. Validace automatizovaného vstupu

Automatický proces musí ověřit data ještě před vytvořením oficiálního výstupu.

Typické kontroly:

- zda byly nalezeny vstupní soubory;
- zda existují povinné sloupce;
- zda lze převést datum a číselné hodnoty;
- zda nechybí povinné hodnoty;
- zda nejsou porušena business pravidla;
- zda neexistují duplicitní klíče;
- zda datum uvnitř dat odpovídá zpracovávanému období.

Kontrola názvu souboru nestačí. Soubor může mít správné datum v názvu, ale obsahovat data za jiný den.

### Kritická a nekritická chyba

- Kritická chyba ukončí proces jako `FAILED`.
- Nekritický problém dovolí pokračovat, ale zapíše se jako `WARNING`.

Rozdělení musí vycházet z business pravidel. Chybějící povinný sloupec je typicky kritický, zatímco chybějící volitelný vstup může být pouze varováním.

---

## 25. Zpracovávané období

U pravidelného procesu má být jednoznačně určeno, za jaké období data zpracovává.

Příklad denního reportu:

```text
spuštění 13. září
→ zpracování dat za 12. září
```

Výběr vstupů podle data omezuje riziko, že se do jednoho běhu omylem smíchají soubory z různých dní.

Datum má být ověřeno:

- v názvu vstupního souboru;
- uvnitř načtených dat;
- v názvu nebo metadatech výstupu;
- při zápisu do databáze.

---

## 26. Logging a monitoring

**Logging** znamená průběžné zapisování informací o běhu procesu. **Monitoring** znamená sledování, zda proces běží správně a zda vyžaduje zásah.

### Úrovně logu

- `INFO` — běžný průběh procesu;
- `WARNING` — nekritický problém;
- `ERROR` — chyba, kvůli které proces selhal.

Log má zaznamenat zejména:

- začátek nového běhu;
- zpracovávané datum;
- počet nalezených souborů;
- počet načtených a uložených řádků;
- výsledek validace;
- vytvořený výstup;
- úspěšné dokončení nebo konkrétní chybu.

Samotný log ještě není plný monitoring. V podnikovém prostředí bývá doplněn upozorněním, dashboardem běhů nebo centrálním monitorovacím nástrojem.

---

## 27. Návratové kódy

**Exit code** neboli návratový kód sděluje operačnímu systému nebo Plánovači, jak proces skončil.

- `0` znamená úspěšné dokončení;
- nenulová hodnota, například `1`, znamená chybu.

Návratový kód není podrobný popis chyby. Podrobnosti patří do logu.

```text
návratový kód
→ rychlá informace pro Plánovač

log
→ podrobné vysvětlení průběhu a chyby
```

BAT soubor musí návratový kód Python skriptu správně předat dál. Jinak může Plánovač označit chybný běh jako úspěšný.

---

## 28. Bezpečný zápis do souboru a databáze

### Souborový výstup

Bezpečný postup:

```text
zapsat dočasný soubor
→ dokončit zápis
→ nahradit oficiální výstup
```

Tím se snižuje riziko, že po chybě zůstane neúplný oficiální soubor.

### Databázový výstup

Související databázové změny mají proběhnout v jedné transakci:

- při úspěchu `COMMIT`;
- při chybě `ROLLBACK`.

Opakované spuštění nad stejným obdobím nesmí vytvářet duplicity. Jedním z řešení je odstranit data daného období a poté vložit jejich novou ověřenou verzi v rámci jedné transakce.

Databázová omezení, například primární klíč nebo kontrola nezáporné hodnoty, tvoří další ochrannou vrstvu. Nenahrazují však validaci ve skriptu.

### Lineage

**Data lineage** označuje dohledatelnost původu dat. Praktickými metadaty mohou být:

- název zdrojového souboru;
- čas načtení;
- datum reportu;
- identifikátor běhu.

---

## 29. Lokální a produkční řešení

Kombinace Windows Task Scheduleru, BAT souboru, Pythonu a SQL Server LocalDB je vhodná pro:

- výuku;
- osobní projekt;
- portfolio;
- menší proces na jednom počítači.

Pro důležitý podnikový proces mohou být potřeba:

- centrální databáze nebo cloudové úložiště;
- správa přístupových údajů;
- automatické upozornění při chybě;
- centrální historie běhů;
- řízené nasazení nové verze;
- specializovaný orchestrační nástroj.

LocalDB je lokální vývojová databáze svázaná s konkrétním uživatelským prostředím. Není náhradou za produkční databázový server.

---

## 30. Rychlý provozní checklist

### Před automatizací

- Je jasné zpracovávané období?
- Jsou definované povinné vstupy?
- Jsou kritické a nekritické chyby rozlišené?
- Je proces idempotentní?

### Při nastavení

- Používá se správný Python a virtuální prostředí?
- Jsou cesty dostupné účtu Plánovače?
- Je nastavena správná pracovní složka?
- Je zakázáno souběžné spuštění více instancí?

### Při testování

- Projde proces se správnými vstupy?
- Selže řízeně při chybném vstupu?
- Vrací správný návratový kód?
- Zůstane při chybě zachován poslední správný výstup?
- Nevzniknou po opakovaném spuštění duplicity?

### Při provozu

- Je z logu poznat výsledek běhu?
- Je možné dohledat zdroj záznamů?
- Je určeno, kdo řeší chybu?
- Je proces po změně kódu znovu otestován?

---
