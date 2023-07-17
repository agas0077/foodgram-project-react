# Third Party Library
from django.urls import path
from recipes import views
from rest_framework.routers import SimpleRouter

app_name = "recipes"

router = SimpleRouter()
router.register(r"recipes", views.RecipeViewSet, basename="recipe")
router.register(r"tags", views.TagViewSet)

urlpatterns = [
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
    path(
        "recipey/download_shopping_cart/",
        views.ShoppingCartViewSet.as_view({"get": "retrieve"}),
        name="download",
    ),
]

urlpatterns += router.urls
