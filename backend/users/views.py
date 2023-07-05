# Third Party Library
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.pagination import LimitPageNumberPaginaion
from users.serializers import CustomAuthTokenSerializer, UserSerializer

User = get_user_model()


class EmailTokenObtainView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
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
        self.serializer_class = super().get_serializer_class()

        if self.request.method == "GET":
            self.serializer_class = UserSerializer

        return self.serializer_class

    def list(self, request, *args, **kwargs):
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
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.id)

        self.check_object_permissions(self.request, obj)

        return obj
