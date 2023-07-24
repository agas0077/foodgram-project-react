# Generated by Django 4.2.2 on 2023-07-18 18:56

# Third Party Library
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0013_remove_recipe_ingredients"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="shopping_cart",
        ),
        migrations.AddField(
            model_name="recipe",
            name="in_shopping_cart",
            field=models.ManyToManyField(
                blank=True,
                related_name="in_shopping_cart",
                to=settings.AUTH_USER_MODEL,
                verbose_name="В корзине",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Время приготовления",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                upload_to="recipe_image/", verbose_name="Изображение"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Название рецепта"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="publishing_date",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Дата публикации рецепта"
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="recipe_list",
                to="recipes.tag",
                verbose_name="Теги",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="text",
            field=models.TextField(verbose_name="Описание рецепта"),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="user_likes",
            field=models.ManyToManyField(
                blank=True,
                related_name="recipe_like_list",
                to=settings.AUTH_USER_MODEL,
                verbose_name="В избранном",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                max_length=7,
                validators=[
                    django.core.validators.RegexValidator(
                        "^#[A-Z0-9]+$", "Check you HEX code"
                    )
                ],
                verbose_name="HEX-код цвета тега",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Тег"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.CharField(
                max_length=200,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[-a-zA-Z0-9_]+$",
                        "Your slug must contain only letters, digits or _ and -",
                    )
                ],
                verbose_name="Название-слаг тега",
            ),
        ),
    ]