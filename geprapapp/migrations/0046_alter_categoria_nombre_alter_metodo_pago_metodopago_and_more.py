# Generated by Django 4.1 on 2022-11-28 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0045_alter_detalle_pedido_id_producto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='metodo_pago',
            name='metodoPago',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=250, unique=True),
        ),
    ]
