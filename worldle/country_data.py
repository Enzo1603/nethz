from copy import deepcopy
import csv
import random
from pathlib import Path

from django.templatetags.static import static


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
CHOICES_KEYS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]


class CountryHeader:
    area = "area"
    capital = "capital"
    cca3 = "cca3"
    common_name = "name.common"
    currencies = "currencies"
    languages = "languages"
    region = "region"


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
    def clean_country_data(cls, country):
        return {
            "name": country[CountryHeader.common_name].strip(),
            "image_url": static(f"worldle/{country[CountryHeader.cca3].lower()}.svg"),
        }

    @classmethod
    def generate_correct_answers(cls, country_data):
        correct_answers = country_data.strip().lower()
        correct_answers = list(
            map(lambda item: item.strip(), correct_answers.split(","))
        )
        correct_answers = list(filter(lambda item: item != "", correct_answers))
        return correct_answers

    @classmethod
    def generate_choices(
        cls, number_of_choices, header_field: CountryHeader, correct_answer
    ):
        answers = cls.get_random_items(
            number_of_choices - 1, header_field, exclude=correct_answer
        )
        answers.append(correct_answer)
        random.shuffle(answers)
        return dict(zip(CHOICES_KEYS, answers))

    @classmethod
    def get_random_filtered_entry(cls, region, header_field: CountryHeader):
        entries = deepcopy(cls.get_csv_entries())

        if region != DEFAULT_REGION:
            entries = [
                entry
                for entry in entries
                if entry[CountryHeader.region].strip().lower() == region.strip().lower()
            ]

        # Filter entries with no specified field
        entries = [entry for entry in entries if entry[header_field].strip()]
        random_row = random.choice(entries)

        return random_row

    @classmethod
    def get_random_countries(
        cls,
        number_of_countries: int,
        filter_empty: list[CountryHeader],
    ) -> list:
        for filter_header in filter_empty:
            filter_header = filter_header.strip().lower()
            entries = [
                entry for entry in cls.get_csv_entries() if entry[filter_header].strip()
            ]

            if filter_header == CountryHeader.area:
                entries = [
                    entry
                    for entry in entries
                    if float(entry[filter_header].strip()) > 0
                ]

        return random.sample(entries, number_of_countries)

    @classmethod
    def get_random_items(
        cls, number_of_items: int, header_field: CountryHeader, exclude: str = None
    ) -> list:
        items = []
        for entry in cls.get_csv_entries():
            item = entry[header_field].strip().lower()
            item = list(map(lambda item: item.strip(), item.split(",")))
            item = list(filter(lambda item: item != "", item))

            for i in item:
                items.append(i)

        result = random.sample(items, number_of_items)

        while exclude in result:
            result = random.sample(items, number_of_items)

        return result
