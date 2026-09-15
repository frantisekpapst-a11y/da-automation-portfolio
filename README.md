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
GitHub Actions workflow.