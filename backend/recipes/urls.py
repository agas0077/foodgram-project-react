# Third Party Library
from django.urls import path
from recipes.views import RecipeViewSet
from rest_framework.routers import SimpleRouter

app_name = "recipes"

router = SimpleRouter()
router.register(r"recipes", RecipeViewSet)

urlpatterns = router.urls
