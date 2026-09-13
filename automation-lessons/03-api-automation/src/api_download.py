from pathlib import Path
from datetime import datetime, timezone
import sys

import pandas as pd
import requests


# ============================================================
# 1. SPOLEČNÉ NASTAVENÍ
# ============================================================

# Endpoint veřejného GitHub REST API.
API_URL = "https://api.github.com/repos/pandas-dev/pandas/issues"

# Počet záznamů požadovaných na jedné stránce.
PER_PAGE = 10

# Maximální počet stažených stránek.
MAX_PAGES = 3

# Klíče, které očekáváme v každém záznamu API.
REQUIRED_KEYS = {
    "id",
    "number",
    "title",
    "state",
    "user",
    "created_at",
    "updated_at",
    "html_url"
}

# Sloupce, které chceme ponechat ve výsledném CSV.
SELECTED_COLUMNS = [
    "id",
    "number",
    "title",
    "state",
    "user.login",
    "created_at",
    "updated_at",
    "html_url"
]

# Sloupce, ve kterých nesmějí chybět hodnoty.
VALIDATION_COLUMNS = [
    "id",
    "number",
    "title",
    "state",
    "created_at"
]


# ============================================================
# 2. UČÍCÍ VERZE
# ============================================================
# Obsahuje pomocné proměnné, komentáře a výpisy,
# abychom viděli jednotlivé kroky API procesu.


def main_learning():
    print("Proces stahování dat byl zahájen.")
    print("Adresa API:", API_URL)
    print("Počet záznamů na stránce:", PER_PAGE)
    print("Maximální počet stránek:", MAX_PAGES)

    # --------------------------------------------------------
    # URČENÍ CEST
    # --------------------------------------------------------

    # __file__ obsahuje cestu k aktuálnímu Python souboru.
    print("Hodnota __file__:", __file__)

    # Převod cesty na objekt Path.
    file_path = Path(__file__)
    print("Hodnota file_path:", file_path)

    # Převod na jednoznačnou absolutní cestu.
    resolved_path = file_path.resolve()
    print("Hodnota resolved_path:", resolved_path)

    # Nadřazená složka skriptu je složka src.
    script_dir = resolved_path.parent
    print("Hodnota script_dir:", script_dir)

    # Nadřazená složka src je kořen lekce 03-api-automation.
    base_dir = script_dir.parent
    print("Hodnota base_dir:", base_dir)

    # Sestavení cest pro raw data a výsledný výstup.
    raw_dir = base_dir / "data" / "raw"
    output_dir = base_dir / "data" / "output"

    print("Hodnota raw_dir:", raw_dir)
    print("Hodnota output_dir:", output_dir)

    # Skript může výstupní složky bezpečně vytvořit.
    raw_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print("Existuje složka raw:", raw_dir.exists())
    print("Existuje složka output:", output_dir.exists())

    # --------------------------------------------------------
    # TIMESTAMP SPUŠTĚNÍ
    # --------------------------------------------------------

    # Aktuální čas v UTC jako Python objekt.
    downloaded_at = datetime.now(timezone.utc)

    # Textová podoba času pro výsledná data.
    downloaded_at_text = downloaded_at.isoformat()

    # Zkrácená podoba času vhodná pro název souboru.
    timestamp = downloaded_at.strftime("%Y%m%d_%H%M%S")

    print("Čas načtení v UTC:", downloaded_at_text)
    print("Timestamp pro názvy souborů:", timestamp)

    # --------------------------------------------------------
    # SPOLEČNÝ SEZNAM PRO VŠECHNY STRÁNKY
    # --------------------------------------------------------

    # Do tohoto seznamu budeme přidávat záznamy
    # z jednotlivých stránek API.
    all_records = []

    print("Počet záznamů před stažením:", len(all_records))

    # --------------------------------------------------------
    # PAGINATION
    # --------------------------------------------------------

    # Při MAX_PAGES = 3 cyklus projde stránky 1, 2 a 3.
    for page in range(1, MAX_PAGES + 1):
        print("--------------------------------------------------")
        print("Stahuji stránku:", page)

        # Parametry budou přidány k adrese API.
        params = {
            "state": "all",
            "per_page": PER_PAGE,
            "page": page
        }

        print("Parametry požadavku:", params)

        # ----------------------------------------------------
        # ODESLÁNÍ API POŽADAVKU
        # ----------------------------------------------------

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=10
            )

        # Timeout nastane, pokud API neodpoví v určeném čase.
        except requests.exceptions.Timeout:
            print("Chyba: API neodpovědělo v časovém limitu.")
            return 1

        # Zachycení ostatních chyb při HTTP komunikaci.
        except requests.exceptions.RequestException as error:
            print("Chyba při komunikaci s API:", error)
            return 1

        print("Skutečná adresa požadavku:", response.url)
        print("HTTP status:", response.status_code)

        # ----------------------------------------------------
        # KONTROLA HTTP STATUSU
        # ----------------------------------------------------

        # Pro tento GET požadavek očekáváme status 200.
        if response.status_code != 200:
            print("Chyba: API vrátilo neúspěšný HTTP status.")
            return 1

        print("HTTP požadavek byl úspěšný.")

        # ----------------------------------------------------
        # KONTROLA RATE LIMITU
        # ----------------------------------------------------

        # GitHub posílá počet zbývajících požadavků
        # v HTTP hlavičce X-RateLimit-Remaining.
        rate_limit_remaining = response.headers.get(
            "X-RateLimit-Remaining",
            "neuvedeno"
        )

        print(
            "Zbývající počet API požadavků:",
            rate_limit_remaining
        )

        # ----------------------------------------------------
        # ULOŽENÍ PŮVODNÍ ODPOVĚDI
        # ----------------------------------------------------

        # Každá stránka dostane vlastní raw JSON soubor.
        raw_file = (
            raw_dir
            / f"github_issues_raw_{timestamp}_page_{page}.json"
        )

        # response.text obsahuje původní text odpovědi serveru.
        raw_file.write_text(
            response.text,
            encoding="utf-8"
        )

        print("Raw odpověď byla uložena:", raw_file)

        # ----------------------------------------------------
        # PŘEVOD JSON ODPOVĚDI
        # ----------------------------------------------------

        try:
            page_data = response.json()

        # API může odpovědět, ale jeho obsah nemusí být
        # možné převést z JSON na Python objekty.
        except ValueError:
            print("Chyba: odpověď neobsahuje platný JSON.")
            return 1

        print("Typ dat aktuální stránky:", type(page_data))

        # ----------------------------------------------------
        # KONTROLA ZÁKLADNÍ STRUKTURY
        # ----------------------------------------------------

        # Očekáváme seznam obsahující jednotlivé záznamy.
        if not isinstance(page_data, list):
            print("Chyba: odpověď API není seznam.")
            return 1

        print(
            "Počet záznamů na aktuální stránce:",
            len(page_data)
        )

        # Prázdná první stránka znamená, že jsme nezískali data.
        if not page_data and page == 1:
            print("Chyba: API nevrátilo žádná data.")
            return 1

        # Prázdná další stránka znamená konec dostupných dat.
        if not page_data:
            print("Další stránka již neobsahuje data.")
            break

        # ----------------------------------------------------
        # KONTROLA JEDNOTLIVÝCH ZÁZNAMŮ
        # ----------------------------------------------------

        for record_number, record in enumerate(
            page_data,
            start=1
        ):
            # Každý záznam má být slovník.
            if not isinstance(record, dict):
                print("Chyba: záznam není slovník.")
                print("Stránka:", page)
                print("Číslo záznamu:", record_number)
                return 1

            # Rozdíl množin ukáže případné chybějící klíče.
            missing_keys = REQUIRED_KEYS - set(record.keys())

            if missing_keys:
                print(
                    "Chyba: v záznamu chybí povinné klíče."
                )
                print("Stránka:", page)
                print("Číslo záznamu:", record_number)
                print(
                    "Chybějící klíče:",
                    sorted(missing_keys)
                )
                return 1

        print("Struktura záznamů na stránce je správná.")

        # ----------------------------------------------------
        # SPOJENÍ JEDNOTLIVÝCH STRÁNEK
        # ----------------------------------------------------

        # extend() přidá jednotlivé záznamy aktuální stránky
        # do společného seznamu.
        all_records.extend(page_data)

        print(
            "Celkový počet dosud získaných záznamů:",
            len(all_records)
        )

        # Pokud stránka obsahuje méně záznamů než PER_PAGE,
        # dosáhli jsme poslední stránky.
        if len(page_data) < PER_PAGE:
            print("Byla dosažena poslední stránka.")
            break

    # --------------------------------------------------------
    # KONTROLA CELKOVÉHO VÝSLEDKU
    # --------------------------------------------------------

    if not all_records:
        print("Chyba: nebyly získány žádné záznamy.")
        return 1

    print("--------------------------------------------------")
    print(
        "Celkový počet získaných záznamů:",
        len(all_records)
    )

    # --------------------------------------------------------
    # NORMALIZACE JSON
    # --------------------------------------------------------

    # json_normalize() převede seznam slovníků na DataFrame
    # a rozbalí vnořené slovníky do samostatných sloupců.
    normalized_df = pd.json_normalize(all_records)

    print("Rozměr normalizované tabulky:", normalized_df.shape)

    # --------------------------------------------------------
    # KONTROLA A VÝBĚR SLOUPCŮ
    # --------------------------------------------------------

    missing_columns = (
        set(SELECTED_COLUMNS)
        - set(normalized_df.columns)
    )

    if missing_columns:
        print("Chyba: ve výsledku chybí očekávané sloupce.")
        print(
            "Chybějící sloupce:",
            sorted(missing_columns)
        )
        return 1

    # Ponecháme pouze sloupce potřebné pro výsledný export.
    output_df = normalized_df[SELECTED_COLUMNS].copy()

    # Ke každému řádku doplníme čas načtení.
    output_df["downloaded_at_utc"] = downloaded_at_text

    print("Rozměr výsledné tabulky:", output_df.shape)

    # --------------------------------------------------------
    # VALIDACE VÝSLEDNÉ TABULKY
    # --------------------------------------------------------

    if output_df.empty:
        print("Chyba: výsledná tabulka je prázdná.")
        return 1

    # any().any() ověří, zda se v kontrolovaných sloupcích
    # nachází alespoň jedna chybějící hodnota.
    if output_df[VALIDATION_COLUMNS].isna().any().any():
        print("Chyba: v povinných sloupcích chybí hodnoty.")
        return 1

    # Číslo issue má být v rámci výsledku jedinečné.
    if output_df["number"].duplicated().any():
        print("Chyba: výstup obsahuje duplicitní čísla.")
        return 1

    print("Validace výsledné tabulky byla úspěšná.")

    # --------------------------------------------------------
    # EXPORT DO CSV
    # --------------------------------------------------------

    output_file = (
        output_dir
        / f"github_issues_{timestamp}.csv"
    )

    output_df.to_csv(
        output_file,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print("Výstupní CSV bylo vytvořeno:", output_file)
    print("Proces byl úspěšně dokončen.")

    # Návratový kód 0 znamená úspěch.
    return 0


# ============================================================
# 3. BĚŽNÁ ZKRÁCENÁ VERZE
# ============================================================
# Provádí stejný proces, ale neobsahuje učící mezikroky
# ani pomocné kontrolní výpisy.


def main():
    # Určení projektových cest.
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent

    raw_dir = base_dir / "data" / "raw"
    output_dir = base_dir / "data" / "output"

    raw_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Timestamp celého spuštění.
    downloaded_at = datetime.now(timezone.utc)
    downloaded_at_text = downloaded_at.isoformat()
    timestamp = downloaded_at.strftime("%Y%m%d_%H%M%S")

    all_records = []

    # Stažení jednotlivých stránek.
    for page in range(1, MAX_PAGES + 1):
        params = {
            "state": "all",
            "per_page": PER_PAGE,
            "page": page
        }

        try:
            response = requests.get(
                API_URL,
                params=params,
                timeout=10
            )

        except requests.exceptions.Timeout:
            print("Chyba: API neodpovědělo v časovém limitu.")
            return 1

        except requests.exceptions.RequestException as error:
            print("Chyba při komunikaci s API:", error)
            return 1

        # Kontrola HTTP statusu.
        if response.status_code != 200:
            print(
                "Chyba: API vrátilo HTTP status:",
                response.status_code
            )
            return 1

        # Základní sledování rate limitu.
        rate_limit_remaining = response.headers.get(
            "X-RateLimit-Remaining",
            "neuvedeno"
        )

        print(
            "Stránka:",
            page,
            "| zbývající API požadavky:",
            rate_limit_remaining
        )

        # Uložení původní odpovědi.
        raw_file = (
            raw_dir
            / f"github_issues_raw_{timestamp}_page_{page}.json"
        )

        raw_file.write_text(
            response.text,
            encoding="utf-8"
        )

        # Převod JSON odpovědi.
        try:
            page_data = response.json()

        except ValueError:
            print("Chyba: odpověď neobsahuje platný JSON.")
            return 1

        # Kontrola struktury odpovědi.
        if not isinstance(page_data, list):
            print("Chyba: odpověď API není seznam.")
            return 1

        if not page_data and page == 1:
            print("Chyba: API nevrátilo žádná data.")
            return 1

        if not page_data:
            break

        # Kontrola jednotlivých záznamů.
        for record in page_data:
            if not isinstance(record, dict):
                print("Chyba: záznam není slovník.")
                return 1

            missing_keys = REQUIRED_KEYS - set(record.keys())

            if missing_keys:
                print(
                    "Chyba: v záznamu chybí povinné klíče:",
                    sorted(missing_keys)
                )
                return 1

        all_records.extend(page_data)

        if len(page_data) < PER_PAGE:
            break

    # Kontrola celkového výsledku.
    if not all_records:
        print("Chyba: nebyly získány žádné záznamy.")
        return 1

    # Normalizace JSON.
    normalized_df = pd.json_normalize(all_records)

    # Kontrola očekávaných sloupců.
    missing_columns = (
        set(SELECTED_COLUMNS)
        - set(normalized_df.columns)
    )

    if missing_columns:
        print(
            "Chyba: ve výsledku chybí očekávané sloupce:",
            sorted(missing_columns)
        )
        return 1

    output_df = normalized_df[SELECTED_COLUMNS].copy()
    output_df["downloaded_at_utc"] = downloaded_at_text

    # Validace výsledné tabulky.
    if output_df.empty:
        print("Chyba: výsledná tabulka je prázdná.")
        return 1

    if output_df[VALIDATION_COLUMNS].isna().any().any():
        print("Chyba: v povinných sloupcích chybí hodnoty.")
        return 1

    if output_df["number"].duplicated().any():
        print("Chyba: výstup obsahuje duplicitní čísla.")
        return 1

    # Export do CSV.
    output_file = (
        output_dir
        / f"github_issues_{timestamp}.csv"
    )

    output_df.to_csv(
        output_file,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    print("Počet uložených záznamů:", len(output_df))
    print("Výstupní CSV bylo vytvořeno:", output_file)
    print("Proces byl úspěšně dokončen.")

    return 0


# ============================================================
# 4. VSTUPNÍ BOD SKRIPTU
# ============================================================
# Při přímém spuštění má __name__ hodnotu "__main__".
# Při importu se tento blok automaticky neprovede.


if __name__ == "__main__":
    print("Soubor byl spuštěn přímo.")
    print("Hodnota __name__:", __name__)

    # UČÍCÍ VERZE JE NYNÍ AKTIVNÍ:
    result = main_learning()

    # PRO SPUŠTĚNÍ BĚŽNÉ VERZE:
    # Zakomentuj předchozí řádek a odkomentuj následující.
    # result = main()

    print("Návratová hodnota funkce:", result)

    # Předání návratového kódu operačnímu systému.
    sys.exit(result)