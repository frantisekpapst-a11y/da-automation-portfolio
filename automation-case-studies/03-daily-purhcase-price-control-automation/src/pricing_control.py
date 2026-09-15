from datetime import datetime
from pathlib import Path
import os
import sys

from dotenv import load_dotenv
import pandas as pd
import pyodbc
import requests


PRODUCT_COLUMNS = [
    "product_id",
    "product_code",
    "product_name",
    "purchase_currency",
    "purchase_price"
]


EXCHANGE_RATE_COLUMNS = [
    "validFor",
    "currencyCode",
    "amount",
    "rate"
]


CLEAN_EXCHANGE_RATE_COLUMNS = [
    "rate_date",
    "currency_code",
    "amount",
    "rate_czk"
]


PRICE_LIMIT_COLUMNS = [
    "product_code",
    "minimum_price_czk",
    "maximum_price_czk"
]


def validate_structure(
    df,
    required_columns,
    source_name
):
    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        print(
            "Ve zdroji",
            source_name,
            "chybí povinné sloupce:",
            missing_columns
        )
        return False

    if df.empty:
        print(
            "Zdroj",
            source_name,
            "neobsahuje žádné řádky."
        )
        return False

    print(
        "Validace struktury zdroje",
        source_name,
        "byla úspěšná."
    )
    return True


def clean_products(df):
    df_clean = df.copy()

    text_columns = [
        "product_code",
        "product_name",
        "purchase_currency"
    ]

    for column in text_columns:
        df_clean[column] = (
            df_clean[column].str.strip()
        )

    df_clean["product_code"] = (
        df_clean["product_code"].str.upper()
    )

    df_clean["purchase_currency"] = (
        df_clean["purchase_currency"].str.upper()
    )

    df_clean["purchase_price"] = pd.to_numeric(
        df_clean["purchase_price"],
        errors="coerce"
    )

    print("Čištění produktů bylo dokončeno.")
    return df_clean


def clean_exchange_rates(df):
    df_clean = df.copy()

    df_clean = df_clean[
        EXCHANGE_RATE_COLUMNS
    ].copy()

    df_clean = df_clean.rename(
        columns={
            "validFor": "rate_date",
            "currencyCode": "currency_code",
            "rate": "rate_czk"
        }
    )

    df_clean["currency_code"] = (
        df_clean["currency_code"]
        .str.strip()
        .str.upper()
    )

    df_clean["amount"] = pd.to_numeric(
        df_clean["amount"],
        errors="coerce"
    )

    df_clean["rate_czk"] = pd.to_numeric(
        df_clean["rate_czk"],
        errors="coerce"
    )

    df_clean["rate_date"] = pd.to_datetime(
        df_clean["rate_date"],
        errors="coerce"
    )

    print("Čištění kurzovního lístku bylo dokončeno.")
    return df_clean


def clean_price_limits(df):
    df_clean = df.copy()

    df_clean["product_code"] = (
        df_clean["product_code"]
        .str.strip()
        .str.upper()
    )

    numeric_columns = [
        "minimum_price_czk",
        "maximum_price_czk"
    ]

    for column in numeric_columns:
        df_clean[column] = pd.to_numeric(
            df_clean[column],
            errors="coerce"
        )

    print("Čištění cenových limitů bylo dokončeno.")
    return df_clean


def validate_data(
    df,
    required_columns,
    source_name
):
    for column in required_columns:
        missing_count = df[column].isna().sum()

        if missing_count > 0:
            print(
                "Ve zdroji",
                source_name,
                "chybí hodnoty ve sloupci",
                column,
                ":",
                missing_count
            )
            return False

    print(
        "Kontrola povinných hodnot zdroje",
        source_name,
        "byla úspěšná."
    )
    return True


def validate_duplicates(
    df,
    key_columns,
    source_name
):
    duplicate_count = (
        df.duplicated(
            subset=key_columns
        ).sum()
    )

    if duplicate_count > 0:
        print(
            "Ve zdroji",
            source_name,
            "byly nalezeny duplicity:",
            duplicate_count
        )
        return False

    print(
        "Kontrola duplicit zdroje",
        source_name,
        "byla úspěšná."
    )
    return True


def validate_business_rules(
    df_products,
    df_exchange_rates,
    df_price_limits
):
    invalid_purchase_prices = (
        df_products["purchase_price"] <= 0
    ).sum()

    if invalid_purchase_prices > 0:
        print(
            "Počet neplatných nákupních cen:",
            invalid_purchase_prices
        )
        return False

    invalid_amounts = (
        df_exchange_rates["amount"] <= 0
    ).sum()

    if invalid_amounts > 0:
        print(
            "Počet neplatných množství měny:",
            invalid_amounts
        )
        return False

    invalid_rates = (
        df_exchange_rates["rate_czk"] <= 0
    ).sum()

    if invalid_rates > 0:
        print(
            "Počet neplatných měnových kurzů:",
            invalid_rates
        )
        return False

    invalid_minimum_prices = (
        df_price_limits["minimum_price_czk"] < 0
    ).sum()

    if invalid_minimum_prices > 0:
        print(
            "Počet neplatných minimálních limitů:",
            invalid_minimum_prices
        )
        return False

    invalid_maximum_prices = (
        df_price_limits["maximum_price_czk"] <= 0
    ).sum()

    if invalid_maximum_prices > 0:
        print(
            "Počet neplatných maximálních limitů:",
            invalid_maximum_prices
        )
        return False

    invalid_price_ranges = (
        df_price_limits["minimum_price_czk"]
        >
        df_price_limits["maximum_price_czk"]
    ).sum()

    if invalid_price_ranges > 0:
        print(
            "Počet neplatných cenových intervalů:",
            invalid_price_ranges
        )
        return False

    print("Kontrola business pravidel byla úspěšná.")
    return True


def validate_merged_data(
    df,
    expected_row_count
):
    if len(df) != expected_row_count:
        print(
            "Počet řádků se po propojení změnil."
        )
        print(
            "Očekávaný počet řádků:",
            expected_row_count
        )
        print(
            "Skutečný počet řádků:",
            len(df)
        )
        return False

    required_columns = [
        "currency_code",
        "amount",
        "rate_czk",
        "rate_date",
        "purchase_price_czk",
        "minimum_price_czk",
        "maximum_price_czk"
    ]

    for column in required_columns:
        missing_count = df[column].isna().sum()

        if missing_count > 0:
            print(
                "Po propojení chybí hodnoty ve sloupci",
                column,
                ":",
                missing_count
            )
            return False

    print(
        "Validace propojených dat byla úspěšná."
    )
    return True


def main():
    base_dir = (
        Path(__file__).resolve().parent.parent
    )

    env_file = base_dir / ".env"

    price_limits_file = (
        base_dir
        / "data"
        / "input"
        / "price_limits.xlsx"
    )

    raw_dir = (
        base_dir
        / "data"
        / "raw"
        / "exchange_rates"
    )

    load_dotenv(env_file)

    connection_string = os.getenv(
        "DB_CONNECTION_STRING"
    )

    api_url = os.getenv(
        "CNB_API_URL"
    )

    if not connection_string or not api_url:
        print(
            "V souboru .env chybí potřebné nastavení."
        )
        return 1

    if not price_limits_file.exists():
        print(
            "Soubor s cenovými limity neexistuje:",
            price_limits_file
        )
        return 1

    raw_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = None

    try:
        connection = pyodbc.connect(
            connection_string
        )

        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME()")

        database_name = cursor.fetchone()[0]

        print(
            "Databáze:",
            database_name
        )

        product_query = """
            SELECT
                product_id,
                product_code,
                product_name,
                purchase_currency,
                purchase_price
            FROM dbo.products
            WHERE is_active = 1
            ORDER BY product_id
        """

        df_products = pd.read_sql_query(
            product_query,
            connection
        )

        print(
            "Počet načtených produktů:",
            len(df_products)
        )

        response = requests.get(
            api_url,
            params={
                "lang": "EN"
            },
            timeout=30
        )

        response.raise_for_status()

        print(
            "HTTP status API:",
            response.status_code
        )

        api_data = response.json()

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        raw_file = (
            raw_dir
            / (
                "exchange_rates_"
                + timestamp
                + ".json"
            )
        )

        raw_file.write_text(
            response.text,
            encoding="utf-8"
        )

        print(
            "Raw API odpověď byla uložena:",
            raw_file
        )

        if "rates" not in api_data:
            print(
                "API odpověď neobsahuje klíč rates."
            )
            return 1

        df_exchange_rates = pd.json_normalize(
            api_data["rates"]
        )

        print(
            "Počet načtených měnových kurzů:",
            len(df_exchange_rates)
        )

        df_price_limits = pd.read_excel(
            price_limits_file,
            sheet_name="Price limits"
        )

        print(
            "Počet načtených cenových limitů:",
            len(df_price_limits)
        )

        products_structure_ok = validate_structure(
            df_products,
            PRODUCT_COLUMNS,
            "produkty"
        )

        exchange_rates_structure_ok = (
            validate_structure(
                df_exchange_rates,
                EXCHANGE_RATE_COLUMNS,
                "kurzovní lístek"
            )
        )

        price_limits_structure_ok = (
            validate_structure(
                df_price_limits,
                PRICE_LIMIT_COLUMNS,
                "cenové limity"
            )
        )

        if not (
            products_structure_ok
            and exchange_rates_structure_ok
            and price_limits_structure_ok
        ):
            return 1

        print(
            "Validace struktury všech vstupů "
            "byla úspěšná."
        )

        df_products = clean_products(
            df_products
        )

        df_exchange_rates = clean_exchange_rates(
            df_exchange_rates
        )

        df_price_limits = clean_price_limits(
            df_price_limits
        )

        products_data_ok = validate_data(
            df_products,
            PRODUCT_COLUMNS,
            "produkty"
        )

        exchange_rates_data_ok = validate_data(
            df_exchange_rates,
            CLEAN_EXCHANGE_RATE_COLUMNS,
            "kurzovní lístek"
        )

        price_limits_data_ok = validate_data(
            df_price_limits,
            PRICE_LIMIT_COLUMNS,
            "cenové limity"
        )

        if not (
            products_data_ok
            and exchange_rates_data_ok
            and price_limits_data_ok
        ):
            return 1

        if not validate_duplicates(
            df_products,
            ["product_id"],
            "produkty podle product_id"
        ):
            return 1

        if not validate_duplicates(
            df_products,
            ["product_code"],
            "produkty podle product_code"
        ):
            return 1

        if not validate_duplicates(
            df_exchange_rates,
            [
                "rate_date",
                "currency_code"
            ],
            "kurzovní lístek"
        ):
            return 1

        if not validate_duplicates(
            df_price_limits,
            ["product_code"],
            "cenové limity"
        ):
            return 1

        if not validate_business_rules(
            df_products,
            df_exchange_rates,
            df_price_limits
        ):
            return 1

        print(
            "Finální validace všech vstupů "
            "byla úspěšná."
        )

        df_results = df_products.merge(
            df_exchange_rates,
            how="left",
            left_on="purchase_currency",
            right_on="currency_code",
            validate="many_to_one"
        )

        czk_rows = (
            df_results["purchase_currency"] == "CZK"
        )

        df_results.loc[
            czk_rows,
            "currency_code"
        ] = "CZK"

        df_results.loc[
            czk_rows,
            "amount"
        ] = 1

        df_results.loc[
            czk_rows,
            "rate_czk"
        ] = 1

        df_results.loc[
            czk_rows,
            "rate_date"
        ] = df_exchange_rates["rate_date"].max()

        df_results["purchase_price_czk"] = (
            df_results["purchase_price"]
            * df_results["rate_czk"]
            / df_results["amount"]
        )

        df_results = df_results.merge(
            df_price_limits,
            how="left",
            on="product_code",
            validate="one_to_one"
        )

        if not validate_merged_data(
            df_results,
            len(df_products)
        ):
            return 1

        df_results["status"] = "OK"

        below_limit_rows = (
            df_results["purchase_price_czk"]
            <
            df_results["minimum_price_czk"]
        )

        above_limit_rows = (
            df_results["purchase_price_czk"]
            >
            df_results["maximum_price_czk"]
        )

        df_results.loc[
            below_limit_rows,
            "status"
        ] = "BELOW LIMIT"

        df_results.loc[
            above_limit_rows,
            "status"
        ] = "ABOVE LIMIT"

        print(
            df_results[
                [
                    "product_code",
                    "product_name",
                    "purchase_currency",
                    "purchase_price",
                    "purchase_price_czk",
                    "minimum_price_czk",
                    "maximum_price_czk",
                    "status"
                ]
            ]
        )

        # Datum zpracovávaného kurzovního lístku.
        control_date = (
            df_exchange_rates["rate_date"]
            .iloc[0]
            .date()
        )

        processed_at = datetime.now()

        # Příprava kurzů pro zápis do SQL.
        df_rates_sql = df_exchange_rates.copy()

        df_rates_sql["rate_date"] = (
            df_rates_sql["rate_date"].dt.date
        )

        df_rates_sql["downloaded_at"] = (
            processed_at
        )

        rate_columns = [
            "rate_date",
            "currency_code",
            "amount",
            "rate_czk",
            "downloaded_at"
        ]

        df_rates_sql = df_rates_sql[
            rate_columns
        ]

        rate_records = list(
            df_rates_sql.itertuples(
                index=False,
                name=None
            )
        )

        # Příprava výsledků pro zápis do SQL.
        df_results_sql = df_results.copy()

        df_results_sql["control_date"] = (
            control_date
        )

        df_results_sql["processed_at"] = (
            processed_at
        )

        df_results_sql["amount"] = (
            df_results_sql["amount"].astype(int)
        )

        result_columns = [
            "control_date",
            "product_id",
            "purchase_currency",
            "purchase_price",
            "amount",
            "rate_czk",
            "purchase_price_czk",
            "minimum_price_czk",
            "maximum_price_czk",
            "status",
            "processed_at"
        ]

        df_results_sql = df_results_sql[
            result_columns
        ]

        result_records = list(
            df_results_sql.itertuples(
                index=False,
                name=None
            )
        )

        # Odstranění případných záznamů stejného dne.
        cursor.execute(
            """
            DELETE FROM dbo.pricing_control_results
            WHERE control_date = ?
            """,
            control_date
        )

        cursor.execute(
            """
            DELETE FROM dbo.exchange_rates
            WHERE rate_date = ?
            """,
            control_date
        )

        # Zápis kurzovního lístku.
        insert_rates_sql = """
            INSERT INTO dbo.exchange_rates
            (
                rate_date,
                currency_code,
                amount,
                rate_czk,
                downloaded_at
            )
            VALUES (?, ?, ?, ?, ?)
        """

        cursor.executemany(
            insert_rates_sql,
            rate_records
        )

        # Zápis výsledků cenové kontroly.
        insert_results_sql = """
            INSERT INTO dbo.pricing_control_results
            (
                control_date,
                product_id,
                purchase_currency,
                purchase_price,
                amount,
                rate_czk,
                purchase_price_czk,
                minimum_price_czk,
                maximum_price_czk,
                status,
                processed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.executemany(
            insert_results_sql,
            result_records
        )

        # Potvrzení obou zápisů současně.
        connection.commit()

        print(
            "Počet kurzů uložených do databáze:",
            len(rate_records)
        )

        print(
            "Počet výsledků uložených do databáze:",
            len(result_records)
        )

        print(
            "Datum cenové kontroly:",
            control_date
        )

        return 0

    except requests.RequestException as error:
        print(
            "Chyba při komunikaci s API:",
            error
        )

        if connection is not None:
            connection.rollback()

        return 1

    except pyodbc.Error as error:
        print(
            "Chyba při práci s databází:",
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

        if connection is not None:
            connection.rollback()

        return 1

    finally:
        if connection is not None:
            connection.close()

            print(
                "Databázové spojení bylo uzavřeno."
            )


if __name__ == "__main__":
    result = main()
    sys.exit(result)