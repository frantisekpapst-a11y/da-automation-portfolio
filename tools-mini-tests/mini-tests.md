# Minitesty – automatizace datového procesu

Minitesty vycházejí z praktického projektu automatického zpracování denních CSV souborů pomocí Pythonu, BAT souboru a Windows Task Scheduleru.

---

## Otázky

### 1. Jaký je správný tok vytvořené automatizace?

A. Python → Windows Task Scheduler → BAT → log  
B. Windows Task Scheduler → BAT → Python → CSV a databáze → log  
C. BAT → databáze → Windows Task Scheduler → Python  
D. SQL Server → Python → Windows Task Scheduler → BAT

### 2. Jaká je hlavní úloha Windows Task Scheduleru?

A. Určit, kdy se proces automaticky spustí  
B. Provést validaci CSV souborů  
C. Spojit data pomocí pandas  
D. Vytvořit databázovou tabulku

### 3. Jaká je hlavní úloha BAT souboru?

A. Nahradit Python skript  
B. Spustit správný Python interpreter a Python skript  
C. Uložit data přímo do SQL Serveru  
D. Vytvořit log bez použití Pythonu

### 4. Proč BAT soubor používá úplné cesty k Pythonu a skriptu?

A. Aby se soubory automaticky přejmenovaly  
B. Aby spuštění nebylo závislé na aktuální složce ani aktivovaném virtuálním prostředí  
C. Aby mohl pandas načíst více CSV souborů  
D. Aby SQL Server povolil připojení

### 5. K čemu slouží `Path(__file__).resolve()`?

A. Vrátí absolutní cestu k právě spuštěnému Python souboru  
B. Spustí Python soubor  
C. Vytvoří databázovou tabulku  
D. Zapíše zprávu do logu

### 6. Co znamená `NaT` v pandas?

A. Nulovou hodnotu v číselném sloupci  
B. Neplatnou nebo chybějící hodnotu data a času  
C. Duplicitní řádek  
D. Nenalezený text

### 7. Co má validace vstupních CSV souborů kontrolovat?

A. Pouze počet souborů  
B. Pouze názvy poboček  
C. Povinné sloupce, datové typy, chybějící a neplatné hodnoty, duplicity a správné datum  
D. Pouze připojení k internetu

### 8. Proč se kontroluje shoda data uvnitř CSV se zpracovávaným dnem?

A. Aby nebyla omylem zpracována data za jiný den  
B. Aby se změnilo pořadí sloupců  
C. Aby se zmenšila velikost souboru  
D. Aby bylo možné spustit BAT soubor

### 9. Co znamená idempotentní proces?

A. Proces lze bezpečně opakovat se stejnými vstupy, aniž by vytvářel další duplicity  
B. Proces může být spuštěn pouze jednou  
C. Proces nepotřebuje validaci  
D. Proces vždy smaže celou databázi

### 10. Proč se před vložením dat odstraní z databáze záznamy za stejný den?

A. Aby opakované spuštění nevytvořilo duplicitní řádky  
B. Aby se odstranily všechny historické záznamy  
C. Aby nebylo nutné použít SQL  
D. Aby se změnil formát data

### 11. K čemu slouží databázová transakce?

A. Zajišťuje, že se související databázové operace potvrdí společně, nebo se při chybě vrátí zpět  
B. Automaticky naplánuje další spuštění  
C. Převádí CSV na Excel  
D. Aktivuje virtuální prostředí

### 12. Jaký je rozdíl mezi `COMMIT` a `ROLLBACK`?

A. `COMMIT` potvrdí změny, `ROLLBACK` je při chybě vrátí zpět  
B. `COMMIT` smaže data, `ROLLBACK` je uloží  
C. Oba příkazy dělají totéž  
D. Používají se pouze pro CSV soubory

### 13. Proč se výsledný CSV soubor nejprve ukládá jako dočasný soubor?

A. Aby se hotový výstup nahradil až po úspěšném dokončení důležitých kroků  
B. Aby se soubor automaticky otevřel ve VS Code  
C. Aby se přeskočila validace  
D. Aby se zvýšil počet řádků

### 14. Co znamená návratový kód `0`?

A. Proces skončil úspěšně  
B. Proces skončil chybou  
C. Nebyl nalezen žádný soubor  
D. Databáze byla odstraněna

### 15. Co obvykle znamená nenulový návratový kód, například `1`?

A. Proces skončil chybou  
B. Proces skončil úspěšně  
C. Byla načtena právě jedna pobočka  
D. Windows Task Scheduler je vypnutý

### 16. K čemu slouží logování?

A. K průběžnému záznamu spuštění, jednotlivých kroků, výsledků a chyb  
B. Pouze ke změně názvů souborů  
C. K vytvoření virtuálního prostředí  
D. K instalaci SQL Serveru

### 17. Jak poznáme v logu jedno samostatné spuštění procesu?

A. Podle úvodního oddělovače a zprávy `NOVÉ SPUŠTĚNÍ PROCESU`  
B. Podle názvu otevřené záložky ve VS Code  
C. Podle barvy textu v terminálu  
D. Podle počtu sloupců v databázi

### 18. Co dělá příkaz `GO` v SQL skriptu?

A. Odděluje dávky příkazů v klientském nástroji; není to běžný příkaz jazyka T-SQL  
B. Potvrzuje databázovou transakci  
C. Spouští BAT soubor  
D. Ukončuje Python program

### 19. Co je nutné pro připojení Pythonu k SQL Serveru pomocí `pyodbc`?

A. Pouze VS Code  
B. Knihovna `pyodbc`, příslušný ODBC ovladač a správný connection string  
C. Pouze pandas  
D. Jupyter Notebook

### 20. Kde ve Windows Task Scheduleru nastavujeme jednotlivé části úlohy?

A. Čas na kartě **Aktivační události**, spouštěný BAT na kartě **Akce** a doplňující pravidla na kartách **Podmínky** a **Nastavení**  
B. Všechno pouze na kartě **Obecné**  
C. Všechno pouze v Python skriptu  
D. Všechno pouze v SQL Serveru

---

## Řešení

1. **B** – Scheduler určí čas, BAT spustí Python a Python zpracuje i uloží data a zapíše průběh do logu.
2. **A** – Scheduler řídí čas a podmínky automatického spuštění.
3. **B** – BAT soubor spouští konkrétní Python interpreter a konkrétní skript.
4. **B** – Úplné cesty zajišťují spolehlivé spuštění i bez ručně aktivovaného virtuálního prostředí.
5. **A** – `__file__` označuje spuštěný soubor, `Path` vytvoří objekt cesty a `resolve()` ji převede na absolutní podobu.
6. **B** – `NaT` znamená **Not a Time**, tedy chybějící nebo neplatné datum či čas.
7. **C** – Validace zachytí strukturální i obsahové problémy ještě před uložením výsledku.
8. **A** – Název souboru sám o sobě nezaručuje, že řádky uvnitř obsahují správné datum.
9. **A** – Opakování se stejnými vstupy vede ke stejnému výsledku bez přidávání duplicit.
10. **A** – Staré záznamy za daný den se nahradí aktuálním výsledkem.
11. **A** – Transakce chrání konzistenci databáze: při úspěchu se změny potvrdí, při chybě vrátí.
12. **A** – `COMMIT` změny uloží, zatímco `ROLLBACK` nepotvrzené změny zruší.
13. **A** – Dočasný soubor omezuje riziko, že po selhání zůstane neúplný nebo zavádějící finální výstup.
14. **A** – Kód `0` standardně označuje úspěšné dokončení procesu.
15. **A** – Nenulový kód signalizuje volajícímu programu nebo Scheduleru chybu.
16. **A** – Log poskytuje dohledatelnost, tedy možnost zpětně ověřit, co proces provedl a kde případně selhal.
17. **A** – Oddělovač a úvodní zpráva jasně rozdělují jednotlivá spuštění v jednom logovacím souboru.
18. **A** – `GO` rozpoznává například SQL klient; odešle předchozí blok jako samostatnou dávku. SQL Server ho nevykonává jako standardní T-SQL příkaz.
19. **B** – Python potřebuje knihovnu, systémový ODBC ovladač i údaje určující server, databázi a způsob ověření.
20. **A** – Každá karta má jinou roli: trigger určuje kdy, action co a conditions/settings za jakých doplňujících pravidel.
