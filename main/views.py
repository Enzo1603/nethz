from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import ExerciseSession, WeekEntry


def home(request):
    tm_card = {
        "title": _("Engineering Mechanics 2024"),
        "button_text": _("To the documents"),
        "image_path": static("images/technische_mechanik_6px.jpg"),
        "link": reverse("main:technische_mechanik", args=["HS24"]),
        "disable": False,
    }

    inf_card = {
        "title": _("Computer Science I 2024"),
        "button_text": _("To the documents"),
        "image_path": static("images/informatik1_3px.jpg"),
        "link": "#",
        "disable": True,
    }

    worldle_card = {
        "title": "Worldle",
        "description": _("Various country quizzes"),
        "button_text": _("To the game modes"),
        "image_path": static("images/Earth_2px.jpg"),
        "link": reverse("worldle:home"),
        "disable": False,
    }

    return render(
        request,
        "main/home.html",
        {
            "tm_card": tm_card,
            "inf_card": inf_card,
            "worldle_card": worldle_card,
        },
    )


def technische_mechanik(request, semester: str):
    template_name = f"TM_{semester}"

    # Check if the template name is valid
    valid_template_names = {"TM_HS24"}
    if template_name not in valid_template_names:
        raise Http404("Invalid link")

    # Get the exercise session and the week entries
    exercise_session = get_object_or_404(ExerciseSession, short_name=template_name)
    week_entries = exercise_session.week_entries.all()

    context = {
        "exercise_session": exercise_session,
        "week_entries": week_entries,
    }
    print(week_entries[1].has_exercise_materials)

    return render(request, f"technische_mechanik/{template_name}.html", context)
