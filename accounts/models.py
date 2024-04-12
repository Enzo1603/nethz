from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators


class CustomUser(AbstractUser):
    username = models.CharField(
        "username",
        max_length=16,
        unique=True,
        help_text="Choose your unique username.",
        validators=[
            validators.RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Enter a valid username. This value may contain only letters, "
                "numbers, and @/./+/-/_ characters.",
                flags=0,
            ),
        ],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    email = models.EmailField("email address", unique=True, blank=False, null=False)
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
