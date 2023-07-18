# Standard Library
import os
import uuid

# Third Party Library
from core.pagination import LimitPageNumberPaginaion
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from ingredientlist.models import (
    AMOUNT_NAME,
    INGREDIENT_NAME_NAME,
    MEASUREMENT_UNIT_NAME,
    IngredientRecipe,
)
import pandas as pd
from recipes.errors import (
    ALREADY_IN_SHOPPING_CART_ERROR,
    EMPTY_SHOPPING_CART_ERROR,
    NO_LIKE_ERROR,
    RECIPE_404_IN_SHOPPING_CART,
    SECOND_LIKE_ERROR,
)
from recipes.models import Recipe, Tag
from recipes.permissions import IsRecipeAuthor
from recipes.serializers import (
    MiniRecipeSerializer,
    RecipeSerializer,
    TagSerializer,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet


class CustomFileResponse(FileResponse):
    """Removes the shopping cart file after the file is sent"""

    def close(self) -> None:
        super().close()
        file = os.path.join(settings.SHOPPING_CART_ROOT, self.filename)
        os.remove(file)


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
            Recipe.objects.filter(**filters).order_by("-publishing_date").distinct()
        )

        return queryset

    def create(self, request, *args, **kwargs):
        # If method == POST, one can't change request data
        # (need to switch _mutable)
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


class DisLikeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Recipe.objects.all()

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]
        recipe = self.get_queryset().get(pk=recipe_id)

        if request.user in recipe.user_likes.all():
            raise ValidationError(SECOND_LIKE_ERROR)

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
        recipe = self.get_queryset().get(pk=recipe_id)

        if request.user not in recipe.user_likes.all():
            raise ValidationError(NO_LIKE_ERROR)

        recipe.user_likes.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(
    RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    def get_queryset(self):
        if self.request.method.lower() == "get":
            return IngredientRecipe.objects.all()
        else:
            return Recipe.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = (
            self.get_queryset()
            .filter(recipe__in_shopping_cart=request.user)
            .values("ingredient__name", "amount", "ingredient__measurement_unit")
        )

        if not queryset.exists():
            raise ValidationError(EMPTY_SHOPPING_CART_ERROR)

        # Create dataframe with required ingredients
        df = pd.DataFrame(list(queryset))
        columns = [INGREDIENT_NAME_NAME, AMOUNT_NAME, MEASUREMENT_UNIT_NAME]
        df.columns = columns
        # Aggregating repeating ingredients
        df = df.pivot_table(
            values=AMOUNT_NAME,
            index=[INGREDIENT_NAME_NAME, MEASUREMENT_UNIT_NAME],
            aggfunc=sum,
        ).reset_index()
        df = df[columns]

        hash = str(uuid.uuid4())
        file_name = f"Список ингредиентов_{hash}.xlsx"
        temp_file_save_path = os.path.join(settings.SHOPPING_CART_ROOT, file_name)
        if not os.path.isdir(settings.SHOPPING_CART_ROOT):
            os.mkdir(settings.SHOPPING_CART_ROOT)

        df.to_excel(temp_file_save_path, index=False)

        fs = FileSystemStorage(settings.SHOPPING_CART_ROOT)
        response = CustomFileResponse(
            fs.open(file_name, "rb"),
            content_type="application/force-download",
            filename=file_name,
        )
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        # os.remove(temp_file_save_path)
        return response

    def create(self, request, *args, **kwargs):
        recipe = self._create_or_destroy("create", request, *args, **kwargs)
        serializer = MiniRecipeSerializer(instance=recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        self._create_or_destroy("destroy", request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _create_or_destroy(self, create_or_destroy, request, *args, **kwargs):
        recipe_id = kwargs.get("pk")
        user = request.user
        recipe = get_object_or_404(self.get_queryset(), pk=recipe_id)

        if create_or_destroy == "create":
            if request.user in recipe.in_shopping_cart.all():
                raise ValidationError(ALREADY_IN_SHOPPING_CART_ERROR)

            recipe.in_shopping_cart.add(user)

        elif create_or_destroy == "destroy":
            if request.user not in recipe.in_shopping_cart.all():
                raise ValidationError(RECIPE_404_IN_SHOPPING_CART)

            recipe.in_shopping_cart.remove(user)

        return recipe
