# Third Party Library
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # TODO: добавить is_subscribed
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class CustomUserCreateSerializer(UserCreateSerializer):
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
