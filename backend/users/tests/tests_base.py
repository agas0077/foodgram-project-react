# Third Party Library
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestsBaseClass(TestCase):
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

    def setUp(self):
        self.guest_client = Client()
        self.force_user = User.objects.create_user(
            username=self.FORCE_USER_NAME,
            password=self.FORCE_CURRENT_PASSWORD,
            email=self.FORCE_USER_EMAIL,
        )

        self.token, _ = Token.objects.get_or_create(user=self.force_user)
        self.auth_headers = {"AUTHORIZATION": f"Token {self.token.key}"}
        self.authorized_client = Client()
        self.authorized_client.force_login(self.force_user)


class UserTestsBaseClass(TestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.ALL_USER_URL = reverse_lazy("users:users")  # /api/users GET POST
        self.CURRENT_USER_URL = reverse_lazy("users:me")  # /api/users/me
        self.CHANGE_PASSWORD_URL = reverse_lazy(
            "users:set-password"
        )  # /api/users/set_password
        self.LOGIN_URL = reverse_lazy("users:login")  # /api/auth/login
        self.LOGOUT_URL = reverse_lazy("users:logout")  # /api/auth/logout
        self.ID_USER_URL = reverse_lazy(  # /api/users/1
            "users:user-detail",
            args=[
                1,
            ],
        )
        self.INVALID_ID_USER_URL = reverse_lazy(  # /api/users/100
            "users:user-detail",
            args=[
                100,
            ],
        )
        self.CHANGE_PASSWORD_DATA = {
            "new_password": self.FORCE_NEW_PASSWORD,
            "current_password": self.FORCE_CURRENT_PASSWORD,
        }
        self.USER_FIELDS = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        self.SIGN_UP_FIELDS = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class SubscriptionTestsBaseClass(TestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.SUBSCRIBE_USER_ID = 2
        self.SUBSCRIBE__INVALID_USER_ID = 200
        self.MY_SUBSCRIPIONS_URL = reverse_lazy("users:my-subscriptions")
        self.UN_SUB_SCRIBE_URL = reverse_lazy(
            "users:un-sub-scribe",
            args=[
                self.SUBSCRIBE_USER_ID,
            ],
        )
        self.UN_SUB_SCRIBE_URL_INVALID_URL = reverse_lazy(
            "users:un-sub-scribe",
            args=[
                self.SUBSCRIBE__INVALID_USER_ID,
            ],
        )
        self.UN_SUBSCRIBE_URLS = {
            "post": self.UN_SUB_SCRIBE_URL,
            "delete": self.UN_SUB_SCRIBE_URL,
        }
        self.UN_SUBSCRIBE_INVALID_URLS = {
            "post": self.UN_SUB_SCRIBE_URL_INVALID_URL,
            "delete": self.UN_SUB_SCRIBE_URL_INVALID_URL,
        }
        self.SUBSCRIPION_FIELDS = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
