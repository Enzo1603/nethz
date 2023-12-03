import random
from copy import deepcopy

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.http import require_GET

from .utils import get_csv_entries


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


def home(request):
    capitals_card = {
        "title": "Capitals",
        "description": "Errate die Hauptstädte",
        "button_text": "Zum Spiel",
        "image_path": static("images/Bern_3px.jpg"),
        "link": reverse("worldle:default_capitals"),
        "disable": False,
    }

    languages_card = {
        "title": "Languages",
        "description": "Errate die Landessprachen",
        "button_text": "Zum Spiel",
        "image_path": static("images/Languages_3px.jpg"),
        "link": reverse("worldle:default_languages"),
        "disable": False,
    }

    areas_card = {
        "title": "Areas",
        "description": "Higher Lower mit Landesflächen",
        "button_text": "Zum Spiel",
        "image_path": static("images/World-Map.jpg"),
        "link": reverse("worldle:areas"),
        "disable": False,
    }

    return render(
        request,
        "worldle/home.html",
        {
            "capitals_card": capitals_card,
            "languages_card": languages_card,
            "areas_card": areas_card,
        },
    )


def default_capitals(request):
    return redirect(reverse("worldle:capitals", args=[DEFAULT_REGION]))


def capitals(request, region):
    if region not in VALID_REGIONS:
        raise Http404()

    entries = deepcopy(get_csv_entries())

    if region != DEFAULT_REGION:
        entries = [
            entry for entry in entries if entry["region"].lower().strip() == region
        ]

    # Filter entries with no capitals
    entries = [entry for entry in entries if entry["capital"].strip()]

    random_row = random.choice(entries)

    country_name = random_row["name.common"].strip()
    country_cca3 = random_row["cca3"].strip().lower()
    country_image_name = f"worldle/data/{country_cca3}.svg"

    capitals_list = random_row["capital"].strip().split(",")
    capitals_list = list(map(str.strip, capitals_list))
    country_capital = ", ".join(capitals_list)

    return render(
        request,
        "worldle/capitals.html",
        {
            "region": region,
            "country_image_name": country_image_name,
            "country_name": country_name,
            "country_capital": country_capital,
        },
    )


def default_languages(request):
    return redirect(reverse("worldle:languages", args=[DEFAULT_REGION]))


def languages(request, region):
    if region not in VALID_REGIONS:
        raise Http404()

    entries = deepcopy(get_csv_entries())

    if region != DEFAULT_REGION:
        entries = [
            entry for entry in entries if entry["region"].lower().strip() == region
        ]

    # Filter entries with no languages
    entries = [entry for entry in entries if entry["languages"].strip()]

    random_row = random.choice(entries)

    country_name = random_row["name.common"].strip()
    country_cca3 = random_row["cca3"].strip().lower()
    country_image_name = f"worldle/data/{country_cca3}.svg"

    languages_list = random_row["languages"].strip().split(",")
    languages_list = list(map(str.strip, languages_list))
    country_languages = ", ".join(languages_list)

    return render(
        request,
        "worldle/languages.html",
        {
            "region": region,
            "country_image_name": country_image_name,
            "country_name": country_name,
            "country_languages": country_languages,
        },
    )


def areas(request):
    return render(request, "worldle/areas.html")


@require_GET
def get_country(request):
    entries = deepcopy(get_csv_entries())

    # Filter entries with no area or negative area
    entries = [
        entry
        for entry in entries
        if entry["area"].strip() or float(entry["area"].strip()) < 0
    ]

    country = random.choice(entries)

    return JsonResponse({"country": country})
