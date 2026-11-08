# ⚙️ Data Automation Portfolio

Portfolio zaměřené na **praktickou automatizaci datových procesů pro datovou analytiku a reporting pomocí Pythonu, SQL a Power Automate**.

Repozitář obsahuje případové studie, technické moduly a referenční materiály pokrývající návrh a implementaci lokálních automatizovaných workflow — od zpracování souborů přes API, validaci a SQL databáze až po plánované spouštění, logování a návaznost na Power BI. Součástí jsou také desktopové toky pro kontrolu tržeb v Excelu a webový export dat s následným načtením přes Power Query.

Repozitář představuje lokální portfolio řešení zaměřená na automatizaci analytických procesů. Použité prostředí odpovídá dostupným technologiím a umožňuje prakticky demonstrovat návrh, implementaci a kontrolu celého workflow. Projekty tedy nejsou prezentovány jako produkční enterprise platforma.

Hlavní oblasti:

- návrh automatizovaných datových procesů;
- Python skripty pro opakovatelné zpracování dat;
- práce s CSV, JSON, Excel a API;
- datová validace a řízení chyb;
- SQL Server LocalDB a databázové transakce;
- idempotentní ukládání bez duplicit;
- logování a provozní kontrola běhů;
- konfigurace prostředí a práce s `.env`;
- BAT soubory a Windows Task Scheduler;
- Power Automate Desktop a automatizace práce v Excelu;
- webová automatizace, selektory a stahování souborů;
- přejmenování, přesun a archivace exportů;
- výběr nejnovějšího souboru a příprava dat přes Power Query;
- příprava dat pro Power BI;
- rozlišení mezi aktualizací zdrojových dat a refreshem reportu.

---

# 📂 Struktura repozitáře

```text
da-automation-portfolio/
├── .github/
├── automation-case-studies/
│   ├── 01-daily-branch-report-automation.md
│   ├── 02-daily-branch-report-task-scheduler/
│   ├── 03-branch-sales-check-power-automate/
│   │   ├── output/
│   │   │   └── Trzby_pobocky.xlsx
│   │   ├── screenshots/
│   │   └── README.md
│   └── 04-csob-web-export-power-automate/
│       ├── data/
│       ├── excel/
│       │   └── CSOB.xlsx
│       ├── output/
│       │   └── logs.txt
│       ├── power-automate/
│       │   ├── error_flow.txt
│       │   └── main_flow.txt
│       ├── screenshots/
│       └── README.md
├── automation-cheatsheet/
│   ├── automation-cheatsheet.md
│   └── power-automate-cheatsheet.md
├── automation-lessons/
│   ├── 02-python-script-basics/
│   ├── 03-api-automation/
│   ├── 04-sql-localdb-python/
│   ├── 05-validation-error-handling/
│   ├── 06-logging-monitoring/
│   ├── 07-secrets-environment-variables/
│   ├── 08-windows-task-scheduler-bat/
│   └── 11-power-query-power-bi-refresh/
├── tools-mini-tests/
│   └── mini-tests.md
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🎯 Zaměření portfolia

Repozitář demonstruje automatizaci v kontextu běžného analytického workflow:

```text
Business Requirement
→ Data Source
→ Trigger
→ Ingestion
→ Validation
→ Transformation
→ Database / Output
→ Logging
→ Reporting
```

Automatizace zde není pojatá pouze jako naplánované spuštění skriptu. Důraz je kladen také na:

- jasně definovaný business účel;
- kontrolu vstupních dat před zpracováním;
- bezpečné a opakovatelné ukládání;
- předvídatelné chování při chybě;
- návratové kódy pro nadřazený spouštěcí nástroj;
- dohledatelnost jednotlivých běhů;
- oddělení datové pipeline od prezentační vrstvy;
- automatizaci opakujících se úkonů v desktopových aplikacích a na webu;
- rozdělení odpovědností mezi Power Automate Desktop a Power Query;
- volbu nástroje podle úlohy — skript, excelový výpočet, datová transformace nebo obsluha uživatelského rozhraní.

Jednotlivé studie mají různý rozsah. Kontrola tržeb ukazuje základní práci s cyklem a podmínkou v Excelu; webový export doplňuje práci se soubory, logování a chybový dílčí tok. Plánované spuštění je implementováno v případové studii s Pythonem a Windows Task Schedulerem, zatímco oba desktopové toky se spouštějí ručně.

---

# 📁 Case Studies

## Case Study 01 — Daily Branch Report Automation

Koncepční návrh automatizovaného denního reportu návštěvnosti poboček.

Case study se zaměřuje na převod business požadavku do návrhu řízeného procesu ještě před výběrem konkrétní implementace.

Použité koncepty:

- událostní a časový trigger;
- závislosti mezi jednotlivými tasky;
- práce s chybějícími a opožděnými vstupy;
- zpracování opravených verzí souborů;
- výběr poslední validní verze;
- stavy `SUCCESS`, `WARNING` a `FAILED`;
- idempotence;
- bezpečné nahrazení výstupu;
- ochrana posledního správného reportu;
- návrh logování a provozních informací pro Power BI.

Projekt ukazuje, že automatizace začíná správnou procesní a business logikou, nikoli až samotným kódem.

➡️ [Otevřít Case Study 01](automation-case-studies/01-daily-branch-report-automation.md)

---

## Case Study 02 — Daily Branch Report with Windows Task Scheduler

Praktická implementace lokální automatizace denního reportu návštěvnosti poboček. Case study navazuje na case study 01.

Hlavní workflow:

```text
Windows Task Scheduler
→ BAT
→ Python
→ denní CSV soubory
→ validace a spojení dat
→ dočasný výstup + databázová transakce
→ výsledný CSV report + SQL tabulka + log
```

Použité koncepty:

- výběr vstupních souborů podle data;
- kontrola povinných sloupců a datových typů;
- validace chybějících hodnot a duplicit;
- spojení dat z více poboček;
- bezpečná publikace přes dočasný soubor;
- databázová transakce s `COMMIT` a `ROLLBACK`;
- opakované spuštění bez vzniku duplicit;
- návratové kódy pro Windows Task Scheduler;
- logování úspěšných běhů a chyb.

Projekt převádí navržený proces do funkční lokální varianty a ukazuje praktické propojení Pythonu, souborového systému, SQL databáze a plánovaného spouštění.

➡️ [Otevřít Case Study 02](automation-case-studies/02-daily-branch-report-task-scheduler/)

---

## Case Study 03 — Branch Sales Check with Power Automate Desktop

Lokální automatizace kontroly plnění tržeb poboček v Excelu. Tok porovná skutečné tržby s cílem, doplní stav a odchylku v Kč a zobrazí souhrnný počet poboček v obou kategoriích.

Použité koncepty:

- otevření a načtení excelového sešitu;
- datová tabulka a přístup ke sloupcům podle názvů;
- proměnné a inicializace počítadel;
- cyklus `For each` nad jednotlivými pobočkami;
- výpočet odchylky `Tržby − Cíl`;
- podmínka `If / Else` pro stavy `Splněno` a `Pod cílem`;
- zápis výsledků do konkrétních buněk;
- souhrnné počty, uložení sešitu a zavření Excelu.

Ověřovací dataset obsahuje čtyři pobočky: dvě splnily cíl a dvě zůstaly pod cílem. Test zahrnuje také přesné splnění cíle s nulovou odchylkou.

Studie dokumentuje základní desktopový tok pomocí screenshotů a výsledného sešitu. Neobsahuje samostatné logování ani chybový dílčí tok. Pro samotné výpočty by byly jednodušší excelové vzorce; zde je cílem procvičit řízení celého postupu v Power Automate Desktop.

➡️ [Otevřít Case Study 03](automation-case-studies/03-branch-sales-check-power-automate/)

---

## Case Study 04 — ČSOB Web Export with Power Automate Desktop

Automatizace stažení úplné historické řady vybraného fondu z veřejného webu ČSOB a následné načtení nejnovějšího exportu do Excelu přes Power Query.

Použité koncepty:

- otevření stránky v Microsoft Edge;
- webové prvky a úprava selektorů;
- výběr celého období grafu a vyvolání exportu;
- čekání na očekávaný CSV soubor s časovým limitem;
- přejmenování souboru podle ISIN a data exportu;
- přesun souboru a uchování denních exportů;
- logování výsledků `OK` a `CHYBA`;
- blok zpracování chyb a dílčí tok `Chyba_export`;
- získání poslední chyby, zavření prohlížeče a řízené zastavení;
- výběr nejnovějšího exportu v Power Query a nastavení datových typů.

Power Query načítá pouze nejnovější soubor, protože každý export již obsahuje úplnou historii. Ověřovací načtení obsahovalo 848 řádků a tři sloupce: `Datum`, `Hodnota` a `Výnos`.

Součástí jsou ukázkové CSV exporty, sešit Excelu, log a textové kopie akcí obou dílčích toků. Desktopový tok i navazující aktualizace Power Query se spouštějí ručně. Jde o samostatnou studii, oddělenou od Python projektu analýzy investičních fondů.

➡️ [Otevřít Case Study 04](automation-case-studies/04-csob-web-export-power-automate/)

---

# 🧩 Data Automation Skills

Portfolio pokrývá praktickou práci s automatizací od návrhu procesu až po lokálně provozované end-to-end řešení. Vedle skriptování obsahuje také vizuálně sestavené desktopové toky a jejich návaznost na Power Query.

Hlavní oblasti:

- analýza ručního procesu a návrh cílového workflow;
- časové a událostní spouštění;
- rozdělení procesu na navazující tasky;
- Python skripty a práce s cestami;
- CSV a JSON;
- veřejná API a HTTP komunikace;
- pandas pro validaci a transformace;
- SQL Server LocalDB;
- `pyodbc` a Windows Authentication;
- transakční zpracování;
- idempotence a ochrana před duplicitami;
- `try/except` a řízené ukončení procesu;
- logging a provozní kontrola;
- `.env` a oddělení konfigurace od zdrojového kódu;
- BAT a Windows Task Scheduler;
- tvorba lokálních toků v Power Automate Desktop;
- čtení a zápis do Excelu, proměnné, počítadla a datové tabulky;
- cykly `For each` a podmínky `If / Else`;
- webové selektory, kliknutí a čekání na stažení;
- přejmenování a přesun souborů, denní historie exportů;
- chybové bloky, dílčí toky a záznam poslední chyby;
- Power Query pro načtení nejnovějšího exportu a převod datových typů;
- rozlišení mezi obsluhou aplikace, datovou transformací a aktualizací reportu.

Důraz je kladen na tento princip:

```text
Reliable Input
→ Validated Data
→ Repeatable Processing
→ Controlled Output
→ Traceable Result
```

---

# 🔄 Technologie v automatizovaném workflow

## Python

Python řídí hlavní proces a zajišťuje zejména:

- načtení souborů, API a databázových dat;
- validaci struktury a obsahu;
- čištění a transformace;
- propojení datových zdrojů;
- business výpočty;
- databázový zápis;
- logování;
- návratový kód procesu.

---

## SQL Server

SQL Server LocalDB je v projektech použit pro:

- relační uložení výsledků;
- primární klíče a kontrolní omezení;
- kontrolní dotazy.

---

## Windows Task Scheduler a BAT

Lokální orchestrace používá následující princip:

```text
Windows Task Scheduler
→ určí čas spuštění

BAT
→ nastaví pracovní složku a spustí správný Python interpreter

Python
→ provede datovou pipeline a vrátí exit code
```

Úspěšný proces vrací kód `0`; chyba vrací nenulový kód použitelný pro provozní kontrolu.

---

## Power Automate Desktop

Power Automate Desktop zajišťuje lokální obsluhu aplikací a webového rozhraní:

- v případové studii 03 načítá Excel, vyhodnocuje tržby a zapisuje výsledky;
- v případové studii 04 ovládá web ČSOB, stahuje export, přejmenovává a přesouvá soubor;
- u webového exportu zaznamenává úspěch nebo chybu a používá samostatný chybový dílčí tok.

Oba toky se spouštějí ručně. Portfolio v těchto studiích neprezentuje cloudové ani bezobslužné spuštění jako implementovanou součást řešení.

---

## Excel a Power Query

Excel slouží jako vstupní i výstupní prostředí pro kontrolu tržeb. V případě ČSOB obsahuje sešit s dotazem Power Query, který:

- načte seznam souborů ve zdrojové složce;
- vyfiltruje příslušné CSV exporty;
- podle názvu vybere nejnovější soubor;
- načte jeho obsah, nastaví záhlaví a datové typy.

Power Automate Desktop řeší získání souboru a Power Query jeho tabulkové zpracování. Obnova dotazu v Excelu zůstává ruční. Denní exporty se nespojují pod sebe, protože každý obsahuje celou dostupnou historii fondu.

---

## Power BI

Power BI navazuje na automatizované datové zdroje jako prezentační a analytická vrstva.

```text
automatizace zdrojových dat
→ SQL / souborový výstup
→ Power Query
→ datový model
→ DAX
→ dashboard
```

Repozitář zároveň rozlišuje dvě samostatné činnosti:

- **aktualizace zdrojových dat** — provádí ji Python pipeline; v případové studii 04 získává CSV export Power Automate Desktop;
- **refresh Power BI** — znovu načte zdroj do datového modelu.

V lokálních projektech používajících Power BI Desktop zůstává refresh `.pbix` souboru ruční. Automatický refresh Power BI Service není vydáván za implementovanou součást řešení.

Případové studie 03 a 04 mají výstup v Excelu a samy neobsahují Power BI report.

---

# 📚 Technické materiály

## Automation Cheatsheet

Referenční dokument shrnující hlavní principy datové automatizace, spouštění, validace, logování, databázového ukládání a návaznosti na reporting.

➡️ [Automation Cheatsheet](automation-cheatsheet/automation-cheatsheet.md)

---

## Power Automate Cheatsheet

Samostatný referenční dokument k Power Automate Desktop: proměnné, podmínky, cykly, Excel, webové prvky, práce se soubory, čekání, logování a zpracování chyb. Doplňuje praktické případové studie 03 a 04.

➡️ [Power Automate Cheatsheet](automation-cheatsheet/power-automate-cheatsheet.md)

---

## Technické moduly

Složka `automation-lessons` obsahuje samostatné praktické implementace jednotlivých částí automatizovaného workflow:

- [Python Script Basics](automation-lessons/02-python-script-basics/)
- [API Automation](automation-lessons/03-api-automation/)
- [SQL LocalDB + Python](automation-lessons/04-sql-localdb-python/)
- [Validation & Error Handling](automation-lessons/05-validation-error-handling/)
- [Logging & Monitoring](automation-lessons/06-logging-monitoring/)
- [Secrets & Environment Variables](automation-lessons/07-secrets-environment-variables/)
- [Windows Task Scheduler & BAT](automation-lessons/08-windows-task-scheduler-bat/)
- [Power Query & Power BI Refresh](automation-lessons/11-power-query-power-bi-refresh/)

Tyto moduly slouží jako technický základ pro komplexnější případové studie. Každý se soustředí na konkrétní část procesu, kterou lze samostatně ověřit a následně zapojit do většího workflow.

Praktické ukázky Power Automate Desktop jsou zdokumentovány přímo v případových studiích 03 a 04. Případová studie 04 navíc obsahuje [text hlavního toku](automation-case-studies/04-csob-web-export-power-automate/power-automate/main_flow.txt) a [text chybového toku](automation-case-studies/04-csob-web-export-power-automate/power-automate/error_flow.txt) pro přenos akcí do návrháře aplikace. Před použitím je nutné upravit lokální cesty a ověřit webové prvky.

---

## Mini Tests

Sada krátkých otázek a odpovědí pro ověření praktického porozumění automatizaci, validaci, logování, Task Scheduleru, SQL integraci a aktualizaci Power BI.

➡️ [Automation Mini Tests](tools-mini-tests/mini-tests.md)

---

# 🛠 Technologie a koncepty

```text
Python
pandas
requests
python-dotenv
pyodbc
CSV
JSON
Excel
REST API
SQL Server LocalDB
SQL
ODBC
database transactions
data validation
error handling
logging
environment variables
BAT
Windows Task Scheduler
Power Automate Desktop
Microsoft Edge
web automation
UI elements and selectors
variables and data tables
For each
If / Else
file download and timeout
file renaming and archiving
subflows and block error handling
Power Query
Power Query M
Power BI
DAX
Git
GitHub
VS Code
```