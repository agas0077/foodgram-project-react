# Third Party Library
from ingredientlist.models import Ingredient, IngredientRecipe
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор инредиентов.
    Обрабатывает ингредиенты при добавлении.
    """

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Основной серализатор для выдачи всего,
    что связано с ингредиентами и конкретным рецептом.
    """

    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = IngredientRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )
