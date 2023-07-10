# Third Party Library
from django.urls import path
from recipes.views import RecipeViewSet, TagViewSet
from rest_framework.routers import SimpleRouter

app_name = "recipes"

router = SimpleRouter()
router.register(r"recipes", RecipeViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = router.urls
