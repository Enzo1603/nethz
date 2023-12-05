from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(
        "username",
        max_length=16,
        unique=True,
        help_text="Choose your unique username of 4 to 16 characters.",
        validators=[
            validators.RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Enter a valid username. This value may contain only letters, "
                "numbers, and @/./+/-/_ characters.",
                flags=0,
            ),
            validators.MinLengthValidator(
                limit_value=4, message="Username must be at least 4 characters long."
            ),
        ],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    areas_highscore = models.PositiveSmallIntegerField(
        null=False, default=0, blank=True
    )
