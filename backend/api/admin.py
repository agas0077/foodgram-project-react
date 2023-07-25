# Third Party Library
from django.contrib import admin
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import SubscriberSubscribee

User = get_user_model()


def custom_titled_filter(title):
    """Создает кастомный фильтр на основе переданного поля."""

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    """Админка модели ингредиентов"""

    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class IngredientRecipeAdmin(admin.ModelAdmin):
    """Админка модели связи рецептов и ингредиентов"""

    list_display = ("recipe", "ingredient", "amount")
    list_filter = ("ingredient__name",)


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    """Админка модели рецептов."""

    list_display = ("author", "name", "user_likes_count")
    list_filter = ("author", "name", "tags")

    def user_likes_count(self, obj):
        return obj.user_likes.count()


class TagAdmin(admin.ModelAdmin):
    """Админка модели тегов."""

    list_display = ("name", "color", "slug")


class UserAdmin(admin.ModelAdmin):
    """Админка модели пользователя."""

    list_display = (
        "username",
        "email",
    )
    list_filter = ("email", "username")


class SubscriberSubscribeeAdmin(admin.ModelAdmin):
    """Админка модели связи подписчиков"""

    SUBSCRIBER_EMAIL_NAME = "Адрес электронной почты того, кто подписывается"
    SUBSCRIBER_USERNAME_NAME = "Ник того, кто подписывается"
    SUBSCRIBEE_EMAIL_NAME = (
        "Адрес электронной почты того, на кого подписываются"
    )
    SUBSCRIBEE_USERNAME_NAME = "Ник того, на кого подписываются"

    list_display = (
        "subscriber",
        "subscribee",
    )
    list_filter = (
        ("subscriber__email", custom_titled_filter(SUBSCRIBER_EMAIL_NAME)),
        (
            "subscriber__username",
            custom_titled_filter(SUBSCRIBER_USERNAME_NAME),
        ),
        ("subscribee__email", custom_titled_filter(SUBSCRIBEE_EMAIL_NAME)),
        (
            "subscribee__username",
            custom_titled_filter(SUBSCRIBEE_USERNAME_NAME),
        ),
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(SubscriberSubscribee, SubscriberSubscribeeAdmin)
