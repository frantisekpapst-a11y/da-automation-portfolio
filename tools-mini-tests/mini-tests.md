# Minitesty – automatizace datového procesu

Minitesty shrnují základy automatizace, strukturu Python skriptu a získávání dat z API.

---

# Lekce 1 – Základy automatizace

## Otázka 1

Jaký je správný tok vytvořené automatizace?

- A) Python → Windows Task Scheduler → BAT → log
- B) Windows Task Scheduler → BAT → Python → CSV a databáze → log
- C) BAT → databáze → Windows Task Scheduler → Python
- D) SQL Server → Python → Windows Task Scheduler → BAT

**Správná odpověď:** B

Task Scheduler určí čas spuštění, BAT spustí Python a Python zpracuje data.

---

## Otázka 2

Jaká je hlavní úloha Windows Task Scheduleru?

- A) Určit, kdy se proces automaticky spustí
- B) Provést validaci CSV souborů
- C) Spojit data pomocí pandas
- D) Vytvořit databázovou tabulku

**Správná odpověď:** A

Task Scheduler zajišťuje časové nebo událostní spuštění procesu.

---

## Otázka 3

Jaká je hlavní úloha BAT souboru?

- A) Nahradit Python skript
- B) Spustit správný Python interpreter a Python skript
- C) Uložit data přímo do SQL Serveru
- D) Vytvořit log bez použití Pythonu

**Správná odpověď:** B

BAT soubor spouští správné prostředí a předává řízení Python skriptu.

---

## Otázka 4

Co znamená `NaT` v pandas?

- A) Nulovou hodnotu v číselném sloupci
- B) Neplatnou nebo chybějící hodnotu data a času
- C) Duplicitní řádek
- D) Nenalezený text

**Správná odpověď:** B

`NaT` je časová obdoba chybějící hodnoty `NaN`.

---

## Otázka 5

Co znamená idempotentní proces?

- A) Proces lze bezpečně opakovat se stejnými vstupy bez vzniku dalších duplicit
- B) Proces může být spuštěn pouze jednou
- C) Proces nepotřebuje validaci
- D) Proces vždy smaže celou databázi

**Správná odpověď:** A

Opakované spuštění se stejnými vstupy vytvoří stejný výsledný stav.

---

## Otázka 6

Proč se před vložením dat odstraní z databáze záznamy za stejný den?

- A) Aby opakované spuštění nevytvořilo duplicitní řádky
- B) Aby se odstranily všechny historické záznamy
- C) Aby nebylo nutné použít SQL
- D) Aby se změnil formát data

**Správná odpověď:** A

Odstranění stejného dne umožňuje bezpečně zopakovat načtení dat.

---

## Otázka 7

Co znamená návratový kód `0`?

- A) Proces skončil úspěšně
- B) Proces skončil chybou
- C) Nebyl nalezen žádný soubor
- D) Databáze byla odstraněna

**Správná odpověď:** A

Návratový kód `0` podle běžné konvence označuje úspěch.

---

## Otázka 8

Co obvykle znamená nenulový návratový kód, například `1`?

- A) Proces skončil chybou
- B) Proces skončil úspěšně
- C) Byla načtena právě jedna pobočka
- D) Windows Task Scheduler je vypnutý

**Správná odpověď:** A

Nenulový návratový kód informuje operační systém o chybě procesu.

---

# Lekce 2 – Základy Python skriptu

## Otázka 9

Co získáme tímto zápisem?

```python
script_dir = Path(__file__).resolve().parent
```

- A) Aktuální pracovní složku
- B) Absolutní cestu ke složce, ve které leží Python skript
- C) Cestu ke vstupnímu souboru

**Správná odpověď:** B

`resolve()` vytvoří absolutní cestu a `parent` vybere složku skriptu.

---

## Otázka 10

Proč při automatizaci odvozujeme cesty od `__file__` místo pouze od `Path.cwd()`?

- A) Protože `Path.cwd()` neumí pracovat ve Windows
- B) Protože pracovní složka se může měnit podle způsobu spuštění skriptu
- C) Protože `__file__` automaticky vytváří chybějící složky

**Správná odpověď:** B

Umístění skriptu zůstává stejné, ale pracovní složka se může měnit.

---

## Otázka 11

Který zápis správně zkontroluje chybějící vstupní složku?

- A)

```python
if not input_dir.exists():
    return 1
```

- B)

```python
if input_dir.exists():
    return 1
```

- C)

```python
if not input_dir:
    return 0
```

**Správná odpověď:** A

`.exists()` ověří existenci a `not` zachytí záporný výsledek.

---

## Otázka 12

K čemu slouží tato podmínka?

```python
if __name__ == "__main__":
    result = main()
```

- A) Kontroluje, zda existuje funkce `main()`
- B) Spustí hlavní proces pouze při přímém spuštění souboru
- C) Zabrání ukončení Python programu

**Správná odpověď:** B

Podmínka zabrání automatickému spuštění `main()` při importu modulu.

---

## Otázka 13

Které tvrzení o `return` a `sys.exit()` je správné?

- A) Oba příkazy pouze vypíšou výsledek do terminálu
- B) `return 1` znamená úspěch a `return 0` znamená chybu
- C) `return` vrátí hodnotu z funkce a `sys.exit()` ji předá operačnímu systému

**Správná odpověď:** C

`return` ukončí funkci, zatímco `sys.exit()` ukončí celý proces.

---

# Lekce 3 – API automatizace

## Otázka 14

Co provádí `requests.get()`?

- A) Vytváří lokální JSON soubor
- B) Odesílá HTTP požadavek pro získání dat
- C) Normalizuje JSON do tabulky

**Správná odpověď:** B

Metoda `GET` slouží k načtení dat ze zvoleného endpointu.

---

## Otázka 15

Co znamená HTTP status `200`?

- A) Požadavek byl úspěšně zpracován
- B) Požadovaný zdroj nebyl nalezen
- C) Byl překročen rate limit

**Správná odpověď:** A

Status `200` potvrzuje úspěšné zpracování HTTP požadavku.

---

## Otázka 16

Proč u API požadavku používáme `timeout`?

- A) Aby API vrátilo méně záznamů
- B) Aby se JSON automaticky uložil
- C) Aby skript nečekal na odpověď neomezeně dlouho

**Správná odpověď:** C

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

- A) `state`
- B) `per_page`
- C) `page`

**Správná odpověď:** C

Parametr `page` určuje konkrétní stránku stránkované odpovědi.

---

## Otázka 18

Co provede tento příkaz?

```python
all_records.extend(page_data)
```

- A) Přidá jednotlivé záznamy aktuální stránky do společného seznamu
- B) Nahradí všechny předchozí záznamy aktuální stránkou
- C) Odstraní duplicitní záznamy

**Správná odpověď:** A

`.extend()` rozšíří existující seznam o jednotlivé položky dalšího seznamu.

---

## Otázka 19

Co vyjadřuje rate limit?

- A) Maximální velikost jednoho JSON souboru
- B) Omezení počtu požadavků na API
- C) Počet sloupců ve výsledné tabulce

**Správná odpověď:** B

Rate limit chrání API omezením počtu požadavků v určitém období.

---

## Otázka 20

Jaký je rozdíl mezi `response.text` a `response.json()`?

- A) Žádný, obě hodnoty jsou vždy slovník
- B) `response.text` obsahuje původní text a `response.json()` ho převádí na Python objekty
- C) `response.text` vytváří DataFrame a `response.json()` vytváří CSV

**Správná odpověď:** B

Raw odpověď ukládáme jako text a pro zpracování ji převádíme na Python objekty.

---

## Otázka 21

Co zjistí tento zápis?

```python
missing_keys = REQUIRED_KEYS - set(record.keys())
```

- A) Které povinné klíče v záznamu chybějí
- B) Kolik stránek ještě můžeme stáhnout
- C) Které záznamy jsou duplicitní

**Správná odpověď:** A

Rozdíl množin vrátí očekávané klíče, které záznam neobsahuje.

---

## Otázka 22

K čemu slouží následující příkaz?

```python
normalized_df = pd.json_normalize(all_records)
```

- A) K odeslání dat zpět do API
- B) K převedení JSON struktury na tabulku
- C) K vytvoření timestampu

**Správná odpověď:** B

`json_normalize()` převede záznamy JSON do tabulkového DataFrame.

---

## Otázka 23

Co znamená, když funkce `main()` vrátí hodnotu `1`?

- A) Proces skončil úspěšně
- B) Byla stažena pouze jedna stránka
- C) Proces skončil chybou

**Správná odpověď:** C

Nenulový návratový kód signalizuje neúspěšné dokončení procesu.

---

## Otázka 24

Jaký je hlavní účel funkce `validate_structure()`?

- A) Uložit data do SQL Serveru
- B) Ověřit povinné sloupce a neprázdný dataset
- C) Odstranit duplicitní řádky
- D) Vytvořit výsledný Excel

**Správná odpověď:** B

Funkce ověřuje, zda lze se vstupními daty bezpečně začít pracovat.

---

## Otázka 25

Proč voláme `validate_structure()` před `clean_data()`?

- A) Aby se vytvořilo databázové spojení
- B) Aby se změnil návratový kód na `0`
- C) Aby cleaning pracoval s očekávanými sloupci
- D) Aby se odstranily všechny hodnoty `NULL`

**Správná odpověď:** C

Pokud by potřebný sloupec chyběl, cleaning by při jeho použití skončil chybou.

---

## Otázka 26

Co vrací funkce `clean_data()`?

- A) Vyčištěný DataFrame
- B) Návratový kód procesu
- C) Databázové spojení
- D) Cestu k Excel souboru

**Správná odpověď:** A

Funkce vrací pracovní kopii DataFrame po provedeném čištění.

---

## Otázka 27

Co způsobí `errors="coerce"` při převodu neplatné číselné hodnoty?

- A) Odstraní celý řádek
- B) Nahradí hodnotu nulou
- C) Okamžitě ukončí Python
- D) Převede hodnotu na `NaN`

**Správná odpověď:** D

Neplatná číselná hodnota se změní na `NaN`, kterou následně zachytí validace.

---

## Otázka 28

Jak má proces reagovat na chybějící hodnotu `issue_id`?

- A) Doplnit hodnotu `unknown`
- B) Zastavit proces jako chybný
- C) Nahradit hodnotu nulou
- D) Pokračovat bez upozornění

**Správná odpověď:** B

`issue_id` je primární klíč, a proto nesmí být prázdný.

---

## Otázka 29

Jaký je rozdíl mezi `drop_duplicates()` a kontrolou `duplicated()` ve sloupci `issue_id`?

- A) Obě kontroly vždy dělají totéž
- B) Obě kontroly pouze vypisují varování
- C) První odstraní stejné řádky, druhá kontroluje duplicitní klíč
- D) První kontroluje klíč, druhá vytváří kopii

**Správná odpověď:** C

Úplné duplicity odstraníme při čištění, ale opakovaný primární klíč zastaví proces.

---

## Otázka 30

Proč `validate_data()` vrací `False`, zatímco `main()` při stejné chybě vrací `1`?

- A) Validace vrací stav dat a `main()` stav procesu
- B) `False` a `1` vždy znamenají úspěch
- C) `main()` nemůže vracet logickou hodnotu
- D) `validate_data()` nemůže vracet číslo

**Správná odpověď:** A

`False` označuje neplatná data, zatímco návratový kód `1` oznamuje chybu celého procesu.

---

## Otázka 31

Co zajišťuje blok `finally` v našem skriptu?

- A) Vždy vytvoří nový Excel
- B) Vždy potvrdí databázové změny
- C) Vždy vrátí návratový kód `0`
- D) Uzavře existující databázové spojení

**Správná odpověď:** D

`finally` se provede při úspěchu, chybě i předčasném ukončení funkce.

---

## Otázka 32

Proč je `connection.commit()` ve finálním skriptu až po vytvoření Excelu?

- A) Aby byl SQL dotaz rychlejší
- B) Aby bylo možné při chybě exportu vrátit databázové změny
- C) Aby Pandas našel vstupní CSV
- D) Aby se odstranily duplicity v Excelu

**Správná odpověď:** B

Pokud export selže před `commit()`, lze pomocí `rollback()` zachovat předchozí stav databáze.

---

## Otázka 33

Která situace je v našem procesu pouze varováním, nikoliv kritickou chybou?

- A) Chybějící sloupec `issue_id`
- B) Duplicitní hodnota `issue_id`
- C) Chybějící nepovinný `user_login`
- D) Nedostupné databázové připojení

**Správná odpověď:** C

`user_login` je nepovinný a chybějící hodnotu lze bezpečně ošetřit.

---

## Otázka 34

Jaký je hlavní účel modulu `logging`?

- A) Čistit data v DataFrame
- B) Vytvářet záznamy o průběhu programu
- C) Připojovat Python k SQL Serveru
- D) Vytvářet Excelové soubory

**Správná odpověď:** B

Modul `logging` zaznamenává průběh, výsledky a případné chyby programu.

---

## Otázka 35

Jaký je hlavní rozdíl mezi `print()` a `logging`?

- A) `print()` může zobrazit text, zatímco `logging` pracuje pouze s čísly
- B) `logging` může ukládat strukturované záznamy do souboru
- C) `print()` automaticky přidává datum a čas
- D) Mezi nimi není žádný rozdíl

**Správná odpověď:** B

`print()` vypíše zprávu do terminálu, zatímco `logging` ji může trvale uložit.

---

## Otázka 36

Co nastavuje tento parametr?

```python
level=logging.INFO
```

- A) Název logovacího souboru
- B) Formát data
- C) Nejnižší zaznamenávanou úroveň logování
- D) Maximální počet řádků v logu

**Správná odpověď:** C

Při nastavení `INFO` se zaznamenávají zprávy úrovní `INFO`, `WARNING` a `ERROR`.

---

## Otázka 37

Která úroveň je vhodná pro běžnou informaci o správném průběhu procesu?

- A) `INFO`
- B) `WARNING`
- C) `ERROR`
- D) `STOP`

**Správná odpověď:** A

`INFO` slouží pro běžné provozní informace, například zahájení procesu.

---

## Otázka 38

Která úroveň je vhodná pro nekritický problém, při kterém může proces pokračovat?

- A) `INFO`
- B) `WARNING`
- C) `ERROR`
- D) `SUCCESS`

**Správná odpověď:** B

`WARNING` upozorňuje na problém, který nemusí vyžadovat zastavení procesu.

---

## Otázka 39

Co znamená timestamp v logu?

- A) Počet zpracovaných řádků
- B) Celkovou délku procesu
- C) Datum a čas konkrétní události
- D) Návratový kód skriptu

**Správná odpověď:** C

Timestamp ukazuje, kdy přesně byl konkrétní záznam vytvořen.

---

## Otázka 40

K čemu používáme následující příkaz?

```python
start_time = time.perf_counter()
```

- A) K získání aktuálního kalendářního data
- B) K zahájení měření délky procesu
- C) K vytvoření timestampu v logu
- D) K zastavení skriptu

**Správná odpověď:** B

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

- A) Zástupné místo pro předanou hodnotu
- B) Název logovacího souboru
- C) Chybový návratový kód
- D) Formát aktuálního času

**Správná odpověď:** A

Na místo `%s` se při vytvoření záznamu vloží hodnota `len(dataframe)`.

---

## Otázka 42

Proč zapisujeme informaci o vytvoření Excelu až po dokončení bloku `ExcelWriter`?

- A) Aby log nepotvrdil vytvoření souboru, který ve skutečnosti nevznikl
- B) Protože `logging` nelze použít uvnitř funkce `main()`
- C) Aby se automaticky vytvořila databázová tabulka
- D) Protože logování funguje pouze po příkazu `return`

**Správná odpověď:** A

Úspěšné vytvoření výstupu zaznamenáme až ve chvíli, kdy byl soubor skutečně uložen.

---

## Otázka 43

Co znamená monitoring v rozsahu této lekce?

- A) Automatickou opravu všech chyb
- B) Vytvoření samostatného Power BI dashboardu
- C) Kontrolu logu, úspěchu procesu, počtů řádků, chyb a délky zpracování
- D) Pravidelné mazání vstupních dat

**Správná odpověď:** C

Jednoduchý monitoring znamená kontrolovat podle logu stav a výsledek automatizovaného procesu.

---

## Otázka 44

Proč citlivé údaje, například API klíč, nemají být zapsané přímo v Python kódu?

- A) Python neumí pracovat s API klíči
- B) Mohly by se zveřejnit spolu s kódem
- C) API klíč musí být vždy uložený v SQL Serveru
- D) Citlivé údaje zpomalují Python

**Správná odpověď:** B

Citlivý údaj zapsaný v kódu by se mohl dostat do repozitáře a být zneužit.

---

## Otázka 45

Jaký je účel lokálního souboru `.env`?

- A) Uchovávat lokální konfigurační a citlivé hodnoty mimo kód
- B) Uchovávat výsledný Excelový report
- C) Zaznamenávat historii spuštění procesu
- D) Instalovat externí Python balíčky

**Správná odpověď:** A

Soubor `.env` odděluje místní konfiguraci a citlivé hodnoty od zdrojového kódu.

---

## Otázka 46

Co má obsahovat soubor `.env.example`?

- A) Skutečná hesla a přístupové tokeny
- B) Kompletní kopii Python skriptu
- C) Názvy proměnných bez skutečných citlivých hodnot
- D) Pouze seznam nainstalovaných knihoven

**Správná odpověď:** C

Soubor `.env.example` ukazuje požadované proměnné, ale neobsahuje jejich skutečné citlivé hodnoty.

---

## Otázka 47

K čemu slouží zápis `.env` v souboru `.gitignore`?

- A) Automaticky smaže soubor `.env` z počítače
- B) Zašifruje hodnoty v souboru `.env`
- C) Načte hodnoty z `.env` do Pythonu
- D) Zabrání Gitu sledovat soubor `.env`

**Správná odpověď:** D

Pravidlo v `.gitignore` zabrání běžnému přidání souboru `.env` do repozitáře.

---

## Otázka 48

Co standardně vrátí `os.getenv("DATABASE_NAME")`, pokud proměnná neexistuje?

- A) Prázdný DataFrame
- B) `None`
- C) Číslo `0`
- D) Návratový kód `1`

**Správná odpověď:** B

Pokud proměnná není dostupná a neurčíme výchozí hodnotu, `os.getenv()` vrátí `None`.

---

## Otázka 49

Co provede `load_dotenv(env_file)`?

- A) Načte hodnoty z `.env` do proměnných prostředí procesu
- B) Nahraje soubor `.env` na GitHub
- C) Vytvoří databázi v SQL Serveru
- D) Zapíše hodnoty do Excelu

**Správná odpověď:** A

Funkce `load_dotenv()` přečte soubor a zpřístupní jeho hodnoty běžícímu Python procesu.

---

## Otázka 50

Co je connection string?

- A) Aktivní databázové spojení
- B) SQL dotaz pro výběr řádků
- C) Text s parametry potřebnými pro připojení k databázi
- D) Soubor se seznamem Python knihoven

**Správná odpověď:** C

Connection string obsahuje například driver, server, databázi a způsob přihlášení.

---

## Otázka 51

Proč náš connection string neobsahuje databázové heslo?

- A) LocalDB žádná hesla nikdy nepodporuje
- B) Heslo automaticky poskytuje soubor `requirements.txt`
- C) Heslo je automaticky uložené v souboru `.env.example`
- D) Používáme přihlášení pomocí účtu Windows

**Správná odpověď:** D

Nastavení `Trusted_Connection=yes` používá ověření aktuálního uživatele Windows.

---

## Otázka 52

K čemu slouží GitHub Secrets?

- A) K bezpečnému uložení citlivých hodnot pro GitHub Actions
- B) K ukládání veřejných screenshotů projektu
- C) K nahrazení všech souborů `.gitignore`
- D) K automatickému čištění CSV souborů

**Správná odpověď:** A

GitHub Secrets umožňují předat citlivé hodnoty workflow bez jejich zapsání do repozitáře.

---

## Otázka 53

Proč jsme do `requirements.txt` přidali `python-dotenv`, ale nepřidali `os` ani `sys`?

- A) `os` a `sys` se nikdy nesmějí importovat
- B) `python-dotenv` je součástí SQL Serveru
- C) `python-dotenv` je externí balíček, zatímco `os` a `sys` jsou součástí Pythonu
- D) `requirements.txt` může obsahovat pouze jeden import

**Správná odpověď:** C

Do `requirements.txt` zapisujeme externí závislosti instalované přes `pip`, nikoliv standardní moduly Pythonu.

---

## Otázka 54

Jaká je hlavní úloha souboru `run_pipeline.bat` v našem procesu?

- A) Provádět transformace v pandas
- B) Spustit správný Python interpreter a Python skript
- C) Vytvořit databázové tabulky
- D) Nahradit Windows Task Scheduler

**Správná odpověď:** B

BAT soubor spustí Python z projektového virtuálního prostředí a předá mu cestu ke skriptu.

---

## Otázka 55

Co způsobí příkaz `@echo off` na začátku BAT souboru?

- A) Skryje vypisování prováděných BAT příkazů
- B) Vypne všechny chybové zprávy
- C) Ukončí otevřený terminál
- D) Aktivuje virtuální prostředí

**Správná odpověď:** A

Příkaz omezí technické výpisy BAT příkazů, ale chyby Pythonu zůstávají viditelné.

---

## Otázka 56

Co v BAT souboru označuje zápis `%~dp0`?

- A) Složku Python interpreteru
- B) Aktuální uživatelský profil
- C) Složku, ve které leží spuštěný BAT soubor
- D) Složku výstupního Excelu

**Správná odpověď:** C

Zápis vrací cestu ke složce aktuálního BAT souboru.

---

## Otázka 57

Proč před spuštěním Python skriptu používáme příkaz `cd /d`?

- A) Aby se vytvořila databáze
- B) Aby se aktivoval Python balíček
- C) Aby se vymazal předchozí výstup
- D) Aby se nastavila správná pracovní složka a případně změnil disk

**Správná odpověď:** D

`cd` změní pracovní složku a přepínač `/d` dovolí současně změnit také disk.

---

## Otázka 58

Proč v BAT souboru voláme přímo `.venv\Scripts\python.exe`?

- A) Aby nebyl potřeba Python skript
- B) Aby se použil Python a knihovny ze správného virtuálního prostředí
- C) Aby se automaticky vytvořilo `.venv`
- D) Aby se otevřel VS Code

**Správná odpověď:** B

Přímá cesta zaručí použití Pythonu a nainstalovaných knihoven z projektového `.venv`.

---

## Otázka 59

K čemu jsme při testování dočasně použili příkaz `pause`?

- A) K ponechání okna otevřeného, abychom mohli přečíst výstup
- B) K pozastavení denního plánu
- C) K vrácení návratového kódu `0`
- D) K uzavření databázového spojení

**Správná odpověď:** A

`pause` čeká na stisknutí klávesy, takže se příkazové okno ihned nezavře.

---

## Otázka 60

Proč nemá příkaz `pause` zůstat ve finálním BAT souboru pro plánované spuštění?

- A) Protože odstraní vytvořený Excel
- B) Protože změní pracovní složku
- C) Protože by automatická úloha čekala na stisknutí klávesy
- D) Protože vypne virtuální prostředí

**Správná odpověď:** C

Plánovaný proces by zůstal čekat na ruční zásah a řádně by se nedokončil.

---

## Otázka 61

Co dělá příkaz `exit /b %ERRORLEVEL%` na konci BAT souboru?

- A) Spustí Python podruhé
- B) Ukončí BAT soubor a předá návratový kód systému Windows
- C) Vymaže předchozí log
- D) Otevře výsledný Excel

**Správná odpověď:** B

BAT soubor předá Windows informaci, zda Python proces skončil úspěchem, nebo chybou.

---

## Otázka 62

Co v našem případě znamená výsledek posledního spuštění `0x0`?

- A) Úloha byla úspěšně dokončena
- B) Úloha ještě nebyla spuštěna
- C) Vstupní soubor nebyl nalezen
- D) Proces vytvořil nula řádků

**Správná odpověď:** A

Hodnota `0x0` odpovídá návratovému kódu `0`, který označuje úspěšné dokončení.

---

## Otázka 63

Jak nejlépe ověříme úspěch automaticky spuštěného procesu?

- A) Pouze otevřením VS Code
- B) Pouze existencí BAT souboru
- C) Kontrolou výsledku `0x0`, nového záznamu v logu a aktualizovaného výstupu
- D) Kontrolou posledního přístupu k Excelu

**Správná odpověď:** C

Návratový kód, log a skutečně aktualizovaný Excel společně potvrzují úspěšný běh.

---
