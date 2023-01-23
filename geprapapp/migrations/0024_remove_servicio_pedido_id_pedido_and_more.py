# Generated by Django 4.1 on 2022-11-17 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geprapapp', '0023_usuario_clave_usuario_nombreusuario_usuario_rol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio_pedido',
            name='id_Pedido',
        ),
        migrations.RemoveField(
            model_name='servicio_pedido',
            name='id_servicio',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='clave',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombreUsuario',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.DeleteModel(
            name='Producto_Pedido',
        ),
        migrations.DeleteModel(
            name='Servicio_Pedido',
        ),
    ]