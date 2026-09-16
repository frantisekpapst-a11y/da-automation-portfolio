# ⚙️ Data Automation Portfolio

Portfolio zaměřené na **praktickou automatizaci datových procesů pro datovou analytiku a reporting**.

Repozitář obsahuje případové studie, technické moduly a referenční materiály pokrývající návrh a implementaci lokálních automatizovaných workflow — od zpracování souborů přes API, validaci a SQL databáze až po plánované spouštění, logování a návaznost na Power BI.

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
│   └── 03-daily-purchase-price-control-automation/
├── automation-cheatsheet/
│   └── automation-cheatsheet.md
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
- oddělení datové pipeline od prezentační vrstvy.

---

# 📁 Case Studies

Případové studie jsou prezentovány **od nejnovějšího a nejreprezentativnějšího projektu po starší a jednodušší řešení**.

Na prvním místě je projekt, který nejlépe ukazuje aktuální rozsah mojí praktické práce s automatizací, Pythonem, API, SQL a Power BI. Původní číslování zůstává zachováno a zároveň dokumentuje vývoj od návrhu procesu k jeho implementaci a následně ke komplexnějšímu end-to-end řešení.

---

## Case Study 03 — Daily Purchase Price Control Automation

Nejkomplexnější projekt v repozitáři propojující externí API, Python, datovou validaci, SQL Server, Windows Task Scheduler a Power BI.

Hlavní workflow:
```text
Windows Task Scheduler
→ BAT
→ Python
→ produkty v SQL + kurzovní lístek ČNB + cenové limity v Excelu
→ validace a business pravidla
→ raw JSON + SQL databáze + log
→ Power BI dashboard
```

Použité koncepty:
- načtení produktů z SQL databáze;
- získání kurzovního lístku z API České národní banky;
- archivace původních JSON odpovědí;
- načtení cenových limitů z Excelu;
- validace struktury, povinných hodnot a duplicit;
- propojení více datových zdrojů;
- přepočet nákupních cen do CZK;
- klasifikace `BELOW LIMIT`, `OK` a `ABOVE LIMIT`;
- idempotentní zápis podle kontrolního data;
- databázový reportingový pohled;
- logování a předání návratového kódu;
- automatické denní spuštění;
- DAX míry a interaktivní manažerský dashboard.

Projekt demonstruje rozdělení rolí mezi jednotlivé technologie:
```text
Python
→ ingestion, validation, transformation a orchestrace procesu

SQL Server
→ relační uložení, integrita a reportovací vrstva

Windows Task Scheduler + BAT
→ časové spuštění a řízení návratového kódu

Power BI
→ datový model, DAX, monitoring výsledků a reporting
```

![Power BI dashboard denní kontroly nákupních cen](automation-case-studies/03-daily-purchase-price-control-automation/screenshots/01_dashboard_overview.png)

➡️ [Otevřít Case Study 03](automation-case-studies/03-daily-purchase-price-control-automation/)

---

## Case Study 02 — Daily Branch Report with Windows Task Scheduler

Praktická implementace lokální automatizace denního reportu návštěvnosti poboček.

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

# 🧩 Data Automation Skills

Portfolio pokrývá praktickou práci s automatizací od návrhu procesu až po lokálně provozované end-to-end řešení.

Hlavní oblasti:
- analýza ručního procesu a návrh cílového workflow;
- časové a událostní spouštění;
- rozdělení procesu na navazující tasky;
- Python skripty a práce s cestami;
- CSV, JSON a Excel;
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
- Power Query, Power BI a DAX;
- rozdíl mezi aktualizací zdroje, datového modelu a reportu.

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
- transakční zpracování;
- ochranu před duplicitami;
- kontrolní dotazy;
- přípravu reportovací vrstvy pro Power BI.

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

- **aktualizace zdrojových dat** — provádí ji Python pipeline;
- **refresh Power BI** — znovu načte zdroj do datového modelu.

V lokálních projektech používajících Power BI Desktop zůstává refresh `.pbix` souboru ruční. Automatický refresh Power BI Service není vydáván za implementovanou součást řešení.

---

# 📚 Technické materiály

## Automation Cheatsheet

Referenční dokument shrnující hlavní principy datové automatizace, spouštění, validace, logování, databázového ukládání a návaznosti na reporting.

➡️ [Automation Cheatsheet](automation-cheatsheet/automation-cheatsheet.md)

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
Power Query
Power BI
DAX
Git
GitHub
VS Code
```