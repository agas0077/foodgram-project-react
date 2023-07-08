from rest_framework.viewsets import ModelViewSet
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, RecipeTagSerializer
from rest_framework import status
from rest_framework.response import Response


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ["GET", "POST", "PATCH", "DELETE"]

    def create(self, request, *args, **kwargs):
        recipe_data = {}
        for key, value in request.data.items():
            if key in RecipeSerializer.Meta.fields:
                recipe_data[key] = value
        recipe_serializer = RecipeSerializer(data=recipe_data)
        recipe_serializer.is_valid(raise_exception=True)
        recipe = recipe_serializer.save()
        
        

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)