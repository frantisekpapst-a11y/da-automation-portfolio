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


# ============================================================
# 1. UČÍCÍ VERZE
# ============================================================
# Ukazuje celý tok:
# CSV -> Pandas -> SQL Server -> Pandas -> Excel


def main_learning():
    # --------------------------------------------------------
    # A. Cesty
    # --------------------------------------------------------

    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent

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

    print("Složka skriptu:", script_dir)
    print("Kořen lekce:", base_dir)
    print("Vstupní soubor:", input_file)
    print("Výstupní soubor:", output_file)

    if not input_file.exists():
        print("Vstupní soubor neexistuje.")
        return 1

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # B. Načtení CSV do Pandas
    # --------------------------------------------------------

    dataframe = pd.read_csv(
        input_file,
        sep=";",
        encoding="utf-8-sig"
    )

    print("Počet načtených řádků:", len(dataframe))
    print("Načtené sloupce:", dataframe.columns.tolist())

    # --------------------------------------------------------
    # C. Příprava dat pro SQL
    # --------------------------------------------------------

    dataframe = dataframe.rename(
        columns={
            "id": "issue_id",
            "number": "issue_number",
            "user.login": "user_login",
            "downloaded_at_utc": "downloaded_at"
        }
    )

    datetime_columns = [
        "created_at",
        "updated_at",
        "downloaded_at"
    ]

    for column in datetime_columns:
        dataframe[column] = (
            pd.to_datetime(
                dataframe[column],
                utc=True
            )
            .dt.tz_localize(None)
        )

    # Všechna issues patří k repozitáři
    # pandas-dev/pandas s repository_id = 1.
    dataframe["repository_id"] = 1

    # Pořadí odpovídá SQL příkazu INSERT.
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

    print("Sloupce po úpravě:", dataframe.columns.tolist())

    print("Datové typy po úpravě:")
    print(dataframe.dtypes)

    print("První připravený řádek:")
    print(dataframe.head(1))

    # Převod DataFrame na seznam řádků,
    # které lze předat metodě executemany().
    records = list(
        dataframe.itertuples(
            index=False,
            name=None
        )
    )

    print(
        "Počet připravených SQL záznamů:",
        len(records)
    )

    # --------------------------------------------------------
    # D. Připojení k SQL Serveru
    # --------------------------------------------------------

    connection = None

    try:
        connection = pyodbc.connect(
            CONNECTION_STRING
        )

        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME()")
        database_name = cursor.fetchone()[0]

        print(
            "Python je připojen k databázi:",
            database_name
        )

        # ----------------------------------------------------
        # E. Odstranění předchozího snapshotu
        # ----------------------------------------------------

        cursor.execute(
            """
            DELETE FROM dbo.github_issues
            WHERE repository_id = ?
            """,
            1
        )

        # ----------------------------------------------------
        # F. Zápis dat do SQL Serveru
        # ----------------------------------------------------

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

        connection.commit()

        print(
            "Počet řádků uložených do databáze:",
            len(records)
        )

        # ----------------------------------------------------
        # G. Načtení SQL výsledku do Pandas
        # ----------------------------------------------------

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

        print(
            "Počet řádků načtených ze SQL:",
            len(report_df)
        )

        print("Souhrn podle stavu:")
        print(summary_df)

        # ----------------------------------------------------
        # H. Export do Excelu
        # ----------------------------------------------------

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

        print("Excel byl vytvořen:", output_file)
        print("Proces byl úspěšně dokončen.")
        return 0

    except pyodbc.Error as error:
        print("Chyba při práci s databází:", error)

        if connection is not None:
            connection.rollback()

        return 1

    except (OSError, ValueError) as error:
        print(
            "Chyba při práci se souborem nebo daty:",
            error
        )
        return 1

    finally:
        if connection is not None:
            connection.close()
            print("Databázové spojení bylo uzavřeno.")


# ============================================================
# 2. BĚŽNÁ ZKRÁCENÁ VERZE
# ============================================================
# Provádí stejný proces bez učících mezivýpisů.


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

    dataframe = dataframe.rename(
        columns={
            "id": "issue_id",
            "number": "issue_number",
            "user.login": "user_login",
            "downloaded_at_utc": "downloaded_at"
        }
    )

    for column in [
        "created_at",
        "updated_at",
        "downloaded_at"
    ]:
        dataframe[column] = (
            pd.to_datetime(
                dataframe[column],
                utc=True
            )
            .dt.tz_localize(None)
        )

    dataframe["repository_id"] = 1

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

    connection = None

    try:
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

        connection.commit()

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

        print(
            "Počet řádků uložených do databáze:",
            len(records)
        )
        print("Excel byl vytvořen:", output_file)

        return 0

    except pyodbc.Error as error:
        print("Chyba při práci s databází:", error)

        if connection is not None:
            connection.rollback()

        return 1

    except (OSError, ValueError) as error:
        print(
            "Chyba při práci se souborem nebo daty:",
            error
        )
        return 1

    finally:
        if connection is not None:
            connection.close()


# ============================================================
# 3. VSTUPNÍ BOD SKRIPTU
# ============================================================
# Při přímém spuštění má __name__ hodnotu "__main__".
# Aktivní je zatím učící verze.


if __name__ == "__main__":
    print("Soubor byl spuštěn přímo.")

    # UČÍCÍ VERZE JE NYNÍ AKTIVNÍ:
    result = main_learning()

    # PRO SPUŠTĚNÍ BĚŽNÉ VERZE:
    # Zakomentuj předchozí řádek a odkomentuj následující.
    # result = main()

    print("Návratová hodnota funkce:", result)
    sys.exit(result)