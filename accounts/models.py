from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    areas_highscore = models.PositiveSmallIntegerField(
        null=False, default=0, blank=True
    )
