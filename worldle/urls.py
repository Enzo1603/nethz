from django.urls import path

from . import views


app_name = "worldle"


urlpatterns = [
    path("", views.home, name="home"),
]
