import csv
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent

PROFANITY_EN_CSV_FILE_PATH = FILE_PATH / "profanity" / "profanity_en.csv"
PROFANITY_DE_CSV_FILE_PATH = FILE_PATH / "profanity" / "profanity_de.csv"

with open(PROFANITY_EN_CSV_FILE_PATH, "r", encoding="utf-8") as f:
    READER = csv.DictReader(f)
    EN_CSV_ENTRIES = list(READER)

with open(PROFANITY_DE_CSV_FILE_PATH, "r", encoding="utf-8") as f:
    READER = csv.DictReader(f)
    DE_CSV_ENTRIES = list(READER)


PROFANITIES = set()
for row in EN_CSV_ENTRIES:
    PROFANITIES.add(row["text"].lower())
    PROFANITIES.add(row["canonical_form_1"].lower())


for row in DE_CSV_ENTRIES:
    PROFANITIES.add(row["text"].lower())
    PROFANITIES.add(row["canonical_form_1"].lower())
