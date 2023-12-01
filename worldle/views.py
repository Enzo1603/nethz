from django.shortcuts import render
from django.templatetags.static import static


# Create your views here.
def home(request):
    capitals_card = {
        "title": "Capitals",
        "description": "Errate die Hauptstädte",
        "button_text": "Zum Spiel",
        "image_path": static("images/Bern_3px.jpg"),
        "link": "#",
        "disable": True,
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
