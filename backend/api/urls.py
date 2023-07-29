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

# recipe_urlpatterns = [
# path(
#     "recipes/download_shopping_cart/",
#     views.ShoppingCartViewSet.as_view({"get": "list"}),
#     name="download",
# ),
# path(
#     "recipes/<int:pk>/favorite/",
#     views.DisLikeViewSet.as_view({"post": "create", "delete": "destroy"}),
#     name="dis-like",
# ),
# path(
#     "recipes/<int:pk>/shopping_cart/",
#     views.ShoppingCartViewSet.as_view(
#         {"post": "create", "delete": "destroy"}
#     ),
#     name="add-remove-recipe",
# ),
# ]

auth_urlpatterns = [
    path(
        "auth/token/login/", views.EmailTokenObtainView.as_view(), name="login"
    ),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]


urlpatterns = auth_urlpatterns + router.urls
