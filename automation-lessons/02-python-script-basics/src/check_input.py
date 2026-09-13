from pathlib import Path
import sys


# ============================================================
# 1. UČÍCÍ VERZE
# ============================================================
# Obsahuje pomocné proměnné a výpisy, abychom viděli
# jednotlivé kroky při sestavování cest a spuštění procesu.


def main_learning():
    # __file__ je speciální proměnná obsahující cestu
    # k aktuálnímu Python souboru jako textový řetězec.
    print("Hodnota __file__:", __file__)

    # Převod textové cesty na objekt Path.
    file_path = Path(__file__)
    print("Hodnota file_path:", file_path)

    # Převod na jednoznačnou absolutní cestu.
    resolved_path = file_path.resolve()
    print("Hodnota resolved_path:", resolved_path)

    # Nadřazená složka souboru check_input.py je složka src.
    script_dir = resolved_path.parent
    print("Hodnota script_dir:", script_dir)

    # Path.cwd() vrací složku, ze které byl proces spuštěn.
    # Nemusí být stejná jako složka, ve které leží skript.
    current_dir = Path.cwd()
    print("Aktuální pracovní složka:", current_dir)
    print("Složka Python skriptu:", script_dir)

    # Nadřazená složka src je kořen tohoto cvičného projektu.
    base_dir = script_dir.parent
    print("Hodnota base_dir:", base_dir)

    # Sestavení cest ke vstupní a výstupní složce.
    input_dir = base_dir / "data" / "input"
    output_dir = base_dir / "data" / "output"

    print("Hodnota input_dir:", input_dir)
    print("Hodnota output_dir:", output_dir)

    # Vstupní složku očekáváme jako součást připraveného vstupu.
    # Pokud neexistuje, proces ukončíme návratovým kódem 1.
    input_exists = input_dir.exists()
    print("Existuje vstupní složka:", input_exists)

    if not input_exists:
        print("Vstupní složka neexistuje.")
        return 1

    print("Vstupní složka existuje.")

    # Výstupní složku spravuje náš skript, proto ji může vytvořit.
    print(
        "Existuje výstupní složka před vytvořením:",
        output_dir.exists()
    )

    # parents=True dovoluje vytvořit i chybějící nadřazené složky.
    # exist_ok=True zabrání chybě, pokud složka již existuje.
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        "Existuje výstupní složka po vytvoření:",
        output_dir.exists()
    )

    # Sestavení cesty k výslednému textovému souboru.
    output_file = output_dir / "check_result.txt"

    # write_text() vytvoří soubor a zapíše do něj text.
    # Pokud soubor existuje, jeho obsah bude nahrazen.
    output_file.write_text(
        "Kontrola byla úspěšná. Vstupní složka existuje.",
        encoding="utf-8"
    )

    print("Výstupní soubor byl vytvořen:", output_file)

    # Návratový kód 0 znamená úspěšné dokončení procesu.
    return 0


# ============================================================
# 2. BĚŽNÁ ZKRÁCENÁ VERZE
# ============================================================
# Provádí stejný proces, ale neobsahuje učící mezikroky
# ani pomocné kontrolní výpisy.


def main():
    # Zjištění složky skriptu a kořene projektu.
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent

    # Sestavení potřebných cest.
    input_dir = base_dir / "data" / "input"
    output_dir = base_dir / "data" / "output"
    output_file = output_dir / "check_result.txt"

    # Chybějící vstup představuje kritickou chybu.
    if not input_dir.exists():
        print("Vstupní složka neexistuje.")
        return 1

    # Bezpečné vytvoření výstupní složky.
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Vytvoření nebo nahrazení výsledného souboru.
    output_file.write_text(
        "Kontrola byla úspěšná. Vstupní složka existuje.",
        encoding="utf-8"
    )

    print("Výstupní soubor byl vytvořen:", output_file)
    return 0


# ============================================================
# 3. VSTUPNÍ BOD SKRIPTU
# ============================================================
# Při přímém spuštění má __name__ hodnotu "__main__".
# Při importu má hodnotu názvu modulu, například "check_input",
# a tento blok se automaticky neprovede.


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