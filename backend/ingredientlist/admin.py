# Third Party Library
from django.contrib import admin
from ingredientlist.models import Ingredient, IngredientRecipe


# Register your models here.
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ("recipe", "amount")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
