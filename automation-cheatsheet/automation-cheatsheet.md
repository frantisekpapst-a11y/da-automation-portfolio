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

## 20. Co si pamatovat

```text
Trigger
→ zahájí proces

Task
→ představuje jednu úlohu

Dependency
→ určuje závislost úloh

Scheduling
→ určuje čas spuštění

Automation
→ provede kroky bez ručního zásahu

Orchestration
→ koordinuje více úloh

Idempotence
→ chrání před nežádoucím výsledkem opakovaného spuštění

Determinismus
→ stejné vstupy vytvářejí stejný výsledek

Fail fast
→ zastaví proces při kritické chybě

Atomic publication
→ chrání poslední správný výstup
```

Hlavní zásada:

> Dobrá automatizace neznamená pouze automatické spuštění. Musí také ověřit vstupy, bezpečně reagovat na chybu, chránit poslední správný výstup a zaznamenat svůj výsledek.

## 21. Základní struktura cvičného projektu

```text
02-python-script-basics/
├── data/
│   ├── input/
│   └── output/
└── src/
    └── check_input.py
```

- `src` obsahuje zdrojový Python kód;
- `data/input` obsahuje očekávané vstupy;
- `data/output` obsahuje výstupy vytvořené skriptem.

---

## 22. Modul `pathlib` a objekt `Path`

```python
from pathlib import Path
```

`pathlib` je standardní Python modul pro práci s cestami k souborům a složkám. `Path` převádí textovou cestu na objekt cesty.

```python
file_path = Path(__file__)
```

Objekt `Path` umožňuje používat například:

- `.resolve()` – vytvoření jednoznačné absolutní cesty;
- `.parent` – získání nadřazené složky;
- `.exists()` – kontrola existence;
- `.mkdir()` – vytvoření složky;
- `.write_text()` – zápis textu do souboru.

---

## 23. `__file__`, `resolve()` a `parent`

`__file__` je speciální proměnná vytvořená Pythonem. Obsahuje cestu k aktuálnímu Python souboru.

Rozepsaná učící varianta:

```python
file_path = Path(__file__)
resolved_path = file_path.resolve()
script_dir = resolved_path.parent
```

Běžná zkrácená varianta:

```python
script_dir = Path(__file__).resolve().parent
```

Význam jednotlivých kroků:

```text
__file__
→ cesta k souboru jako text

Path(__file__)
→ objekt cesty

.resolve()
→ jednoznačná absolutní cesta

.parent
→ složka, ve které leží skript
```

Další `.parent` umožní přejít ze složky `src` do kořene projektu:

```python
base_dir = script_dir.parent
```

---

## 24. Pracovní složka versus složka skriptu

```python
current_dir = Path.cwd()
script_dir = Path(__file__).resolve().parent
```

- `Path.cwd()` vrací složku, ze které byl proces spuštěn;
- `script_dir` označuje složku, ve které skutečně leží Python skript.

Tyto složky nemusí být stejné. Při automatizaci proto odvozujeme cesty od `__file__`, nikoliv od aktuální pracovní složky.

```text
jiná pracovní složka
→ může se měnit podle způsobu spuštění

složka skriptu
→ zůstává stejná
```

---

## 25. Skládání cest

Jednotlivé části cesty spojujeme pomocí znaku `/`:

```python
input_dir = base_dir / "data" / "input"
output_dir = base_dir / "data" / "output"
```

U objektu `Path` znak `/` neznamená dělení. Slouží ke skládání cest a Python použije správný oddělovač pro daný operační systém.

---

## 26. Kontrola vstupní složky

```python
input_exists = input_dir.exists()
```

Metoda `.exists()` vrací:

- `True`, pokud cesta existuje;
- `False`, pokud cesta neexistuje.

Chybějící vstupní složku můžeme považovat za kritickou chybu:

```python
if not input_dir.exists():
    print("Vstupní složka neexistuje.")
    return 1
```

Tento způsob zápisu kontroluje chybový stav jako první. Jde o **guard clause**, tedy vstupní kontrolu, která při kritickém problému funkci včas ukončí.

---

## 27. Vytvoření výstupní složky

```python
output_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

- `parents=True` dovolí vytvořit také chybějící nadřazené složky;
- `exist_ok=True` zabrání chybě, pokud už složka existuje.

Vstupní složku očekáváme od zdroje dat, proto její chybějící stav kontrolujeme. Výstupní složku spravuje náš proces, proto ji může bezpečně vytvořit.

---

## 28. Funkce `main()`

```python
def main():
    # jednotlivé kroky procesu
    return 0
```

`main()` je běžná konvence pro hlavní funkci, která řídí pořadí celého procesu. Název není v Pythonu povinný ani speciální.

Funkce může například koordinovat:

```text
určení cest
→ kontrolu vstupu
→ vytvoření výstupní složky
→ vytvoření výstupu
→ vrácení výsledného stavu
```

---

## 29. `__name__` a přímé spuštění

```python
if __name__ == "__main__":
    result = main()
```

`__name__` je speciální proměnná vytvořená Pythonem.

| Způsob použití souboru | Hodnota `__name__` | Automatické spuštění `main()` |
|---|---|---|
| Přímé spuštění souboru | `"__main__"` | Ano |
| Import do jiného souboru | název modulu, například `"check_input"` | Ne |

Podmínka chrání hlavní proces před nechtěným spuštěním při importu souboru.

Import pouze zpřístupní obsah modulu:

```python
import check_input
```

Funkci lze následně spustit záměrně:

```python
check_input.main()
```

---

## 30. Návratové kódy a `sys.exit()`

```python
import sys
```

Funkce `main()` vrací stav procesu:

```python
return 0
```

znamená úspěšné dokončení.

```python
return 1
```

znamená chybu.

`sys.exit()` předá návratovou hodnotu operačnímu systému:

```python
result = main()
sys.exit(result)
```

Běžná zkrácená varianta:

```python
sys.exit(main())
```

Poslední návratový kód lze v PowerShellu ověřit:

```powershell
$LASTEXITCODE
```

Základní konvence:

```text
0
→ úspěch

nenulová hodnota
→ chyba
```

---

## 31. Jednoduchý textový výstup

Cestu k souboru vytvoříme stejně jako cestu ke složce:

```python
output_file = output_dir / "check_result.txt"
```

Text zapíšeme metodou `.write_text()`:

```python
output_file.write_text(
    "Kontrola byla úspěšná. Vstupní složka existuje.",
    encoding="utf-8"
)
```

Pokud soubor neexistuje, metoda ho vytvoří. Pokud existuje, jeho původní obsah nahradí.

---

## 32. Učící a běžná verze kódu

Učící verze používá pomocné proměnné a `print()` pro zobrazení mezikroků:

```python
file_path = Path(__file__)
resolved_path = file_path.resolve()
script_dir = resolved_path.parent
```

Běžná verze stejnou logiku zkracuje:

```python
script_dir = Path(__file__).resolve().parent
```

Učící verze pomáhá pochopit postup. Běžná verze je přehlednější pro standardní provoz. Pokud jsou obě varianty uložené v jednom souboru, aktivně se má volat pouze jedna z nich, aby se proces nespustil dvakrát.

---

## 33. Základní tok skriptu

```text
přímé spuštění souboru
→ zavolání main()
→ určení cest
→ kontrola vstupní složky
→ vytvoření výstupní složky
→ vytvoření výstupního souboru
→ return 0 nebo return 1
→ sys.exit()
→ předání výsledku operačnímu systému
```

---

## 34. Hlavní poznatky Lekce 2

- notebook je vhodný pro průzkum a vývoj, skript pro opakovatelný provoz;
- `Path` umožňuje pracovat s cestami jako s objekty;
- cesty při automatizaci odvozujeme od `__file__`;
- `Path.cwd()` a složka skriptu mohou být rozdílné;
- vstupní složku kontrolujeme, výstupní složku může skript vytvořit;
- `main()` koordinuje celý proces;
- blok `if __name__ == "__main__":` rozlišuje přímé spuštění a import;
- návratový kód `0` znamená úspěch;
- nenulový návratový kód znamená chybu;
- `sys.exit()` předává návratový kód operačnímu systému.

