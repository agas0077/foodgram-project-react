# Third Party Library
from ingredientlist.models import Ingredient
from ingredientlist.serializers import IngredientSerializer
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet


class IngredientViewSet(ModelViewSet):
    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = [
        "get",
    ]
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [
        SearchFilter,
    ]
    search_fields = [
        "^name",
    ]
