from django.shortcuts import render

#from .carrito import Carrito #por aitageo
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



#Tienda----------------------------------------------------------------------------------------------------
def Tienda(request):
    Productos=Producto.objects.all()
    return render(request, 'Tienda/tienda.html', {"Productos":Productos})
