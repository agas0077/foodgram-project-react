# Third Party Library
from api.errors import (
    ALREADY_IN_SHOPPING_CART_ERROR,
    EMPTY_SHOPPING_CART_ERROR,
    NOT_SUBSCRIBED_ERROR,
    RECIPE_404_IN_SHOPPING_CART_ERROR,
)
from api.filters import RecipeFilter
from api.pagination import LimitPageNumberPaginaion
from api.permissions import RecipePermission
from api.serializers import (
    CustomAuthTokenSerializer,
    CustomUserSerializer,
    IngredientSerializer,
    MiniRecipeSerializer,
    MySubscriptionSerializer,
    RecipeSerializer,
    TagSerializer,
    UnSubScribeSerializer,
)
from api.utils import create_excel_order_list
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import Subscription

User = get_user_model()


class IngredientViewSet(ModelViewSet):
    """Вьюсет для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = [
        "get",
    ]
    permission_classes = [
        AllowAny,
    ]
    filter_backends = [
        SearchFilter,
    ]
    search_fields = [
        "^name",
    ]


class RecipeViewSet(ModelViewSet):
    """Вьюсет рецептов"""

    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = RecipeSerializer
    permission_classes = [
        RecipePermission,
    ]
    pagination_class = LimitPageNumberPaginaion
    queryset = Recipe.objects.all().order_by("-publishing_date")
    filter_backends = [
        RecipeFilter,
    ]

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk):
        user = request.user
        recipe = self.get_queryset().get(pk=pk)

        if request.method.lower() == "delete":
            like_obj = Favorite.objects.filter(user=user, recipe=recipe)
            if like_obj.exists():
                like_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        like_obj, is_created = Favorite.objects.get_or_create(
            user=user, recipe=recipe
        )

        serializer = MiniRecipeSerializer(like_obj.recipe)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, request, pk):
        if request.method.lower() == "delete":
            self._add_remove_shopping_cart("destroy", request, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)

        recipe = self._add_remove_shopping_cart("create", request, pk)
        serializer = MiniRecipeSerializer(instance=recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False)
    def download_shopping_cart(self, request):
        queryset = self.get_queryset().filter(in_shopping_cart=request.user)

        # Если у пользовател, что-то добавлено в корзину, то берутся
        # только нужные элементы
        if queryset.exists():
            queryset = queryset.values(
                "recipe_ingredient_recipe__ingredient__name",
                "recipe_ingredient_recipe__amount",
                "recipe_ingredient_recipe__ingredient__measurement_unit",
            )
        else:
            raise ValidationError(EMPTY_SHOPPING_CART_ERROR)

        return create_excel_order_list(list(queryset))

    def _add_remove_shopping_cart(self, create_or_destroy, request, recipe_id):
        """
        Проверяет, есть ли у текущего пользователя
        в корзине рецепт и добавляет/удаляет его.
        """
        user = request.user
        recipe = get_object_or_404(self.get_queryset(), pk=recipe_id)

        if create_or_destroy == "create":
            if request.user in recipe.in_shopping_cart.all():
                raise ValidationError(ALREADY_IN_SHOPPING_CART_ERROR)

            recipe.in_shopping_cart.add(user)

        elif create_or_destroy == "destroy":
            if request.user not in recipe.in_shopping_cart.all():
                raise ValidationError(RECIPE_404_IN_SHOPPING_CART_ERROR)

            recipe.in_shopping_cart.remove(user)

        return recipe


class TagViewSet(ModelViewSet):
    """Вьюсет тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = [
        "get",
    ]
    permission_classes = [
        AllowAny,
    ]


class EmailTokenObtainView(ObtainAuthToken):
    """Вьюсет получения токена."""

    serializer_class = CustomAuthTokenSerializer
    permission_classes = [
        AllowAny,
    ]
    http_method_names = ["get", "post"]

    def post(self, request, *args, **kwargs):
        """
        Заменяет в ответе поле 'token' на 'auth_token', а
        также статус с 200 на 201.
        """
        response = super().post(request, *args, **kwargs)
        data = {}
        data["auth_token"] = response.data.pop("token")
        return Response(data, status=status.HTTP_201_CREATED)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPaginaion
    lookup_url_kwarg = "pk"
    lookup_field = "pk"
    permission_classes = [
        AllowAny,
    ]

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            user_subscribee__subscriber=request.user.id
        )
        serializer = MySubscriptionSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, pk):
        """
        Использует два разных сериализатора:
        Один для получения запроса с создания подписки,
        второй для возвращения созданного объекта.
        """
        subscriber = request.user
        subscriber_id = subscriber.id
        subscribee = get_object_or_404(User, pk=pk)
        subscribee_id = subscribee.id

        queryset = Subscription.objects.all()

        pair = {
            "subscriber": subscriber_id,
            "subscribee": subscribee_id,
        }

        if request.method.lower() == "delete":
            try:
                queryset.get(**pair).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except queryset.model.DoesNotExist:
                raise ValidationError({"errors": NOT_SUBSCRIBED_ERROR})

        serializer = UnSubScribeSerializer(data=pair)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            headers = self.get_success_headers(serializer.data)

            return_serializer = MySubscriptionSerializer(
                subscribee, context={"request": request}
            )

            return Response(
                return_serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
