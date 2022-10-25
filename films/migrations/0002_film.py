# Generated by Django 4.1.2 on 2022-10-25 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Film",
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
                ("name", models.CharField(max_length=128, unique=True)),
                (
                    "users",
                    models.ManyToManyField(
                        related_name="films", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
