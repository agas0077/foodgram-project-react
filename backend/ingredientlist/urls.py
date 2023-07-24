# Third Party Library
from ingredientlist.views import IngredientViewSet
from rest_framework.routers import SimpleRouter

app_name = "ingredientlist"

router = SimpleRouter()
router.register(r"ingredients", IngredientViewSet, basename="ingredientlist")

urlpatterns = [] + router.urls
