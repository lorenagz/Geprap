# Generated by Django 4.1 on 2022-11-29 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0050_alter_usuario_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('A', 'Administrador'), ('O', 'Operario'), ('C', 'Cliente'), ('I', 'Instalador')], max_length=100),
        ),
    ]
