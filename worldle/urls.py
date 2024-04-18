from django.urls import path

from . import views


app_name = "worldle"


urlpatterns = [
    # HOME
    path("", views.home, name="home"),
    # LEADERBOARDS
    path("leaderboards/", views.leaderboards, name="leaderboards"),
    path(
        "leaderboards/<str:highscore_db>/",
        views.leaderboard_data,
        name="leaderboard_data",
    ),
    # CAPITALS
    path("capitals/", views.default_capitals, name="default_capitals"),
    path(
        "capitals/competitive/", views.competitive_capitals, name="competitive_capitals"
    ),
    path("capitals/<str:region>/", views.capitals, name="capitals"),
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
    path(
        "languages/competitive/",
        views.competitive_languages,
        name="competitive_languages",
    ),
    path("languages/<str:region>", views.languages, name="languages"),
    # AREAS
    path("areas/competitive/", views.competitive_areas, name="competitive_areas"),
]
