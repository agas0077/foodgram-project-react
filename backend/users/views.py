# Third Party Library
from core.pagination import LimitPageNumberPaginaion
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import mixins, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.errors import NOT_SUBSCRIBED_ERROR
from users.models import SubscriberSubscribee
from users.serializers import (
    CustomAuthTokenSerializer,
    MySubscriptionSerializer,
    UnSubScribeSerializer,
    UserSerializer,
)

User = get_user_model()


class EmailTokenObtainView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        """
        Redefine response 'token' to 'auth_token'.
        Change response status 200 to 201.
        """
        response = super().post(request, *args, **kwargs)
        data = {}
        data["auth_token"] = response.data.pop("token")
        return Response(data, status=status.HTTP_201_CREATED)


class ListCreateUserDjoserCustomViewSet(UserViewSet):
    http_method_names = ["post", "get"]
    permission_classes = [
        AllowAny,
    ]
    pagination_class = LimitPageNumberPaginaion

    def get_serializer_class(self):
        """Add special serializer for djoser custom list method."""
        self.serializer_class = super().get_serializer_class()

        if self.request.method == "GET":
            self.serializer_class = UserSerializer

        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        Add special method to list all users overriding djoser
        filtered method.
        """
        queryset = User.objects.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveUserByIdViewSet(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "pk"
    lookup_field = "pk"


class RetrieveUserViewSet(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        """Search for a particular user by its pk."""
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.id)

        self.check_object_permissions(self.request, obj)

        return obj


class ListSubscriptionsViewSet(ListAPIView):
    serializer_class = MySubscriptionSerializer
    pagination_class = LimitPageNumberPaginaion

    def get_queryset(self):
        queryset = User.objects.filter(user_subscribee__subscriber=self.request.user.id)
        return queryset


class UnSubScribeViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet
):
    queryset = SubscriberSubscribee.objects.all()

    def get_object(self):
        """Get necessary subscription for delete method."""
        subscriber_id = self.request.user.id
        subscribee_id = get_object_or_404(User, pk=self.kwargs["pk"])
        queryset = self.get_queryset()
        try:
            obj = queryset.get(subscriber=subscriber_id, subscribee=subscribee_id)
        except queryset.model.DoesNotExist:
            raise ValidationError({"errors": NOT_SUBSCRIBED_ERROR})
        return obj

    def create(self, request, *args, **kwargs):
        """
        Use two different serializers:
        one to get request and create a model record (i.e. subscription)
        and another one to return the user object.
        """
        subscribee = get_object_or_404(User, pk=kwargs["pk"])
        initial_data = {
            "subscriber": request.user.id,
            "subscribee": subscribee.id,
        }
        get_serializer = UnSubScribeSerializer(data=initial_data)
        get_serializer.is_valid(raise_exception=True)
        self.perform_create(get_serializer)
        headers = self.get_success_headers(get_serializer.data)

        return_serializer = MySubscriptionSerializer(
            subscribee, context={"request": request}
        )

        return Response(
            return_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
