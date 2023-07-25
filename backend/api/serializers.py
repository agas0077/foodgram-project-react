# Standard Library
import base64  # Модуль с функциями кодирования и декодирования base64
import uuid

# Third Party Library
from api.errors import (
    SELF_SUBSCRIPTION_ERROR,
    TAG_NOT_FOUND_ERROR,
    WRONG_EMAIL_CREDENTIAL,
)
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_list_or_404
from djoser.serializers import UserCreateSerializer
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from users.models import SubscriberSubscribee

User = get_user_model()


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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Основной серализатор для выдачи всего,
    что связано с ингредиентами и конкретным рецептом.
    """

    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = IngredientRecipe
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


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


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        """
        Возвращает bool если текущий пользователь
        подписан на пользователя obj.
        """
        return obj.user_subscribee.filter(
            subscriber_id=self.context["request"].user.id
        ).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """Основной сериализатор рецептов."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
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


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор инредиентов.
    Обрабатывает ингредиенты при добавлении.
    """

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Кастомизация сериализатора djoser
    для добавления нужных полей в ответ.
    """

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "id",
        )
        read_only_fields = ("id",)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    """
    Кастомизация сериализатора для получения токена
    по email вместо username.
    """

    email = serializers.CharField()
    password = serializers.CharField()
    username = None

    def validate(self, attrs):
        """Ищет пользователя по email и возвращает его username."""
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = User.objects.filter(
                email=email,
            )
            if not user.exists():
                raise ValidationError(WRONG_EMAIL_CREDENTIAL)
            username = user.first().get_username()
            attrs["username"] = username

        return super().validate(attrs)


class MySubscriptionSerializer(CustomUserSerializer):
    """Сериализатор подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )

    def get_recipes(self, obj):
        """Получает список рецептов конкретного пользователя."""
        recipes = obj.recipes.all().order_by("-publishing_date")
        recipes_limit = int(
            self.context["request"].query_params.get("recipes_limit", 999)
        )
        recipes = recipes[:recipes_limit]

        serializer = MiniRecipeSerializer(instance=recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.all().order_by("-publishing_date").count()


class UnSubScribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberSubscribee
        fields = ("subscriber", "subscribee")

    def validate(self, attrs):
        if attrs["subscriber"] == attrs["subscribee"]:
            raise serializers.ValidationError(SELF_SUBSCRIPTION_ERROR)
        return super().validate(attrs)
