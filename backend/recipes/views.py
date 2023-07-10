# Third Party Library
from core.pagination import LimitPageNumberPaginaion
from recipes.models import Recipe, Tag
from recipes.permissions import IsRecipeAuthor
from recipes.serializers import LikeSerializer, RecipeSerializer, TagSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet


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


class DisLikeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]
        recipe = Recipe.objects.get(pk=recipe_id)

        if request.user in recipe.user_likes.all():
            raise ValidationError("You can't like twice!")

        recipe.user_likes.add(request.user)

        serializer = LikeSerializer(recipe)
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
