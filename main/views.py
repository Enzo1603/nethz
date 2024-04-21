from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your views here.
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

    valid_template_names = {"TM_HS24"}
    if template_name not in valid_template_names:
        raise Http404("Invalid link")

    return render(request, f"technische_mechanik/{template_name}.html")
