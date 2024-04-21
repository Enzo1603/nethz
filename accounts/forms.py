from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField


from .models import CustomUser
from .utils import PROFANITIES


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email Address"),
        help_text=_("We'll never share your email address with anyone else."),
        required=True,
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Minimum length of 8 characters."),
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username_lower = username.lower()
        if any(word in username_lower for word in PROFANITIES):
            raise forms.ValidationError(
                _("The username contains not allowed characters.")
            )
        return username

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField(
                    "username",
                    placeholder=_("Username"),
                    maxlength=16,
                    autofocus=True,
                ),
                FloatingField("email", placeholder=_("Email Address")),
                FloatingField("password1", placeholder=_("Password"), minlength=8),
                FloatingField("password2", placeholder=_("Confirm Password")),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    _("Sign up"),
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
                FloatingField("username", placeholder=_("Username")),
                FloatingField("password", placeholder=_("Password")),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit", _("Login"), css_class="btn btn-primary mx-4 mt-3 mb-2"
                ),
                HTML(
                    format_html(
                        "<a href='{}' class='btn btn-outline-danger mx-4 mt-2'>{}</a>",
                        reverse("accounts:password_reset"),
                        _("Forgot Password?"),
                    ),
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Minimum length of 8 characters."),
        required=False,
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
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
            raise forms.ValidationError(
                _("The username contains not allowed characters.")
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError(_("The two password entries do not match."))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML(
                        format_html(
                            "<h4 class='mb-4'>{}</h4>", _("Username and Email Address")
                        )
                    ),
                    FloatingField(
                        "username",
                        placeholder=_("Username"),
                        maxlength=16,
                    ),
                    FloatingField("email", placeholder=_("Email Address")),
                    css_class="m-4",
                ),
                css_class="col-lg-6 col-md-8 mx-auto mb-5 p-1 rounded-3 bg-body-tertiary zoom",
            ),
            Div(
                Div(
                    HTML(
                        format_html(
                            "<h4 class='mb-4'>{}</h4>", _("First and Last name")
                        )
                    ),
                    FloatingField("first_name", placeholder=_("First Name")),
                    FloatingField("last_name", placeholder=_("Last Name")),
                    css_class="m-4",
                ),
                css_class="col-lg-6 col-md-8 mx-auto mb-5 p-1 rounded-3 bg-body-tertiary zoom",
            ),
            Div(
                Div(
                    HTML(format_html("<h4 class='mb-4'>{}</h4>", _("Change Password"))),
                    FloatingField(
                        "password1", placeholder=_("New Password"), minlength=8
                    ),
                    FloatingField("password2", placeholder=_("Confirm New Password")),
                    css_class="m-4",
                ),
                css_class="col-lg-6 col-md-8 mx-auto mb-5 p-1 rounded-3 bg-body-tertiary zoom",
            ),
            Div(
                Submit(
                    "submit",
                    _("Update"),
                    css_class="btn btn-primary",
                ),
                css_class="d-grid col-lg-6 col-md-8 mx-auto",
            ),
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField("email", placeholder=_("Email Address")),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    _("Reset my password"),
                    css_class="btn btn-danger mx-4",
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomSetPasswordForm(SetPasswordForm):
    """Used in Password Reset Confirm View."""

    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Minimum length of 8 characters."),
    )

    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                FloatingField(
                    "new_password1", placeholder=_("New Password"), minlength=8
                ),
                FloatingField("new_password2", placeholder=_("New Password")),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    _("Change my password"),
                    css_class="btn btn-primary mx-4 mb-4",
                ),
                css_class="d-grid col-12",
            ),
        )
