# Third Party Library
from core.tests_base import TestsBaseClass
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class UserTestsBaseClass(TestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        # /api/users GET POST
        self.ALL_USER_URL = reverse_lazy("users:users")
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
