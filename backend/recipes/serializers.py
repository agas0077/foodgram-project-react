# Standard Library
import base64  # Модуль с функциями кодирования и декодирования base64
import uuid

# Third Party Library
from django.core.files.base import ContentFile
from django.shortcuts import get_list_or_404
from recipes.models import Recipe, Tag
from rest_framework import serializers
from rest_framework.serializers import ValidationError


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            filename = str(uuid.uuid4())
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=".".join([filename, ext]))

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)

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
        )
        read_only_fields = (
            "id",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user in obj.user_likes.all():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        return False

    def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data)

        tag_ids_list = self.initial_data.get("tags", [])
        tags = self._check_tags(tag_ids_list)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        tag_ids_list = self.initial_data.get("tags", [])
        tags = self._check_tags(tag_ids_list)
        instance.tags.set(tags)
        return instance

    def _check_tags(self, tag_ids_list):
        valid_tag_ids = []
        invalid_tag_ids = []
        for tag in tag_ids_list:
            if Tag.objects.filter(pk=tag).exists():
                valid_tag_ids.append(tag)
            else:
                invalid_tag_ids.append(tag)
        if invalid_tag_ids:
            raise ValidationError(f"Tag id num {tag} not found!")

        tags = get_list_or_404(Tag, pk__in=valid_tag_ids)
        return tags


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
