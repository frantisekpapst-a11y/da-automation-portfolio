# Minitesty – automatizace datového procesu

Minitesty shrnují celý výukový blok automatizace datového procesu.

---

# Lekce 1 – Základy automatizace

## Otázka 1

Jaký je správný tok vytvořené automatizace?

**Správná odpověď:** Windows Task Scheduler → BAT → Python → CSV a databáze → log

Task Scheduler určí čas spuštění, BAT spustí Python a Python zpracuje data.

---

## Otázka 2

Jaká je hlavní úloha Windows Task Scheduleru?

**Správná odpověď:** Určit, kdy se proces automaticky spustí

Task Scheduler zajišťuje časové nebo událostní spuštění procesu.

---

## Otázka 3

Jaká je hlavní úloha BAT souboru?

**Správná odpověď:** Spustit správný Python interpreter a Python skript

BAT soubor spouští správné prostředí a předává řízení Python skriptu.

---

## Otázka 4

Co znamená `NaT` v pandas?

**Správná odpověď:** Neplatnou nebo chybějící hodnotu data a času

`NaT` je časová obdoba chybějící hodnoty `NaN`.

---

## Otázka 5

Co znamená idempotentní proces?

**Správná odpověď:** Proces lze bezpečně opakovat se stejnými vstupy bez vzniku dalších duplicit

Opakované spuštění se stejnými vstupy vytvoří stejný výsledný stav.

---

## Otázka 6

Proč se před vložením dat odstraní z databáze záznamy za stejný den?

**Správná odpověď:** Aby opakované spuštění nevytvořilo duplicitní řádky

Odstranění stejného dne umožňuje bezpečně zopakovat načtení dat.

---

## Otázka 7

Co znamená návratový kód `0`?

**Správná odpověď:** Proces skončil úspěšně

Návratový kód `0` podle běžné konvence označuje úspěch.

---

## Otázka 8

Co obvykle znamená nenulový návratový kód, například `1`?

**Správná odpověď:** Proces skončil chybou

Nenulový návratový kód informuje operační systém o chybě procesu.

---

# Lekce 2 – Základy Python skriptu

## Otázka 9

Co získáme tímto zápisem?

```python

script_dir = Path(__file__).resolve().parent

```

**Správná odpověď:** Absolutní cestu ke složce, ve které leží Python skript

`resolve()` vytvoří absolutní cestu a `parent` vybere složku skriptu.

---

## Otázka 10

Proč při automatizaci odvozujeme cesty od `__file__` místo pouze od `Path.cwd()`?

**Správná odpověď:** Protože pracovní složka se může měnit podle způsobu spuštění skriptu

Umístění skriptu zůstává stejné, ale pracovní složka se může měnit.

---

## Otázka 11

Který zápis správně zkontroluje chybějící vstupní složku?

**Správná odpověď:**

```python

if not input_dir.exists():

    return 1

```

`.exists()` ověří existenci a `not` zachytí záporný výsledek.

---

## Otázka 12

K čemu slouží tato podmínka?

```python

if __name__ == "__main__":

    result = main()

```

**Správná odpověď:** Spustí hlavní proces pouze při přímém spuštění souboru

Podmínka zabrání automatickému spuštění `main()` při importu modulu.

---

## Otázka 13

Které tvrzení o `return` a `sys.exit()` je správné?

**Správná odpověď:** `return` vrátí hodnotu z funkce a `sys.exit()` ji předá operačnímu systému

`return` ukončí funkci, zatímco `sys.exit()` ukončí celý proces.

---

# Lekce 3 – API automatizace

## Otázka 14

Co provádí `requests.get()`?

**Správná odpověď:** Odesílá HTTP požadavek pro získání dat

Metoda `GET` slouží k načtení dat ze zvoleného endpointu.

---

## Otázka 15

Co znamená HTTP status `200`?

**Správná odpověď:** Požadavek byl úspěšně zpracován

Status `200` potvrzuje úspěšné zpracování HTTP požadavku.

---

## Otázka 16

Proč u API požadavku používáme `timeout`?

**Správná odpověď:** Aby skript nečekal na odpověď neomezeně dlouho

Timeout stanovuje maximální dobu čekání na odpověď API.

---

## Otázka 17

Který parametr určuje číslo požadované stránky?

```python

params = {

    "state": "all",

    "per_page": 10,

    "page": 2

}

```

**Správná odpověď:** `page`

Parametr `page` určuje konkrétní stránku stránkované odpovědi.

---

## Otázka 18

Co provede tento příkaz?

```python

all_records.extend(page_data)

```

**Správná odpověď:** Přidá jednotlivé záznamy aktuální stránky do společného seznamu

`.extend()` rozšíří existující seznam o jednotlivé položky dalšího seznamu.

---

## Otázka 19

Co vyjadřuje rate limit?

**Správná odpověď:** Omezení počtu požadavků na API

Rate limit chrání API omezením počtu požadavků v určitém období.

---

## Otázka 20

Jaký je rozdíl mezi `response.text` a `response.json()`?

**Správná odpověď:** `response.text` obsahuje původní text a `response.json()` ho převádí na Python objekty

Raw odpověď ukládáme jako text a pro zpracování ji převádíme na Python objekty.

---

## Otázka 21

Co zjistí tento zápis?

```python

missing_keys = REQUIRED_KEYS - set(record.keys())

```

**Správná odpověď:** Které povinné klíče v záznamu chybějí

Rozdíl množin vrátí očekávané klíče, které záznam neobsahuje.

---

## Otázka 22

K čemu slouží následující příkaz?

```python

normalized_df = pd.json_normalize(all_records)

```

**Správná odpověď:** K převedení JSON struktury na tabulku

`json_normalize()` převede záznamy JSON do tabulkového DataFrame.

---

## Otázka 23

Co znamená, když funkce `main()` vrátí hodnotu `1`?

**Správná odpověď:** Proces skončil chybou

Nenulový návratový kód signalizuje neúspěšné dokončení procesu.

---

# Lekce 5 – Validace a error handling

## Otázka 24

Jaký je hlavní účel funkce `validate_structure()`?

**Správná odpověď:** Ověřit povinné sloupce a neprázdný dataset

Funkce ověřuje, zda lze se vstupními daty bezpečně začít pracovat.

---

## Otázka 25

Proč voláme `validate_structure()` před `clean_data()`?

**Správná odpověď:** Aby cleaning pracoval s očekávanými sloupci

Pokud by potřebný sloupec chyběl, cleaning by při jeho použití skončil chybou.

---

## Otázka 26

Co vrací funkce `clean_data()`?

**Správná odpověď:** Vyčištěný DataFrame

Funkce vrací pracovní kopii DataFrame po provedeném čištění.

---

## Otázka 27

Co způsobí `errors="coerce"` při převodu neplatné číselné hodnoty?

**Správná odpověď:** Převede hodnotu na `NaN`

Neplatná číselná hodnota se změní na `NaN`, kterou následně zachytí validace.

---

## Otázka 28

Jak má proces reagovat na chybějící hodnotu `issue_id`?

**Správná odpověď:** Zastavit proces jako chybný

`issue_id` je primární klíč, a proto nesmí být prázdný.

---

## Otázka 29

Jaký je rozdíl mezi `drop_duplicates()` a kontrolou `duplicated()` ve sloupci `issue_id`?

**Správná odpověď:** První odstraní stejné řádky, druhá kontroluje duplicitní klíč

Úplné duplicity odstraníme při čištění, ale opakovaný primární klíč zastaví proces.

---

## Otázka 30

Proč `validate_data()` vrací `False`, zatímco `main()` při stejné chybě vrací `1`?

**Správná odpověď:** Validace vrací stav dat a `main()` stav procesu

`False` označuje neplatná data, zatímco návratový kód `1` oznamuje chybu celého procesu.

---

## Otázka 31

Co zajišťuje blok `finally` v našem skriptu?

**Správná odpověď:** Uzavře existující databázové spojení

`finally` se provede při úspěchu, chybě i předčasném ukončení funkce.

---

## Otázka 32

Proč je `connection.commit()` ve finálním skriptu až po vytvoření Excelu?

**Správná odpověď:** Aby bylo možné při chybě exportu vrátit databázové změny

Pokud export selže před `commit()`, lze pomocí `rollback()` zachovat předchozí stav databáze.

---

## Otázka 33

Která situace je v našem procesu pouze varováním, nikoliv kritickou chybou?

**Správná odpověď:** Chybějící nepovinný `user_login`

`user_login` je nepovinný a chybějící hodnotu lze bezpečně ošetřit.

---

# Lekce 6 – Logging a monitoring

## Otázka 34

Jaký je hlavní účel modulu `logging`?

**Správná odpověď:** Vytvářet záznamy o průběhu programu

Modul `logging` zaznamenává průběh, výsledky a případné chyby programu.

---

## Otázka 35

Jaký je hlavní rozdíl mezi `print()` a `logging`?

**Správná odpověď:** `logging` může ukládat strukturované záznamy do souboru

`print()` vypíše zprávu do terminálu, zatímco `logging` ji může trvale uložit.

---

## Otázka 36

Co nastavuje tento parametr?

```python

level=logging.INFO

```

**Správná odpověď:** Nejnižší zaznamenávanou úroveň logování

Při nastavení `INFO` se zaznamenávají zprávy úrovní `INFO`, `WARNING` a `ERROR`.

---

## Otázka 37

Která úroveň je vhodná pro běžnou informaci o správném průběhu procesu?

**Správná odpověď:** `INFO`

`INFO` slouží pro běžné provozní informace, například zahájení procesu.

---

## Otázka 38

Která úroveň je vhodná pro nekritický problém, při kterém může proces pokračovat?

**Správná odpověď:** `WARNING`

`WARNING` upozorňuje na problém, který nemusí vyžadovat zastavení procesu.

---

## Otázka 39

Co znamená timestamp v logu?

**Správná odpověď:** Datum a čas konkrétní události

Timestamp ukazuje, kdy přesně byl konkrétní záznam vytvořen.

---

## Otázka 40

K čemu používáme následující příkaz?

```python

start_time = time.perf_counter()

```

**Správná odpověď:** K zahájení měření délky procesu

`time.perf_counter()` použijeme jako přesné stopky pro měření délky zpracování.

---

## Otázka 41

Co představuje `%s` v tomto zápisu?

```python

logging.info(

    "Počet řádků: %s",

    len(dataframe)

)

```

**Správná odpověď:** Zástupné místo pro předanou hodnotu

Na místo `%s` se při vytvoření záznamu vloží hodnota `len(dataframe)`.

---

## Otázka 42

Proč zapisujeme informaci o vytvoření Excelu až po dokončení bloku `ExcelWriter`?

**Správná odpověď:** Aby log nepotvrdil vytvoření souboru, který ve skutečnosti nevznikl

Úspěšné vytvoření výstupu zaznamenáme až ve chvíli, kdy byl soubor skutečně uložen.

---

## Otázka 43

Co znamená monitoring v rozsahu této lekce?

**Správná odpověď:** Kontrolu logu, úspěchu procesu, počtů řádků, chyb a délky zpracování

Jednoduchý monitoring znamená kontrolovat podle logu stav a výsledek automatizovaného procesu.

---

# Lekce 7 – Secrets a environment variables

## Otázka 44

Proč citlivé údaje, například API klíč, nemají být zapsané přímo v Python kódu?

**Správná odpověď:** Mohly by se zveřejnit spolu s kódem

Citlivý údaj zapsaný v kódu by se mohl dostat do repozitáře a být zneužit.

---

## Otázka 45

Jaký je účel lokálního souboru `.env`?

**Správná odpověď:** Uchovávat lokální konfigurační a citlivé hodnoty mimo kód

Soubor `.env` odděluje místní konfiguraci a citlivé hodnoty od zdrojového kódu.

---

## Otázka 46

Co má obsahovat soubor `.env.example`?

**Správná odpověď:** Názvy proměnných bez skutečných citlivých hodnot

Soubor `.env.example` ukazuje požadované proměnné, ale neobsahuje jejich skutečné citlivé hodnoty.

---

## Otázka 47

K čemu slouží zápis `.env` v souboru `.gitignore`?

**Správná odpověď:** Zabrání Gitu sledovat soubor `.env`

Pravidlo v `.gitignore` zabrání běžnému přidání souboru `.env` do repozitáře.

---

## Otázka 48

Co standardně vrátí `os.getenv("DATABASE_NAME")`, pokud proměnná neexistuje?

**Správná odpověď:** `None`

Pokud proměnná není dostupná a neurčíme výchozí hodnotu, `os.getenv()` vrátí `None`.

---

## Otázka 49

Co provede `load_dotenv(env_file)`?

**Správná odpověď:** Načte hodnoty z `.env` do proměnných prostředí procesu

Funkce `load_dotenv()` přečte soubor a zpřístupní jeho hodnoty běžícímu Python procesu.

---

## Otázka 50

Co je connection string?

**Správná odpověď:** Text s parametry potřebnými pro připojení k databázi

Connection string obsahuje například driver, server, databázi a způsob přihlášení.

---

## Otázka 51

Proč náš connection string neobsahuje databázové heslo?

**Správná odpověď:** Používáme přihlášení pomocí účtu Windows

Nastavení `Trusted_Connection=yes` používá ověření aktuálního uživatele Windows.

---

## Otázka 52

K čemu slouží GitHub Secrets?

**Správná odpověď:** K bezpečnému uložení citlivých hodnot pro GitHub Actions

GitHub Secrets umožňují předat citlivé hodnoty workflow bez jejich zapsání do repozitáře.

---

## Otázka 53

Proč jsme do `requirements.txt` přidali `python-dotenv`, ale nepřidali `os` ani `sys`?

**Správná odpověď:** `python-dotenv` je externí balíček, zatímco `os` a `sys` jsou součástí Pythonu

Do `requirements.txt` zapisujeme externí závislosti instalované přes `pip`, nikoliv standardní moduly Pythonu.

---

# Lekce 8 – Windows Task Scheduler a BAT

## Otázka 54

Jaká je hlavní úloha souboru `run_pipeline.bat` v našem procesu?

**Správná odpověď:** Spustit správný Python interpreter a Python skript

BAT soubor spustí Python z projektového virtuálního prostředí a předá mu cestu ke skriptu.

---

## Otázka 55

Co způsobí příkaz `@echo off` na začátku BAT souboru?

**Správná odpověď:** Skryje vypisování prováděných BAT příkazů

Příkaz omezí technické výpisy BAT příkazů, ale chyby Pythonu zůstávají viditelné.

---

## Otázka 56

Co v BAT souboru označuje zápis `%\~dp0`?

**Správná odpověď:** Složku, ve které leží spuštěný BAT soubor

Zápis vrací cestu ke složce aktuálního BAT souboru.

---

## Otázka 57

Proč před spuštěním Python skriptu používáme příkaz `cd /d`?

**Správná odpověď:** Aby se nastavila správná pracovní složka a případně změnil disk

`cd` změní pracovní složku a přepínač `/d` dovolí současně změnit také disk.

---

## Otázka 58

Proč v BAT souboru voláme přímo `.venv\Scripts\python.exe`?

**Správná odpověď:** Aby se použil Python a knihovny ze správného virtuálního prostředí

Přímá cesta zaručí použití Pythonu a nainstalovaných knihoven z projektového `.venv`.

---

## Otázka 59

K čemu jsme při testování dočasně použili příkaz `pause`?

**Správná odpověď:** K ponechání okna otevřeného, abychom mohli přečíst výstup

`pause` čeká na stisknutí klávesy, takže se příkazové okno ihned nezavře.

---

## Otázka 60

Proč nemá příkaz `pause` zůstat ve finálním BAT souboru pro plánované spuštění?

**Správná odpověď:** Protože by automatická úloha čekala na stisknutí klávesy

Plánovaný proces by zůstal čekat na ruční zásah a řádně by se nedokončil.

---

## Otázka 61

Co dělá příkaz `exit /b %ERRORLEVEL%` na konci BAT souboru?

**Správná odpověď:** Ukončí BAT soubor a předá návratový kód systému Windows

BAT soubor předá Windows informaci, zda Python proces skončil úspěchem, nebo chybou.

---

## Otázka 62

Co v našem případě znamená výsledek posledního spuštění `0x0`?

**Správná odpověď:** Úloha byla úspěšně dokončena

Hodnota `0x0` odpovídá návratovému kódu `0`, který označuje úspěšné dokončení.

---

## Otázka 63

Jak nejlépe ověříme úspěch automaticky spuštěného procesu?

**Správná odpověď:** Kontrolou výsledku `0x0`, nového záznamu v logu a aktualizovaného výstupu

Návratový kód, log a skutečně aktualizovaný Excel společně potvrzují úspěšný běh.

---

# Lekce 9 – GitHub Actions

## Otázka 64

Ve které složce repozitáře musí být uložen soubor GitHub Actions workflow?

**Správná odpověď:** `.github/workflows`

GitHub automaticky načítá workflow soubory uložené ve složce `.github/workflows`.

---

## Otázka 65

Co je runner v GitHub Actions?

**Správná odpověď:** Počítač, na kterém běží job

Runner poskytuje operační systém a prostředí potřebné k provedení jobu.

---

## Otázka 66

K čemu slouží `workflow_dispatch`?

**Správná odpověď:** K ručnímu spuštění workflow

`workflow_dispatch` zpřístupní na kartě Actions tlačítko **Run workflow**.

---

## Otázka 67

Co znamená cron zápis `0 6 * * *` v našem workflow?

**Správná odpověď:** Každý den v 06:00

První hodnota určuje minutu `0`, druhá hodinu `6` a hvězdičky povolují každý den.

---

## Otázka 68

Co provede `actions/checkout` v prvním kroku jobu?

**Správná odpověď:** Stáhne obsah repozitáře na runner

Akce zpřístupní runneru Python skripty, `requirements.txt` a další projektové soubory.

---

## Otázka 69

Proč workflow používá `actions/setup-python`?

**Správná odpověď:** Aby připravilo požadovanou verzi Pythonu

Akce připraví na runneru verzi Pythonu uvedenou v nastavení `python-version`.

---

## Otázka 70

Proč se knihovny na runneru instalují ze souboru `requirements.txt`?

**Správná odpověď:** Runner nepoužívá naše lokální `.venv`

Nový runner si připravuje vlastní prostředí a potřebné knihovny musí nainstalovat znovu.

---

## Otázka 71

Co je workflow artifact?

**Správná odpověď:** Balíček výstupů vytvořených během konkrétního běhu

Artifact umožňuje po dokončení workflow stáhnout soubory vytvořené na runneru.

---

## Otázka 72

Co se stane, když Python skript ve workflow vrátí nenulový návratový kód?

**Správná odpověď:** Krok se označí jako neúspěšný

Nenulový návratový kód signalizuje chybu a workflow se standardně zastaví.

---

## Otázka 73

Proč náš GitHub Actions workflow nezapisuje přímo do LocalDB na osobním počítači?

**Správná odpověď:** Vzdálený runner nemá přímý přístup k lokálnímu počítači

GitHub-hosted runner je oddělený virtuální počítač bez automatického přístupu k lokální LocalDB.

---

# Lekce 10 – SQL scheduling

## Otázka 74

Jaká je hlavní úloha SQL Server Agentu?

**Správná odpověď:** Plánovat a spouštět databázové úlohy

SQL Server Agent řídí automatické spouštění databázových jobů podle nastaveného plánu.

---

## Otázka 75

Co představuje job v SQL Server Agentu?

**Správná odpověď:** Celou automaticky spouštěnou úlohu

Job představuje celou naplánovanou úlohu a může obsahovat jeden nebo více kroků.

---

## Otázka 76

Co určuje job step?

**Správná odpověď:** Konkrétní činnost uvnitř jobu

Job step může například spustit SQL příkaz nebo uloženou proceduru.

---

## Otázka 77

Co určuje schedule?

**Správná odpověď:** Kdy a jak často se job spustí

Schedule stanovuje čas a opakování automatického spuštění.

---

## Otázka 78

Proč nemůžeme v LocalDB používat SQL Server Agent?

**Správná odpověď:** LocalDB službu SQL Server Agent neobsahuje

LocalDB nemá SQL Server Agent, a proto potřebuje externí plánovač.

---

## Otázka 79

Jak lze automaticky spustit SQL soubor v LocalDB bez použití Pythonu?

**Správná odpověď:** Task Scheduler → BAT → `sqlcmd`

Task Scheduler spustí BAT soubor a `sqlcmd` provede SQL soubor v LocalDB.

---

## Otázka 80

Jaký je rozdíl mezi SQL skriptem a uloženou procedurou?

**Správná odpověď:** Skript je soubor, procedura je uložená v databázi

SQL skript existuje jako soubor, zatímco uložená procedura je databázový objekt.

---

## Otázka 81

Kdy je zpravidla vhodnější řídit proces Pythonem?

**Správná odpověď:** Když kombinujeme API, soubory a databázi

Python je vhodný pro řízení procesu napříč API, soubory a databázemi.

---

## Otázka 82

Kdy dává smysl použít orchestrační platformu?

**Správná odpověď:** Při řízení navazujících úloh ve více systémech

Orchestrace koordinuje pořadí, závislosti, monitoring a chyby napříč systémy.

---

## Otázka 83

Proč se při volání `sqlcmd` používá parametr `-b`?

**Správná odpověď:** Aby při SQL chybě vznikl nenulový návratový kód

Parametr `-b` umožní předat selhání SQL úlohy BAT souboru a plánovači.

---

# Lekce 11 – Power Query a Power BI refresh

## Otázka 84

Co v našem procesu primárně určuje Power Query?

**Správná odpověď:** Způsob načtení a transformace dat

Power Query ukládá připojení ke zdroji a jednotlivé transformační kroky.

---

## Otázka 85

Co bychom měli po načtení dat do Power Query vždy rychle zkontrolovat?

**Správná odpověď:** Názvy, datové typy, počet řádků, prázdné a konkrétní hodnoty

Tato kontrola pomáhá rychle odhalit chybnou strukturu, datové typy i nekvalitní hodnoty.

---

## Otázka 86

Proč se datum z Excelu může v Power Query zobrazit jako číslo `46278,78365`?

**Správná odpověď:** Excel ukládá datum a čas jako pořadové číslo

Celá část čísla představuje datum a desetinná část čas.

---

## Otázka 87

Která funkce Power Query nejrychleji ukáže prázdné a chybné hodnoty ve všech sloupcích?

**Správná odpověď:** Kvalita sloupce

Kvalita sloupce zobrazuje podíly platných, chybných a prázdných hodnot.

---

## Otázka 88

Proč lze profilaci Power Query přepnout na celou datovou sadu?

**Správná odpověď:** Aby kontrola zahrnula i řádky mimo první tisícovku

Výchozí profilace může vyhodnocovat pouze prvních 1 000 řádků.

---

## Otázka 89

Co provede tlačítko **Aktualizovat** v Power BI Desktop?

**Správná odpověď:** Znovu načte zdroj a provede kroky Power Query

Výsledek dotazů se znovu načte do datového modelu a vizualizace se přepočítají.

---

## Otázka 90

Proč může Power BI úspěšně dokončit aktualizaci, ale přesto zobrazovat stará data?

**Správná odpověď:** Zdrojový soubor byl dostupný, ale obsahoval stará data

Technicky úspěšná aktualizace nezaručuje aktuální obsah zdroje, proto kontrolujeme také datový timestamp.

---

## Otázka 91

Co znamená **scheduled refresh** v Power BI Service?

**Správná odpověď:** Plánovanou aktualizaci sémantického modelu

Power BI Service se podle plánu připojí ke zdroji a znovu provede uložené dotazy.

---

## Otázka 92

K čemu slouží **on-premises data gateway**?

**Správná odpověď:** K propojení Power BI Service s lokálním zdrojem

Gateway zprostředkuje cloudové službě přístup k lokálním souborům nebo databázím.

---

## Otázka 93

Které tvrzení o zpřístupnění Power BI reportu je správné?

**Správná odpověď:** Power BI Service umožňuje webové sdílení řízené oprávněními

Power BI Service slouží k publikování, zabezpečenému sdílení a používání reportů v internetovém prohlížeči.