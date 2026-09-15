Case Study 03 — Daily Purchase Price Control Automation
Obchodní zadání

Firma nakupuje produkty v různých měnách. Každý pracovní den potřebuje:

získat aktuální měnové kurzy;
přepočítat nákupní ceny do CZK;
porovnat je se schválenými cenovými limity;
označit produkty mimo limit;
uložit výsledky do databáze;
připravit Excel pro analytický tým;
aktualizovat podklad pro Power BI;
zaznamenat průběh do logu.
Navržená architektura

Power BI tedy nebude číst Excel. Excel i Power BI budou dva rozdílné výstupy stejného procesu:

Python → SQL výsledky → Power BI Desktop
       └→ Excel pro analytický tým

Tím se vyhneme zbytečnému toku:

Python → SQL → Excel → Power BI

Excel by se v takovém případě stal zbytečným a potenciálně problematickým mezikrokem.

Použité zdroje a formáty
Oblast	Zdroj nebo formát	Proč
Produkty a nákupní ceny	SQL LocalDB	Jde o strukturovaná firemní data
Měnové kurzy	ČNB API – JSON	JSON je přirozený výstup API
Cenové limity	Excel	Limity může udržovat nákupní nebo finanční tým
Výsledky kontroly	SQL tabulka	Stabilní zdroj pro dotazy a Power BI
Analytický výstup	Excel	Ad hoc kontrola a další práce analytiků
Nezpracovaná API odpověď	JSON	Audit, dohledání chyb a opakovatelnost
Provozní informace	LOG	Monitoring automatizace

Použijeme skutečné JSON API České národní banky, nikoliv uměle vytvořené kurzy.

CSV bych do hlavního procesu nepřidával. Použili bychom ho pouze tehdy, kdyby ho skutečně dodával některý systém nebo obchodní partner.

SQL tabulky

Rozumný rozsah budou tři tabulky:

dbo.products
dbo.exchange_rates
dbo.pricing_control_results

Případně nad výslednou tabulkou vytvoříme pohled:

dbo.vw_pricing_control_report

Na tento pohled se připojí Power BI.

Výsledná data mohou obsahovat například:

control_date
product_id
product_name
purchase_currency
purchase_price_original
exchange_rate
purchase_price_czk
minimum_price_czk
maximum_price_czk
control_status
processed_at

Stav kontroly:

BELOW_LIMIT
OK
ABOVE_LIMIT
Důležitý detail přepočtu měn

Kurz nemusí být vždy uveden pro jednu jednotku měny. Některá měna může být například uvedena pro 100 jednotek.

Proto použijeme:

cena v CZK = nákupní cena / množství z kurzu × kurz v CZK

Pro CZK nastavíme:

množství = 1
kurz = 1

Tohle je velmi dobrý reálný validační případ.

Validace

Proces před publikací ověří:

dostupnost SQL databáze;
dostupnost API;
existenci Excelu s limity;
povinné sloupce;
neprázdná vstupní data;
unikátní product_id;
kladné nákupní ceny;
kladné kurzy;
dostupnost kurzu pro každou používanou měnu;
existenci limitu pro každý produkt;
že minimální limit není vyšší než maximální;
aktuálnost kurzovního lístku;
chybějící a neplatné hodnoty.

U aktuálnosti nesmíme jednoduše vyžadovat dnešní datum. O víkendu nebo ve svátek bude správně použit poslední dostupný pracovní den.

Denní lokální úlohu bychom spouštěli až odpoledne, například v 15:30, protože ČNB zveřejňuje kurzovní lístek během pracovního dne.

Výstupy
SQL

dbo.pricing_control_results

Výsledky jednoho běhu pro všechny produkty.

Excel

Například:

pricing_control_report_20260915.xlsx

Listy:

All products
Exceptions
Run summary

Excel bude určený pro analytiky, nikoliv jako zdroj Power BI.

Power BI

Power BI Desktop se připojí na:

dbo.vw_pricing_control_report

Základní report může obsahovat:

počet kontrolovaných produktů;
počet produktů v limitu;
počet produktů nad limitem;
počet produktů pod limitem;
podíl produktů mimo limit;
tabulku výjimek;
porovnání ceny s minimálním a maximálním limitem;
filtr podle měny a výsledného stavu;
datum posledního zpracování.

Obnovu v Power BI Desktop zatím provedeme ručně. Automatickou obnovu prostřednictvím OneDrive, Power BI Service nebo gateway necháme na pozdější end-to-end projekt.

Další technické výstupy
data/raw/exchange_rates_YYYYMMDD_HHMMSS.json
data/output/pricing_control_report_YYYYMMDD.xlsx
logs/pricing_control.log

Do GitHubu bychom uložili pouze malé ukázkové soubory. Pravidelně vytvářená provozní data do repozitáře nepatří.

Role GitHub Actions

GitHub Actions bych nepoužíval jako druhý produkční plánovač stejného procesu. Lokální pipeline totiž pracuje s LocalDB a lokálním Excelem, ke kterým GitHub runner nemá přístup.

GitHub Actions bude mít realističtější roli:

push nebo ruční spuštění
→ instalace Pythonu
→ instalace knihoven
→ kontrola syntaxe
→ test validačních funkcí
→ test dostupnosti API
→ vytvoření testovacího výstupu
→ uložení testovacího reportu jako artifact

Workflow artifact je výstup konkrétního běhu workflow, vhodný například pro testovací report, nikoliv jako hlavní provozní úložiště dat. GitHub Docs – workflow artifacts

Upravený seznam výstupů case study
funkční Python pipeline;
SQL skripty pro vytvoření tabulek a pohledu;
ukázková data produktů;
Excel s cenovými limity;
připojení na skutečné kurzovní API;
ukládání raw JSON odpovědí;
validace a čištění dat;
transakční zápis do SQL;
Excelový report;
Power BI report připojený na SQL;
logovací soubor;
.bat soubor;
.env.example;
naplánovaná úloha ve Windows Task Scheduleru;
GitHub Actions workflow pro kontrolu projektu;
ukázkový workflow artifact;
README s popisem architektury a spuštění.

Tento rozsah je velmi dobrý závěrečný projekt pro juniorního datového analytika: propojuje SQL, Python, API, Excel, Power BI, validaci, logging, plánování i GitHub Actions, ale zatím nevyžaduje cloudovou infrastrukturu ani gateway.