# Generated by Django 3.2.6 on 2022-04-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0018_alter_proyecto_valor_proyecto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='valor_proyecto',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
