from django.templatetags.static import static
from django.urls import reverse_lazy

from django.utils.translation import gettext_lazy as _


capitals_card = {
    "title": "Capitals",
    "description": _("Guess the capitals"),
    "button_text": _("Play"),
    "image_path": static("images/Bern_3px.webp"),
    "link": reverse_lazy("worldle:default_capitals"),
    "disable": False,
}

languages_card = {
    "title": "Languages",
    "description": _("Guess the national languages"),
    "button_text": _("Play"),
    "image_path": static("images/Languages_3px.webp"),
    "link": reverse_lazy("worldle:default_languages"),
    "disable": False,
}

competitive_areas_card = {
    "title": "Competitive Areas",
    "description": _("Higher Lower with country areas"),
    "button_text": _("Play"),
    "image_path": static("images/World-Map.webp"),
    "link": reverse_lazy("worldle:competitive_areas"),
    "disable": False,
}

competitive_capitals_card = {
    "title": "Competitive Capitals",
    "description": _("Guess the capitals"),
    "button_text": _("Play"),
    "image_path": static("images/Bern_3px.webp"),
    "link": reverse_lazy("worldle:competitive_capitals"),
    "disable": False,
}

competitive_currencies_card = {
    "title": "Competitive Currencies",
    "description": _("Guess the currency"),
    "button_text": _("Play"),
    "image_path": static("images/SwissFrancs_3px.webp"),
    "link": reverse_lazy("worldle:competitive_currencies"),
    "disable": False,
}

competitive_languages_card = {
    "title": "Competitive Languages",
    "description": _("Guess the national languages"),
    "button_text": _("Play"),
    "image_path": static("images/Languages_3px.webp"),
    "link": reverse_lazy("worldle:competitive_languages"),
    "disable": False,
}
