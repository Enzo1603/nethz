from django.http import Http404
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse


# Create your views here.
def home(request):
    tm_card = {
        "title": "Technische Mechanik 2023",
        "description": "Übungsbetrieb und wichtige Unterlagen",
        "button_text": "Zu den Unterlagen",
        "image_path": static("images/technische_mechanik_6px.jpg"),
        "link": reverse("main:technische_mechanik", args=["HS23"]),
        "disable": False,
    }

    ph_card = {
        "title": "Physik I 2024",
        "description": "Übungsbetrieb und wichtige Unterlagen",
        "button_text": "Zu den Unterlagen",
        "image_path": static("images/physik1_2px.jpg"),
        "link": "#",
        "disable": True,
    }

    inf_card = {
        "title": "Informatik I 2024",
        "description": "Übungsbetrieb und wichtige Unterlagen",
        "button_text": "Zu den Unterlagen",
        "image_path": static("images/informatik1_3px.jpg"),
        "link": "#",
        "disable": True,
    }

    worldle_card = {
        "title": "Worldle",
        "description": "Verschiedene Länderquizzes",
        "button_text": "Zu den Spielmodi",
        "image_path": static("images/Earth_2px.jpg"),
        "link": reverse("worldle:home"),
        "disable": False,
    }

    return render(
        request,
        "main/home.html",
        {
            "tm_card": tm_card,
            "ph_card": ph_card,
            "inf_card": inf_card,
            "worldle_card": worldle_card,
        },
    )


def technische_mechanik(request, semester: str):
    template_name = f"TM_{semester}"

    valid_template_names = {"TM_HS23"}
    if template_name not in valid_template_names:
        raise Http404()

    return render(request, f"technische_mechanik/{template_name}.html")
