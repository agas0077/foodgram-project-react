# Third Party Library
from django.urls import path
from djoser.views import TokenDestroyView, UserViewSet
from users import views

app_name = "users"

urlpatterns = [
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
    path("auth/token/login/", views.EmailTokenObtainView.as_view(), name="login"),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]
