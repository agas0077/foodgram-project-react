# Third Party Library
from core.pagination import LimitPageNumberPaginaion
from recipes.models import Recipe, Tag
from recipes.permissions import IsRecipeAuthor
from recipes.serializers import (
    RecipeSerializer,
    RecipeTagSerializer,
    TagSerializer,
)
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = RecipeSerializer
    permission_classes = [IsRecipeAuthor, IsAuthenticated]
    pagination_class = LimitPageNumberPaginaion

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.id
        request.POST._mutable = False
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super().update(request, *args, **kwargs)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = [
        "get",
    ]
