# Automation Cheatsheet

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

## 35. Základní datový tok

```text
API

→ Python odešle HTTP požadavek

→ odpověď se uloží jako raw JSON

→ JSON se převede na Python objekty

→ data se zkontrolují a normalizují

→ výsledek se uloží do CSV
```

---

## 36. API endpoint

Endpoint je konkrétní adresa, na kterou Python posílá požadavek.

```python
API_URL = "https://api.github.com/repos/pandas-dev/pandas/issues"
```

V této lekci používáme metodu `GET`, protože z API data získáváme.

---

## 37. Odeslání GET požadavku

```python
response = requests.get(
    API_URL,
    params=params,
    timeout=10
)
```

- `API_URL` určuje adresu API;
- `params` obsahuje parametry požadavku;
- `timeout=10` ukončí čekání, pokud API včas neodpoví.

---

## 38. Parametry požadavku

```python
params = {
    "state": "all",
    "per_page": PER_PAGE,
    "page": page
}
```

Parametry upravují požadavek bez ručního skládání celé URL.

---

## 39. HTTP status

HTTP status informuje, jak požadavek dopadl.

| Status | Význam |
|---:|---|
| `200` | požadavek byl úspěšný |
| `404` | požadovaný zdroj nebyl nalezen |
| `429` | byl překročen povolený počet požadavků |
| `500–599` | chyba na straně serveru |

```python
if response.status_code != 200:
    print("Chyba HTTP:", response.status_code)
    return 1
```

---

## 40. Timeout a komunikační chyba

Timeout zabraňuje tomu, aby skript čekal na odpověď neomezeně dlouho.

```python
try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=10
    )
except requests.RequestException as error:
    print("Chyba při komunikaci s API:", error)
    return 1
```

`RequestException` zachytí například timeout nebo problém s připojením.

---

## 41. Pagination

Pagination znamená, že API rozděluje větší množství dat na stránky.

```python
for page in range(1, MAX_PAGES + 1):
    params = {
        "state": "all",
        "per_page": PER_PAGE,
        "page": page
    }
```

Při `MAX_PAGES = 3` stáhneme stránky `1`, `2` a `3`.

---

## 42. Spojení záznamů ze stránek

```python
all_records = []

all_records.extend(page_data)
```

Metoda `extend()` přidá jednotlivé záznamy ze stránky do společného seznamu.

---

## 43. Rate limit

Rate limit omezuje počet požadavků, které můžeme za určitou dobu odeslat.

```python
remaining = response.headers.get(
    "X-RateLimit-Remaining",
    "neuvedeno"
)
```

Hodnota `X-RateLimit-Remaining` ukazuje počet zbývajících požadavků.

---

## 44. Uložení původní odpovědi

Raw data jsou původní data přesně v podobě, v jaké je API poslalo.

```python
raw_file.write_text(
    response.text,
    encoding="utf-8"
)
```

Raw odpověď pomáhá při kontrole, ladění a opakovaném zpracování dat.

---

## 45. Timestamp načtení

Timestamp zaznamenává, kdy byla data získána.

```python
downloaded_at = datetime.now(timezone.utc)
timestamp = downloaded_at.strftime("%Y%m%d_%H%M%S")
```

Je možné jej použít v názvu raw souboru i jako sloupec ve výsledných datech.

---

## 46. Převod JSON odpovědi

```python
page_data = response.json()
```

Metoda `.json()` převede JSON odpověď na Python objekty:

- JSON pole se obvykle převede na `list`;
- JSON objekt se obvykle převede na `dict`.

---

## 47. Kontrola základní struktury odpovědi

Nejdříve ověříme, zda API vrátilo očekávaný seznam.

```python
if not isinstance(page_data, list):
    print("Odpověď API nemá očekávanou strukturu.")
    return 1
```

Pokud očekáváme seznam záznamů a získáme jiný typ, proces bezpečně ukončíme.

---

## 48. Kontrola neúplné odpovědi

```python
required_keys = {
    "id",
    "number",
    "title",
    "state",
    "user",
    "created_at",
    "updated_at",
    "html_url"
}

missing_keys = required_keys - record.keys()
```

Pokud `missing_keys` není prázdné, záznam neobsahuje všechny povinné klíče.

---

## 49. Vnořená data v JSON

Hodnota pod jedním klíčem může obsahovat další objekt nebo seznam.

```python
record["user"]["login"]
```

V tomto příkladu je `user` vnořený objekt a `login` je jeho položka.

---

## 50. Normalizace JSON

```python
dataframe = pd.json_normalize(all_records)
```

`json_normalize()` převede seznam JSON objektů na tabulku a zpřístupní vnořené hodnoty například jako `user.login`.

---

## 51. Výběr sloupců

Z API nemusíme ukládat všechny dostupné položky.

```python
selected_columns = [
    "id",
    "number",
    "title",
    "state",
    "user.login",
    "created_at",
    "updated_at",
    "html_url"
]

result_df = dataframe[selected_columns].copy()
```

Výsledný dataset tak obsahuje pouze sloupce potřebné pro další analýzu.

---

## 52. Validace výsledku

Před exportem kontrolujeme zejména:

- zda výsledek není prázdný;
- zda existují povinné sloupce;
- zda v povinných sloupcích nechybějí hodnoty;
- zda se neopakují hodnoty, které mají být jedinečné.

```python
if result_df.empty:
    print("Výsledná data jsou prázdná.")
    return 1

if result_df["number"].duplicated().any():
    print("Výsledná data obsahují duplicity.")
    return 1
```

---

## 53. Export do CSV

```python
result_df.to_csv(
    output_file,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)
```

- `sep=";"` nastaví oddělovač;
- `index=False` neuloží index DataFrame;
- `utf-8-sig` usnadní správné zobrazení češtiny v Excelu.

---

## 54. Řízené ukončení

```python
if __name__ == "__main__":
    result = main()
    sys.exit(result)
```

- `return 0` znamená úspěch;
- `return 1` znamená chybu;
- `sys.exit()` předá návratový kód operačnímu systému.

---

## 55. Pravidelné stahování dat

Skript je připravený na opakované spouštění, protože při každém běhu:

- kontaktuje API;
- stáhne aktuální data;
- uloží raw odpovědi;
- provede validaci;
- vytvoří nový výstup.

Samotné časové plánování pomocí Windows Task Scheduleru patří do pozdější lekce.

---

## 56. Retry – základní princip

Retry znamená opakování požadavku po dočasné chybě, například po timeoutu, statusu `429` nebo chybě serveru `500–599`.

Má mít:

- omezený počet pokusů;
- krátkou prodlevu mezi pokusy;
- ukončení po vyčerpání pokusů.

Retry jsme ve finálním kódu Lekce 3 záměrně nepoužili. Nejprve upevňujeme základní tok jednoho požadavku a zpracování odpovědi.

---

## 57. Základní tok skriptu

```text
přímé spuštění souboru

→ zavolání main()

→ určení výstupních cest a timestampu

→ odeslání GET požadavku s timeoutem

→ kontrola HTTP statusu a rate limitu

→ uložení raw odpovědi

→ převod JSON na Python objekty

→ kontrola struktury odpovědi

→ opakování pro další stránky

→ spojení všech záznamů

→ normalizace do DataFrame

→ validace výsledku

→ export do CSV

→ return 0 nebo return 1

→ sys.exit()
```

---

## 58. Hlavní poznatky Lekce 3

- API umožňuje programu získávat data z jiné aplikace nebo služby;
- metoda `GET` slouží ke čtení dat;
- HTTP status informuje o výsledku požadavku;
- timeout omezuje dobu čekání na odpověď;
- pagination rozděluje větší výsledek na více stránek;
- rate limit omezuje počet požadavků;
- raw odpověď uchovává původní podobu získaných dat;
- timestamp zaznamenává čas načtení;
- JSON se v Pythonu převádí hlavně na `list` a `dict`;
- před zpracováním kontrolujeme typ odpovědi a povinné klíče;
- `pd.json_normalize()` převádí vnořený JSON na tabulku;
- před exportem ověřujeme úplnost, prázdné hodnoty a duplicity;
- výsledek lze uložit jako CSV nebo JSON;
- `return 0`, `return 1` a `sys.exit()` umožňují řízené ukončení procesu;
- retry patří mezi užitečné rozšíření, ale není součástí základního finálního kódu této lekce.

---

## 59. Datový tok Lekce 4

```text
CSV z Lekce 3
→ Pandas
→ příprava dat
→ SQL Server LocalDB
→ SQL dotaz
→ Pandas
→ Excel
```

---

## 60. SQL Server, LocalDB a SSMS

- **SQL Server** je databázový systém, který ukládá a zpracovává data;
- **LocalDB** je lehká lokální varianta SQL Serveru;
- **SSMS** nebo rozšíření MSSQL ve VS Code je klient pro práci s databází;
- Python se připojuje přímo k SQL Serveru přes `pyodbc` a ODBC ovladač.

---

## 61. Systémová a uživatelská databáze

- `master` je systémová databáze SQL Serveru;
- používá se například při vytváření nové databáze;
- `automation_lesson_04` je naše databáze pro Lekci 4;
- `automation_practice` je jiná, dříve vytvořená databáze.

---

## 62. Vytvoření databáze

```sql
IF DB_ID('automation_lesson_04') IS NULL
    CREATE DATABASE automation_lesson_04;
GO

USE automation_lesson_04;
```

`DB_ID()` vrátí identifikátor databáze. Pokud databáze neexistuje, vrátí `NULL`.

---

## 63. Význam příkazu `GO`

- `GO` odděluje skupiny SQL příkazů neboli **batche**;
- není příkazem jazyka T-SQL, ale pokynem pro SQL klienta;
- po vytvoření databáze umožní v následujícím batchi použít `USE`;
- není nutné ho psát mezi každý SQL příkaz.

---

## 64. `BEGIN` a `END`

```sql
IF podmínka
BEGIN
    příkaz_1;
    příkaz_2;
END;
```

`BEGIN` a `END` spojují více příkazů do jednoho bloku.

Sami o sobě nevytvářejí databázovou transakci. Pokud má podmínka jen jeden příkaz, nejsou nutné.

---

## 65. Základní datové typy v SQL Serveru

| Datový typ | Typické použití |
|---|---|
| `INT` | běžná celá čísla a identifikátory |
| `BIGINT` | velmi velká celá čísla, například ID z API |
| `NVARCHAR(n)` | text včetně českých znaků |
| `DATETIME2` | datum a čas |

Datový typ by měl odpovídat významu a rozsahu ukládané hodnoty.

---

## 66. Primární a cizí klíč

- `PRIMARY KEY` jednoznačně identifikuje řádek tabulky;
- nesmí obsahovat duplicity ani hodnotu `NULL`;
- `FOREIGN KEY` propojuje záznam s primárním klíčem jiné tabulky;
- pomáhá udržet platné vztahy mezi tabulkami.

```text
repositories.repository_id
→ github_issues.repository_id
```

---

## 67. Automaticky generované ID

```sql
repository_id INT IDENTITY PRIMARY KEY
```

`IDENTITY` zajistí automatické číslování nových řádků.

Zápis `IDENTITY(1,1)` výslovně určuje:

- první hodnota bude `1`;
- každá další hodnota se zvýší o `1`.

U SQL Serveru jsou to výchozí hodnoty, proto v tomto případě stačí i samotné `IDENTITY`.

---

## 68. Textové hodnoty v SQL

```sql
WHERE repository_owner = 'pandas-dev'
```

- textové hodnoty se zapisují do jednoduchých uvozovek;
- názvy tabulek a sloupců se do jednoduchých uvozovek nepíšou;
- prefix `N`, například `N'Plzeň'`, označuje Unicode text;
- u hodnoty `'pandas-dev'` prefix `N` nepotřebujeme.

---

## 69. Bezpečné vytvoření tabulky

```sql
IF OBJECT_ID('dbo.repositories', 'U') IS NULL
    CREATE TABLE dbo.repositories
    (
        repository_id INT IDENTITY PRIMARY KEY,
        repository_owner NVARCHAR(100) NOT NULL,
        repository_name NVARCHAR(200) NOT NULL
    );
```

`OBJECT_ID()` ověří existenci objektu a `'U'` označuje uživatelskou tabulku.

---

## 70. Ruční vytvoření tabulky versus Python

- tabulku může vytvořit SQL skript i Python;
- databázové schéma se v praxi často spravuje samostatnými SQL skripty;
- Python potom pracuje s již připravenou tabulkou;
- toto rozdělení zpřehledňuje odpovědnost jednotlivých částí procesu.

---

## 71. Připojení Pythonu k SQL Serveru

```python
import pyodbc

connection = pyodbc.connect(CONNECTION_STRING)
```

Knihovna `pyodbc` zprostředkuje komunikaci mezi Pythonem a SQL Serverem prostřednictvím ODBC ovladače.

---

## 72. Connection string

```python
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=(localdb)\\DataAnalyticsLocalDB;"
    "DATABASE=automation_lesson_04;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
```

Connection string určuje:

- použitý ODBC ovladač;
- instanci SQL Serveru;
- cílovou databázi;
- způsob přihlášení;
- nastavení důvěryhodnosti certifikátu.

---

## 73. Cursor a provedení SQL příkazu

```python
cursor = connection.cursor()

cursor.execute("SELECT DB_NAME()")

database_name = cursor.fetchone()[0]
```

- **cursor** odesílá SQL příkazy databázi a čte výsledky;
- `execute()` provede SQL příkaz;
- `fetchone()` načte jeden řádek výsledku;
- `[0]` vybere první hodnotu z načteného řádku.

---

## 74. Načtení CSV do Pandas

```python
dataframe = pd.read_csv(
    input_file,
    sep=";",
    encoding="utf-8-sig"
)
```

Před zápisem do databáze jsme:

- načetli CSV do DataFrame;
- přejmenovali sloupce podle databázového schématu;
- převedli datumové sloupce;
- odstranili časovou zónu kvůli typu `DATETIME2`;
- seřadili sloupce podle SQL příkazu `INSERT`.

---

## 75. Přejmenování sloupců

```python
dataframe = dataframe.rename(
    columns={
        "id": "issue_id",
        "number": "issue_number",
        "user.login": "user_login",
        "downloaded_at_utc": "downloaded_at"
    }
)
```

Přejmenováním sjednotíme názvy z CSV s názvy sloupců v databázi.

---

## 76. Převod data a času

```python
for column in [
    "created_at",
    "updated_at",
    "downloaded_at"
]:
    dataframe[column] = (
        pd.to_datetime(
            dataframe[column],
            utc=True
        )
        .dt.tz_localize(None)
    )
```

- `pd.to_datetime()` převede hodnoty na datum a čas;
- `utc=True` správně interpretuje čas jako UTC;
- `tz_localize(None)` odstraní informaci o časové zóně;
- výsledek lze uložit do SQL typu `DATETIME2`.

---

## 77. Pořadí databázových sloupců

```python
database_columns = [
    "issue_id",
    "repository_id",
    "issue_number",
    "title",
    "state",
    "user_login",
    "created_at",
    "updated_at",
    "html_url",
    "downloaded_at"
]

dataframe = dataframe[database_columns]
```

Pořadí hodnot musí odpovídat pořadí sloupců v SQL příkazu `INSERT`.

---

## 78. Převod dat pro hromadný zápis

```python
records = list(
    dataframe.itertuples(
        index=False,
        name=None
    )
)
```

`itertuples()` převede řádky DataFrame na n-tice hodnot, které lze předat metodě `executemany()`.

---

## 79. Parametrizovaný SQL příkaz

```python
cursor.execute(
    """
    DELETE FROM dbo.github_issues
    WHERE repository_id = ?
    """,
    1
)
```

- otazník `?` je zástupný symbol pro hodnotu;
- skutečná hodnota se předává odděleně;
- parametrizace správně ošetřuje hodnoty a datové typy;
- hodnoty nevkládáme do SQL příkazu skládáním textu.

---

## 80. Hromadné vložení záznamů

```python
cursor.executemany(
    insert_sql,
    records
)
```

`executemany()` provede stejný parametrizovaný SQL příkaz pro více záznamů.

Je vhodnější než ruční volání `execute()` pro každý řádek zvlášť.

---

## 81. `commit()` a `rollback()`

```python
connection.commit()
```

- `commit()` potvrdí změny a trvale je uloží;
- `rollback()` vrátí nepotvrzené změny při chybě;
- používají se pro základní řízení databázové transakce.

```python
if connection is not None:
    connection.rollback()
```

---

## 82. Bezpečné uzavření spojení

```python
finally:
    if connection is not None:
        connection.close()
```

Blok `finally` se provede při úspěchu i při chybě.

Databázové spojení se proto uzavře také tehdy, když funkce skončí pomocí `return`.

---

## 83. `JOIN` mezi tabulkami

```sql
SELECT
    r.repository_owner,
    r.repository_name,
    i.issue_number,
    i.title,
    i.state
FROM dbo.github_issues i
JOIN dbo.repositories r
    ON i.repository_id = r.repository_id;
```

- `JOIN` bez dalšího označení znamená `INNER JOIN`;
- vrací řádky, které mají odpovídající klíč v obou tabulkách;
- `LEFT JOIN` zachová všechny řádky z levé tabulky;
- pro běžnou práci analytika jsou nejdůležitější `JOIN` a `LEFT JOIN`.

---

## 84. Načtení SQL výsledku do Pandas

```python
report_df = pd.read_sql_query(
    report_query,
    connection
)
```

Výsledek SQL dotazu se načte do DataFrame.

S výsledkem můžeme dále pracovat v Pythonu nebo ho exportovat.

---

## 85. Export více tabulek do jednoho Excelu

```python
with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:
    report_df.to_excel(
        writer,
        sheet_name="Issues",
        index=False
    )

    summary_df.to_excel(
        writer,
        sheet_name="State summary",
        index=False
    )
```

`ExcelWriter` umožňuje uložit více DataFrame do různých listů jednoho souboru.

Knihovna `openpyxl` zajišťuje vytvoření souboru `.xlsx`.

---

## 86. Kontrola balíčků ve virtuálním prostředí

Výpis nainstalovaných balíčků:

```powershell
python -m pip list
```

Ověření používaného Python interpreteru:

```powershell
python -c "import sys; print(sys.executable)"
```

Instalace chybějícího balíčku:

```powershell
python -m pip install openpyxl
```

Použití `python -m pip` pomáhá zajistit, že balíček instalujeme ke stejnému Pythonu, kterým spouštíme skript.

---

## 87. Rozdělení práce mezi SQL a Python

### SQL je vhodné pro

- tabulky, klíče a vztahy;
- filtrování databázových dat;
- spojování tabulek;
- agregace;
- ukládání a kontrolu integrity dat.

### Python je vhodný pro

- práci se soubory;
- načítání a přípravu dat v Pandas;
- řízení celého procesu;
- komunikaci mezi různými zdroji;
- export výsledku do Excelu.

---

## 88. Hlavní tok Python skriptu

```text
určení cest
→ kontrola vstupního CSV
→ vytvoření výstupní složky
→ načtení CSV do Pandas
→ přejmenování sloupců
→ převod datových typů
→ připojení k SQL Serveru
→ odstranění starého snímku dat
→ vložení aktuálních řádků
→ commit
→ SQL dotaz s JOIN
→ načtení výsledku do Pandas
→ export do Excelu
→ uzavření databázového spojení
→ návratový kód 0 nebo 1
```

---

## 89. Hlavní poznatky Lekce 4

- SQL Server je databázový systém, zatímco SSMS nebo VS Code jsou klientské nástroje;
- LocalDB umožňuje pracovat se SQL Serverem lokálně;
- primární klíč identifikuje řádek;
- cizí klíč propojuje tabulky;
- Python se připojuje přes `pyodbc` a ODBC ovladač;
- hodnoty do SQL předáváme parametrizovaně;
- `executemany()` slouží k hromadnému vložení záznamů;
- `commit()` změny potvrdí;
- `rollback()` nepotvrzené změny při chybě vrátí;
- `finally` zajistí uzavření databázového spojení;
- SQL připraví relační výsledek;
- Pandas může výsledek exportovat do Excelu;
- `openpyxl` je potřeba pro vytvoření souboru `.xlsx`.¨

---

## 90. Datový tok Lekce 5

```text
načtení vstupu
→ validate_structure()
→ clean_data()
→ validate_data()
→ zápis do databáze
→ vytvoření Excelu
→ návratový kód procesu
```

---

## 91. Rozdělení odpovědnosti funkcí

```python
validate_structure(dataframe)
```

Ověří, zda lze s daty bezpečně začít pracovat.

```python
clean_data(dataframe)
```

Vyčistí data a vrátí nový DataFrame.

```python
validate_data(dataframe)
```

Ověří kvalitu vyčištěných dat.

```python
main()
```

Řídí pořadí celého procesu a vrací návratový kód `0` nebo `1`.

---

## 92. Kontrola povinných sloupců

```python
missing_columns = []

for column in REQUIRED_COLUMNS:
    if column not in dataframe.columns:
        missing_columns.append(column)
```

- `dataframe.columns` obsahuje názvy sloupců DataFrame;
- chybějící názvy ukládáme do seznamu `missing_columns`;
- pokud některý povinný sloupec chybí, proces se zastaví.

---

## 93. Kontrola prázdného DataFrame

```python
if dataframe.empty:
    print("Vstupní data neobsahují žádné řádky.")
    return False
```

Atribut `.empty` vrací `True`, pokud DataFrame neobsahuje žádné datové řádky.

---

## 94. Proč validovat strukturu před čištěním

Funkce pro čištění používá konkrétní sloupce. Pokud by některý chyběl, cleaning by skončil Python chybou.

```text
kontrola struktury
→ potvrzení očekávaných sloupců
→ bezpečné zahájení čištění
```

---

## 95. Cleaning a validace

- **cleaning** data opravuje nebo standardizuje;
- **validace** kontroluje, zda data splňují stanovená pravidla;
- kritická validační chyba proces zastaví;
- bezpečně ošetřitelná situace může skončit pouze varováním.

---

## 96. Čištění pracovní kopie

```python
clean_dataframe = dataframe.copy()
```

Čištění provádíme na kopii původního DataFrame. Vyčištěnou kopii funkce vrátí:

```python
return clean_dataframe
```

V `main()` ji převezmeme:

```python
dataframe = clean_data(dataframe)
```

---

## 97. Text cleaning

```python
for column in text_columns:
    clean_dataframe[column] = (
        clean_dataframe[column].str.strip()
    )
```

`.str.strip()` odstraní mezery na začátku a konci textu.

```python
clean_dataframe["state"] = (
    clean_dataframe["state"].str.lower()
)
```

`.str.lower()` sjednotí text na malá písmena.

---

## 98. Prázdný text a chybějící hodnota

```python
clean_dataframe[column] = (
    clean_dataframe[column].replace("", pd.NA)
)
```

Po odstranění mezer může zůstat prázdný text `""`. Pomocí `pd.NA` ho označíme jako chybějící hodnotu.

---

## 99. Povinná a nepovinná hodnota

- chybějící povinnou hodnotu nevymýšlíme a proces zastavíme;
- nepovinnou hodnotu můžeme ponechat prázdnou nebo bezpečně doplnit;
- v našem projektu je `user_login` nepovinný.

```python
clean_dataframe["user.login"] = (
    clean_dataframe["user.login"].fillna("unknown")
)
```

---

## 100. Odstranění identických řádků

```python
clean_dataframe = clean_dataframe.drop_duplicates()
```

Bez parametru `subset` porovnává `drop_duplicates()` všechny sloupce a odstraní pouze úplně stejné řádky.

Počet odstraněných řádků:

```python
removed_duplicates = row_count_before - row_count_after
```

---

## 101. Převod čísel s `errors="coerce"`

```python
clean_dataframe[column] = pd.to_numeric(
    clean_dataframe[column],
    errors="coerce"
)
```

```text
platná číselná hodnota
→ číslo

neplatná číselná hodnota
→ NaN
```

Následná validace hodnotu `NaN` zachytí jako chybu.

---

## 102. Převod data a času

```python
clean_dataframe[column] = (
    pd.to_datetime(
        clean_dataframe[column],
        errors="coerce",
        utc=True
    )
    .dt.tz_localize(None)
)
```

Neplatné datum se při použití `errors="coerce"` převede na `NaT`.

---

## 103. Kontrola povinných hodnot

```python
missing_count = dataframe[column].isna().sum()

if missing_count > 0:
    return False
```

`.isna().sum()` spočítá hodnoty `NaN`, `NA` a `NaT`. Pokud chybí povinná hodnota, data nesmějí pokračovat do databáze.

---

## 104. Kontrola duplicitního primárního klíče

```python
duplicate_id_count = (
    dataframe["issue_id"].duplicated().sum()
)

if duplicate_id_count > 0:
    return False
```

`issue_id` je primární klíč, proto musí být vyplněný a unikátní.

Rozdíl:

```text
drop_duplicates()
→ odstraní úplně stejné řádky

duplicated() na issue_id
→ odhalí opakovaný primární klíč
```

---

## 105. Ochrana klíčů v Pythonu a SQL

```text
Python
→ včasná kontrola prázdných a duplicitních klíčů

SQL Server
→ konečná ochrana pomocí PRIMARY KEY a FOREIGN KEY
```

Pokud odkazované `repository_id` neexistuje, SQL Server vložení odmítne.

---

## 106. `True`, `False`, `0` a `1`

Validační funkce odpovídají na otázku, zda jsou data platná:

```python
True   # data jsou platná
False  # data nejsou platná
```

Funkce `main()` vrací stav celého procesu:

```python
0  # úspěch
1  # chyba
```

---

## 107. `return` a `sys.exit()`

- `return` ukončí právě běžící funkci a vrátí hodnotu volajícímu;
- `sys.exit()` ukončí celý skript a předá návratový kód operačnímu systému.

```python
result = main()
sys.exit(result)
```

---

## 108. Kritická chyba a varování

| Situace | Reakce |
|---|---|
| Chybí povinný sloupec | zastavit proces |
| Dataset je prázdný | zastavit proces |
| Chybí primární klíč | zastavit proces |
| Primární klíč je duplicitní | zastavit proces |
| Databáze není dostupná | zastavit proces |
| Chybí nepovinný `user_login` | doplnit nebo pokračovat |
| Byl odstraněn identický řádek | oznámit a pokračovat |

Kritická chyba může způsobit nesprávný výsledek nebo porušit integritu dat.

---

## 109. `try`, `except` a `finally`

```text
try
→ pokus o provedení procesu

except
→ zachycení a ošetření očekávané chyby

finally
→ úklid, který proběhne při úspěchu i chybě
```

V našem skriptu `finally` zajišťuje uzavření databázového spojení.

---

## 110. `commit()` a `rollback()`

```python
connection.commit()
```

`commit()` trvale potvrdí databázové změny.

```python
connection.rollback()
```

`rollback()` vrátí nepotvrzené změny při chybě.

---

## 111. Bezpečná publikace

```text
načtení úspěšné
+ čištění úspěšné
+ validace úspěšná
+ databázové zpracování úspěšné
+ výstup vytvořený
= proces úspěšně dokončen
```

Neplatná data se nesmějí dostat do publikační části procesu.

V našem skriptu potvrzujeme databázové změny až po úspěšném vytvoření Excelu:

```python
connection.commit()
```

---

## 112. Zachování posledního správného výstupu

Pokud validace selže před zápisem:

```text
databáze se nezmění
→ Excel se nepřepíše
→ poslední správný výstup zůstane zachován
```

Pokročilejší řešení může nejdříve vytvořit dočasný soubor a původní výstup nahradit až po úspěšné kontrole.

---

## 113. Základní tok validačního procesu

```text
kontrola existence vstupu
→ načtení CSV
→ kontrola povinných sloupců
→ kontrola neprázdného datasetu
→ text cleaning
→ převod prázdných textů na NA
→ odstranění identických řádků
→ převod čísel a datumů
→ přejmenování sloupců
→ kontrola povinných hodnot
→ kontrola duplicitního issue_id
→ zápis do SQL Serveru
→ vytvoření Excelu
→ commit nebo rollback
→ uzavření spojení
→ návratový kód 0 nebo 1
```

---

## 114. Hlavní poznatky Lekce 5

- strukturu vstupu kontrolujeme před čištěním;
- cleaning a validace mají rozdílnou odpovědnost;
- vyčištěný DataFrame vracíme zpět do `main()`;
- neplatné hodnoty lze pomocí `errors="coerce"` převést na `NaN` nebo `NaT`;
- povinné hodnoty nesmějí být prázdné;
- primární klíč musí být unikátní;
- validační funkce vracejí `True` nebo `False`;
- `main()` vrací stav procesu `0` nebo `1`;
- kritická chyba proces zastaví, varování může umožnit pokračování;
- `rollback()` chrání databázi při chybě;
- poslední správný výstup se nemá přepsat neplatnými daty.

---

# Lekce 6 – Logging a monitoring

## 115. K čemu slouží logging

Modul `logging` vytváří trvalé záznamy o průběhu skriptu.

Umožňuje zaznamenat:

- datum a čas události;
- úroveň zprávy;
- zahájení a dokončení procesu;
- počty zpracovaných řádků;
- výsledky validace;
- vytvořené výstupy;
- chyby.

```python
import logging
```

Modul `logging` je součástí Pythonu a nemusí se instalovat přes `pip`.

---

## 116. Print a logging

```python
print("Proces byl zahájen.")
```

`print()` zobrazí zprávu během aktuálního spuštění skriptu.

```python
logging.info("Proces byl zahájen.")
```

`logging.info()` může zprávu trvale uložit do logovacího souboru.

```text
print()
→ okamžitá informace v terminálu

logging
→ trvalý záznam o průběhu procesu
```

---

## 117. Složka a soubor pro log

```python
logs_dir = base_dir / "logs"
log_file = logs_dir / "github_issues.log"
```

- `logs_dir` obsahuje cestu ke složce s logy;
- `log_file` obsahuje cestu ke konkrétnímu logovacímu souboru.

Tyto řádky pouze sestavují cesty. Složku ani soubor zatím nevytvářejí.

---

## 118. Vytvoření složky pro logy

```python
logs_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

- `parents=True` umožní vytvořit také chybějící nadřazené složky;
- `exist_ok=True` zabrání chybě, pokud složka již existuje.

---

## 119. Základní konfigurace logování

```python
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)
```

Význam parametrů:

- `filename` určuje logovací soubor;
- `level` určuje nejnižší zaznamenávanou úroveň;
- `format` určuje podobu jednoho řádku;
- `datefmt` určuje formát data a času;
- `encoding` nastavuje kódování souboru.

---

## 120. Formát jednoho záznamu

```python
format="%(asctime)s | %(levelname)s | %(message)s"
```

- `%(asctime)s` vloží datum a čas;
- `%(levelname)s` vloží úroveň zprávy;
- `%(message)s` vloží samotný text zprávy.

Příklad výsledku:

```text
2026-09-14 20:30:01 | INFO | Proces byl zahájen.
```

Znak `%` označuje zástupné místo. Písmeno `s` znamená vložení hodnoty jako textu.

---

## 121. Formát data a času

```python
datefmt="%Y-%m-%d %H:%M:%S"
```

- `%Y` – rok;
- `%m` – měsíc;
- `%d` – den;
- `%H` – hodina;
- `%M` – minuta;
- `%S` – sekunda.

Výsledek:

```text
2026-09-14 20:30:01
```

---

## 122. Timestamp a délka procesu

Timestamp označuje konkrétní datum a čas události:

```text
2026-09-14 20:30:01
```

Délka procesu říká, kolik času zpracování zabralo:

```text
Délka zpracování v sekundách: 1.25
```

```text
timestamp
→ kdy se událost stala

délka procesu
→ jak dlouho proces trval
```

---

## 123. Úrovně logování

Základní úrovně používané v našem procesu:

```python
logging.info("Proces byl zahájen.")

logging.warning("Některé nepovinné hodnoty chybějí.")

logging.error("Vstupní soubor neexistuje.")
```

- `INFO` – běžná provozní informace;
- `WARNING` – problém, při kterém může proces pokračovat;
- `ERROR` – chyba, kvůli které proces zpravidla končí.

`WARNING` nepřidáváme do skriptu uměle, pokud nemáme skutečnou situaci vhodnou pro varování.

---

## 124. Zahájení procesu

```python
logging.info("Proces byl zahájen.")
```

Tento záznam ukazuje, že se skript skutečně spustil.

Logovací soubor se standardně vytvoří při zápisu prvního záznamu.

---

## 125. Zápis hodnoty do logu

```python
logging.info(
    "Načten počet vstupních řádků: %s",
    len(dataframe)
)
```

`%s` je zástupné místo pro předanou hodnotu.

Do logu se může zapsat:

```text
2026-09-14 20:30:01 | INFO | Načten počet vstupních řádků: 30
```

---

## 126. Záznam vstupních a výstupních řádků

Po načtení vstupu:

```python
logging.info(
    "Načten počet vstupních řádků: %s",
    len(dataframe)
)
```

Po čištění a validaci:

```python
logging.info(
    "Počet řádků po vyčištění a validaci: %s",
    len(dataframe)
)
```

Po vytvoření reportu:

```python
logging.info(
    "Počet řádků v Excelovém výstupu: %s",
    len(report_df)
)
```

Porovnáním počtů lze zjistit, zda se během zpracování řádky odstranily nebo ztratily.

---

## 127. Záznam výsledku validace

Úspěšná validace:

```python
if not validate_structure(dataframe):
    logging.error("Validace struktury selhala.")
    return 1

logging.info("Validace struktury byla úspěšná.")
```

Pokud validace vrátí `False`, proces zapíše chybu a skončí.

Pokud vrátí `True`, pokračuje se zápisem úspěšného výsledku.

---

## 128. Záznam vytvořeného výstupu

```python
logging.info(
    "Excelový výstup byl vytvořen: %s",
    output_file
)
```

Záznam včetně cesty umožňuje zjistit, kde byl výsledný soubor vytvořen.

Tento příkaz patří až za vytvoření Excelu, aby log nepotvrdil výstup, který ve skutečnosti nevznikl.

---

## 129. Záznam databázové chyby

```python
except pyodbc.Error as error:
    logging.error(
        "Chyba při práci s databází: %s",
        error
    )

    if connection is not None:
        connection.rollback()

    return 1
```

`logging.error()` uloží chybovou zprávu do logu a `return 1` oznámí neúspěšné dokončení procesu.

---

## 130. Záznam souborové nebo datové chyby

```python
except (OSError, ValueError) as error:
    logging.error(
        "Chyba při práci se souborem nebo daty: %s",
        error
    )

    if connection is not None:
        connection.rollback()

    return 1
```

Log pomáhá zpětně zjistit, proč automatizovaný proces skončil chybou.

---

## 131. Měření délky procesu

Modul `time` použijeme jako stopky:

```python
import time
```

Na začátku procesu:

```python
start_time = time.perf_counter()
```

Na konci procesu:

```python
duration_seconds = round(
    time.perf_counter() - start_time,
    2
)
```

`round(..., 2)` zaokrouhlí výsledek na dvě desetinná místa.

---

## 132. Záznam délky a dokončení procesu

```python
logging.info(
    "Délka zpracování v sekundách: %s",
    duration_seconds
)

logging.info("Proces byl úspěšně dokončen.")
```

Tyto záznamy patří až na konec úspěšné části před:

```python
return 0
```

---

## 133. Příklad výsledného logu

```text
2026-09-14 20:30:01 | INFO | Proces byl zahájen.
2026-09-14 20:30:01 | INFO | Načten počet vstupních řádků: 30
2026-09-14 20:30:01 | INFO | Validace struktury byla úspěšná.
2026-09-14 20:30:01 | INFO | Finální validace dat byla úspěšná.
2026-09-14 20:30:01 | INFO | Počet řádků po vyčištění a validaci: 30
2026-09-14 20:30:02 | INFO | Excelový výstup byl vytvořen: C:\...\github_issues_report.xlsx
2026-09-14 20:30:02 | INFO | Počet řádků v Excelovém výstupu: 30
2026-09-14 20:30:02 | INFO | Počet řádků uložených do databáze: 30
2026-09-14 20:30:02 | INFO | Délka zpracování v sekundách: 1.25
2026-09-14 20:30:02 | INFO | Proces byl úspěšně dokončen.
```

---

## 134. Co znamená monitoring

Monitoring znamená sledování, zda automatizovaný proces funguje správně.

V našem juniorském rozsahu kontrolujeme v logu:

- kdy se proces naposledy spustil;
- zda byl úspěšně dokončen;
- kolik řádků zpracoval;
- zda validace proběhla úspěšně;
- zda vznikl očekávaný výstup;
- zda se objevilo `WARNING` nebo `ERROR`;
- jak dlouho proces trval.

Monitoring zatím nevyžaduje samostatný dashboard ani automatické e-mailové upozornění.

---

## 135. Základní tok logování

```text
spuštění skriptu

→ vytvoření nebo otevření logovacího souboru

→ záznam zahájení procesu

→ záznam počtu vstupních řádků

→ záznam výsledků validace

→ záznam počtu zpracovaných řádků

→ záznam vytvořeného výstupu

→ záznam případné chyby

→ výpočet délky procesu

→ záznam úspěšného dokončení
```

---

## 136. Hlavní poznatky Lekce 6

- `logging` vytváří trvalý záznam o průběhu skriptu;
- `print()` slouží především pro okamžitý výpis do terminálu;
- `basicConfig()` nastavuje způsob logování;
- timestamp označuje datum a čas konkrétní události;
- délka procesu určuje dobu celého zpracování;
- `INFO` označuje běžnou provozní informaci;
- `WARNING` označuje nekritický problém;
- `ERROR` označuje chybu;
- do logu zapisujeme počty řádků, výsledky validace a vytvořené výstupy;
- `time.perf_counter()` lze použít jako stopky;
- log umožňuje zpětně zkontrolovat automatický běh procesu;
- jednoduchý monitoring znamená pravidelnou kontrolu úspěchu, chyb a délky zpracování.

---