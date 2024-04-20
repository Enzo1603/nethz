from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("user_account/", views.UserUpdateView.as_view(), name="user_account"),
    path(
        "activate/<uidb64>/<token>/",
        views.ActivateAccountView.as_view(),
        name="activate_account",
    ),
    # Password reset
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
