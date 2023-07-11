# Third Party Library
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from users.models import SubscriberSubscribee

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Custom djoser serializer to add necessary fields to response."""

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
    email = serializers.CharField()
    password = serializers.CharField()
    username = None

    def validate(self, attrs):
        """Search for user by given email and return username instead."""
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = get_object_or_404(
                User,
                email=email,
            )

            username = user.get_username()
            attrs["username"] = username

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    """General user serializer."""

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
        return obj.user_subscribee.filter(
            subscriber_id=self.context["request"].user.id
        ).exists()


class MySubscriptionSerializer(UserSerializer):
    """
    Serializer for subscriptions.
    Add recepes list and recipes_count
    """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("recipes", "recipes_count")

    def get_recipes(self, obj):
        # Third Party Library
        from recipes.serializers import MiniRecipeSerializer

        serializer = MiniRecipeSerializer(instance=obj.recipe.all(), many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe.all().count()


class UnSubScribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberSubscribee
        fields = "__all__"

    def validate(self, attrs):
        if attrs["subscriber"] == attrs["subscribee"]:
            raise serializers.ValidationError(
                "You cannot subscriber to yourself!"
            )
        return super().validate(attrs)
