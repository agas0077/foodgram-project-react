# Third Party Library
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserTestsBaseClass(TestCase):
    ALL_USER_URL = reverse_lazy("users:users")  # /api/users GET POST
    CURRENT_USER_URL = reverse_lazy("users:me")  # /api/users/me
    CHANGE_PASSWORD_URL = reverse_lazy("users:set-password")  # /api/users/set_password
    LOGIN_URL = reverse_lazy("users:login")  # /api/auth/login
    LOGOUT_URL = reverse_lazy("users:logout")  # /api/auth/logout
    ID_USER_URL = reverse_lazy(  # /api/users/1
        "users:user-detail",
        args=[
            1,
        ],
    )
    INVALID_ID_USER_URL = reverse_lazy(  # /api/users/100
        "users:user-detail",
        args=[
            100,
        ],
    )

    FORCE_USER_NAME = "HasNoName"
    FORCE_USER_EMAIL = "force@force.ru"
    FORCE_CURRENT_PASSWORD = "Kalina3333!"
    FORCE_NEW_PASSWORD = "Kalina4444!"

    CHANGE_PASSWORD_DATA = {
        "new_password": FORCE_NEW_PASSWORD,
        "current_password": FORCE_CURRENT_PASSWORD,
    }
    NUM_USERS = 10

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
        self.user = User.objects.create_user(
            username=self.FORCE_USER_NAME,
            password=self.FORCE_CURRENT_PASSWORD,
            email=self.FORCE_USER_EMAIL,
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {"AUTHORIZATION": f"Token {self.token.key}"}
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
