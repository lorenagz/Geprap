# Generated by Django 4.1 on 2023-01-22 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0053_alter_detalle_pedido_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geprapapp.categoria'),
        ),
    ]