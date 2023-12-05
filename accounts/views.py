from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout, Field
from crispy_bootstrap5.bootstrap5 import FloatingField


from .forms import CustomUserCreationForm, CustomAuthenticationForm


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("main:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You're already logged in.")
            return redirect("main:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        messages.success(self.request, "You successfully signed up.")
        return response


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("main:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "You successfully logged in.")
        return response


def logout_view(request):
    logout(request)
    messages.success(request, "You successfully logged out.")
    return redirect("main:home")
