# Generated by Django 5.0.1 on 2024-01-20 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
