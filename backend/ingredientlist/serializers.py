# Third Party Library
from ingredientlist.models import Ingredient
from rest_framework.serializers import ModelSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")
