import csv
import random
from copy import deepcopy
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent
PROFANITY_EN_CSV_FILE_PATH = (
    FILE_PATH.parent / "static" / "profanity" / "profanity_en.csv"
)

with open(PROFANITY_EN_CSV_FILE_PATH, "r", encoding="utf-8") as f:
    READER = csv.DictReader(f)
    CSV_ENTRIES = list(READER)
    PROFANITIES = []
    for row in CSV_ENTRIES:
        PROFANITIES.append(row["text"].lower())
