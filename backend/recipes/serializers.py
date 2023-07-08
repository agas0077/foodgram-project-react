from rest_framework import serializers
from recipes.models import Recipe, Tag, RecipeTag


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("image", "text", "name", "cooking_time")
        readread_only_fields = (
            "id",
            "recipe_author",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
