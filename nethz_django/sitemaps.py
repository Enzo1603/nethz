from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from main.models import ExerciseSession
from worldle.country_data import VALID_REGIONS


class I18nSitemap(Sitemap):
    """
    Basis-Sitemap-Klasse mit i18n-Unterstützung.
    Generiert URLs für alle konfigurierten Sprachen.
    """

    protocol = "https"

    def _urls(self, page, protocol, domain):
        """
        Überschreibt die Standard-URL-Generierung um sicherzustellen,
        dass für jede Sprache separate URLs generiert werden.
        """
        urls = []

        # Für jede konfigurierte Sprache URLs generieren
        for lang_code, lang_name in settings.LANGUAGES:
            # Aktiviere temporär die Sprache für URL-Generierung
            from django.utils.translation import activate

            activate(lang_code)

            # Generiere URLs für diese Sprache
            for item in self.items():
                loc = self._location(item)
                priority = self._get("priority", item)
                lastmod = self._get("lastmod", item)
                changefreq = self._get("changefreq", item)

                # Erstelle absolute URL mit Protokoll und Domain
                url = f"{protocol}://{domain}{loc}"

                url_info = {
                    "item": item,
                    "location": url,
                    "lastmod": lastmod,
                    "changefreq": changefreq,
                    "priority": str(priority if priority is not None else ""),
                    "lang_code": lang_code,
                }

                urls.append(url_info)

        return urls

    def _location(self, item):
        """
        Generiert die Location-URL für ein Item.
        Die Sprache wird bereits durch activate() gesetzt.
        Muss in Unterklassen überschrieben werden.
        """
        raise NotImplementedError("Subclasses must implement _location()")


class StaticViewSitemap(I18nSitemap):
    """Sitemap für statische Views in beiden Sprachen"""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        """Return list of URL names for static pages"""
        return [
            "main:home",
            "main:technische_mechanik",
            "worldle:home",
            "worldle:default_capitals",
            "worldle:competitive_capitals",
            "worldle:default_languages",
            "worldle:competitive_languages",
            "worldle:competitive_currencies",
            "worldle:competitive_areas",
            "worldle:leaderboards",
        ]

    def _location(self, item):
        """Return the URL for each item (language is set via activate())"""
        return reverse(item)

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()


class TechnischeMechanikSitemap(I18nSitemap):
    """Sitemap für Technische Mechanik Semester-Seiten in beiden Sprachen"""

    priority = 0.7
    changefreq = "weekly"

    def items(self):
        """Return list of semesters from database"""
        # Get all TM exercise sessions and extract semester names
        tm_sessions = ExerciseSession.objects.filter(
            short_name__startswith="TM_"
        ).values_list("short_name", flat=True)

        # Extract semester part from "TM_HS24" -> "hs24"
        semesters = sorted(
            [session.replace("TM_", "").lower() for session in tm_sessions]
        )
        return semesters

    def _location(self, item):
        """Return the URL for each semester (language is set via activate())"""
        return reverse("main:technische_mechanik_semester", args=[item])

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()


class WorldleRegionSitemap(I18nSitemap):
    """Sitemap für Worldle Region-spezifische Seiten (Capitals) in beiden Sprachen"""

    priority = 0.6
    changefreq = "monthly"

    def items(self):
        """Return list of regions from country data"""
        # Get valid regions from worldle country data, excluding 'worldwide' and 'antarctic'
        regions = [
            region
            for region in VALID_REGIONS
            if region not in ["worldwide", "antarctic"]
        ]
        return sorted(regions)

    def _location(self, item):
        """Return the URL for each region (language is set via activate())"""
        return reverse("worldle:capitals", args=[item])

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()


class WorldleLanguageRegionSitemap(I18nSitemap):
    """Sitemap für Worldle Language Region Seiten in beiden Sprachen"""

    priority = 0.6
    changefreq = "monthly"

    def items(self):
        """Return list of language regions from country data"""
        # Get valid regions from worldle country data, excluding 'worldwide' and 'antarctic'
        regions = [
            region
            for region in VALID_REGIONS
            if region not in ["worldwide", "antarctic"]
        ]
        return sorted(regions)

    def _location(self, item):
        """Return the URL for each language region (language is set via activate())"""
        return reverse("worldle:languages", args=[item])

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()
