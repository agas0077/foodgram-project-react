# Third Party Library
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


# Create your models here.
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Author",
    )
    name = models.CharField(verbose_name="Recipe name", max_length=200)
    image = models.ImageField(
        "Image",
        upload_to="recipe_image/",
    )
    text = models.TextField("Recipe text")
    cooking_time = models.IntegerField(
        verbose_name="Cooking time",
        validators=[
            MinValueValidator(1),
        ],
    )
    tags = models.ManyToManyField(
        "Tag",
        verbose_name="Tag",
        related_name="recipe_list",
        blank=True,
    )
    user_likes = models.ManyToManyField(
        User,
        verbose_name="Like",
        related_name="recipe_like_list",
        blank=True,
    )
    publishing_date = models.DateTimeField(
        verbose_name="publishing_date", auto_now_add=True
    )
    shopping_cart = models.ManyToManyField(
        User,
        related_name="shopping_cart",
        verbose_name="shopping_cart",
        blank=True,
    )

    def __str__(self) -> str:
        return "-".join([self.name, str(self.pk)])


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag name", max_length=200)
    color = models.CharField(
        verbose_name="Tag color",
        max_length=7,
        validators=[
            RegexValidator(r"^#[A-Z0-9]+$", "Check you HEX code"),
        ],
    )
    slug = models.CharField(
        verbose_name="Tag slug",
        max_length=200,
        validators=[
            RegexValidator(
                r"^[-a-zA-Z0-9_]+$",
                "Your slug must contain only letters, digits or _ and -",
            ),
        ],
    )

    def __str__(self) -> str:
        return self.name
