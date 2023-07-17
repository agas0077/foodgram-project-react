# Third Party Library
from core.tests_base import TestsBaseClass
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class RecipeTestsBaseClass(TestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.RECIPES_ALL = reverse_lazy("recipes:recipe-list")
        self.RECIPES_DETAIL = reverse_lazy("recipes:recipe-detail")
        self.RECIPES_DETAIL_ID = reverse_lazy(
            "recipes:recipe-detail",
            args=[
                1,
            ],
        )
        self.RECIPES_DETAIL_ID_INVALID = reverse_lazy(
            "recipes:recipe-detail",
            args=[
                100,
            ],
        )

        self.RECIPE_FIELDS = list(self.RECIPE_DATA.keys()) + [
            "author",
            "is_favorited",
            "is_in_shopping_cart",
            "id",
        ]

    def _create_recipe_and_get_url(self):
        response = self.client.post(
            self.RECIPES_ALL, data=self.RECIPE_DATA, headers=self.auth_headers
        )
        id = response.data.get("id")
        url = reverse_lazy(
            "recipes:recipe-detail",
            args=[
                id,
            ],
        )
        return id, url


class TagTestsBaseClass(TestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.ALL_TAGS_URL = reverse_lazy("recipes:tag-list")
        self.TAG_ID_URL = reverse_lazy(
            "recipes:tag-detail",
            args=[
                1,
            ],
        )
        self.TAG_ID_URL_INVALID = reverse_lazy(
            "recipes:tag-detail",
            args=[
                100,
            ],
        )
        self.TAGS_FIELDS = ["name", "color", "slug"]


class LikeTestsBaseClass(RecipeTestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.LIKE_ID_URL = reverse_lazy(
            "recipes:dis-like",
            args=[
                1,
            ],
        )
        self.LIKE_FIELDS = ["id", "name", "image", "cooking_time"]
