import csv
from pathlib import Path


FILE_PATH = Path(__file__).resolve().parent


class CurrencyHeader:
    alphabetic_code = "AlphabeticCode"
    currency = "Currency"


class CurrencyData:
    __instance = None
    __CSV_ENTRIES = None
    __COUNTRIES_CSV_FILE_PATH = FILE_PATH / "data" / "currency-codes.csv"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CurrencyData, cls).__new__(cls)
            with open(cls.__COUNTRIES_CSV_FILE_PATH, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                cls.__CSV_ENTRIES = tuple(list(reader))
        return cls.__instance

    @classmethod
    def get_csv_entries(cls):
        return cls.__CSV_ENTRIES

    @classmethod
    def code_to_currency_name(cls, code: str) -> str:
        for entry in cls.get_csv_entries():
            if (
                entry[CurrencyHeader.alphabetic_code].strip().lower()
                == code.strip().lower()
            ):
                return entry[CurrencyHeader.currency]

        return ""
