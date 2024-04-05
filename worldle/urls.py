from django.urls import path

from . import views


app_name = "worldle"


urlpatterns = [
    # HOME
    path("", views.home, name="home"),
    # CAPITALS
    path("capitals/", views.default_capitals, name="default_capitals"),
    path("capitals/<str:region>/", views.capitals, name="capitals"),
    path(
        "capitals/competitive/", views.competitive_capitals, name="competitive_capitals"
    ),
    # CURRENCIES
    path(
        "code_to_currency_name/<str:code>/",
        views.code_to_currency_name,
        name="code_to_currency_name",
    ),
    path(
        "currencies/competitive/",
        views.competitive_currencies,
        name="competitive_currencies",
    ),
    # LANGUAGES
    path("languages/", views.default_languages, name="default_languages"),
    path("languages/<str:region>", views.languages, name="languages"),
    path(
        "languages/competitive/",
        views.competitive_languages,
        name="competitive_languages",
    ),
    # AREAS
    path("areas/", views.areas, name="areas"),
]
