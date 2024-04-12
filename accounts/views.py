from threading import Thread

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.views.generic import CreateView, UpdateView


from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserChangeForm,
)
from .models import CustomUser
from .emails import send_verification_email

UserModel = get_user_model()


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("main:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You're already logged in.")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # response = super().form_valid(form)
        user = form.save(commit=False)
        user.save()

        send_verification_email(user, self.request)

        return HttpResponse("Activation E-Mail was sent.")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("main:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You're already logged in.")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # response = super().form_valid(form)
        user = form.get_user()
        if user.is_email_verified:
            login(self.request, user)
            messages.success(self.request, "You successfully logged in.")
            return redirect(self.success_url)

        messages.warning(self.request, "Activation E-Mail was sent.")
        # Resend activation email
        send_verification_email(user, self.request)
        return redirect("main:home")


def logout_view(request):
    logout(request)
    messages.success(request, "You successfully logged out.")
    return redirect("main:home")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            # user.is_active = True
            user.is_email_verified = True
            user.save()
            # login(request, user)
            return HttpResponse(
                "Vielen Dank für Ihre E-Mail-Bestätigung. Jetzt können Sie sich in Ihr Konto einloggen."
            )
        else:
            return HttpResponse("Aktivierungslink ist ungültig!")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/user_account.html"
    success_url = reverse_lazy("accounts:user_account")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        password = form.cleaned_data.get("password1")
        if password:
            self.object.set_password(password)
            self.object.save()

        messages.success(self.request, "Your data has been successfully updated.")
        return response
