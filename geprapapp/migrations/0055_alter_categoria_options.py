# Generated by Django 4.1 on 2023-01-23 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0054_alter_producto_categoria'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
    ]
