import csv
import random
from copy import deepcopy
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent
COUNTRIES_CSV_FILE_PATH = FILE_PATH.parent / "static" / "worldle" / "countries.csv"

with open(COUNTRIES_CSV_FILE_PATH, "r", encoding="utf-8") as f:
    READER = csv.DictReader(f)
    CSV_ENTRIES = list(READER)


def get_csv_entries():
    return CSV_ENTRIES


def get_random_countries(number_of_countries: int, filter_empty: list[str]) -> list:
    entries = deepcopy(CSV_ENTRIES)

    for filter_str in filter_empty:
        filter_str = filter_str.strip().lower()
        entries = [entry for entry in entries if entry[filter_str].strip()]

        if filter_str == "area":
            entries = [
                entry for entry in entries if float(entry[filter_str].strip()) > 0
            ]

    return random.sample(entries, number_of_countries)
