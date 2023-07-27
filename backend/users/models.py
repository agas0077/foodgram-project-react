# Third Party Library
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _

EMAIL_NAME = "Адрес электронной почты"
FIRST_NAME_NAME = "Имя"
LAST_NAME_NAME = "Фамилия"
USERNAME_NAME = "Имя пользователя"

SUBSCRIBER_NAME = "Кто подписывается"
SUBSCRIBEE_NAME = "На кого подписывается"


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер user model, который использует поле email в качестве
    уникального идентификатора, вместо username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Создает и сохранеяет объект пользователя с email и password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохранеяет объект супер-пользователя с email и password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя, расширяющая стандартную модель."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        USERNAME_NAME,
        max_length=150,
        unique=True,
        help_text=_(
            (
                "Required. 150 characters or fewer. "
                "Letters, digits and @/./+/-/_ only."
            )
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name=EMAIL_NAME, max_length=254, unique=True
    )
    first_name = models.CharField(verbose_name=FIRST_NAME_NAME, max_length=150)
    last_name = models.CharField(verbose_name=LAST_NAME_NAME, max_length=150)

    def __str__(self):
        return "-".join([self.get_username(), str(self.id)])


class Subscription(models.Model):
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
