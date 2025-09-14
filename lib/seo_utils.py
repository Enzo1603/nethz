"""
Simple SEO utility functions for basic meta tag management.
"""

from django.utils.translation import gettext as _


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
def translate_region_name(region):
    """Translate region names for display"""
    region_translations = {
        "worldwide": _("Worldwide"),
        "africa": _("Africa"),
        "americas": _("Americas"),
        "asia": _("Asia"),
        "europe": _("Europe"),
        "oceania": _("Oceania"),
        "antarctic": _("Antarctic"),
    }
    return region_translations.get(region, region.replace("-", " ").title())


=======
>>>>>>> seo
=======
>>>>>>> seo
=======
>>>>>>> seo
class SEOData:
    """Container for basic SEO meta data"""

    def __init__(self, title=None, description=None, keywords=None):
        self.title = title
        self.description = description
        self.keywords = keywords

    def to_context(self):
        """Convert to dictionary for template context"""
        return {
            "title": self.title,
            "meta_description": self.description,
            "meta_keywords": self.keywords,
        }


def get_home_seo():
    """SEO data for the home page"""
    return SEOData(
        title="Enzo Baraldi",
        description=_(
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            "Engineering mechanics study materials and geography games for ETH students"
        ),
        keywords=_(
            "Enzo Baraldi, ETH Zurich, ETHZ, engineering mechanics, technische mechanik, worldle, geography, study materials"
=======
=======
>>>>>>> seo
=======
>>>>>>> seo
            "Engineering mechanics study materials and geography games for ETH Zurich students"
        ),
        keywords=_(
            "ETH Zurich, engineering mechanics, worldle, geography, study materials"
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> seo
=======
>>>>>>> seo
=======
>>>>>>> seo
        ),
    )


def get_technische_mechanik_seo(semester=None):
    """SEO data for Technische Mechanik pages"""
    if semester:
        title = _("Engineering Mechanics {}").format(semester.upper())
        description = _(
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            "Engineering mechanics study materials and solutions for ETH students"
        )
        keywords = _(
            "Enzo Baraldi, technische mechanik, engineering mechanics, ETH Zurich, ETHZ, study materials"
        )
    else:
        title = _("Engineering Mechanics")
        description = _(
            "Engineering mechanics study materials and solutions for ETH students"
        )
        keywords = _(
            "Enzo Baraldi, technische mechanik, engineering mechanics, ETH Zurich, ETHZ, study materials"
        )
=======
=======
>>>>>>> seo
=======
>>>>>>> seo
            "Engineering mechanics study materials and solutions for ETH Zurich students"
        )
        keywords = _("engineering mechanics, ETH Zurich, study materials, engineering")
    else:
        title = _("Engineering Mechanics")
        description = _(
            "Engineering mechanics study materials and solutions for ETH Zurich students"
        )
        keywords = _("engineering mechanics, ETH Zurich, study materials, engineering")
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> seo
=======
>>>>>>> seo
=======
>>>>>>> seo

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        region_display = translate_region_name(region)
=======
        region_display = region.replace("-", " ").title()
>>>>>>> seo
=======
        region_display = region.replace("-", " ").title()
>>>>>>> seo
=======
        region_display = region.replace("-", " ").title()
>>>>>>> seo
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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        region_display = translate_region_name(region)
=======
        region_display = region.replace("-", " ").title()
>>>>>>> seo
=======
        region_display = region.replace("-", " ").title()
>>>>>>> seo
=======
        region_display = region.replace("-", " ").title()
>>>>>>> seo
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


def add_seo_to_context(context, seo_data):
    """Helper function to add SEO data to view context"""
    if isinstance(seo_data, SEOData):
        context.update(seo_data.to_context())
    return context
