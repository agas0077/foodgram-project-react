# Generated by Django 4.2.2 on 2023-07-14 18:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ingredientlist", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserRecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="amount",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_recipe_ingredient_user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user_recipe_ingredient_user",
                    ),
                ),
            ],
        ),
    ]
