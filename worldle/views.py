import random
from copy import deepcopy

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .utils import get_csv_entries, get_random_countries


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
    country_image_name = f"worldle/{country_cca3}.svg"

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
    country_image_name = f"worldle/{country_cca3}.svg"

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


@login_required
def areas(request):
    if request.method == "GET":
        country1, country2 = get_random_countries(2, filter_empty=["area"])
        request.session["country1"] = country1
        request.session["country2"] = country2

        score = int(request.session.get("score", 0))

        request.session["score"] = score

        areas_highscore = request.user.areas_highscore

        country1_cleaned = {
            "name": country1["name.common"],
            "image_url": static(f"worldle/{country1['cca3'].lower()}.svg"),
            "area": float(country1["area"]),
        }

        country2_cleaned = {
            "name": country2["name.common"],
            "image_url": static(f"worldle/{country2['cca3'].lower()}.svg"),
        }

        return render(
            request,
            "worldle/areas.html",
            {
                "country1": country1_cleaned,
                "country2": country2_cleaned,
                "score": score,
                "highscore": areas_highscore,
            },
        )

    elif request.method == "POST":
        country1 = request.session.get("country1")
        country2 = request.session.get("country2")
        user_choice = request.POST.get("choice")

        correct_answer = (
            "higher"
            if float(country2["area"]) > float(country1["area"])
            else "lower"
            if float(country2["area"]) < float(country1["area"])
            else "equal"
        )

        is_correct = correct_answer == "equal" or correct_answer == user_choice

        if is_correct:
            request.session["score"] += 1
        else:
            request.session["score"] = 0

        score = request.session["score"]
        areas_highscore = request.user.areas_highscore
        if score > areas_highscore:
            request.user.areas_highscore = score
            request.user.save()
            areas_highscore = score

        # generate new countries
        country1 = country2  # old country2 becomes new country1
        country2 = get_random_countries(1, filter_empty=["area"])[0]
        request.session["country1"] = country1
        request.session["country2"] = country2

        country1_cleaned = {
            "name": country1["name.common"],
            "image_url": static(f"worldle/{country1['cca3'].lower()}.svg"),
            "area": float(country1["area"]),
        }

        country2_cleaned = {
            "name": country2["name.common"],
            "image_url": static(f"worldle/{country2['cca3'].lower()}.svg"),
        }

        return JsonResponse(
            {
                "country1": country1_cleaned,
                "country2": country2_cleaned,
                "score": score,
                "highscore": areas_highscore,
                "is_correct": is_correct,
            }
        )
