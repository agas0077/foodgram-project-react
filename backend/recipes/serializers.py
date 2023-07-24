# Standard Library
import base64  # Модуль с функциями кодирования и декодирования base64
import uuid

# Third Party Library
from django.core.files.base import ContentFile
from django.shortcuts import get_list_or_404
from ingredientlist.models import Ingredient, IngredientRecipe
from ingredientlist.serializers import IngredientRecipeSerializer
from recipes.errors import TAG_NOT_FOUND_ERROR
from recipes.models import Recipe, Tag
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    """Преобразование и сохранения файла изображения"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            filename = str(uuid.uuid4())
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=".".join([filename, ext])
            )

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )
        read_only_fields = ("name", "color", "slug")


class RecipeSerializer(serializers.ModelSerializer):
    """Основной сериализатор рецептов."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        source="recipe_ingredient_recipe", many=True, read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            "image",
            "text",
            "name",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
            "author",
            "id",
            "tags",
            "ingredients",
        )
        read_only_fields = (
            "id",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        """Определяет добавлен ли рецепт в избранное у конкретного юзера"""
        user = self.context["request"].user
        if user in obj.user_likes.all():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        """Определяет добавлен ли рецепт в корзину у конкретного юзера"""
        user = self.context["request"].user
        if user in obj.in_shopping_cart.all():
            return True
        return False

    def create(self, validated_data):
        # Создается рецепт по переданным данным
        validated_data["author"] = self.context["request"].user
        recipe = Recipe.objects.create(**validated_data)

        # Из изначальных данных достаются id и amount ингредиентов
        # С помощью доп. функции создаются записи в моделе IngredientRecipe
        ingredients = self.initial_data.pop("ingredients")
        self._add_ingredients(recipe, ingredients)

        # Обнавляется список тегов
        tag_ids_list = self.initial_data.get("tags", [])
        tags = self._check_tags(tag_ids_list)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        validated_data["author"] = self.context["request"].user
        super().update(instance, validated_data)

        # Аналогично create()
        ingredients = self.initial_data.pop("ingredients")
        self._add_ingredients(instance, ingredients, update=True)

        # Аналогично create()
        tag_ids_list = self.initial_data.get("tags", [])
        tags = self._check_tags(tag_ids_list)
        instance.tags.set(tags)
        return instance

    def _check_tags(self, tag_ids_list):
        """
        Разделяет список id тегов на существующие и не существующие.
        Получает список тегов, которые надо добавить к рецепту в связь
        ManyToMany.
        """
        valid_tag_ids = []
        invalid_tag_ids = []
        for tag in tag_ids_list:
            if Tag.objects.filter(pk=tag).exists():
                valid_tag_ids.append(tag)
            else:
                invalid_tag_ids.append(tag)
        if invalid_tag_ids:
            invalid_tag_ids_str = ", ".join(invalid_tag_ids)
            raise ValidationError(TAG_NOT_FOUND_ERROR(invalid_tag_ids_str))

        tags = get_list_or_404(Tag, pk__in=valid_tag_ids)
        return tags

    def _add_ingredients(self, recipe, ingredients, update=False):
        """
        Обновляет список ингредиентов у рецепта.
        Если update == True, то предварительно удаляются старые связи.
        """
        if update:
            IngredientRecipe.objects.filter(recipe=recipe).delete()

        for ingredient in ingredients:
            ingredient = {
                "ingredient": Ingredient.objects.get(pk=ingredient["id"]),
                "recipe": recipe,
                "amount": ingredient["amount"],
            }
            IngredientRecipe.objects.get_or_create(**ingredient)


class MiniRecipeSerializer(serializers.ModelSerializer):
    """Сераилизатор для предоставления урезаной информации о рецепте."""

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
