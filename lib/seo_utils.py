"""
Simple SEO utility functions for basic meta tag management.
"""

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext as _


class SEOData:
    """Container for basic SEO meta data"""

    def __init__(self, title=None, description=None, keywords=None, canonical_url=None):
        self.title = title
        self.description = description
        self.keywords = keywords
        self.canonical_url = canonical_url

    def to_context(self):
        """Convert to dictionary for template context"""
        return {
            "title": self.title,
            "meta_description": self.description,
            "meta_keywords": self.keywords,
            "canonical_url": self.canonical_url,
        }


def get_home_seo():
    """SEO data for the home page"""
    return SEOData(
        title="Enzo Baraldi",
        description=_(
            "Engineering mechanics study materials and geography games for ETH Zurich students"
        ),
        keywords=_(
            "ETH Zurich, engineering mechanics, worldle, geography, study materials"
        ),
    )


def get_technische_mechanik_seo(semester=None):
    """SEO data for Technische Mechanik pages"""
    if semester:
        title = _("Engineering Mechanics {}").format(semester.upper())
        description = _(
            "Engineering mechanics study materials and solutions for ETH Zurich students"
        )
        keywords = _("engineering mechanics, ETH Zurich, study materials, engineering")
    else:
        title = _("Engineering Mechanics")
        description = _(
            "Engineering mechanics study materials and solutions for ETH Zurich students"
        )
        keywords = _("engineering mechanics, ETH Zurich, study materials, engineering")

    return SEOData(title=title, description=description, keywords=keywords)


def get_worldle_home_seo():
    """SEO data for Worldle home page"""
    return SEOData(
        title="Worldle",
        description=_(
            "Geography games - guess capitals, languages, currencies and countries"
        ),
        keywords=_("worldle, geography, capitals, languages, currencies, quiz, game"),
    )


def get_worldle_capitals_seo(region=None):
    """SEO data for Worldle capitals pages"""
    if region:
        region_display = region.replace("-", " ").title()
        title = "Worldle {}".format(region_display)
        description = _("Geography quiz game - guess the capitals")
        keywords = _("capitals, geography, worldle, quiz, game")
    else:
        title = "Worldle"
        description = _("Geography quiz game - guess the capitals")
        keywords = _("capitals, geography, worldle, quiz, game")

    return SEOData(title=title, description=description, keywords=keywords)


def get_worldle_languages_seo(region=None):
    """SEO data for Worldle languages pages"""
    if region:
        region_display = region.replace("-", " ").title()
        title = "Worldle {}".format(region_display)
        description = _("Geography quiz game - guess the languages")
        keywords = _("languages, geography, worldle, quiz, game")
    else:
        title = "Worldle"
        description = _("Geography quiz game - guess the languages")
        keywords = _("languages, geography, worldle, quiz, game")

    return SEOData(title=title, description=description, keywords=keywords)


def get_worldle_competitive_seo(game_type):
    """SEO data for competitive Worldle games"""
    return SEOData(
        title="Worldle {}".format(game_type),
        description=_("Competitive geography quiz with leaderboards"),
        keywords=_("worldle, geography, competitive, quiz, leaderboard"),
    )


def get_leaderboards_seo():
    """SEO data for leaderboards page"""
    return SEOData(
        title=_("Worldle Leaderboards"),
        description=_("View top players in geography quiz games"),
        keywords=_("leaderboards, worldle, geography, quiz, rankings"),
    )


def localized_path(url_name, url_args=None, url_kwargs=None, lang_code=None):
    """Return the language-prefixed path for a named URL.

    Special case: the German (default language) home is canonically served at
    the domain root ("/") so Google can index the property root without a
    redirect. "/de/" stays reachable as an alias that canonicalizes to "/".
    """
    from django.urls import reverse

    if url_name == "main:home" and lang_code == settings.LANGUAGE_CODE:
        return "/"
    with translation.override(lang_code):
        return reverse(url_name, args=url_args or [], kwargs=url_kwargs or {})


def add_seo_to_context(
    context, seo_data, request=None, url_name=None, url_args=None, url_kwargs=None
):
    """Helper function to add SEO data to view context"""
    if isinstance(seo_data, SEOData):
        context.update(seo_data.to_context())

        # Generate canonical URL if not provided but request and url_name are available
        if request and url_name and not seo_data.canonical_url:
            scheme = "https" if request.is_secure() else "http"
            host = request.get_host()
            current_lang = translation.get_language()
            path = localized_path(
                url_name, url_args, url_kwargs, lang_code=current_lang
            )
            context["canonical_url"] = f"{scheme}://{host}{path}"

            # Generate hreflang URLs for bilingual support
            hreflang_urls = {}
            try:
                for lang_code, _lang_name in getattr(settings, "LANGUAGES", ()):
                    hreflang_urls[lang_code] = (
                        f"{scheme}://{host}"
                        f"{localized_path(url_name, url_args, url_kwargs, lang_code)}"
                    )
            finally:
                translation.activate(current_lang)
            context["hreflang_urls"] = hreflang_urls

    return context
