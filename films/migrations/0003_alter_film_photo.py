# Generated by Django 4.1.2 on 2022-10-27 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("films", "0002_film_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="film",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="film_photos/"),
        ),
    ]