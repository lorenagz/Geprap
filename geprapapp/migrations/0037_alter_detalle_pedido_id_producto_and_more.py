# Generated by Django 4.1 on 2022-11-17 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0036_detalle_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_pedido',
            name='id_producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='geprapapp.producto'),
        ),
        migrations.AlterField(
            model_name='detalle_pedido',
            name='id_servicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='geprapapp.servicio'),
        ),
    ]