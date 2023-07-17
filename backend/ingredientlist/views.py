# Create your views here.
# Third Party Library
from ingredientlist.models import Ingredient
from ingredientlist.serializers import IngredientSerializer
from rest_framework.viewsets import ModelViewSet


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = [
        "get",
    ]
