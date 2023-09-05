from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model


class CustomUser(AbstractUser):
    def __str__(self) -> str:
        return self.username
