# Third Party Library
from core.pagination import LimitPageNumberPaginaion
from recipes.models import Recipe, Tag
from recipes.permissions import IsRecipeAuthor
from recipes.serializers import (
    MiniRecipeSerializer,
    RecipeSerializer,
    TagSerializer,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class RecipeViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = RecipeSerializer
    permission_classes = [IsRecipeAuthor, IsAuthenticated]
    pagination_class = LimitPageNumberPaginaion

    def get_queryset(self):
        filters = {}
        if self.request.query_params.get("is_favorited"):
            filters["user_likes"] = self.request.user

        tags = self.request.query_params.getlist("tags")
        if tags:
            filters["tags__slug__in"] = tags

        queryset = (
            Recipe.objects.filter(**filters)
            .order_by("-publishing_date")
            .distinct()
        )
        return queryset

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
    permission_classes = [
        AllowAny,
    ]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DisLikeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]
        recipe = Recipe.objects.get(pk=recipe_id)

        if request.user in recipe.user_likes.all():
            raise ValidationError("You can't like twice!")

        recipe.user_likes.add(request.user)

        serializer = MiniRecipeSerializer(recipe)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]
        recipe = Recipe.objects.get(pk=recipe_id)

        if request.user not in recipe.user_likes.all():
            raise ValidationError("You didn't like the recipe!")

        recipe.user_likes.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
