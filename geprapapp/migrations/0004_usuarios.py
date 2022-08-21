# Generated by Django 4.1 on 2022-08-10 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0003_rol_permisos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField()),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.IntegerField(max_length=20)),
                ('direccion', models.CharField(max_length=30)),
                ('correo', models.EmailField(blank=True, max_length=250, null=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='geprapapp.roles')),
            ],
        ),
    ]
