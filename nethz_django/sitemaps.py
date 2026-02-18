from __future__ import annotations

from typing import List

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone, translation

from main.models import ExerciseSession
from worldle.country_data import VALID_REGIONS


class I18nSitemap(Sitemap):
    """
    Minimal i18n-aware Sitemap base.

    Key points:
    - Do NOT override internal URL generation hooks like `_urls()`.
      Django's sitemap view expects each Sitemap to yield relative locations,
      and it renders proper XML (<urlset>, <url>, <loc>, etc.).
    - We instead override `get_urls()` to emit one entry per configured language.
      This uses Django's public API and produces valid XML output via the
      built-in `django.contrib.sitemaps.views.sitemap` view.
    """

    protocol = "https"

    def get_urls(self, page=1, site=None, protocol=None):
        """
        Return URL dicts for all languages.

        We temporarily activate each language to make `reverse()` (within `location()`)
        produce language-prefixed URLs under `i18n_patterns`.
        """
        urls: List[dict] = []

        # Respect protocol passed in by the sitemap view, otherwise fall back.
        protocol = protocol or self.protocol

        with translation.override(None):
            for lang_code, _lang_name in getattr(settings, "LANGUAGES", ()):
                with translation.override(lang_code):
                    # Important: call super().get_urls so Django builds absolute <loc>
                    # and includes lastmod/changefreq/priority correctly.
                    urls.extend(
                        super().get_urls(page=page, site=site, protocol=protocol)
                    )

        return urls


class StaticViewSitemap(I18nSitemap):
    """Sitemap for static pages in both languages."""

    priority = 0.8
    changefreq = "weekly"

    def items(self) -> List[str]:
        return [
            "main:home",
            "main:technische_mechanik",
            "worldle:home",
            "worldle:leaderboards",
        ]

    def location(self, item: str) -> str:
        # `translation.override()` in base ensures i18n_patterns adds /de/ or /en/
        return reverse(item)

    def lastmod(self, obj) -> timezone.datetime:
        # If you have per-page update times, return them here instead.
        return timezone.now()


class TechnischeMechanikSitemap(I18nSitemap):
    """Sitemap for Engineering Mechanics semester pages in both languages."""

    priority = 0.7
    changefreq = "weekly"

    def items(self) -> List[str]:
        tm_sessions = ExerciseSession.objects.filter(
            short_name__startswith="TM_"
        ).values_list("short_name", flat=True)

        # "TM_HS24" -> "hs24"
        semesters = sorted([s.replace("TM_", "").lower() for s in tm_sessions])
        return semesters

    def location(self, item: str) -> str:
        return reverse("main:technische_mechanik_semester", args=[item])

    def lastmod(self, obj) -> timezone.datetime:
        return timezone.now()


class WorldleRegionSitemap(I18nSitemap):
    """Sitemap for Worldle capitals region pages in both languages."""

    priority = 0.6
    changefreq = "monthly"

    def items(self) -> List[str]:
        regions = [r for r in VALID_REGIONS if r not in ["worldwide", "antarctic"]]
        return sorted(regions)

    def location(self, item: str) -> str:
        return reverse("worldle:capitals", args=[item])

    def lastmod(self, obj) -> timezone.datetime:
        return timezone.now()


class WorldleLanguageRegionSitemap(I18nSitemap):
    """Sitemap for Worldle languages region pages in both languages."""

    priority = 0.6
    changefreq = "monthly"

    def items(self) -> List[str]:
        regions = [r for r in VALID_REGIONS if r not in ["worldwide", "antarctic"]]
        return sorted(regions)

    def location(self, item: str) -> str:
        return reverse("worldle:languages", args=[item])

    def lastmod(self, obj) -> timezone.datetime:
        return timezone.now()
