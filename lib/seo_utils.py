"""
SEO utility functions for easy meta tag management in Django views.
"""

from django.urls import reverse
from django.utils.translation import gettext as _


class SEOData:
    """Container for SEO meta data"""

    def __init__(
        self,
        title=None,
        description=None,
        keywords=None,
        og_title=None,
        og_description=None,
        og_image=None,
        og_type="website",
        twitter_card="summary",
        canonical_url=None,
        structured_data_type="WebSite",
        robots="index, follow",
    ):
        self.title = title
        self.description = description
        self.keywords = keywords
        self.og_title = og_title or title
        self.og_description = og_description or description
        self.og_image = og_image
        self.og_type = og_type
        self.twitter_card = twitter_card
        self.canonical_url = canonical_url
        self.structured_data_type = structured_data_type
        self.robots = robots

    def to_context(self):
        """Convert to dictionary for template context"""
        return {
            "title": self.title,
            "meta_description": self.description,
            "meta_keywords": self.keywords,
            "og_title": self.og_title,
            "og_description": self.og_description,
            "og_image": self.og_image,
            "og_type": self.og_type,
            "twitter_card": self.twitter_card,
            "canonical_url": self.canonical_url,
            "structured_data_type": self.structured_data_type,
            "meta_robots": self.robots,
        }


def get_home_seo():
    """SEO data for the home page"""
    return SEOData(
        title=_("NethZ - ETH Studienressourcen & Worldle"),
        description=_(
            "Technische Mechanik Übungsstunden, Studienunterlagen und Worldle Geographie-Spiele für ETH Zürich Studenten. Zugang zu Prüfungen und Lösungen."
        ),
        keywords=_(
            "ETH Zürich, Technische Mechanik, Studium, Übungsstunden, Worldle, Geographie, Hauptstädte, Sprachen, Polybox, Prüfungen"
        ),
        structured_data_type="EducationalOrganization",
    )


def get_technische_mechanik_seo(semester=None):
    """SEO data for Technische Mechanik pages"""
    if semester:
        title = _("Technische Mechanik {} - ETH Übungsstunden").format(semester.upper())
        description = _(
            "Technische Mechanik Übungsstunden für {} - Lösungen, Prüfungen und Studienunterlagen für ETH Zürich Studenten."
        ).format(semester)
        keywords = _(
            "Technische Mechanik, {}, ETH Zürich, Übungsstunden, Prüfungen, Lösungen, Maschinenbau"
        ).format(semester)
    else:
        title = _("Technische Mechanik - ETH Übungsstunden")
        description = _(
            "Technische Mechanik Übungsstunden - Lösungen, Prüfungen und Studienunterlagen für ETH Zürich Studenten."
        )
        keywords = _(
            "Technische Mechanik, ETH Zürich, Übungsstunden, Prüfungen, Lösungen, Maschinenbau"
        )

    return SEOData(
        title=title,
        description=description,
        keywords=keywords,
        structured_data_type="Course",
    )


def get_worldle_home_seo():
    """SEO data for Worldle home page"""
    return SEOData(
        title=_("Worldle - Geographie-Spiele"),
        description=_(
            "Teste dein Wissen über Hauptstädte, Sprachen, Währungen und Länder weltweit. Interaktive Geographie-Spiele mit Bestenlisten."
        ),
        keywords=_(
            "Worldle, Geographie, Hauptstädte, Sprachen, Währungen, Quiz, Spiel, Länder, Welt"
        ),
        og_type="game",
        structured_data_type="Game",
    )


def get_worldle_capitals_seo(region=None):
    """SEO data for Worldle capitals pages"""
    if region:
        region_display = region.replace("-", " ").title()
        title = _("Hauptstädte Quiz {} - Worldle").format(region_display)
        description = _(
            "Teste dein Wissen über die Hauptstädte von {}. Interaktives Quiz mit Bestenlisten und Wettkampfmodus."
        ).format(region_display)
        keywords = _("Hauptstädte, {}, Quiz, Geographie, Worldle, Spiel").format(
            region_display
        )
    else:
        title = _("Hauptstädte Quiz - Worldle")
        description = _(
            "Teste dein Wissen über Hauptstädte weltweit. Interaktives Quiz mit verschiedenen Regionen und Wettkampfmodus."
        )
        keywords = _("Hauptstädte, Quiz, Geographie, Worldle, Spiel, Welt")

    return SEOData(
        title=title,
        description=description,
        keywords=keywords,
        og_type="game",
        structured_data_type="Game",
    )


def get_worldle_languages_seo(region=None):
    """SEO data for Worldle languages pages"""
    if region:
        region_display = region.replace("-", " ").title()
        title = _("Sprachen Quiz {} - Worldle").format(region_display)
        description = _(
            "Teste dein Wissen über die Sprachen von {}. Lerne Weltsprachen spielerisch kennen."
        ).format(region_display)
        keywords = _("Sprachen, {}, Quiz, Geographie, Worldle, Spiel").format(
            region_display
        )
    else:
        title = _("Sprachen Quiz - Worldle")
        description = _(
            "Teste dein Wissen über Weltsprachen. Interaktives Quiz über Sprachen verschiedener Länder und Regionen."
        )
        keywords = _("Sprachen, Quiz, Geographie, Worldle, Spiel, Welt")

    return SEOData(
        title=title,
        description=description,
        keywords=keywords,
        og_type="game",
        structured_data_type="Game",
    )


def get_worldle_competitive_seo(game_type):
    """SEO data for competitive Worldle games"""
    game_types = {
        "capitals": _("Hauptstädte"),
        "languages": _("Sprachen"),
        "currencies": _("Währungen"),
        "areas": _("Flächen"),
    }

    game_name = game_types.get(game_type, game_type.title())

    return SEOData(
        title=_("Wettkampf {} Quiz - Worldle").format(game_name),
        description=_(
            "Wettkampfmodus für {} - Spiele gegen die Zeit und andere Spieler. Bestenlisten und Achievements."
        ).format(game_name),
        keywords=_("{}, Wettkampf, Quiz, Bestenliste, Worldle, Spiel").format(
            game_name
        ),
        og_type="game",
        structured_data_type="Game",
    )


def get_leaderboards_seo():
    """SEO data for leaderboards page"""
    return SEOData(
        title=_("Bestenlisten - Worldle"),
        description=_(
            "Sieh dir die besten Spieler in allen Worldle-Kategorien an. Hauptstädte, Sprachen, Währungen und mehr."
        ),
        keywords=_("Bestenliste, Highscore, Worldle, Rangliste, Quiz, Geographie"),
        structured_data_type="WebPage",
    )


def add_seo_to_context(context, seo_data):
    """Helper function to add SEO data to view context"""
    if isinstance(seo_data, SEOData):
        context.update(seo_data.to_context())
    return context
