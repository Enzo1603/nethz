from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user_account/", views.UserUpdateView.as_view(), name="user_account"),
]
