from copy import deepcopy
import csv
import random
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent


DEFAULT_REGION = "worldwide"
VALID_REGIONS = {
    "africa",
    "americas",
    "antarctic",
    "asia",
    "europe",
    "oceania",
    "worldwide",
}


class CountryData:
    __instance = None
    __CSV_ENTRIES = None
    __COUNTRIES_CSV_FILE_PATH = FILE_PATH / "data" / "countries.csv"

    def __new__(cls):
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
    def get_random_filtered_entry(self, region, field):
        entries = deepcopy(self.get_csv_entries())

        if region != DEFAULT_REGION:
            entries = [
                entry
                for entry in entries
                if entry["region"].strip().lower() == region.strip().lower()
            ]

        # Filter entries with no specified field
        entries = [entry for entry in entries if entry[field].strip()]

        # Get random row
        random_row = random.choice(entries)

        return random_row

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

    @classmethod
    def get_random_currencies(
        cls, number_of_currencies: int, exclude: str = None
    ) -> list:
        currencies = []
        for entry in cls.get_csv_entries():
            currency = entry["currencies"].strip().lower()
            currency = list(map(lambda currency: currency.strip(), currency.split(",")))
            currency = list(filter(lambda currency: currency != "", currency))

            for c in currency:
                currencies.append(c)

        result = random.sample(currencies, number_of_currencies)

        while exclude in result:
            result = random.sample(currencies, number_of_currencies)

        return result

    @classmethod
    def get_random_languages(
        cls, number_of_languages: int, exclude: str = None
    ) -> list:
        languages = []
        for entry in cls.get_csv_entries():
            language_entry = entry["languages"].strip().lower()
            language_entry = list(
                map(lambda language: language.strip(), language_entry.split(","))
            )
            language_entry = list(
                filter(lambda language: language != "", language_entry)
            )

            for language in language_entry:
                languages.append(language)

        result = random.sample(languages, number_of_languages)

        while exclude in result:
            result = random.sample(languages, number_of_languages)

        return result
