from django.urls import path

from . import views


app_name = "worldle"


urlpatterns = [
    path("", views.home, name="home"),
    path("capitals", views.default_capitals, name="default_capitals"),
    path("capitals/<str:region>", views.capitals, name="capitals"),
]
