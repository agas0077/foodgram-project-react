# Standard Library
import io

# Third Party Library
from api.errors import (
    ALREADY_IN_SHOPPING_CART_ERROR,
    EMPTY_SHOPPING_CART_ERROR,
    NO_LIKE_ERROR,
    NOT_SUBSCRIBED_ERROR,
    RECIPE_404_IN_SHOPPING_CART_ERROR,
    SECOND_LIKE_ERROR,
)
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
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
import pandas as pd
from recipes.models import (
    AMOUNT_NAME,
    INGREDIENT_NAME_NAME,
    MEASUREMENT_UNIT_NAME,
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag,
)
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from users.models import SubscriberSubscribee

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

    def get_queryset(self):
        """
        Создает queryset с учетом фильтрации п
        о параметрам переданным в query string
        """
        filters = {}
        if self.request.query_params.get("is_favorited"):
            filters["user_likes"] = self.request.user

        tags = self.request.query_params.getlist("tags")
        if tags:
            filters["tags__slug__in"] = tags

        author_id = self.request.query_params.get("author")
        if author_id:
            filters["author__id"] = author_id

        if self.request.query_params.get("is_in_shopping_cart"):
            filters["in_shopping_cart"] = self.request.user

        queryset = (
            Recipe.objects.filter(**filters)
            .order_by("-publishing_date")
            .distinct()
        )

        return queryset


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


class DisLikeViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """Вьюсет создает и убирает лайки с постов."""

    queryset = Recipe.objects.all().order_by("-publishing_date")

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]
        recipe = self.get_queryset().get(pk=recipe_id)

        if request.user in recipe.user_likes.all():
            raise ValidationError(SECOND_LIKE_ERROR)

        recipe.user_likes.add(request.user)

        serializer = MiniRecipeSerializer(recipe)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        recipe_id = kwargs["pk"]
        recipe = self.get_queryset().get(pk=recipe_id)

        if request.user not in recipe.user_likes.all():
            raise ValidationError(NO_LIKE_ERROR)

        recipe.user_likes.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    """
    Вьюсет добавления или удаления рецепта из списка покупок,
    а также получения выгрузки списка покупок.
    """

    def get_queryset(self):
        if self.request.method.lower() == "get":
            return IngredientRecipe.objects.all()
        else:
            return Recipe.objects.all().order_by("-publishing_date")

    def list(self, request, *args, **kwargs):
        """Функция выгрузки списка покупок в формате xlsx"""
        queryset = self.get_queryset().filter(
            recipe__in_shopping_cart=request.user
        )

        # Если у пользовател, что-то добавлено в корзину, то берутся
        # только нужные элементы
        if queryset.exists():
            queryset = queryset.values(
                "ingredient__name", "amount", "ingredient__measurement_unit"
            )
        else:
            raise ValidationError(EMPTY_SHOPPING_CART_ERROR)

        # Создаем датафрейм и переименовываем столбцы
        df = pd.DataFrame(list(queryset))
        columns = [INGREDIENT_NAME_NAME, AMOUNT_NAME, MEASUREMENT_UNIT_NAME]
        df.columns = columns

        # Создаем сводную таблицу, чтобы сумировать объем необходимых
        # ингредиентов
        df = df.pivot_table(
            values=AMOUNT_NAME,
            index=[INGREDIENT_NAME_NAME, MEASUREMENT_UNIT_NAME],
            aggfunc=sum,
        ).reset_index()
        df = df[columns]

        # Отправляем файл
        file_name = "Ingredients.xlsx"

        with io.BytesIO() as b:
            with pd.ExcelWriter(b) as writer:
                df.to_excel(writer, index=False)

            response = HttpResponse(
                b.getvalue(),
                content_type=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                ),
            )
            response[
                "Content-Disposition"
            ] = f"attachment; filename={file_name}"
            return response

    def create(self, request, *args, **kwargs):
        recipe = self._create_or_destroy("create", request, *args, **kwargs)
        serializer = MiniRecipeSerializer(instance=recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        self._create_or_destroy("destroy", request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _create_or_destroy(self, create_or_destroy, request, *args, **kwargs):
        """
        Проверяет, есть ли у текущего пользователя
        в корзине рецепт и добавляет/удаляет его.
        """
        recipe_id = kwargs.get("pk")
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
    def subscribe(self, request, pk=None):
        """
        Использует два разных сериализатора:
        Один для получения запроса с создания подписки,
        второй для возвращения созданного объекта.
        """
        subscriber = request.user
        subscriber_id = subscriber.id
        subscribee = get_object_or_404(User, pk=self.kwargs["pk"])
        subscribee_id = subscribee.id

        queryset = SubscriberSubscribee.objects.all()

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
