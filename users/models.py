from django.db import models
from django.contrib.auth.models import AbstractUser






class Person(AbstractUser):
    cin = models.CharField(
        "CIN",
        primary_key=True,
        max_length=8
    )
    username = models.CharField("Username", max_length=255, unique=True)
    email = models.EmailField(
        unique=True,
    )

    USERNAME_FIELD = 'username'
