from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import reverse


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField


from .models import CustomUser
from .utils import PROFANITIES


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        help_text="We'll never share your email address with anyone else.",
        required=True,
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Minimum length of 8 characters.",
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_lower = username.lower()
        if any(word in username_lower for word in PROFANITIES):
            raise forms.ValidationError("The username contains not allowed characters.")
        return username

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField(
                    "username",
                    placeholder="Username",
                    maxlength=16,
                    autofocus=True,
                ),
                FloatingField("email", placeholder="Email Address"),
                FloatingField("password1", placeholder="Password", minlength=8),
                FloatingField("password2", placeholder="Confirm Password"),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    "Sign up",
                    css_class="btn btn-primary m-4 mt-3",
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("username", placeholder="Username"),
                FloatingField("password", placeholder="Password"),
                css_class="m-4",
            ),
            Div(
                Submit("submit", "Login", css_class="btn btn-primary mx-4 mt-3 mb-2"),
                HTML(
                    f"<a href='{reverse('accounts:password_reset')}' class='btn btn-outline-danger mx-4 mt-2'>Forgot Password?</a>",
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Minimum length of 8 characters.",
        required=False,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_lower = username.lower()
        if any(word in username_lower for word in PROFANITIES):
            raise forms.ValidationError("The username contains not allowed characters.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("The two password entries do not match.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField(
                    "username",
                    placeholder="Username",
                    maxlength=16,
                ),
                FloatingField("email", placeholder="Email Address"),
                FloatingField("first_name", placeholder="First Name"),
                FloatingField("last_name", placeholder="Last Name"),
                FloatingField("password1", placeholder="New Password", minlength=8),
                FloatingField("password2", placeholder="Confirm New Password"),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    "Update",
                    css_class="btn btn-primary m-4 mt-3",
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("email", placeholder="Email Address"),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    "Reset my password",
                    css_class="btn btn-danger mx-4",
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomSetPasswordForm(SetPasswordForm):
    """Used in Password Reset Confirm View."""

    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Minimum length of 8 characters.",
    )

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("new_password1", placeholder="New Password", minlength=8),
                FloatingField("new_password2", placeholder="New Password"),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    "Change my password",
                    css_class="btn btn-primary mx-4 mb-4",
                ),
                css_class="d-grid col-12",
            ),
        )
