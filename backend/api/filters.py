# Third Party Library
from rest_framework import filters


class RecipeFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        filters = {}
        if request.query_params.get("is_favorited"):
            filters["user_recipe_recipe__user"] = request.user

        tags = request.query_params.getlist("tags")
        if tags:
            filters["tags__slug__in"] = tags

        author_id = request.query_params.get("author")
        if author_id:
            filters["author__id"] = author_id

        if request.query_params.get("is_in_shopping_cart"):
            filters["in_shopping_cart"] = request.user

        queryset = (
            queryset.filter(**filters).order_by("-publishing_date").distinct()
        )

        return queryset
