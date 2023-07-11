# Third Party Library
from django.urls import path
from recipes.views import DisLikeViewSet, RecipeViewSet, TagViewSet
from rest_framework.routers import SimpleRouter

app_name = "recipes"

router = SimpleRouter()
router.register(r"recipes", RecipeViewSet, basename="recipe")
router.register(r"tags", TagViewSet)

urlpatterns = [
    path(
        "recipes/<int:pk>/favorite/",
        DisLikeViewSet.as_view({"post": "create", "delete": "destroy"}),
        name="dis-like",
    ),
]

urlpatterns += router.urls
