from pathlib import Path
import sys

import pandas as pd
import pyodbc


CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=(localdb)\\DataAnalyticsLocalDB;"
    "DATABASE=automation_lesson_04;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


# Povinné sloupce očekávané v původním vstupním CSV.
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
    # Nejdříve ověříme, zda lze se vstupními daty bezpečně pracovat.
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
    # Čištění provádíme na kopii původních dat.
    clean_dataframe = dataframe.copy()

    text_columns = [
        "title",
        "state",
        "user.login",
        "html_url"
    ]

    # Odstranění nadbytečných mezer z textových hodnot.
    for column in text_columns:
        clean_dataframe[column] = (
            clean_dataframe[column].str.strip()
        )

    # Sjednocení hodnot state na malá písmena.
    clean_dataframe["state"] = (
        clean_dataframe["state"].str.lower()
    )

    # Prázdný text převedeme na chybějící hodnotu.
    for column in text_columns:
        clean_dataframe[column] = (
            clean_dataframe[column].replace("", pd.NA)
        )

    # user.login je nepovinný, proto lze chybějící hodnotu doplnit.
    clean_dataframe["user.login"] = (
        clean_dataframe["user.login"].fillna("unknown")
    )

    row_count_before = len(clean_dataframe)

    # Odstranění pouze úplně identických řádků.
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

    # Neplatné číselné hodnoty se převedou na NaN.
    # Následná validace je zachytí jako kritickou chybu.
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

    # Neplatná data se převedou na NaT.
    # Následná validace je zachytí jako kritickou chybu.
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
    # Tyto sloupce odpovídají sloupcům, které v SQL nepovolují NULL.
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

    # Chybějící povinná hodnota představuje kritickou chybu.
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

    # issue_id je primární klíč, proto musí být unikátní.
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
        # Chybějící vstupní soubor je kritická chyba.
        if not input_file.exists():
            print("Vstupní soubor neexistuje.")
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

        # Při chybné struktuře proces skončí před čištěním a zápisem.
        if not validate_structure(dataframe):
            return 1

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

        # Neplatná data se nesmějí dostat do databáze.
        if not validate_data(dataframe):
            return 1

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

        # Změny v databázi potvrdíme až po úspěšném vytvoření Excelu.
        connection.commit()

        print(
            "Počet řádků uložených do databáze:",
            len(records)
        )
        print("Excel byl vytvořen:", output_file)

        return 0

    except pyodbc.Error as error:
        # Databázová chyba představuje kritickou chybu procesu.
        print("Chyba při práci s databází:", error)

        if connection is not None:
            connection.rollback()

        return 1

    except (OSError, ValueError) as error:
        # Zachycení chyb při načítání, čištění nebo ukládání souboru.
        print(
            "Chyba při práci se souborem nebo daty:",
            error
        )

        # Pokud už začala databázová transakce, změny se vrátí.
        if connection is not None:
            connection.rollback()

        return 1

    finally:
        # Spojení se uzavře při úspěchu, chybě i předčasném return.
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    print("Soubor byl spuštěn přímo.")

    result = main()

    print("Návratová hodnota funkce:", result)
    sys.exit(result)