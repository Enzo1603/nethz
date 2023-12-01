import random
from copy import deepcopy
from django.http import Http404

from django.urls import reverse

from .utils import get_csv_entries


from django.shortcuts import redirect, render
from django.templatetags.static import static


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
        "link": "#",
        "disable": True,
    }

    areas_card = {
        "title": "Areas",
        "description": "Higher Lower mit Landesflächen",
        "button_text": "Zum Spiel",
        "image_path": static("images/World-Map.jpg"),
        "link": "#",
        "disable": True,
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
