import random

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .leaders import get_leaders, get_leaders_dict, LeaderDatabase
from .country_data import (
    CountryData,
    CountryHeader,
    DEFAULT_REGION,
    VALID_REGIONS,
)
from .currency_data import CurrencyData


def home(request):
    from .cards import (
        capitals_card,
        languages_card,
        competitive_areas_card,
        competitive_capitals_card,
        competitive_currencies_card,
        competitive_languages_card,
    )

    return render(
        request,
        "worldle/home.html",
        {
            "capitals_card": capitals_card,
            "languages_card": languages_card,
            "competitive_areas_card": competitive_areas_card,
            "competitive_capitals_card": competitive_capitals_card,
            "competitive_currencies_card": competitive_currencies_card,
            "competitive_languages_card": competitive_languages_card,
        },
    )


def leaderboard_data(request, highscore_db: str):
    if highscore_db not in (
        LeaderDatabase.areas_highscore,
        LeaderDatabase.capitals_highscore,
        LeaderDatabase.currencies_highscore,
        LeaderDatabase.languages_highscore,
    ):
        raise Http404()
    users = get_leaders(highscore_db)[:20]
    data = [
        {
            "username": user.username,
            "highscore": getattr(user, highscore_db),
        }
        for user in users
    ]
    return JsonResponse(data, safe=False)


def leaderboards(request):
    return render(
        request,
        "worldle/leaderboards.html",
        get_leaders_dict(
            [
                LeaderDatabase.areas_highscore,
                LeaderDatabase.capitals_highscore,
                LeaderDatabase.currencies_highscore,
                LeaderDatabase.languages_highscore,
            ]
        ),
    )


def default_capitals(request):
    return redirect(reverse("worldle:capitals", args=[DEFAULT_REGION]))


def capitals(request, region):
    if region not in VALID_REGIONS:
        raise Http404()

    random_row = CountryData().get_random_filtered_entry(region, CountryHeader.capital)

    country_name = random_row[CountryHeader.common_name].strip()
    country_cca3 = random_row[CountryHeader.cca3].strip().lower()
    country_image_name = f"worldle/{country_cca3}.svg"

    capitals_list = random_row[CountryHeader.capital].strip().split(",")
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


@login_required
def competitive_capitals(request):
    if request.method == "GET":
        country = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.capital]
        )[0]
        request.session["country"] = country

        score = 0
        request.session["score"] = score

        capitals_highscore = request.user.capitals_highscore

        country_cleaned = CountryData().clean_country_data(country)

        correct_answers = CountryData().generate_correct_answers(
            country[CountryHeader.capital]
        )
        correct_answer = random.choice(correct_answers)

        choices = CountryData().generate_choices(
            4, CountryHeader.capital, correct_answer
        )

        return render(
            request,
            "worldle/competitive_capitals.html",
            {
                "country": country_cleaned,
                "choices": choices,
                "score": score,
                "highscore": capitals_highscore,
            },
        )

    elif request.method == "POST":
        country = request.session.get("country")
        user_choice = request.POST.get("choice")

        correct_answers_old = CountryData().generate_correct_answers(
            country[CountryHeader.capital]
        )
        is_correct = user_choice in correct_answers_old

        if is_correct:
            request.session["score"] += 1
        else:
            request.session["score"] = 0

        score = request.session["score"]
        capitals_highscore = request.user.capitals_highscore
        if score > capitals_highscore:
            request.user.capitals_highscore = score
            request.user.save()
            capitals_highscore = score

        # generate new country
        country = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.capital]
        )[0]
        request.session["country"] = country

        country_cleaned = CountryData().clean_country_data(country)

        correct_answers = CountryData().generate_correct_answers(
            country[CountryHeader.capital]
        )
        correct_answer = random.choice(correct_answers)

        choices = CountryData().generate_choices(
            4, CountryHeader.capital, correct_answer
        )

        return JsonResponse(
            {
                "country": country_cleaned,
                "choices": choices,
                "score": score,
                "highscore": capitals_highscore,
                "is_correct": is_correct,
                "correct_answers": ", ".join(correct_answers_old).upper(),
            }
        )


def default_languages(request):
    return redirect(reverse("worldle:languages", args=[DEFAULT_REGION]))


def languages(request, region):
    if region not in VALID_REGIONS:
        raise Http404()

    random_row = CountryData().get_random_filtered_entry(
        region, CountryHeader.languages
    )

    country_name = random_row[CountryHeader.common_name].strip()
    country_cca3 = random_row[CountryHeader.cca3].strip().lower()
    country_image_name = f"worldle/{country_cca3}.svg"

    languages_list = random_row[CountryHeader.languages].strip().split(",")
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
def competitive_languages(request):
    if request.method == "GET":
        country = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.languages]
        )[0]
        request.session["country"] = country

        score = 0
        request.session["score"] = score

        languages_highscore = request.user.languages_highscore

        country_cleaned = CountryData().clean_country_data(country)

        correct_answers = CountryData().generate_correct_answers(
            country[CountryHeader.languages]
        )
        correct_answer = random.choice(correct_answers)

        choices = CountryData().generate_choices(
            4, CountryHeader.languages, correct_answer
        )

        # Leaderboard
        users = get_leaders(LeaderDatabase.languages_highscore)[:20]

        return render(
            request,
            "worldle/competitive_languages.html",
            {
                "country": country_cleaned,
                "choices": choices,
                "score": score,
                "highscore": languages_highscore,
                "users": users,
            },
        )

    elif request.method == "POST":
        country = request.session.get("country")
        user_choice = request.POST.get("choice")

        correct_answers_old = CountryData().generate_correct_answers(
            country[CountryHeader.languages]
        )
        is_correct = user_choice in correct_answers_old

        if is_correct:
            request.session["score"] += 1
        else:
            request.session["score"] = 0

        score = request.session["score"]
        languages_highscore = request.user.languages_highscore
        if score > languages_highscore:
            request.user.languages_highscore = score
            request.user.save()
            languages_highscore = score

        # generate new country
        country = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.languages]
        )[0]
        request.session["country"] = country

        country_cleaned = CountryData().clean_country_data(country)

        correct_answers = CountryData().generate_correct_answers(
            country[CountryHeader.languages]
        )
        correct_answer = random.choice(correct_answers)

        choices = CountryData().generate_choices(
            4, CountryHeader.languages, correct_answer
        )

        return JsonResponse(
            {
                "country": country_cleaned,
                "choices": choices,
                "score": score,
                "highscore": languages_highscore,
                "is_correct": is_correct,
                "correct_answers": ", ".join(correct_answers_old).upper(),
            }
        )


@login_required
def competitive_areas(request):
    if request.method == "GET":
        country1, country2 = CountryData().get_random_countries(
            2, filter_empty=[CountryHeader.area]
        )
        request.session["country1"] = country1
        request.session["country2"] = country2

        score = 0
        request.session["score"] = score

        areas_highscore = request.user.areas_highscore

        country1_cleaned = CountryData().clean_country_data(country1)
        country1_cleaned["area"] = float(country1[CountryHeader.area])

        country2_cleaned = CountryData().clean_country_data(country2)

        return render(
            request,
            "worldle/competitive_areas.html",
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
        country2 = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.area]
        )[0]
        request.session["country1"] = country1
        request.session["country2"] = country2

        country1_cleaned = CountryData().clean_country_data(country1)
        country1_cleaned["area"] = float(country1[CountryHeader.area])

        country2_cleaned = CountryData().clean_country_data(country2)

        return JsonResponse(
            {
                "country1": country1_cleaned,
                "country2": country2_cleaned,
                "score": score,
                "highscore": areas_highscore,
                "is_correct": is_correct,
            }
        )


def code_to_currency_name(request, code):
    currency_name = CurrencyData().code_to_currency_name(code)
    return JsonResponse({"currency_name": currency_name})


@login_required
def competitive_currencies(request):
    if request.method == "GET":
        country = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.currencies]
        )[0]
        request.session["country"] = country

        score = 0
        request.session["score"] = score

        currencies_highscore = request.user.currencies_highscore

        country_cleaned = CountryData().clean_country_data(country)

        correct_answers = CountryData().generate_correct_answers(
            country[CountryHeader.currencies]
        )
        correct_answer = random.choice(correct_answers)

        choices = CountryData().generate_choices(
            4, CountryHeader.currencies, correct_answer
        )

        return render(
            request,
            "worldle/competitive_currencies.html",
            {
                "country": country_cleaned,
                "choices": choices,
                "score": score,
                "highscore": currencies_highscore,
            },
        )

    elif request.method == "POST":
        country = request.session.get("country")
        user_choice = request.POST.get("choice")

        correct_answers_old = CountryData().generate_correct_answers(
            country[CountryHeader.currencies]
        )
        is_correct = user_choice in correct_answers_old

        if is_correct:
            request.session["score"] += 1
        else:
            request.session["score"] = 0

        score = request.session["score"]
        currencies_highscore = request.user.currencies_highscore
        if score > currencies_highscore:
            request.user.currencies_highscore = score
            request.user.save()
            currencies_highscore = score

        # generate new country
        country = CountryData().get_random_countries(
            1, filter_empty=[CountryHeader.currencies]
        )[0]
        request.session["country"] = country

        country_cleaned = CountryData().clean_country_data(country)

        correct_answers = CountryData().generate_correct_answers(
            country[CountryHeader.currencies]
        )
        correct_answer = random.choice(correct_answers)

        choices = CountryData().generate_choices(
            4, CountryHeader.currencies, correct_answer
        )

        return JsonResponse(
            {
                "country": country_cleaned,
                "choices": choices,
                "score": score,
                "highscore": currencies_highscore,
                "is_correct": is_correct,
                "correct_answers": ", ".join(correct_answers_old).upper(),
            }
        )
