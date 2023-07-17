# Third Party Library
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from recipes.models import Recipe

User = get_user_model()


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(verbose_name="ingredient name", max_length=100)
    measurement_unit = models.CharField(
        verbose_name="measurement_unit", max_length=50
    )


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name="user_recipe_ingredient_recipe",
        verbose_name="user_recipe_ingredient_recipe",
        on_delete=models.PROTECT,
    )

    ingredient = models.ForeignKey(
        Ingredient,
        related_name="user_recipe_ingredient_ingredient",
        verbose_name="user_recipe_ingredient_ingredient",
        on_delete=models.PROTECT,
    )

    amount = models.IntegerField(
        verbose_name="amount", validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = (
            "recipe",
            "ingredient",
        )
