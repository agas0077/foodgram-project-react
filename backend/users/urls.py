# Third Party Library
from django.urls import path
from djoser.views import TokenDestroyView, UserViewSet
from users import views

app_name = "users"

users_urlpatterns = [
    path(
        "users/set_password/",
        UserViewSet.as_view({"post": "set_password"}),
        name="set-password",
    ),
    path(
        "users/<int:pk>/",
        views.RetrieveUserByIdViewSet.as_view(),
        name="user-detail",
    ),
    path("users/me/", views.RetrieveUserViewSet.as_view(), name="me"),
    path(
        "users/",
        views.ListCreateUserDjoserCustomViewSet.as_view(
            {"post": "create", "get": "list"}
        ),
        name="users",
    ),
]

auth_urlpatterns = [
    path(
        "auth/token/login/", views.EmailTokenObtainView.as_view(), name="login"
    ),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]

subscripions_urlpatterns = [
    path(
        "users/subscriptions/",
        views.ListSubscriptionsViewSet.as_view(),
        name="my-subscriptions",
    ),
    path(
        "users/<int:pk>/subscribe/",
        views.UnSubScribeViewSet.as_view(
            {"post": "create", "delete": "destroy"}
        ),
        name="un-sub-scribe",
    ),
]

urlpatterns = users_urlpatterns + auth_urlpatterns + subscripions_urlpatterns
