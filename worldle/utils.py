import csv
import random
from copy import deepcopy
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent
COUNTRIES_CSV_FILE_PATH = FILE_PATH / "data" / "countries.csv"

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


def get_random_capitals(number_of_capitals: int) -> list:
    entries = deepcopy(CSV_ENTRIES)

    capitals = []
    for entry in entries:
        # TODO: handle multiple capitals -> south africa
        # TODO: finish implementation
        capital = entry["capital"].strip().lower()
        capital = list(map(lambda capital: capital.strip(), capital.split(",")))
        capital = list(filter(lambda capital: capital != "", capital))

        for c in capital:
            capitals.append(c)

    return random.sample(capitals, number_of_capitals)
