from pathlib import Path
import sys
import logging
import time

import pandas as pd
import pandas as pd
import pyodbc


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=(localdb)\\DataAnalyticsLocalDB;"
    "DATABASE=automation_lesson_04;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


REQUIRED_COLUMNS = [
    "id",
    "number",
    "title",
    "state",
    "user.login",
    "created_at",
    "updated_at",
    "html_url",
    "downloaded_at_utc"
]


def validate_structure(dataframe):
    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in dataframe.columns:
            missing_columns.append(column)

    if missing_columns:
        print("Chybí povinné sloupce:", missing_columns)
        return False

    print("Kontrola povinných sloupců byla úspěšná.")

    if dataframe.empty:
        print("Vstupní data neobsahují žádné řádky.")
        return False

    print("Kontrola prázdného datasetu byla úspěšná.")
    return True


def clean_data(dataframe):
    clean_dataframe = dataframe.copy()

    text_columns = [
        "title",
        "state",
        "user.login",
        "html_url"
    ]

    for column in text_columns:
        clean_dataframe[column] = (
            clean_dataframe[column].str.strip()
        )

    clean_dataframe["state"] = (
        clean_dataframe["state"].str.lower()
    )

    for column in text_columns:
        clean_dataframe[column] = (
            clean_dataframe[column].replace("", pd.NA)
        )

    clean_dataframe["user.login"] = (
        clean_dataframe["user.login"].fillna("unknown")
    )

    row_count_before = len(clean_dataframe)

    clean_dataframe = clean_dataframe.drop_duplicates()

    row_count_after = len(clean_dataframe)

    removed_duplicates = (
        row_count_before - row_count_after
    )

    print(
        "Počet odstraněných duplicitních řádků:",
        removed_duplicates
    )

    numeric_columns = [
        "id",
        "number"
    ]

    for column in numeric_columns:
        clean_dataframe[column] = pd.to_numeric(
            clean_dataframe[column],
            errors="coerce"
        )

    datetime_columns = [
        "created_at",
        "updated_at",
        "downloaded_at_utc"
    ]

    for column in datetime_columns:
        clean_dataframe[column] = (
            pd.to_datetime(
                clean_dataframe[column],
                errors="coerce",
                utc=True
            )
            .dt.tz_localize(None)
        )

    print("Čištění dat bylo dokončeno.")
    return clean_dataframe


def validate_data(dataframe):
    required_value_columns = [
        "issue_id",
        "repository_id",
        "issue_number",
        "title",
        "state",
        "created_at",
        "updated_at",
        "html_url",
        "downloaded_at"
    ]

    for column in required_value_columns:
        missing_count = dataframe[column].isna().sum()

        if missing_count > 0:
            print(
                "Chybějící povinné hodnoty ve sloupci",
                column,
                ":",
                missing_count
            )
            return False

    print("Kontrola povinných hodnot byla úspěšná.")

    duplicate_id_count = (
        dataframe["issue_id"].duplicated().sum()
    )

    if duplicate_id_count > 0:
        print(
            "Počet duplicitních hodnot issue_id:",
            duplicate_id_count
        )
        return False

    print("Kontrola duplicitních issue_id byla úspěšná.")
    return True


def main():
    base_dir = Path(__file__).resolve().parent.parent

    # Sestavení cesty ke složce a souboru s logem.
    logs_dir = base_dir / "logs"
    log_file = logs_dir / "github_issues.log"

    # Složka pro logy se vytvoří, pokud ještě neexistuje.
    logs_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Základní konfigurace logování:
    # - záznamy se ukládají do souboru,
    # - ukládají se úrovně INFO, WARNING a ERROR,
    # - každý záznam obsahuje timestamp, úroveň a zprávu.
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8"
    )

    # Spuštění stopek pro změření celkové délky procesu.
    start_time = time.perf_counter()

    # První provozní informace v logu.
    logging.info("Proces byl zahájen.")

    input_file = (
        base_dir
        / "data"
        / "input"
        / "github_issues.csv"
    )

    output_dir = base_dir / "data" / "output"

    output_file = (
        output_dir
        / "github_issues_report.xlsx"
    )

    connection = None

    try:
        if not input_file.exists():
            print("Vstupní soubor neexistuje.")

            # ERROR označuje kritickou chybu, kvůli které proces končí.
            logging.error(
                "Vstupní soubor neexistuje: %s",
                input_file
            )
            return 1

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe = pd.read_csv(
            input_file,
            sep=";",
            encoding="utf-8-sig"
        )

        # Záznam počtu řádků bezprostředně po načtení vstupu.
        logging.info(
            "Načten počet vstupních řádků: %s",
            len(dataframe)
        )

        if not validate_structure(dataframe):
            # LEKCE 6:
            # Neúspěšná validace je důvodem k ukončení procesu.
            logging.error("Validace struktury selhala.")
            return 1

        # Záznam úspěšného výsledku první validace.
        logging.info("Validace struktury byla úspěšná.")

        dataframe = clean_data(dataframe)

        dataframe = dataframe.rename(
            columns={
                "id": "issue_id",
                "number": "issue_number",
                "user.login": "user_login",
                "downloaded_at_utc": "downloaded_at"
            }
        )

        dataframe["repository_id"] = 1

        if not validate_data(dataframe):
            # LEKCE 6:
            # Záznam neúspěšné finální validace.
            logging.error("Finální validace dat selhala.")
            return 1

        # Záznam úspěšné finální validace.
        logging.info("Finální validace dat byla úspěšná.")

        # Počet řádků, které prošly čištěním a validací.
        logging.info(
            "Počet řádků po vyčištění a validaci: %s",
            len(dataframe)
        )

        database_columns = [
            "issue_id",
            "repository_id",
            "issue_number",
            "title",
            "state",
            "user_login",
            "created_at",
            "updated_at",
            "html_url",
            "downloaded_at"
        ]

        dataframe = dataframe[database_columns]

        records = list(
            dataframe.itertuples(
                index=False,
                name=None
            )
        )

        connection = pyodbc.connect(
            CONNECTION_STRING
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM dbo.github_issues
            WHERE repository_id = ?
            """,
            1
        )

        insert_sql = """
            INSERT INTO dbo.github_issues
            (
                issue_id,
                repository_id,
                issue_number,
                title,
                state,
                user_login,
                created_at,
                updated_at,
                html_url,
                downloaded_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.executemany(
            insert_sql,
            records
        )

        report_query = """
            SELECT
                r.repository_owner,
                r.repository_name,
                i.issue_number,
                i.title,
                i.state,
                i.user_login,
                i.created_at,
                i.updated_at,
                i.html_url,
                i.downloaded_at
            FROM dbo.github_issues i
            JOIN dbo.repositories r
                ON i.repository_id = r.repository_id
            ORDER BY i.issue_number DESC
        """

        report_df = pd.read_sql_query(
            report_query,
            connection
        )

        summary_query = """
            SELECT
                state,
                COUNT(*) AS issue_count
            FROM dbo.github_issues
            GROUP BY state
            ORDER BY state
        """

        summary_df = pd.read_sql_query(
            summary_query,
            connection
        )

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
        ) as writer:
            report_df.to_excel(
                writer,
                sheet_name="Issues",
                index=False
            )

            summary_df.to_excel(
                writer,
                sheet_name="State summary",
                index=False
            )

        # Záznam vytvořeného výstupu včetně jeho cesty.
        logging.info(
            "Excelový výstup byl vytvořen: %s",
            output_file
        )

        # Skutečný počet řádků v hlavním listu Excelového reportu.
        logging.info(
            "Počet řádků v Excelovém výstupu: %s",
            len(report_df)
        )

        connection.commit()

        # Záznam počtu řádků uložených do SQL Serveru.
        logging.info(
            "Počet řádků uložených do databáze: %s",
            len(records)
        )

        print(
            "Počet řádků uložených do databáze:",
            len(records)
        )
        print("Excel byl vytvořen:", output_file)

        # Výpočet délky procesu v sekundách.
        duration_seconds = round(
            time.perf_counter() - start_time,
            2
        )

        logging.info(
            "Délka zpracování v sekundách: %s",
            duration_seconds
        )

        # Poslední záznam potvrzuje úspěšné dokončení procesu.
        logging.info("Proces byl úspěšně dokončen.")

        return 0

    except pyodbc.Error as error:
        print("Chyba při práci s databází:", error)

        # Uložení databázové chyby do logu.
        logging.error(
            "Chyba při práci s databází: %s",
            error
        )

        if connection is not None:
            connection.rollback()

        return 1

    except (OSError, ValueError) as error:
        print(
            "Chyba při práci se souborem nebo daty:",
            error
        )

        # Uložení souborové nebo datové chyby do logu.
        logging.error(
            "Chyba při práci se souborem nebo daty: %s",
            error
        )

        if connection is not None:
            connection.rollback()

        return 1

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    print("Soubor byl spuštěn přímo.")

    result = main()

    print("Návratová hodnota funkce:", result)
    sys.exit(result)