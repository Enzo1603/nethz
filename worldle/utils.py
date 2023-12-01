import csv
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent
COUNTRIES_CSV_FILE_PATH = FILE_PATH.parent / "static" / "worldle" / "countries.csv"

with open(COUNTRIES_CSV_FILE_PATH, "r", encoding="utf-8") as f:
    READER = csv.DictReader(f)
    CSV_ENTRIES = list(READER)


def get_csv_entries():
    return CSV_ENTRIES
