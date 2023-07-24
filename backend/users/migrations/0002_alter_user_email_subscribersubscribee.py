# Generated by Django 4.2.2 on 2023-07-05 15:19

# Third Party Library
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="email"),
        ),
        migrations.CreateModel(
            name="SubscriberSubscribee",
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
                    "subscribee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_subscribee",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="subscribee",
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_subscriber",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="subscriber",
                    ),
                ),
            ],
        ),
    ]
