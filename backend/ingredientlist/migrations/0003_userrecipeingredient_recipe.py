# Generated by Django 4.2.2 on 2023-07-14 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0013_remove_recipe_ingredients"),
        ("ingredientlist", "0002_userrecipeingredient"),
    ]

    operations = [
        migrations.AddField(
            model_name="userrecipeingredient",
            name="recipe",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="user_recipe_ingredient_recipe",
                to="recipes.recipe",
                verbose_name="user_recipe_ingredient_recipe",
            ),
            preserve_default=False,
        ),
    ]
