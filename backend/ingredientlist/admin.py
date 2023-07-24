# Third Party Library
from django.contrib import admin
from ingredientlist.models import Ingredient, IngredientRecipe


# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    """Админка модели ингредиентов"""

    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class IngredientRecipeAdmin(admin.ModelAdmin):
    """Админка модели связи рецептов и ингредиентов"""

    list_display = ("recipe", "ingredient", "amount")
    list_filter = ("ingredient__name",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
