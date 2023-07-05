# Third Party Library
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField("Email", max_length=254, unique=True)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)

    # TODO: is_subscribed

    # @property
    # def is_admin(self):
    #     return self.role == self.Role.ADMIN
