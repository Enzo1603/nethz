from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from django import forms


from django.core import validators
from django.utils.safestring import mark_safe

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        help_text="Choose your unique username.",
        validators=[
            validators.RegexValidator(
                regex="^[A-Za-z][A-Za-z0-9_.]*$",
                message="Usernames must have only letters, numbers, dots, or underscores.",
            ),
            validators.MinLengthValidator(
                limit_value=4, message="Username must be at least 4 characters long."
            ),
        ],
    )

    email = forms.EmailField(
        label="Email Address",
        help_text="We'll never share your email address with anyone else.",
    )

    password1 = forms.CharField(
        label="Password",
        help_text="Minimum length of 8 characters.",
        widget=forms.PasswordInput,
        validators=[
            validators.MinLengthValidator(limit_value=8),
        ],
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                "csrf_token",
                FloatingField(
                    "username", placeholder="Username", maxlength=16, minlength=4
                ),
                FloatingField("email", placeholder="Email Address"),
                FloatingField("password1", placeholder="Password", minlength=8),
                FloatingField("password2", placeholder="Confirm Password"),
                css_class="m-4",
            ),
            Div(
                Submit(
                    "submit",
                    "Register",
                    css_class="btn btn-primary m-4 mt-3",
                ),
                css_class="d-grid col-12",
            ),
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField("email", placeholder="Email Address"),
            Submit("submit", "Update", css_class="btn btn-dark m-4 mt-3"),
        )
