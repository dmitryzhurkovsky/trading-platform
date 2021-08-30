from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user"""
    money = models.IntegerField(null=True, blank=True)
