# Third Party Library
from api import views
from django.urls import path
from djoser.views import TokenDestroyView
from rest_framework.routers import SimpleRouter

app_name = "api"

router = SimpleRouter()

router.register(
    r"ingredients", views.IngredientViewSet, basename="ingredientlist"
)
router.register(r"recipes", views.RecipeViewSet, basename="recipe")
router.register(r"tags", views.TagViewSet)

router.register("users", views.CustomUserViewSet)

recipe_urlpatterns = [
    path(
        "recipes/download_shopping_cart/",
        views.ShoppingCartViewSet.as_view({"get": "list"}),
        name="download",
    ),
    path(
        "recipes/<int:pk>/favorite/",
        views.DisLikeViewSet.as_view({"post": "create", "delete": "destroy"}),
        name="dis-like",
    ),
    path(
        "recipes/<int:pk>/shopping_cart/",
        views.ShoppingCartViewSet.as_view(
            {"post": "create", "delete": "destroy"}
        ),
        name="add-remove-recipe",
    ),
]

# users_urlpatterns = [
#     path(
#         "users/set_password/",
#         UserViewSet.as_view({"post": "set_password"}),
#         name="set-password",
#     ),
#     path(
#         "users/<int:pk>/",
#         views.RetrieveUserByIdViewSet.as_view(),
#         name="user-detail",
#     ),
#     path("users/me/", views.RetrieveUserViewSet.as_view(), name="me"),
#     path(
#         "users/",
#         views.ListCreateUserDjoserCustomViewSet.as_view(
#             {"post": "create", "get": "list"}
#         ),
#         name="users",
#     ),
# ]

auth_urlpatterns = [
    path(
        "auth/token/login/", views.EmailTokenObtainView.as_view(), name="login"
    ),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]

# subscripions_urlpatterns = [
#     path(
#         "users/subscriptions/",
#         views.ListSubscriptionsViewSet.as_view(),
#         name="my-subscriptions",
#     ),
#     path(
#         "users/<int:pk>/subscribe/",
#         views.UnSubScribeViewSet.as_view(
#             {"post": "create", "delete": "destroy"}
#         ),
#         name="un-sub-scribe",
#     ),
# ]

urlpatterns = (
    recipe_urlpatterns
    # + users_urlpatterns
    + auth_urlpatterns
    # + subscripions_urlpatterns
    + router.urls
)
