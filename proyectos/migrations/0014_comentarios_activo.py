# Generated by Django 3.2.6 on 2022-01-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0013_auto_20220128_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]