from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=16,
        unique=True,
        help_text=_("Choose your unique username."),
        validators=[
            validators.RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message=_(
                    "Enter a valid username. This username may contain only letters, "
                    "numbers, and @/./+/-/_ characters."
                ),
                flags=0,
            ),
        ],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    is_email_verified = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    areas_highscore = models.PositiveSmallIntegerField(
        null=False, default=0, blank=True
    )

    capitals_highscore = models.PositiveSmallIntegerField(
        null=False, default=0, blank=True
    )

    currencies_highscore = models.PositiveSmallIntegerField(
        null=False, default=0, blank=True
    )

    languages_highscore = models.PositiveSmallIntegerField(
        null=False, default=0, blank=True
    )
