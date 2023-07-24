# Third Party Library
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from recipes.models import RECIPE_NAME_NAME, Recipe

User = get_user_model()

INGREDIENT_NAME_NAME = "Название ингредиента"
MEASUREMENT_UNIT_NAME = "Единица измерения"
AMOUNT_NAME = "Объем/количество"


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
        unique_together = (
            "recipe",
            "ingredient",
        )

    def __str__(self) -> str:
        return " - ".join([self.recipe.name, self.ingredient.name])
