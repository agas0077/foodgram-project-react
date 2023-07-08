# Third Party Library
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField("email", max_length=254, unique=True)
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)

    # @property
    # def is_admin(self):
    #     return self.role == self.Role.ADMIN

    def __str__(self):
        return "-".join([self.get_username(), str(self.id)])


class SubscriberSubscribee(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_subscriber",
        verbose_name="subscriber",
    )
    subscribee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_subscribee",
        verbose_name="subscribee",
    )

    class Meta:
        unique_together = (
            "subscriber",
            "subscribee",
        )
