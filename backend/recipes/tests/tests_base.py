# Third Party Library
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse_lazy
from recipes.models import Tag
from rest_framework.authtoken.models import Token

User = get_user_model()


class RecipeTestsBaseClass(TestCase):
    FORCE_USER_NAME = "HasNoName"
    FORCE_USER_EMAIL = "force@force.ru"
    FORCE_CURRENT_PASSWORD = "Kalina3333!"
    FORCE_NEW_PASSWORD = "Kalina4444!"

    NUM_USERS = 10

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.FORCE_USER_NAME = "HasNoName"
        self.FORCE_USER_EMAIL = "force@force.ru"
        self.FORCE_CURRENT_PASSWORD = "Kalina3333!"
        self.FORCE_NEW_PASSWORD = "Kalina4444!"
        self.PAGINATION_FIELDS = (
            "count",
            "next",
            "previous",
            "results",
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        for i in range(0, cls.NUM_USERS):
            User.objects.create(
                email=f"aaa{i}@aaa.ert",
                username=f"username_{i}",
                first_name=f"name_{i}",
                last_name=f"ln_{i}",
                password="Kalina3333!",
            )
        User.objects.create_user(
            username=cls.FORCE_USER_NAME,
            password=cls.FORCE_CURRENT_PASSWORD,
            email=cls.FORCE_USER_EMAIL,
        )
        Tag.objects.bulk_create(
            [
                {"name": "White", "color": "#FFFFFF", "slug": "white"},
                {"name": "Black", "color": "#000000", "slug": "black"},
            ]
        )

    def setUp(self):
        self.client = Client()
        self.force_user = User.objects.get(username=self.FORCE_USER_NAME)
        self.token, _ = Token.objects.get_or_create(user=self.force_user)
        self.auth_headers = {"AUTHORIZATION": f"Token {self.token.key}"}


class RecipeTestsBaseClass(RecipeTestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.RECIPES_ALL = reverse_lazy("recipes:recipes:recipe-list")
        self.RECIPES_DETAIL = reverse_lazy("recipes:recipes:recipe-detail")
        self.RECIPES_DETAIL_ID = reverse_lazy(
            "recipes:recipes:recipe-detail",
            args=[
                1,
            ],
        )
        self.RECIPES_DETAIL_ID_INVALID = reverse_lazy(
            "recipes:recipes:recipe-detail",
            args=[
                100,
            ],
        )
