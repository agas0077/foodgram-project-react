# Standard Library
import json

# Third Party Library
from django.core.management.base import BaseCommand
from recipes.models import Tag

from backend.settings import BASE_DIR


class Command(BaseCommand):
    """Пакетная загрузка данных в базу"""

    def handle(self, *args, **kwargs):
        try:
            print(self.load_tags())
        except Exception as error:
            raise Exception(f"Ошибка загрузки {error}")

    def load_tags(self):
        """Пакетная загрузка тегов в БД."""

        if Tag.objects.all().count() != 0:
            return "Tags already exist"

        file_to_load = BASE_DIR.parent / "data" / "tags.json"
        with open(file_to_load, encoding="utf-8") as json_data:
            data = json.load(json_data)

        Tag.objects.bulk_create([Tag(**kwargs) for kwargs in data])
        return "Tags loaded"
