# Generated by Django 4.1 on 2022-09-12 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0017_evaluacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto_pedido',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='servicio_pedido',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
