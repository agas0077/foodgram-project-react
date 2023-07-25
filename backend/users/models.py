# Third Party Library
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.constraints import UniqueConstraint

EMAIL_NAME = "Адрес электронной почты"
FIRST_NAME_NAME = "Имя"
LAST_NAME_NAME = "Фамилия"

SUBSCRIBER_NAME = "Кто подписывается"
SUBSCRIBEE_NAME = "На кого подписывается"


class User(AbstractUser):
    """Модель пользователя, расширяющая стандартную модель."""

    email = models.EmailField(verbose_name=EMAIL_NAME, max_length=254, unique=True)
    first_name = models.CharField(verbose_name=FIRST_NAME_NAME, max_length=150)
    last_name = models.CharField(verbose_name=LAST_NAME_NAME, max_length=150)

    def __str__(self):
        return "-".join([self.get_username(), str(self.id)])


class SubscriberSubscribee(models.Model):
    """Модель для поддержки связи подписчиков."""

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_subscriber",
        verbose_name=SUBSCRIBER_NAME,
    )
    subscribee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_subscribee",
        verbose_name=SUBSCRIBEE_NAME,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["subscriber", "subscribee"], name="unique_subscription"
            )
        ]

    def __str__(self) -> str:
        return " - ".join([self.subscriber.username, self.subscribee.username])
