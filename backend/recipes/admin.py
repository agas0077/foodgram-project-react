# Third Party Library
from django.contrib import admin
from recipes.models import Recipe, RecipeTag, Tag


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "text")


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")


class RecipeTagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
