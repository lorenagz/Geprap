# Generated by Django 4.1 on 2022-11-17 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0032_alter_garantia_pedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='id_venta',
        ),
        migrations.AddField(
            model_name='agenda',
            name='pedido',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='geprapapp.pedido'),
        ),
    ]
