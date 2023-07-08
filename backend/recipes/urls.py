# Third Party Library
from django.urls import path
from rest_framework.routers import SimpleRouter


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls

app_name = "recipes"

urlpatterns = []
