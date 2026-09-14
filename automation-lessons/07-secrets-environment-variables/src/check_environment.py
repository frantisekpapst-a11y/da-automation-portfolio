from pathlib import Path
import os
import sys

from dotenv import load_dotenv

def main():
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / ".env"

    print("Kořen lekce:", base_dir)
    print("Soubor s proměnnými prostředí:", env_file)

    if not env_file.exists():
        print("Soubor .env neexistuje.")
        return 1

    load_dotenv(env_file)

    print("Soubor .env byl načten.")

    database_server = os.getenv("DATABASE_SERVER")
    database_name = os.getenv("DATABASE_NAME")

    print("Databázový server:", database_server)
    print("Název databáze:", database_name)

    if not database_server:
        print("Chybí proměnná DATABASE_SERVER.")
        return 1

    if not database_name:
        print("Chybí proměnná DATABASE_NAME.")
        return 1

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={database_server};"
        f"DATABASE={database_name};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )

    print("Connection string byl úspěšně sestaven.")

    print("Všechny požadované proměnné byly načteny.")
    return 0

if __name__ == "__main__":
    result = main()
    sys.exit(main())
