# Third Party Library
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from recipes.errors import COOKING_TIME_MIN_VAL_ERROR
from users.models import USERNAME_NAME

User = get_user_model()

AUTHOR_NAME = "Автор"
RECIPE_NAME_NAME = "Название рецепта"
IMAGE_NAME = "Изображение"
TEXT_NAME = "Описание рецепта"
COOKING_TIME_NAME = "Время приготовления"
TAGS_NAME = "Теги"
PUBLISHING_DATE_NAME = "Дата публикации рецепта"
SHOPPING_CART_NAME = "В корзине"

TAG_NAME_NAME = "Тег"
TAG_COLOR_NAME = "HEX-код цвета тега"
TAG_SLUG_NAME = "Название-слаг тега"

INGREDIENT_NAME_NAME = "Название ингредиента"
MEASUREMENT_UNIT_NAME = "Единица измерения"
AMOUNT_NAME = "Объем/количество"


class Recipe(models.Model):
    """Модель рецепта"""

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
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=COOKING_TIME_NAME,
        validators=[
            MinValueValidator(1, COOKING_TIME_MIN_VAL_ERROR),
        ],
    )
    tags = models.ManyToManyField(
        "Tag",
        verbose_name=TAGS_NAME,
        related_name="recipe_list",
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
    """Модель тега"""

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


class Ingredient(models.Model):
    """Моедль игредиентов"""

    name = models.CharField(verbose_name=INGREDIENT_NAME_NAME, max_length=100)
    measurement_unit = models.CharField(
        verbose_name=MEASUREMENT_UNIT_NAME, max_length=50
    )

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    """Модель для связи рецептов и ингредиентов"""

    recipe = models.ForeignKey(
        Recipe,
        related_name="recipe_ingredient_recipe",
        verbose_name=RECIPE_NAME_NAME,
        on_delete=models.CASCADE,
    )

    ingredient = models.ForeignKey(
        Ingredient,
        related_name="recipe_ingredient_ingredient",
        verbose_name=INGREDIENT_NAME_NAME,
        on_delete=models.PROTECT,
    )

    amount = models.IntegerField(
        verbose_name=AMOUNT_NAME, validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self) -> str:
        return " - ".join([self.recipe.name, self.ingredient.name])


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_recipe_user",
        on_delete=models.CASCADE,
        verbose_name=USERNAME_NAME,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="user_recipe_recipe",
        on_delete=models.CASCADE,
        verbose_name=RECIPE_NAME_NAME,
    )
