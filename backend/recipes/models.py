# Third Party Library
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()

AUTHOR_NAME = "Автор"
RECIPE_NAME_NAME = "Название рецепта"
IMAGE_NAME = "Изображение"
TEXT_NAME = "Описание рецепта"
COOKING_TIME_NAME = "Время приготовления"
TAGS_NAME = "Теги"
USER_LIKES_NAME = "В избранном"
PUBLISHING_DATE_NAME = "Дата публикации рецепта"
SHOPPING_CART_NAME = "В корзине"

TAG_NAME_NAME = "Тег"
TAG_COLOR_NAME = "HEX-код цвета тега"
TAG_SLUG_NAME = "Название-слаг тега"


class Recipe(models.Model):
    """Recipe model"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name=AUTHOR_NAME,
    )
    name = models.CharField(verbose_name=RECIPE_NAME_NAME, max_length=200)
    image = models.ImageField(
        verbose_name=IMAGE_NAME,
        upload_to="recipe_image/",
    )
    text = models.TextField(verbose_name=TEXT_NAME)
    cooking_time = models.IntegerField(
        verbose_name=COOKING_TIME_NAME,
        validators=[
            MinValueValidator(1),
        ],
    )
    tags = models.ManyToManyField(
        "Tag",
        verbose_name=TAGS_NAME,
        related_name="recipe_list",
        blank=True,
    )
    user_likes = models.ManyToManyField(
        User,
        verbose_name=USER_LIKES_NAME,
        related_name="recipe_like_list",
        blank=True,
    )
    publishing_date = models.DateTimeField(
        verbose_name=PUBLISHING_DATE_NAME, auto_now_add=True
    )
    in_shopping_cart = models.ManyToManyField(
        User,
        related_name="in_shopping_cart",
        verbose_name=SHOPPING_CART_NAME,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Tag model"""

    name = models.CharField(verbose_name=TAG_NAME_NAME, max_length=200)
    color = models.CharField(
        verbose_name=TAG_COLOR_NAME,
        max_length=7,
        validators=[
            RegexValidator(r"^#[A-Z0-9]+$", "Check you HEX code"),
        ],
    )
    slug = models.CharField(
        verbose_name=TAG_SLUG_NAME,
        max_length=200,
        validators=[
            RegexValidator(
                r"^[-a-zA-Z0-9_]+$",
                "Your slug must contain only letters, digits or _ and -",
            ),
        ],
    )

    def __str__(self) -> str:
        return self.name
