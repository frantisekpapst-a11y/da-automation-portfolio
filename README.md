A10 — SQL scheduling
Témata
princip SQL Server Agentu;
job;
job step;
schedule;
historie spuštění;
úspěch a chyba;
kdy plánovat proces v databázi;
kdy použít Python;
kdy použít orchestrační platformu.
Omezení LocalDB

LocalDB nemá SQL Server Agent. Praktickou variantou proto bude:

Windows Task Scheduler
→ Python nebo sqlcmd
→ SQL LocalDB
→ SQL skript nebo uložená procedura
SQL scheduling je vhodný, když
celý proces zůstává v SQL Serveru;
transformaci lze provést uloženou procedurou;
výstup zůstává v databázi;
nejsou potřeba API ani soubory;
databázový tým job spravuje.
Python je vhodnější, když
získáváme data z API;
zpracováváme JSON, CSV nebo Excel;
kombinujeme různé zdroje;
potřebujeme nestandardní logiku;
vytváříme souborové výstupy;
Python řídí validaci a logování.

A11 — Power Query a Power BI refresh
Power Query refresh

Power Query definuje:

připojení ke zdroji;
načítání;
transformační kroky;
načtení výsledku.

Prostředí, ve kterém Power Query běží, určuje způsob obnovy.

Power Query
→ jak data načíst a transformovat

Excel nebo Power BI
→ kdy obnovu spustit
Kdy Power Query stačí
proces má málo zdrojů;
transformace jsou jednoduché;
zdroje jsou přímo dostupné;
nejsou složité závislosti;
není potřeba pokročilé logování;
případná chyba nevyžaduje speciální reakci.
Kdy potřebujeme další automatizaci
nejprve se musí stáhnout API;
musí proběhnout Python;
několik zdrojů je dostupných v různých časech;
publikace závisí na validaci;
je potřeba detailní log;
chyba musí zastavit navazující kroky.
Power BI
scheduled refresh;
data source credentials;
refresh history;
gateway;
závislost na dostupnosti zdroje;
poslední úspěšná aktualizace;
Power BI Desktop versus Power BI Service.
Praktický rozsah
SQL LocalDB nebo exportní soubor
→ Power BI Desktop
Gateway a plánovanou obnovu v Power BI Service probereme koncepčně.

A12 — Závěrečná case study Automation
Daily Pricing Control Automation
Vstupy
SQL Server LocalDB s produkty a nákupními cenami;
API s měnovými kurzy;
Excel s cenovými limity.
Datový tok
Windows Task Scheduler
→ .bat
→ Python
→ SQL LocalDB + API + Excel
→ validace
→ převod cen do CZK
→ kontrola cenových limitů
→ zápis výsledku
→ export pro Power BI
→ log
GitHub Actions větev
GitHub Actions
→ plánované stažení kurzů
→ validace
→ export
→ workflow artifact
Výstupy
funkční Python skript;
SQL skripty;
.bat;
.env.example;
log;
ukázkový export;
naplánovaná úloha;
GitHub Actions workflow;
README;
Automation cheatsheet;
minitesty.