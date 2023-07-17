# Generated by Django 4.2.2 on 2023-07-14 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ingredientlist", "0001_initial"),
        ("recipes", "0009_alter_recipe_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="recipes",
                to="ingredientlist.ingredient",
                verbose_name="ingredient list",
            ),
            preserve_default=False,
        ),
    ]
