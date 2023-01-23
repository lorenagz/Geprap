from django.shortcuts import render
from .carrito import Carrito #por aitageo
from audioop import reverse
from http import server
from logging import exception
from re import S
from types import MethodDescriptorType
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

#gestion de errorres base de datos
from django.db import IntegrityError



from django.core.paginator import Paginator
from django.db.models import Q
from geprapapp.models import Producto

#por aitageo
#Carrito---------------------------------------------------------------------------------------------------------------------------
def agregar_producto(request,producto_id):
    carrito=Carrito(request)
    
    producto=Producto.objects.get(id=producto_id)
    carrito.agregar(producto=producto)
    
    return redirect('Tienda')

def eliminar_producto(request,producto_id):
    carrito=Carrito(request)
    
    producto=Producto.objects.get(id=producto_id)
    carrito.eliminar(producto=producto)
    
    return redirect('Tienda')

def restar_producto(request,producto_id):
    carrito=Carrito(request)
    
    producto=Producto.objects.get(id=producto_id)
    carrito.restar_producto(producto=producto)
    
    return redirect('Tienda')


def limpiar_carrito(request):
    carrito=Carrito(request)
    
    carrito.limpiar_carrito()
    
    return redirect('Tienda')



#fin carrito----------------------------------------------------------------------------------------------

