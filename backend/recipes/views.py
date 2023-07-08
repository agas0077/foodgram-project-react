# Third Party Library
from recipes.models import Recipe, Tag
from recipes.serializers import RecipeSerializer, RecipeTagSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        request.data["author"] = request.user.id

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super().update(request, *args, **kwargs)
