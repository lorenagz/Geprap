# Generated by Django 4.1 on 2022-11-17 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0027_remove_evaluacion_id_venta_remove_garantia_id_venta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='geprapapp.usuario'),
        ),
    ]