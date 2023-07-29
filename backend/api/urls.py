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

auth_urlpatterns = [
    path(
        "auth/token/login/", views.EmailTokenObtainView.as_view(), name="login"
    ),
    path("auth/token/logout/", TokenDestroyView.as_view(), name="logout"),
]


urlpatterns = auth_urlpatterns + router.urls
