from pyexpat import model
from turtle import Vec2D
from django.contrib import admin

from .models import Agenda, Categoria, Evaluacion, Factura, Garantia, Metodo_Pago, Pago, Pedido, Permiso, Producto, Producto_Pedido, Rol, Rol_Permiso, Servicio, Servicio_Pedido, Usuario, Venta
# Register your models here.

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Permiso)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Rol_Permiso)
class Rol_PermisosAdmin(admin.ModelAdmin):
    list_display = ('id', 'rol', 'permiso')

@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cedula', 'nombre', 'telefono', 'direccion', 'correo', 'rol')
    search_fields = ['cedula', 'nombre']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio', 'categoria')
    search_fields = ['nombre']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_pedido', 'total', 'usuario')

@admin.register(Producto_Pedido)
class Producto_PedidoAdmin(admin.ModelAdmin):
    list_display = ('id','id_Pedido', 'id_producto', 'cantidad')

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion')

@admin.register(Servicio_Pedido)
class Servicio_PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_Pedido', 'id_servicio')

@admin.register(Venta)
class VentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_Pedido')

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_asignada', 'id_venta')

@admin.register(Metodo_Pago)
class Metodo_PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'metodoPago')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fechaEntregaProducto', 'id_venta')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id','plazos', 'factura', 'formaPago')


@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'fechaGarantia', 'id_venta')

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'calificacionEvaluacion', 'comentarios', 'id_venta')


