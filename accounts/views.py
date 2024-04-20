from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.tokens import default_token_generator


from urllib.parse import urlparse, urlunparse

from django.conf import settings

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
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

        messages.success(
            self.request,
            "Account creation successful. A confirmation email has been sent to your email address.",
        )
        messages.warning(
            self.request,
            "You will not be able to log in until you have confirmed your email.",
        )

        return redirect("main:home")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You're already logged in.")
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if user.is_email_verified:
            login(self.request, user)
            messages.success(self.request, "You successfully logged in.")
            return redirect(self.success_url)

        messages.warning(
            self.request,
            "Another confirmation email has been sent to your email address since you have not confirmed it yet.",
        )
        # Resend activation email
        send_verification_email(user, self.request)
        return redirect("accounts:login")


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
            user.is_email_verified = True
            user.save()

            messages.success(
                request,
                "Thank you for confirming your email. You can now log in to your account.",
            )
            return redirect("accounts:login")
        else:
            raise Http404(
                "Invalid confirmation link. Please make sure you are using the correct link provided in the confirmation email."
            )


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/user_account.html"
    success_url = reverse_lazy("accounts:user_account")

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        self.old_email = form.initial[
            "email"
        ]  # Speichern Sie die ursprüngliche E-Mail-Adresse
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        new_email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        if password:
            self.object.set_password(password)
            self.object.save()
            messages.success(self.request, "Your password has been updated.")
        if self.old_email != new_email:
            self.object.is_email_verified = False
            self.object.save()
            send_verification_email(self.object, self.request)
            logout(self.request)
            messages.success(
                self.request,
                "Your email has been updated. A confirmation link has been sent to your new email address. Please confirm your email to log in.",
            )
            return redirect("main:home")
        else:
            messages.success(self.request, "Your data has been successfully updated.")

        return response

        # response = super().form_valid(form)
        # password = form.cleaned_data.get("password1")
        # if password:
        #     self.object.set_password(password)
        #     self.object.save()

        # messages.success(self.request, "Your data has been successfully updated.")
        # return response


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset/password_reset_form.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("accounts:login")
    html_email_template_name = "accounts/password_reset/password_reset_email.html"
    subject_template_name = "accounts/password_reset/password_reset_subject.txt"

    # TODO: if user is logged in, redirect to user update view to change password with message

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "If your email address is linked to an account, a password reset link has been sent to it.",
        )
        return response


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("accounts:login")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        raise Http404(
            "The password reset link was invalid, possibly because it has already been used. Please request a new password reset."
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Your password has been successfully reset. You can now log in with your new password.",
        )
        return response
