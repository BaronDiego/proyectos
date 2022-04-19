# Generated by Django 3.2.6 on 2021-10-20 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0006_alter_bibliotecaproyecto_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProyectoMacro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(verbose_name='Descripción')),
            ],
        ),
        migrations.AlterModelOptions(
            name='bibliotecaproyecto',
            options={'ordering': ['-creado']},
        ),
        migrations.AddField(
            model_name='proyecto',
            name='proyecto_macro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyectomacro'),
        ),
    ]