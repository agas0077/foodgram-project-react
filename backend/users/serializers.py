# Third Party Library
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from users.errors import SELF_SUBSCRIPTION_ERROR, WRONG_EMAIL_CREDENTIAL
from users.models import SubscriberSubscribee

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
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


class MySubscriptionSerializer(UserSerializer):
    """Сериализатор подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("recipes", "recipes_count")

    def get_recipes(self, obj):
        """Получает список рецептов конкретного пользователя."""
        # Импорт здесь из-за циклического импортирования
        # Third Party Library
        from recipes.serializers import MiniRecipeSerializer

        recipes = obj.recipes.all().order_by("-publishing_date")
        recipes_limit = int(
            self.context["request"].query_params.get("recipes_limit")
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
