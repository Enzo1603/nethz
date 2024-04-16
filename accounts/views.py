from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
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
