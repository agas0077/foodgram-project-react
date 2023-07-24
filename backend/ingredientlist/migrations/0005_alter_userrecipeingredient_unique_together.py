# Generated by Django 4.2.2 on 2023-07-14 18:12

# Third Party Library
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0013_remove_recipe_ingredients"),
        ("ingredientlist", "0004_userrecipeingredient_ingredient"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="userrecipeingredient",
            unique_together={("user", "recipe", "amount")},
        ),
    ]
