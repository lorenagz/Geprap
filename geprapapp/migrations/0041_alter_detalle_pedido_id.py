# Generated by Django 4.1 on 2022-11-28 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0040_pedido_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_pedido',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
