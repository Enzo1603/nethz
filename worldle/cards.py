from django.templatetags.static import static
from django.urls import reverse


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

competitive_areas_card = {
    "title": "Competitive Areas",
    "description": "Higher Lower mit Landesflächen",
    "button_text": "Zum Spiel",
    "image_path": static("images/World-Map.jpg"),
    "link": reverse("worldle:competitive_areas"),
    "disable": False,
}

competitive_capitals_card = {
    "title": "Competitive Capitals",
    "description": "Errate die Hauptstädte",
    "button_text": "Zum Spiel",
    "image_path": static("images/Bern_3px.jpg"),
    "link": reverse("worldle:competitive_capitals"),
    "disable": False,
}

competitive_currencies_card = {
    "title": "Competitive Currencies",
    "description": "Errate die Währung",
    "button_text": "Zum Spiel",
    "image_path": static("images/SwissFrancs_3px.jpg"),
    "link": reverse("worldle:competitive_currencies"),
    "disable": False,
}

competitive_languages_card = {
    "title": "Competitive Languages",
    "description": "Errate die Landessprachen",
    "button_text": "Zum Spiel",
    "image_path": static("images/Languages_3px.jpg"),
    "link": reverse("worldle:competitive_languages"),
    "disable": False,
}
