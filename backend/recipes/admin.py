# Third Party Library
from django.contrib import admin
from recipes.models import Recipe, Tag


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "user_likes_count")
    list_filter = ("author", "name", "tags")

    def user_likes_count(self, obj):
        return obj.user_likes.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "slug")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
