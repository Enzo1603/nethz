from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from main.models import ExerciseSession
from worldle.country_data import VALID_REGIONS


class StaticViewSitemap(Sitemap):
    """Sitemap for static views that don't change often"""

    priority = 0.8
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        """Return list of URL names for static pages"""
        return [
            "main:home",
            "main:technische_mechanik",
            "worldle:home",
            "worldle:default_capitals",
<<<<<<< HEAD
            "worldle:default_languages",
=======
            "worldle:competitive_capitals",
            "worldle:default_languages",
            "worldle:competitive_languages",
            "worldle:competitive_currencies",
            "worldle:competitive_areas",
>>>>>>> seo
            "worldle:leaderboards",
        ]

    def location(self, item):
        """Return the URL for each item"""
        return reverse(item)

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()


class TechnischeMechanikSitemap(Sitemap):
    """Sitemap for Technische Mechanik semester pages"""

    priority = 0.7
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        """Return list of semesters from database"""
        # Get all TM exercise sessions and extract semester names
        tm_sessions = ExerciseSession.objects.filter(
            short_name__startswith="TM_"
        ).values_list("short_name", flat=True)

        # Extract semester part from "TM_HS24" -> "HS24"
<<<<<<< HEAD
        semesters = [session.replace("TM_", "") for session in tm_sessions]
=======
        semesters = [session.replace("TM_", "").lower() for session in tm_sessions]
>>>>>>> seo
        return semesters

    def location(self, item):
        """Return the URL for each semester"""
        return reverse("main:technische_mechanik_semester", args=[item])

    def lastmod(self, obj):
        """Return last modification date from database"""
        try:
            # Since we don't have a modified date field, use current time
            # You could add a 'modified' field to the model later
            return timezone.now()
        except Exception:
            return timezone.now()


class WorldleRegionSitemap(Sitemap):
    """Sitemap for Worldle region-specific pages"""

    priority = 0.6
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        """Return list of regions from country data"""
        # Get valid regions from worldle country data, excluding 'worldwide' and 'antarctic'
        regions = [
            region
            for region in VALID_REGIONS
            if region not in ["worldwide", "antarctic"]
        ]
        return sorted(regions)

    def location(self, item):
        """Return the URL for each region"""
        return reverse("worldle:capitals", args=[item])

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()


class WorldleLanguageRegionSitemap(Sitemap):
    """Sitemap for Worldle language region pages"""

    priority = 0.6
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        """Return list of language regions from country data"""
        # Get valid regions from worldle country data, excluding 'worldwide' and 'antarctic'
        regions = [
            region
            for region in VALID_REGIONS
            if region not in ["worldwide", "antarctic"]
        ]
        return sorted(regions)

    def location(self, item):
        """Return the URL for each language region"""
        return reverse("worldle:languages", args=[item])

    def lastmod(self, obj):
        """Return last modification date"""
        return timezone.now()
