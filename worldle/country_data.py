import csv
import random
from pathlib import Path
from typing import Self


FILE_PATH = Path(__file__).resolve().parent


class CountryData:
    __instance = None
    __CSV_ENTRIES = None
    __COUNTRIES_CSV_FILE_PATH = FILE_PATH / "data" / "countries.csv"

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super(CountryData, cls).__new__(cls)
            with open(cls.__COUNTRIES_CSV_FILE_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                cls.__CSV_ENTRIES = tuple(list(reader))
        return cls.__instance

    @classmethod
    def get_csv_entries(cls):
        return cls.__CSV_ENTRIES

    @classmethod
    def get_random_countries(
        cls,
        number_of_countries: int,
        filter_empty: list[str],
    ) -> list:
        for filter_str in filter_empty:
            filter_str = filter_str.strip().lower()
            entries = [
                entry for entry in cls.get_csv_entries() if entry[filter_str].strip()
            ]

            if filter_str == "area":
                entries = [
                    entry for entry in entries if float(entry[filter_str].strip()) > 0
                ]

        return random.sample(entries, number_of_countries)

    @classmethod
    def get_random_capitals(cls, number_of_capitals: int, exclude: str = None) -> list:
        capitals = []
        for entry in cls.get_csv_entries():
            capital = entry["capital"].strip().lower()
            capital = list(map(lambda capital: capital.strip(), capital.split(",")))
            capital = list(filter(lambda capital: capital != "", capital))

            for c in capital:
                capitals.append(c)

        result = random.sample(capitals, number_of_capitals)

        while exclude in result:
            result = random.sample(capitals, number_of_capitals)

        return result
