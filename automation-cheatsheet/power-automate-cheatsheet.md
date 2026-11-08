# Power Automate Cheatsheet

Referenční přehled pro automatizaci práce se soubory, Excelem a webem. Hlavní část se věnuje **Power Automate Desktop (PAD)**; bod 20 rozšiřuje přehled o principy a praktické využití cloudových toků.

**Doporučené umístění v repozitáři:** `automation-cheatsheet/power-automate-cheatsheet.md`  

**Příklady:** klasické desktopové toky s vypnutým Power Fx, zápis proměnných `%Promenna%`.  

**Aktualizováno:** 8. 11. 2026. České názvy akcí se mohou mezi verzemi lišit; při hledání pomůže anglický název.

## 1. Kdy použít který nástroj

| Potřeba | Vhodný nástroj | Proč |
|---|---|---|
| Klikání ve webové nebo desktopové aplikaci, export reportu | Power Automate Desktop | Ovládání uživatelského rozhraní |
| Příchozí příloha, uložení na SharePoint, schválení, upozornění | Cloudový tok | Propojení služeb prostřednictvím konektorů |
| Spojení souborů, čištění a transformace tabulek | Power Query | Opakovatelné zpracování dat |
| API, rozsáhlejší validace, databázové načítání | Python / SQL | Přehlednější a výkonnější zpracování větších objemů |
| Opakované operace uvnitř excelového sešitu | Office Scripts / VBA podle prostředí | Práce přímo s objekty sešitu |

**Praktický návrh:** PAD stáhne a uloží export, Power Query ho načte a transformuje, Excel nebo Power BI zobrazí výsledky. Není nutné převádět všechny výpočty do akcí PAD.

## 2. Desktopový a cloudový tok

| Pojem | Význam |
|---|---|
| Desktop flow | Tok běžící na počítači s Windows |
| Cloud flow | Tok provozovaný službou Power Automate |
| RPA | Robotická automatizace procesů — ovládání aplikací podobně jako uživatelem |
| Trigger / spouštěč | Událost nebo plán, který zahájí tok |
| Action / akce | Jeden krok automatizace |
| Connector / konektor | Sada operací pro propojení s určitou službou |
| Connection / připojení | Konkrétní přihlášení a oprávnění pro použití konektoru |
| Attended / běh s obsluhou | Desktopový běh v aktivní uživatelské relaci |
| Unattended / běh bez obsluhy | Spravované spuštění desktopového toku bez přítomnosti uživatele; má další požadavky |

Naplánovaný start sám o sobě neznamená režim unattended. Cloudový tok, který pracuje jen s cloudovými službami, nepotřebuje zapnutý osobní notebook; desktopová část potřebuje dostupný stroj.

## 3. Účty, licence a provoz

- Lokální vytváření a ruční spouštění desktopových toků lze používat v rámci bezplatných oprávnění; pokročilé možnosti mají samostatné podmínky.

- Windows Home podporují místní desktopové toky, ale nepodporují jejich spouštění z cloudu.

- Pro cloudové propojení desktopového toku se používá pracovní nebo školní účet a odpovídající licence.

- Oficiální spuštění desktopového toku přes URL, zástupce nebo Plánovač úloh vyžaduje Premium nebo prostředí s platbou podle využití. Plánovač toto omezení neodstraňuje.

- Běh bez obsluhy má zvláštní licenční a provozní požadavky; samotná instalace PAD jej nezajišťuje.

- U místního běhu s obsluhou počítej se zapnutým počítačem, aktivní odemčenou relací a přístupem ke zdrojům.

- Uspání přeruší běžnou práci počítače. Zavření víka může notebook uspat podle nastavení Windows.

Licenční podmínky se mění. Před nasazením ověř konkrétní účet, plán a způsob spouštění v aktuální dokumentaci, ne pouze skutečnost, že aplikace jde otevřít. [1][2]

## 4. Orientace v návrháři

| Část | Použití |
|---|---|
| Akce vlevo | Vyhledání a vložení operace |
| Main | Hlavní posloupnost kroků |
| Dílčí toky | Oddělené části, například obsluha chyb |
| Proměnné vpravo | Průběžné hodnoty a výstupy akcí |
| Prvky uživatelského rozhraní | Uložené popisy tlačítek, polí a dalších prvků |
| Seznam chyb | Chybová zpráva, dílčí tok a řádek |

Akce běží postupně shora dolů. Odsazení a `End` určují rozsah podmínek, cyklů a chybových bloků.

**Pozor na „Spustit odtud“:** přeskočené kroky nevytvoří své proměnné. Bez předchozího spuštění Edge nebo Excelu může být `Browser` či `ExcelInstance` prázdná.

## 5. Proměnné a jejich zápis

Proměnná uchovává hodnotu pro další kroky. Vytvoří ji například akce **Nastavit proměnnou** nebo výstup jiné akce.

| Zápis | Příklad použití |
|---|---|
| `%NazevReportu%` | Hodnota proměnné |
| `Připravený report: %NazevReportu%` | Text doplněný hodnotou |
| `%Trzby - Cil%` | Číselný výpočet |
| `%CurrentItem.Name%` | Název souborového objektu |
| `%CurrentItem.Extension%` | Přípona souboru, např. `.csv` |
| `%AktualniRadek['Tržby']%` | Hodnota sloupce datového řádku |
| `%LastError.Message%` | Zpráva poslední zachycené chyby |

Při pojmenování proměnné zadávej například `NazevReportu`; při použití její hodnoty `%NazevReportu%`. Objektové vlastnosti, například `.Extension`, fungují jen pro odpovídající typ objektu, ne pro libovolnou textovou cestu. [3]

### Běžné datové typy

| Typ | Příklad | K čemu |
|---|---|---|
| Text | `Přehled prodeje` | Názvy, zprávy, cesty |
| Číslo | `120000` | Výpočty, čítače |
| Logická hodnota | True / False | Stav a rozhodování |
| Datum a čas | Aktuální okamžik | Logování a názvy exportů |
| Seznam | Soubory ve složce | Procházení přes For each |
| Datová tabulka | Načtená oblast Excelu | Práce s řádky a sloupci |
| Datový řádek | Jeden řádek tabulky | Přístup přes názvy sloupců |
| Instance | `Browser`, `ExcelInstance` | Odkaz na konkrétní ovládanou aplikaci |

## 6. Podmínky

**If → Else → End** rozděluje běh podle výsledku porovnání.

Příklad v návrháři:

1. První operand: `%Trzby%`.

2. Operátor: **Je menší než**.

3. Druhý operand: `100000`.

4. Uvnitř If: zpracování stavu „Pod cílem“.

5. Uvnitř Else: zpracování stavu „Splněno“.

Hodnota přesně `100000` patří do Else, protože podmínka používá `<`, nikoli `<=`.

**Else se provede, když je podmínka nepravdivá.** Akce za příslušným `End` se vykonají po obou větvích, pokud běh nebyl ukončen chybou nebo jiným řízením toku.

## 7. Cykly

| Akce | Kdy ji použít | Příklad |
|---|---|---|
| Cyklus / Loop | Známý číselný rozsah | Od 1 do 3 s krokem 1 |
| For each | Každá položka seznamu nebo řádek tabulky | Každý soubor v `Files` |
| Podmínka smyčky / Loop condition | Opakování závisí na podmínce | Dokud není dosažena mez |
| Výstupní smyčka / Exit loop | Předčasné ukončení cyklu | Po nalezení hledaného souboru |

Praktické zásady:

- Součty a čítače nastav před cyklem, například na `0`.

- `CurrentItem` je aktuální položka; s každým průchodem se mění.

- Akce uvnitř cyklu se opakují, akce za jeho `End` se provedou po dokončení.

- Nekonečné čekání nahraď limitem času nebo počtu pokusů.

- Pokud zpracováváš větší tabulku, zvaž Power Query, SQL nebo dávkový zápis místo tisíců samostatných operací.

## 8. Zprávy a ButtonPressed

Akce **Zobrazit zprávu** vytvoří dialog. Výstup `ButtonPressed` obsahuje zvolené tlačítko, například `OK`.

- Proměnná vzniká automaticky jako výstup akce.

- Lze ji použít v další podmínce při volbě Ano/Ne.

- Bez automatického zavření dialog obvykle čeká na reakci uživatele.

- Automatické zavření je jiné nastavení než „udržovat okno nahoře“.

- Dialog uvnitř cyklu vyžaduje opakované potvrzování; pro běžný provoz bývá vhodnější souhrn nebo log.

## 9. Soubory a složky

| Akce | Použití |
|---|---|
| Získat soubory ve složce | Načtení seznamu souborových objektů |
| Pokud soubor existuje | Rozhodnutí podle existence cesty |
| Počkat na soubor / Wait for file | Čekání na vytvoření nebo odstranění |
| Přejmenovat soubory | Úprava názvu |
| Přesunout soubory | Přesun do cílové složky |
| Zapsat text do souboru | Textový log nebo jiný textový výstup |

### Přesný název a výstupy

`export_FOND123` a `export_FOND123_1.csv` jsou různé názvy. U pevné cesty kontroluj i příponu.

Po přejmenování používej pro přesun výstup `%RenamedFiles%`, ne původní cestu. Po úspěšném přesunu lze dále pracovat s výstupem `%MovedFiles%`.

### Kolize názvů

| Cíl | Strategie |
|---|---|
| Poslední export každého dne | Datum v názvu a přepsání souboru stejného dne |
| Více exportů denně | Datum a čas nebo pořadové číslo |
| Jen aktuální stav | Pevný název a řízené přepsání |

**Přeskočení existujícího souboru nemusí vyvolat chybu.** Záznam OK má následovat až po kontrole požadovaného výsledku. [4]

## 10. Datum a čas v názvech

Postup: **Získat aktuální datum a čas → Převést datum a čas na text → vlastní formát**.

| Formát | Výsledek |
|---|---|
| `yyyy-MM-dd` | `2026-11-08` |
| `yyyy-MM-dd_HHmm` | `2026-11-08_1645` |
| `yyyy-MM-dd_HHmmss` | `2026-11-08_164530` |

`MM` = měsíc, `mm` = minuty, `HH` = hodiny ve 24hodinovém formátu. Pro názvy souborů nepoužívej dvojtečky ani lomítka.

Příklad pole **Nový název** při zapnutém zachování přípony:

```text
CSOB_FOND123_%CasExportu%
```

Název s datem stažení neříká, ke kterému dni jsou nejnovější hodnoty uvnitř exportu.

## 11. Excel: instance, čtení a zápis

Typický postup:

1. **Spustit Excel** a otevřít sešit → výstup `ExcelInstance`.

2. **Číst z listu aplikace Excel** → buňka nebo tabulka.

3. Zpracovat data.

4. **Zapsat do listu aplikace Excel** → cílová buňka nebo oblast.

5. Uložit a zavřít Excel.

Při čtení tabulky se záhlavím nastav první řádek jako názvy sloupců. Pak lze použít `%AktualniRadek['Pobočka']%`.

Pokud první datový řádek v Excelu leží na řádku 2, nastav `RadekExcel = 2` před cyklem a zvyšuj jej o 1 po zpracování každého řádku. Index položky seznamu není automaticky číslem řádku listu.

**Excel zavírej až za koncem cyklu.** Zavření uvnitř For each zneplatní instanci pro další průchod. Chyba „Instance aplikace Excel není inicializována“ proto nemusí znamenat překlep v názvu proměnné. [5]

## 12. Web: Browser a selektory

1. **Spustit nový Microsoft Edge** → otevřít URL → výstup `Browser`.

2. Webové akce používají `%Browser%`.

3. Prvek zachyť ve výběru pomocí **Ctrl + levého kliknutí**.

4. Ulož, otestuj a ověř skutečný výsledek.

Podle zvoleného způsobu propojení je potřeba příslušné rozšíření prohlížeče nebo kompatibilní WebDriver. [6]

**Selektor** popisuje prvek podle vlastností a umístění ve struktuře stránky. Nejde jen o obrázek nebo souřadnice.

Příklad příliš konkrétního atributu:

```text
Id je rovno highcharts-abc123-0
```

Pokud se identifikátor při načtení mění, lze po ověření zkusit:

```text
Id začíná na highcharts-
```

Širší selektor může odpovídat více grafům. Vždy ověř, že najde právě zamýšlený prvek; stabilní text a další vhodné vlastnosti pomáhají výběr zpřesnit.

### Fyzické a webové kliknutí

- Fyzické kliknutí závisí na zobrazení a poloze prvku; může ho ovlivnit překrytí okna nebo posun stránky.

- Kliknutí bez fyzické myši může být vhodnější pro konkrétní webový prvek.

- V našem exportním cvičení pomohlo vypnout **Odeslat fyzické kliknutí**. Není to univerzální nastavení pro všechny weby.

## 13. Čekání a ověření stažení

| Čekání | Účel |
|---|---|
| Pevné čekání, například 3 s | Jednoduchá prodleva; nezaručuje připravenost stránky |
| Počkat na obsah webové stránky | Čekání na požadovaný obsah/prvek |
| Počkat na soubor | Čekání na vznik očekávaného souboru |

U čekání na soubor zapni **Selhání s chybou časového limitu** a nastav například **60 sekund**. Chybějící export pak nezpůsobí neomezené čekání.

Před stažením zohledni existující soubory. Jinak prohlížeč může vytvořit název s `(1)` a čekání na původní cestu může použít starý soubor. Pro robustnější návrh použij vyhrazenou složku a rozlišení nových souborů od těch, které existovaly před během.

Samotná existence souboru ještě neověřuje jeho obsah. Podle významu procesu kontroluj velikost, možnost čtení, očekávané sloupce a počet řádků.

## 14. Dílčí toky a obsluha chyb

**Main** řídí hlavní postup. Dílčí tok může obsahovat opakovanou činnost nebo obsluhu chyby.

Pro společné ošetření více akcí:

1. Vlož **Chyba bloku / On block error**.

2. Do jeho rozsahu až po odpovídající `End` umísti chráněné akce.

3. Ve zpracování chyb přidej přes **+** pravidlo **Spustit dílčí tok**.

4. Vyber například `Chyba_export`.

Konkrétní nastavení chyby jednotlivé akce může změnit chování nadřazeného bloku. Zvlášť kontroluj specifickou chybu i položku **Všechny chyby (výchozí)**.

### Dílčí tok Chyba_export

1. **Získat poslední chybu** → `LastError`.

2. Připojit zprávu do logu.

3. Pokusit se zavřít `%Browser%`.

4. **Zastavit tok s chybou**.

U pomocného zavírání povol pokračování na další akci, pokud zavření selže. Prohlížeč totiž nemusel být vytvořen. Tento postup nepoužívej plošně na hlavní exportní operace.

Původní chybu zachyť před úklidem. Závěrečná vlastní zpráva „Export nebyl dokončen“ nenahrazuje informaci o původní příčině v logu. [7]

## 15. Jednoduché logování

Textový soubor může mít příponu `.txt`, `.log` nebo `.md`; v tomto příkladu se do něj zapisují obyčejné řádky.

Akce **Zapsat text do souboru**:

- při existenci souboru **připojit obsah**;

- připojit nový řádek;

- kódování UTF-8;

- stejná cesta pro úspěšnou i chybovou větev.

Úspěch:

```text
%CasExportu% | OK | Export stažen a přesunut.
```

Chyba:

```text
%CasExportu% | CHYBA | %LastError.Message%
```

Datum pro název exportu a čas logové události mohou být různé proměnné. I při denním názvu souboru je pro rozlišení opakovaných běhů užitečný přesný čas v logu.

OK pro stažení a přesun zapisuj po jejich ověření. Pokud má znamenat úspěch celého toku včetně zavření aplikace, zapisuj ho až po těchto krocích. Do logu neukládej hesla nebo přístupové tokeny.

## 16. Ověřený vzor: webový export → archiv → Power Query

Následující seznam popisuje pořadí akcí, nejde o importovatelný kód PAD.

1. Získat datum a vytvořit `CasExportu`.

2. Zahájit blok `Export_CSOB`.

3. Otevřít Edge → `Browser`.

4. Vybrat požadované období grafu.

5. Počkat na připravenost exportu.

6. Kliknout na export.

7. Počkat na vznik CSV s časovým limitem.

8. Přejmenovat soubor → `RenamedFiles`.

9. Přesunout `%RenamedFiles%` do archivu → `MovedFiles`.

10. Ověřit přesun a zaznamenat úspěch.

11. Zavřít prohlížeč.

12. Ukončit blok pomocí `End`.

Při chybě blok zavolá `Chyba_export`. Celý příklad je samostatná výuková automatizace; nevyžaduje zásah do existující Python pipeline.

## 17. Power Query: vždy nejnovější export

Pokud každý export obsahuje celou historii, nespojuj automaticky všechny exporty pod sebe — vznikaly by opakované záznamy.

1. **Data → Načíst data → Ze souboru → Ze složky**.

2. **Transformovat data**.

3. Vyfiltrovat `.csv` a prefix příslušného fondu; vyloučit logy a ostatní soubory.

4. Seřadit názvy sestupně, pokud mají jednotný formát `yyyy-MM-dd` nebo `yyyy-MM-dd_HHmmss`.

5. **Zachovat horní řádky → 1**.

6. Načíst `Content`, rozdělit CSV správným oddělovačem, povýšit záhlaví a nastavit typy.

Kliknutí na Binary může vytvořit navigaci s pevným názvem CSV. Pro dynamický výběr prvního řádku použij například:

```powerquery
= #"Zachované první řádky"{0}[Content]
```

Název předchozího kroku musí odpovídat dotazu. `{0}` je první řádek, `[Content]` jeho binární obsah. Funkce `Table.FirstN` slouží k zachování prvních řádků. [8]

| Sloupec | Doporučený typ |
|---|---|
| Datum | Datum |
| Hodnota | Desetinné číslo / pevné desetinné číslo podle potřebné přesnosti |
| Výnos | Desetinné číslo; procentní formát až po kontrole měřítka |

Pokud `166,03` znamená 166,03 %, před použitím procentního typu je třeba dělit 100. Typ „měna“ v Power Query je pevné desetinné číslo, nikoli důkaz, že údaj představuje peněžní částku.

Po dokončení PAD použij v Excelu **Aktualizovat vše**. Aktualizace dotazu sama nespouští stahovací tok. Sešit ukládej mimo složku určenou jen pro zdrojové exporty.

## 18. Časté chyby a diagnostika

| Projev | Co zkontrolovat |
|---|---|
| `Browser` je prázdný | Běžel krok otevření prohlížeče? |
| Selektor nenalezen | Dynamické Id, změna stránky, nedokončené načítání |
| Tok bez chyby, export nikde | Skutečné kliknutí, fyzický režim, download panel, cílová složka |
| Otevře se nabídka Start místo exportu | Kam dopadá fyzické kliknutí |
| Soubor k přejmenování nenalezen | Přesná cesta, `_1.csv`, přípona, varianta `(1)` |
| Soubor zůstává ve Stažených | Vstup přesunu po přejmenování, kolize cílového názvu |
| Log OK, ale výstup chybí | Zda akce pouze nepřeskočila existující soubor; zda OK není příliš brzy |
| Excel instance není inicializována | Pořadí kroků, uzavření uvnitř cyklu, správná instance |
| Chyba je uvedena na Zastavit tok | Původní příčinu hledej v `LastError` a logu |
| PQ používá starý export | Řazení, filtry, pevný název v navigačním kroku, aktualizace |
| Timeout | Soubor nevznikl v limitu; ověř název i příčinu nestahování |

## 19. Testování a ladění

Měň jednu věc najednou a kontroluj skutečný výsledek, ne pouze zelený konec běhu.

| Test | Očekávaný výsledek |
|---|---|
| Běžný export | Soubor v archivu, správný název, záznam OK |
| Neexistující vstup pro přejmenování | Konkrétní chyba v logu, úklid, ukončení |
| Čekání na neexistující soubor s limitem 5 s | Chyba časového limitu |
| Opakovaný export ve stejný den | Chování podle zvolené strategie kolizí |
| Aktualizace Power Query po novém exportu | Výběr nového souboru; hodnoty mohou zůstat stejné |

Po testu obnov správné názvy a provozní limity. Zbylé testovací exporty mohou ovlivnit další stažení. Pro ladění používej přerušovací body, krokování a panel proměnných.

## 20. Cloudové toky — obecný a praktický přehled

Cloudový tok běží ve službě Power Automate a propojuje aplikace pomocí konektorů. Typické využití: příjem podkladů, ukládání dokumentů, evidence požadavků, schvalování, upozornění a předávání informací mezi systémy.

Tato část shrnuje principy a návrhové příklady. Nepopisuje prakticky dokončený cloudový projekt.

### 20.1 Typy cloudových toků

| Typ | Jak se spouští | Příklad |
|---|---|---|
| Automatizovaný / Automated | Událostí ve službě | Příchod e-mailu, vytvoření položky v SharePointu |
| Okamžitý / Instant | Na vyžádání uživatele | Tlačítko pro odeslání dokumentu ke schválení |
| Naplánovaný / Scheduled | Podle času a opakování | Ranní kontrola nevyřízených požadavků |

Tok má jeden spouštěč a navazující akce. Spouštěč předá údaje o události, které další kroky využívají. Konkrétní spouštěče a akce závisejí na konektoru. [9]

### 20.2 Základní pojmy

| Pojem | Co znamená | Příklad |
|---|---|---|
| Trigger / spouštěč | Zahájí nový běh | Nový e-mail ve sledované složce |
| Action / akce | Provede operaci | Vytvoření souboru v SharePointu |
| Connector / konektor | Nabízí operace určité služby | Office 365 Outlook, SharePoint, Teams |
| Connection / připojení | Konkrétní ověření identity pro konektor | Přihlášení k pracovní schránce |
| Dynamic content / dynamický obsah | Hodnota převzatá ze spouštěče nebo předchozí akce | Předmět, název přílohy, ID položky |
| Expression / výraz | Výpočet nebo úprava hodnoty | Spojení textů či formátování data |
| Condition / podmínka | Rozhodnutí mezi větvemi | Částka přesahuje schvalovací limit |
| Apply to each | Cyklus nad kolekcí | Zpracování každé přílohy |
| Scope / rozsah | Seskupení souvisejících akcí | Hlavní zpracování a chybová větev |
| Run history / historie běhů | Přehled spuštění a výsledků kroků | Nalezení neúspěšné akce |

**Konektor není totéž co připojení:** konektor určuje dostupné operace, připojení určuje použitou identitu. Přístup k toku sám nezaručuje oprávnění ke všem souborům, schránkám a seznamům.

### 20.3 Jak se tok prakticky sestavuje

1. Vybrat typ toku a konkrétní spouštěč.
2. Vytvořit připojení ke službám, které tok používá.
3. Nastavit sledovaný objekt — například schránku, složku nebo seznam.
4. Přidat akce a vyplnit jejich vstupy.
5. Do vstupů vložit dynamický obsah z předchozích kroků.
6. Doplnit podmínky, cykly a chybové větve.
7. Uložit a vyzkoušet tok na kontrolovaném vstupu.
8. V historii běhu ověřit jednotlivé kroky i skutečný výsledek v cílové aplikaci.

**Příklad předání dat:** akce „Vytvořit soubor“ potřebuje cílovou složku, název a obsah souboru. Název přílohy a její obsah převezme z e-mailu nebo z akce pro načtení přílohy. Samotný název nestačí k vytvoření souboru se správným obsahem.

### 20.4 Dynamický obsah, výrazy a cykly

V cloudovém toku se nepoužívá desktopový zápis `%Promenna%`. Hodnoty se vkládají přes dynamický obsah nebo editor výrazů.

| Potřeba | Postup |
|---|---|
| Použít předmět konkrétního e-mailu | Vložit dynamický obsah ze spouštěče |
| Použít ID nově vytvořené položky | Vzít ID z výstupu vytvářecí akce |
| Zpracovat více příloh | Použít `Apply to each` nad kolekcí příloh |
| Upravit nebo spojit text | Použít výraz, případně akci `Compose` |
| Uchovat měnící se hodnotu | Inicializovat proměnnou a později ji nastavit |

Příklady výrazů zadávaných v editoru výrazů:

```text
utcNow()
formatDateTime(utcNow(), 'yyyy-MM-dd')
concat('Report_', formatDateTime(utcNow(), 'yyyy-MM-dd'), '.csv')
```

`utcNow()` vrací čas UTC. Pokud datum nebo termín závisí na českém místním čase, nejprve nastav odpovídající časové pásmo nebo proveď převod. Datum z UTC může být kolem půlnoci jiné než v Česku.

Podmínka uvnitř toku rozhoduje o dalším postupu již zahájeného běhu. **Podmínka spouštěče** omezuje, pro které události se běh vůbec zahájí. Dostupné nastavení závisí na spouštěči.

### 20.5 Praktická využití ve firmě

| Potřeba | Co může dělat Power Automate | Co řeší navazující nástroj nebo člověk |
|---|---|---|
| Příjem podkladů | Převzít přílohu, uložit ji, zaznamenat přijetí | Kontrolu tabulkového obsahu provede Python nebo Power Query |
| Schválení dokumentu | Poslat žádost, počkat na výsledek, rozdělit další postup | Schvalovatel rozhodne a doplní komentář |
| Evidence požadavků | Založit položku, přiřadit odpovědnost a upozornit řešitele | Řešitel provede požadovanou práci |
| Hlídání termínů | Najít nevyřízené položky po termínu a poslat připomínku | Odpovědná osoba doplní nebo vyřeší podklad |
| Předání výsledku | Rozeslat odkaz na připravený report a aktualizovat stav | Výpočty a vytvoření reportu zajistí příslušná datová část |

Power Automate je užitečný zejména tam, kde proces přechází mezi aplikacemi a lidmi. Nemusí přebírat samotné analytické výpočty.

### 20.6 Schvalování

Typický příklad: uživatel odešle dokument → tok požádá vedoucího o schválení → počká na odpověď → podle výsledku aktualizuje stav a informuje žadatele.

Pro tento postup lze použít akci **Start and wait for an approval**. Do žádosti se nastaví schvalovatel, název, podrobnosti a případně odkaz na podklad. Další podmínka pracuje s výsledkem schválení. [10]

Před sestavením určuj:

- kdo rozhoduje a zda stačí první odpověď, nebo musí souhlasit všichni;
- co se stane při zamítnutí;
- do kdy má rozhodnutí přijít a co následuje bez odpovědi;
- kde se uloží výsledek a komentář;
- zda schvalovatel skutečně otevře odkazovaný dokument.

Schvalovací tok může evidovat rozhodnutí o neúplném reportu, obchodní výjimce nebo změně podkladů. Konkrétní pravidla musí určit vlastník procesu.

### 20.7 Chyby, opakované pokusy a historie běhů

**Configure run after / nastavení následného spuštění** určuje, po jakém výsledku předchozího kroku se má akce provést: například po úspěchu, selhání, přeskočení nebo vypršení limitu. [11]

Praktický vzor:

- rozsah `Zpracovani` obsahuje hlavní operace;
- rozsah `Chyba` se spouští při selhání nebo timeoutu hlavního rozsahu;
- chybová větev zapíše informace a odešle upozornění;
- podle pravidel proces ukončí akce `Terminate` se stavem selhání.

Samotné úspěšné odeslání chybového upozornění neznamená, že původní zpracování uspělo.

| Nástroj | K čemu slouží |
|---|---|
| Historie běhů | Kontrola stavu, vstupů a výstupů jednotlivých kroků |
| Retry policy | Opakování podporované akce při dočasném problému |
| Timeout | Omezení doby čekání podle podpory dané akce |
| Vlastní evidence | Dlouhodobý přehled business výsledků, souborů a požadavků |

Opakované pokusy pomáhají při dočasné nedostupnosti služby. Neopraví chybějící oprávnění nebo neplatná data. Před opakováním ověř riziko duplicitního vytvoření položky či odeslání zprávy. [11]

Historie běhů je diagnostika s omezenou dobou uchování podle služby a plánu. Pokud je potřeba trvalý přehled, ukládej například ID požadavku, čas, stav a odkaz na výsledek do samostatné evidence.

### 20.8 Duplicity, souběh a verze

- **Jedinečný klíč:** určuj, podle čeho poznáš již zpracovaný podklad — například ID zprávy a přílohy nebo business klíč dokumentu.
- **Idempotence:** opětovné zpracování stejného vstupu nemá vytvořit druhý nežádoucí výsledek.
- **Souběh:** více běhů může současně měnit stejný cíl. Ověř nastavení souběhu a způsob ochrany sdílených dat.
- **Verze:** uchování souborů a výběr aktuální verze jsou dvě odlišná pravidla. Novější soubor není automaticky platnější.
- **Opakované spuštění:** znovu spuštěný běh může zopakovat i dříve dokončené operace; návrh musí počítat s jejich vedlejšími účinky.

Samotná posloupnost „ověř, že položka neexistuje → vytvoř ji“ nezaručuje ochranu při souběhu: dva běhy mohou kontrolou projít současně. Podle cílové služby využij také jedinečnost klíče nebo jiné řízení zápisu.

### 20.9 Cloud, Desktop a datové nástroje

| Úloha | Praktická volba |
|---|---|
| Propojit Outlook, SharePoint a schválení | Cloudový tok |
| Ovládat aplikaci bez použitelného datového rozhraní | Desktopový tok |
| Čistit a spojovat tabulky | Power Query, Python nebo SQL podle rozsahu |
| Zajistit složitější datové validace a transakční zápis | Python / SQL |
| Uvnitř online sešitu provést podporované operace skriptem | Office Scripts, případně volané z cloudového toku |
| Rozeslat výsledek a evidovat rozhodnutí člověka | Cloudový tok |

**Cloudové konektory běžně neklikají na obrazovce:** volají operace služby a předávají data. Desktopová automatizace uživatelského rozhraní naopak závisí na dostupném počítači a ovládané aplikaci.

Propojení cloudového a desktopového toku je možné při splnění podmínek prostředí a licence. Cloudový tok nemá automaticky přístup k libovolné místní cestě. Pokud proces používá desktopovou část nebo místní datovou bránu, tato část potřebuje dostupný stroj.

### 20.10 Účet, oprávnění a licence

- Pro cloudový portál a cloudové toky je potřeba pracovní nebo školní účet Microsoft. Osobní účty byly z podpory cloudového Power Automate vyřazeny v červenci 2025; PAD s osobním účtem tímto vyřazením dotčen nebyl. [12]
- Dostupnost akce závisí na konektoru, licenci a pravidlech organizace. Rozlišuj standardní a prémiové konektory. [13]
- Oprávnění připojení musí odpovídat konkrétním zdrojům a cílům.
- Firemní zásady ochrany dat mohou některé kombinace konektorů zakázat.
- U důležitého toku řeš vlastnictví, zastupitelnost a připojení i při odchodu autora.
- Úspěšný běh cloudové části nezaručuje připravenost navazující aplikace nebo datového reportu.

### 20.11 Co by změnil oproti Python pipeline

U hotové pipeline Python → validace → SQL → CSV není nutné přepisovat datové zpracování do vizuálních akcí. Přínos cloudu může být v okolních krocích:

| Oblast | Přínos nebo náročnost |
|---|---|
| Příjem příloh a ukládání do Microsoft 365 | Často jednodušší díky hotovým konektorům |
| Schvalování a komunikace | Hotové akce a návaznost na rozhodnutí člověka |
| Rozsáhlé tabulkové transformace | Mnoho akcí a výrazů může být méně přehledných než pandas nebo SQL |
| Databázové transakce | Samostatné kroky toku automaticky nenahrazují jednu databázovou transakci |
| Verzování a kontrola změn | U Pythonu je běžná práce s textovým kódem v Gitu; cloudové toky mají vlastní možnosti správy a přenosu |
| Provoz | Odpadá osobní notebook u čistě cloudového procesu; přibývá správa připojení, oprávnění a limitů |

Rozhoduj podle konkrétní úlohy. Vhodným výsledkem může být kombinace: Power Automate převezme požadavek a zajistí schválení, datový nástroj provede zpracování a Power Automate následně předá výsledek.

### 20.12 Kontrola před spuštěním

1. Co tok spouští a pro které vstupy má opravdu běžet?
2. Z jaké identity používá jednotlivá připojení?
3. Které kroky mohou vytvořit duplicitu při opakování?
4. Mohou dva běhy měnit stejný soubor nebo záznam?
5. Jak se projeví zamítnutí, chyba nebo chybějící odpověď?
6. Co přesně znamená dokončený business výsledek?
7. Kde bude výsledek a chyba dohledatelná?