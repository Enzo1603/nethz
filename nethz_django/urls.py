"""
URL configuration for nethz_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.shortcuts import redirect
from main.views import root_redirect
from .sitemaps import (
    StaticViewSitemap,
    TechnischeMechanikSitemap,
    WorldleRegionSitemap,
    WorldleLanguageRegionSitemap,
)

# Sitemap configuration
sitemaps = {
    "static": StaticViewSitemap,
    "technische_mechanik": TechnischeMechanikSitemap,
    "worldle_regions": WorldleRegionSitemap,
    "worldle_language_regions": WorldleLanguageRegionSitemap,
}

urlpatterns = [
    path(
        "", root_redirect, name="root_redirect"
    ),  # Root redirect for language detection
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    # SEO URLs
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
    # Serve favicon from static files
    path("favicon.ico", lambda request: redirect("/static/images/eth-logo.ico")),
]

urlpatterns += i18n_patterns(
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("main.urls")),
    path("worldle/", include("worldle.urls")),
)
