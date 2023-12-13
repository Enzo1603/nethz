from django.urls import path

from . import views


app_name = "worldle"


urlpatterns = [
    path("", views.home, name="home"),
    path("capitals", views.default_capitals, name="default_capitals"),
    path(
        "capitals/competitive", views.competitive_capitals, name="competitive_capitals"
    ),
    path("capitals/<str:region>", views.capitals, name="capitals"),
    path("languages", views.default_languages, name="default_languages"),
    path("languages/<str:region>", views.languages, name="languages"),
    path("areas/", views.areas, name="areas"),
]
