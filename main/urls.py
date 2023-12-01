from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "technische-mechanik/<str:semester>/",
        views.technische_mechanik,
        name="technische_mechanik",
    ),
]
