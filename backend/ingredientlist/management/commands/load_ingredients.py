# Standard Library
import json

# Third Party Library
from django.core.management.base import BaseCommand
from ingredientlist.models import Ingredient

from backend.settings import BASE_DIR


class Command(BaseCommand):
    """Пакетная загрузка данных в базу"""

    def handle(self, *args, **kwargs):
        try:
            print(self.load_ingredients())
        except Exception as error:
            raise Exception(f"Ошибка загрузки {error}")

    def load_ingredients(self):
        file_to_load = BASE_DIR.parent / "data" / "ingredients.json"
        with open(file_to_load, encoding="utf-8") as json_data:
            data = json.load(json_data)

        Ingredient.objects.bulk_create([Ingredient(**kwargs) for kwargs in data])
        return "Ingredients loaded"
