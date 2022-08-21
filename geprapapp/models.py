from msilib.schema import Class
from django.db import models

# Create your models here.

class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre}"

class Permiso(models.Model):
    nombre = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.nombre}"

class Rol_Permiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete = models.DO_NOTHING) 
    permiso = models.ForeignKey(Permiso, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.rol}"

class Usuario(models.Model):
    cedula = models.IntegerField()
    nombre = models.CharField(max_length=100)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=30)
    correo = models.EmailField(max_length=250, null=True, blank=True)
    rol = models.ForeignKey(Rol, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.cedula}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"

class Producto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, unique = True)
    descripcion = models.CharField(max_length= 254, null= True, blank=True)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"

class Pedido(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_pedido = models.DateField()
    total = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING )

    def __str__(self):
        return f"{self.id}"

class Producto_Pedido(models.Model):
    id_Pedido =  models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)
    id_producto = models.ForeignKey(Producto, on_delete = models.DO_NOTHING)
    cantidad = models.IntegerField()

class Servicio(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id}"

class Servicio_Pedido(models.Model):
    id_Pedido =  models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)
    id_servicio = models.ForeignKey(Servicio, on_delete = models.DO_NOTHING)
    
class Venta(models.Model):
    id = models.IntegerField(primary_key=True)
    id_Pedido = models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"

class Agenda(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_asignada = models.DateField()
    id_venta = models.ForeignKey(Venta,  on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"

class Metodo_Pago(models.Model):
    metodoPago = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.metodoPago}"

class Factura(models.Model):
    id = models.IntegerField(primary_key=True)
    fechaEntregaProducto = models.DateField()
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"

class Pago(models.Model):
    plazos = models.IntegerField()
    factura = models.ForeignKey(Factura, on_delete=models.DO_NOTHING)
    formaPago = models.ForeignKey(Metodo_Pago, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.plazos}"

class Garantia(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.TextField()
    fechaGarantia = models.DateField()
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"

class Evaluacion(models.Model):
    id = models.IntegerField(primary_key=True)
    calificacionEvaluacion = models.IntegerField()
    comentarios = models.TextField()
    id_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.id}"
