# Generated by Django 4.2.2 on 2023-07-14 18:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0012_recipe_shopping_cart"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="ingredients",
        ),
    ]
