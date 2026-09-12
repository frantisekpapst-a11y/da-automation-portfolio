from pathlib import Path
import logging
import sys
import pandas as pd
import pyodbc
from datetime import date, timedelta



SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "daily_branch_report.log"

CONNECTION_STRING = (
    r"DRIVER={ODBC Driver 18 for SQL Server};"
    r"SERVER=(localdb)\DataAnalyticsLocalDB;"
    r"DATABASE=automation_practice;"
    r"Trusted_Connection=yes;"
    r"Encrypt=yes;"
    r"TrustServerCertificate=yes;"
)

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def save_to_database(data):
    connection = pyodbc.connect(
        CONNECTION_STRING,
        autocommit=False
    )

    try:
        cursor = connection.cursor()

        report_date = data["visit_date"].iloc[0].date()

        cursor.execute(
            """
            DELETE FROM dbo.branch_visits
            WHERE visit_date = ?;
            """,
            report_date
        )

        rows = []

        for row in data.itertuples(index=False):
            rows.append(
                (
                    str(row.visit_id),
                    str(row.branch_code),
                    row.visit_date.date(),
                    int(row.customer_id),
                    str(row.service_type),
                    int(row.duration_minutes),
                    str(row.status),
                    str(row.source_file)
                )
            )

        cursor.executemany(
            """
            INSERT INTO dbo.branch_visits
            (
                visit_id,
                branch_code,
                visit_date,
                customer_id,
                service_type,
                duration_minutes,
                status,
                source_file
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            rows
        )

        connection.commit()

        logging.info(
            "Do databáze bylo uloženo řádků: %s",
            len(rows)
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def main():
    logging.info("=" * 60)
    logging.info("NOVÉ SPUŠTĚNÍ PROCESU")
    logging.info("Proces denního reportu byl zahájen.")

    input_dir = BASE_DIR / "data" / "input"
    output_dir = BASE_DIR / "data" / "output"

    report_date = date.today() - timedelta(days=1)
    report_date_text = report_date.isoformat()

    input_pattern = (
        "branch_visits_"
        + report_date_text
        + "_*.csv"
    )

    input_files = sorted(input_dir.glob(input_pattern))

    logging.info(
        "Zpracovávané datum reportu: %s",
        report_date_text
    )

    logging.info("Nalezený počet CSV souborů: %s", len(input_files))

    if not input_files:
        logging.warning("Ve vstupní složce nebyly nalezeny žádné CSV soubory.")
        return

    dataframes = []

    required_columns = {
        "visit_id",
        "branch_code",
        "visit_date",
        "customer_id",
        "service_type",
        "duration_minutes",
        "status"
    }

    for input_file in input_files:
        df = pd.read_csv(
            input_file,
            sep=";",
            encoding="utf-8"
        )

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                "V souboru "
                + input_file.name
                + " chybí povinné sloupce: "
                + ", ".join(sorted(missing_columns))
            )

        df["source_file"] = input_file.name
        dataframes.append(df)

        logging.info(
            "Soubor %s byl načten. Počet řádků: %s",
            input_file.name,
            len(df)
        )

    combined_df = pd.concat(dataframes, ignore_index=True)

    combined_df["visit_date"] = pd.to_datetime(
        combined_df["visit_date"],
        errors="coerce"
    )

    combined_df["duration_minutes"] = pd.to_numeric(
        combined_df["duration_minutes"],
        errors="coerce"
    )

    invalid_rows = combined_df[
        combined_df["visit_id"].isna()
        | combined_df["branch_code"].isna()
        | combined_df["visit_date"].isna()
        | combined_df["duration_minutes"].isna()
        | (combined_df["duration_minutes"] < 0)
    ]

    if not invalid_rows.empty:
        raise ValueError(
            "Validace selhala. Počet neplatných řádků: "
            + str(len(invalid_rows))
        )

    duplicate_count = combined_df.duplicated(
        subset=["visit_id"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            "Validace selhala. Počet duplicitních visit_id: "
            + str(duplicate_count)
        )
        
    invalid_report_dates = combined_df[
        combined_df["visit_date"].dt.date != report_date
    ]

    if not invalid_report_dates.empty:
        raise ValueError(
            "Některé řádky obsahují jiné datum než "
            + report_date_text
            + "."
        )

    logging.info(
        "Datum uvnitř CSV odpovídá zpracovávanému dni."
    )

    logging.info("Validace dat byla úspěšně dokončena.")

    logging.info(
        "Celkový počet spojených řádků: %s",
        len(combined_df)
    )

    report_dates = (
        combined_df["visit_date"]
        .dt.strftime("%Y-%m-%d")
        .unique()
    )

    if len(report_dates) != 1:
        raise ValueError(
            "Vstupní soubory neobsahují právě jedno datum reportu."
        )

    report_date = report_dates[0]

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = (
        output_dir
        / ("daily_branch_report_" + report_date + ".csv")
    )

    temporary_file = (
        output_dir
        / ("daily_branch_report_" + report_date + ".tmp")
    )

    output_df = combined_df.copy()

    output_df["visit_date"] = (
        output_df["visit_date"]
        .dt.strftime("%Y-%m-%d")
    )

    output_df.to_csv(
        temporary_file,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )

    save_to_database(combined_df)

    temporary_file.replace(output_file)

    logging.info(
        "Výstupní soubor byl bezpečně uložen: %s",
        output_file
    )

    logging.info("Vstupní složka: %s", input_dir)
    logging.info("Výstupní složka: %s", output_dir)
    logging.info("Proces byl úspěšně dokončen.")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)

    except Exception:
        logging.exception("Proces skončil neočekávanou chybou.")
        sys.exit(1)