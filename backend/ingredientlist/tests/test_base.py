# Third Party Library
from core.tests_base import TestsBaseClass
from django.urls import reverse_lazy


class IngredientlistTestsBaseClass(TestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.GET_INGREDIENTS_URL = reverse_lazy(
            "ingredientlist:ingredient-list"
        )
        self.GET_INGREDIENT_URL = lambda ingredient_id: reverse_lazy(
            "ingredientlist:ingredient-detail",
            args=[
                ingredient_id,
            ],
        )
        self.GET_ORDER_LIST_URL = reverse_lazy("ingredientlist:order-list")
        self.ADD_REMOVE_RECIPE_ORDER_LIST_URL = lambda recipe_id: reverse_lazy(
            "ingredientlist:add-remove-recipe",
            args=[
                recipe_id,
            ],
        )
        self.INGREDIENT_FIELDS = ["id", "name", "measurement_unit"]
        self.RECIPE_FIELDS = ["id", "name", "cooking_time", "image"]
