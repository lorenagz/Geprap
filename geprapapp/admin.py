
from django.contrib import admin

from .models import Agenda, Categoria, Detalle_Pedido, Evaluacion, Garantia, Metodo_Pago, Pago, Pedido, Producto, Servicio, Usuario
# Register your models here.
@admin.register(Usuario)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('id','cedula', 'nombre', 'telefono', 'direccion', 'correo', 'nombreUsuario', 'clave', 'rol', )
    search_fields = ['cedula', 'nombre']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'desc')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio', 'categoria')
    search_fields = ['nombre']

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_pedido', 'total', 'usuario', 'estado')

@admin.register(Detalle_Pedido)
class Detalle_PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_pedido', 'id_producto', 'id_servicio', 'cantidad', 'codigoPedido', 'usuario')

    def codigoPedido(self, obj):
        return obj.id_pedido.id

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_asignada', 'pedido')

@admin.register(Metodo_Pago)
class Metodo_PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'metodoPago')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id','plazos', 'pedido', 'formaPago')

@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'fechaGarantia', 'pedido')

@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'calificacionEvaluacion', 'comentarios', 'pedido', 'usuario')


