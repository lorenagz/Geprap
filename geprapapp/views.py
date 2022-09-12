from audioop import reverse
from logging import exception
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

#gestion de errorres base de datos
from django.db import IntegrityError


from .models import Permiso, Rol, Rol_Permiso
# Create your views here.

def index(request):
    return render(request, 'geprapapp/index.html')

# CRUD Roles-----------------------------------------------------------
def listaRol(request):
    rol = Rol.objects.all()
    contexto = {"datos":rol}
    return render(request, 'geprapapp/rol/listarRol.html', contexto)

def formularioRol(request):
    return render(request, 'geprapapp/rol/nuevoRol.html')

def guardarRol(request):
    try:
        if request.method == "POST":
            rol = Rol(
                nombre = request.POST["nombre"]
            )
            rol.save()
            messages.success(request, "Rol guardado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos....")

    except Exception as e :
        messages.error(request, f"Error: {e}")

    return redirect('geprapapp:listarRol')

def edicionRol(request, id):
    rol = Rol.objects.get(id=id)
    return render(request, 'geprapapp/rol/edicionRol.html', {"rol":rol})

def editarRol(request):
    id = request.POST["id"]
    print(id)
    nombre = request.POST["nombre"]
    
    rol = Rol.objects.get(id=id)
    rol.id = id
    rol.nombre = nombre
    rol.save()
    return redirect('geprapapp:listarRol')

def eliminarRol(request, id):
    try:
        print(id)
        rol = Rol.objects.get(id=id)
        rol.delete()
        messages.success(request, "El rol se eliminó correctamente!!")

    except Exception as e: 
        messages.error(request, f"Error: {e}")

    return redirect('geprapapp:listarRol')

# CRUD Permisos----------------------------------------------------------
def listaPermiso(request):
    permiso = Permiso.objects.all()
    contexto = {"datos":permiso}
    return render(request, 'geprapapp/permiso/listarPermisos.html', contexto)

def formularioPermiso(request):
    return render(request, 'geprapapp/permiso/nuevoPermiso.html')

def guardarPermiso(request):
    try:
        if request.method == "POST":
            permiso = Permiso(
                nombre = request.POST["nombre"]
            )
            permiso.save()
            messages.success(request, "Permiso guardado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos....")

    except Exception as e :
        messages.error(request, f"Error: {e}")

    return redirect('geprapapp:listarPermiso')

def edicionPermiso(request, id):
    permiso = Permiso.objects.get(id=id)
    return render(request, 'geprapapp/permiso/edicionPermiso.html', {"permiso":permiso})

def editarPermiso(request):
    id = request.POST["id"]
    print(id)
    nombre = request.POST["nombre"]
    
    permiso = Permiso.objects.get(id=id)
    permiso.id = id
    permiso.nombre = nombre
    permiso.save()
    return redirect('geprapapp:listarPermiso')

def eliminarPermiso(request, id):
    try:
        print(id)
        permiso = Permiso.objects.get(id=id)
        permiso.delete()
        messages.success(request, "El permiso se eliminó correctamente!!")

    except Exception as e: 
        messages.error(request, f"Error: {e}")

    return redirect('geprapapp:listarPermiso')

# CRUD PermisosRol----------------------------------------------------------
def listaPermisoRol(request):
    permiso = Rol_Permiso.objects.all()
    contexto = {"datos":permiso}
    return render(request, 'geprapapp/permisosRol/listarPermisosRol.html', contexto)

def formularioPermisoRol(request):
    return render(request, 'geprapapp/permisosRol/nuevoPermisoRol.html')

def guardarPermisoRol(request):
    try:
        if request.method == "POST":
            permisoRol = Rol_Permiso(
                rol = request.POST["nombreRol"],
                permiso = request.POST["nombrePermiso"]
            )
            permisoRol.save()
            messages.success(request, "Permiso por Rol guardado correctamente!!")
        else:
            messages.warning(request, "Usted no ha enviado datos....")

    except Exception as e :
        messages.error(request, f"Error: {e}")

    return redirect('geprapapp:listarPermisoRol')