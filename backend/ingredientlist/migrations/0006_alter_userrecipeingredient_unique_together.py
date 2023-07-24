# Generated by Django 4.2.2 on 2023-07-14 18:13

# Third Party Library
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0013_remove_recipe_ingredients"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ingredientlist", "0005_alter_userrecipeingredient_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="userrecipeingredient",
            unique_together={("user", "recipe", "ingredient")},
        ),
    ]