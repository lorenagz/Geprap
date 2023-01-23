from django.core.serializers import serialize
from django.db import models


class Usuario(models.Model):
    """Módulo que contiene los campos necesarios para los registros de los usuarios
    """
    cedula = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=30)
    correo = models.EmailField(max_length=250, unique=True)
    nombreUsuario = models.CharField(max_length=100,  unique=True)
    clave = models.CharField(max_length=254)
    ROLES = (
        ('A', 'Administrador'),
        ('O', 'Operario'),
        ('C', 'Cliente'),
        ('I', 'Instalador')
    )

    rol = models.CharField(max_length=100, choices=ROLES)

    def __str__(self):
        return f"{self.cedula} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        #Cifrado de claves
        from .crypt import claveEncriptada
        
        """if self.clave != "":
            anterior = self.clave
            encriptada = claveEncriptada(kwargs["id_clave"])
            if anterior == encriptada:
                print("Update: permace la misma clave")
            else:
                print("Update:cambio de clave")
                self.clave = claveEncriptada(kwargs["id_clave"])
        else:
            print("nuevo trabajdor")"""
        self.clave = claveEncriptada(self.clave)
        super(Usuario, self).save(*args, **kwargs)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, null= True, blank=True)
    
    
    class Meta:
        verbose_name= "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique = True)
    descripcion = models.CharField(max_length= 254, null= True, blank=True)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.nombre}"

class Servicio(models.Model):
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.descripcion}"

class Pedido(models.Model):
    fecha_pedido = models.DateField()
    total = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING)
    estado = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.usuario}"

class Detalle_Pedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)
    id_producto = models.ForeignKey(Producto, null=True, blank=True, on_delete = models.DO_NOTHING )
    id_servicio = models.ForeignKey(Servicio, null=True, blank=True, on_delete = models.DO_NOTHING )
    cantidad = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.id_pedido}"

class Agenda(models.Model):
    fecha_asignada = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete = models.DO_NOTHING)

    def __str__(self):
        return f"{self.fecha_asignada}"

class Metodo_Pago(models.Model):
    metodoPago = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.metodoPago}"

class Pago(models.Model):
    plazos = models.IntegerField()
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)
    formaPago = models.ForeignKey(Metodo_Pago, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.pedido}"

class Garantia(models.Model):
    descripcion = models.TextField()
    fechaGarantia = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.pedido}"

class Evaluacion(models.Model):
    calificacionEvaluacion = models.TextField()
    comentarios = models.TextField()
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.usuario}"
