# Generated by Django 4.1 on 2022-08-21 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0016_rename_permisos_permiso_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('calificacionEvaluacion', models.IntegerField()),
                ('comentarios', models.TextField()),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='geprapapp.venta')),
            ],
        ),
    ]
