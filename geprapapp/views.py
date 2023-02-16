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
from carrito import *

#gestion de errorres base de datos
from django.db import IntegrityError

from .models import Agenda, Categoria, Detalle_Pedido, Evaluacion, Garantia, Metodo_Pago, Pago, Pedido, Producto, Servicio, Usuario

from django.core.paginator import Paginator
from django.db.models import Q

#Cifrado de claves
from .crypt import claveEncriptada

# Login----------------------------------------------------------------------------------------------------------------------------
def loginFormulario(request):
    return render(request, 'geprapapp/login/login.html')

def login(request):
    if request.method == "POST":
        try:
            user = request.POST["usuario"]
            passw = claveEncriptada(request.POST["clave"])
            q = Usuario.objects.get(nombreUsuario = user, clave = passw)
            # crear la sesión
            request.session["logueo"] = [q.nombre, q.rol, q.cedula, q.id, q.correo, q.get_rol_display()]
            # ----------------------------
            messages.success(request, "Bienvenido!!")
            return redirect('geprapapp:listarUsuarios') 
            
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect('geprapapp:loginFormulario')
        
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('geprapapp:loginFormulario')
    else:
        messages.warning(request, "Usted no ha enviado datos...")
        return redirect('geprapapp:loginFormulario')

def logout(request):
    try:

        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente!!")
        return redirect('geprapapp:index')
    except Exception as e:
        messages.error(request, f"Error: {e}")
        return redirect('geprapapp:index')

#Restablecer contraseña--------------------------------------------------------------------------------------------------------------
def solicitudRestablecer(request):
    return render(request, 'geprapapp/restablecerContraseña/solicitarRestablecer.html')

def cambiarContrasena(request, id):
    contexto = {"id":id}
    return render(request, 'geprapapp/restablecerContraseña/formularioRestablecer.html', contexto)

def cambiarClave(request):
    try :
        if request.method=="POST":
            usuario = Usuario.objects.get(pk = request.POST['id'])
            usuario.clave = claveEncriptada(request.POST['clave']) 
            usuario.save()
            messages.success(request,"Cambio de contraseña exitoso!!")

        else:
            messages.warning(request,"No se han eviado los datos correctamente...")
    except Exception as e:
        messages.error(request,f"error: {e}")
           
    return redirect('geprapapp:index')

def restablecerContrasena(request):
    from django.core.mail import send_mail
    try: 
        if request.method=="POST":
            correoRest = request.POST["correo"]
            print(correoRest)
            usuario = Usuario.objects.get(correo = correoRest)
            print(usuario.clave)
            send_mail(
                'Mensaje de Geprap:',
                'Para reestablecer su contraseña ingrese al siguiente enlace:\n'+
                'http://127.0.0.1:8000/geprapapp/restablecerContrasena/'+str(usuario.pk),
                'astrid.saldarriaga6@misena.edu.co',
                [correoRest],

                fail_silently=False,
        )
        messages.info(request,'correo enviado')
    except Exception as e: 
        messages.error(request,f"ERROR:{e}")
    return render(request,'geprapapp/index.html')


#Index---------------------------------------------------------------------------------------------------------------------------------
def index(request):
    return render(request, 'geprapapp/index.html')

#CRUD Registro cliente-----------------------------------------------------------------------------------------------------------------
def ClienteFormulario(request):
    return render(request, 'geprapapp/Cliente/registro_cliente.html')



def RegistroCliente(request):
    try:
        if request.method == "POST":
            user = Usuario(
                    cedula = request.POST["cedula"],
                    nombre = request.POST["nombre"],
                    telefono = request.POST["telefono"],
                    direccion = request.POST["direccion"],
                    correo = request.POST["correo"],
                    nombreUsuario = request.POST["nombreUsuario"],
                    clave = request.POST["clave"],
                    rol = "C",
                    )
            user.save()
            messages.success(request, "Usuario guardado correctamente!!")
        else:
                messages.warning(request, "Usted no ha enviado datos....")
    except Exception as e :
            messages.error(request, f"Error: {e}")
    return redirect('geprapapp:listarUsuarios')   
    

# CRUD Usuarios-------------------------------------------------------------------------------------------------------------------------
def listaUsuarios(request):
    """Lista todos los registros de los usuarios y los muestra en el tamplate
    
    Args:
        u: recibe los objetos del modelo Usuario
    Return:
        el retorno de los registros es dependiendo el rol
        Administrador: templates:´geprapapp/usuario/listarUsuarioAdmin.html´
        Cliente: templates:´geprapapp/usuario/listarUsuario.html´
        Instalador: templates:´geprapapp/usuario/listarUsuarioInstalador.html´
    """

    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        u = Usuario.objects.all()
        paginator = Paginator(u, 3)
        page_number = request.GET.get('page')
        u = paginator.get_page(page_number)
        contexto = {"datos": u }
        return render(request, 'geprapapp/usuario/listarUsuarioAdmin.html', contexto)
    elif login and (login[1] == "I"):
        u = Usuario.objects.all()
        paginator = Paginator(u, 3)
        page_number = request.GET.get('page')
        u = paginator.get_page(page_number)
        contexto = {"datos": u }
        return render(request, 'geprapapp/usuario/listarUsuarioInstalador.html', contexto)
    elif login and (login[1] == "C"):
        u = Usuario.objects.get(cedula = request.session.get('logueo')[2])
        contexto = {"datos": [u]}
        return render(request, 'geprapapp/usuario/listarUsuarios.html', contexto)
    else:
        if login and(login[1] == "O"):
            messages.warning(request, "No tiene acceso al módulo usuarios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
         
def formularioUsuario(request):
    """Muestra el formulario para el usuario ingresar los datos
    Args:

    Returns:

    """
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        return render(request, 'geprapapp/usuario/nuevoUsuario.html')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para agregar usuarios...")
            return redirect('geprapapp:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarUsuario(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        try:
            if request.method == "POST":
                u = Usuario(
                    cedula = request.POST["cedula"],
                    nombre = request.POST["nombre"],
                    telefono = request.POST["telefono"],
                    direccion = request.POST["direccion"],
                    correo = request.POST["correo"],
                    nombreUsuario = request.POST["nombreUsuario"],
                      clave = request.POST["clave"],
                    rol = request.POST["rol"]
                    )
                u.save()
                messages.success(request, "Usuario guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarUsuarios')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para agregar usuarios...")
            return redirect('geprapapp:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
    
def edicionUsuario(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        u = Usuario.objects.get(pk = id)
        contexto = {"usuario":u}
        return render(request, 'geprapapp/usuario/edicionUsuario.html', contexto)
    elif login and(login[1] == "C"):
        u = Usuario.objects.get(id = request.session.get('logueo')[3])
        contexto = {"usuario":u}
        return render(request, 'geprapapp/usuario/edicionUsuario.html', contexto)
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene permisos para editar usuarios...")
            return redirect('geprapapp:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
    

def editarUsuario(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1] == "C"):
        try:
            if request.method == "POST":
                u = Usuario.objects.get(pk = request.POST["id"])
            
                u.cedula = request.POST["cedula"]
                u.nombre = request.POST["nombre"]
                u.telefono = request.POST["telefono"]
                u.direccion = request.POST["direccion"]
                u.correo = request.POST["correo"]
                u.nombreUsuario = request.POST["nombreUsuario"]
                u.clave = request.POST["clave"]
                u.rol = request.POST["rol"]

                u.save()
                messages.success(request, "Usuario actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarUsuarios')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene permisos para editar usuarios...")
            return redirect('geprapapp:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
    
def eliminarUsuario(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"): 
        try:
            u = Usuario.objects.get(id=id)
            u.delete()
            messages.success(request, "El usuario se eliminó correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este usuario porque otros registros están relacionados con él....")
        except Exception as e: 
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarUsuarios')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para eliminar usuarios...")
            return redirect('geprapapp:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
        
def buscarUsuario(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1] == "I"):
        if request.method == "POST":
            dato = request.POST["buscar"]
            u = Usuario.objects.filter( Q(nombre__icontains = dato) | Q(cedula__icontains = dato) )
            
            paginator = Paginator(u, 4) # Mostrar 4 registros por página...

            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            u = paginator.get_page(page_number)
            
            contexto = { "datos": u }
            return render(request, 'geprapapp/usuario/listar_usuario_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
        return redirect('geprapapp:listarUsuarios')
    else:
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene permiso para buscar información de usuarios...")
            return redirect('geprapapp:listarUsuarios')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')  

# CRUD Categoría------------------------------------------------------------------------------------------------------------------------
def listaCategoria(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        categoria = Categoria.objects.all()

        paginator = Paginator(categoria, 4)
        page_number = request.GET.get('page')
        categoria = paginator.get_page(page_number)

        contexto = {"datos":categoria}
        return render(request, 'geprapapp/categoria/listarCategoria.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permiso para acceder al módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioCategoria(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        return render(request, 'geprapapp/categoria/nuevaCategoria.html')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarCategoria(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        try: 
            if request.method == "POST":
                categoria = Categoria(
                    nombre = request.POST["nombre"],
                    desc = request.POST["descripcion"]
                )
                categoria.save()
                messages.success(request, "Categoría guardada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarCategoria')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionCategoria(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        c = Categoria.objects.get(pk = id)
        contexto = {"categoria": c}
        return render(request, 'geprapapp/categoria/edicionCategoria.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarCategoria(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        try:
            if request.method == "POST":
                c = Categoria.objects.get(pk = request.POST["id"])

                c.nombre = request.POST["nombre"]
                c.desc = request.POST["desc"]
                c.save()
                messages.success(request, "Categoría actualizada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarCategoria')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
    
def eliminarCategoria(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"): 
        try:
            categoria = Categoria.objects.get(id=id)
            categoria.delete()
            messages.success(request, "La categoría se eliminó correctamente!!")

        except IntegrityError:
            messages.warning(request, "No puede eliminar esta categoría porque otros registros están relacionados con él....")

        except Exception as e: 
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarCategoria')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarCategoria(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        if request.method == "POST":
            dato = request.POST["buscar"]
            c = Categoria.objects.filter( Q(nombre__icontains = dato) | Q(desc__icontains = dato) )
            
            paginator = Paginator(c, 4) # Mostrar 4 registros por página...

            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            c = paginator.get_page(page_number)
            
            contexto = { "datos": c }
            return render(request, 'geprapapp/categoria/listar_categoria_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarCategoria')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo categorías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

# CRUD Producto------------------------------------------------------------------------------------------------------------------------
def listaProducto(request):
    login = request.session.get('logueo', False)

    if login and(login[1] == "A"):
        p = Producto.objects.all()

        paginator = Paginator(p, 4)
        page_number = request.GET.get('page')
        p = paginator.get_page(page_number)

        contexto = {"datos":p }
        return render(request, 'geprapapp/producto/listarProducto.html', contexto)
    else:
        if login and(login[1] == "  A"):
            messages.warning(request, "No tiene acceso al módulo productos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioProducto(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        c = Categoria.objects.all()
        contexto = {"cat": c}
        return render(request, 'geprapapp/producto/nuevoProducto.html', contexto)
    else:    
        if login and(login[1] == "C"):
            messages.warning(request, "No tiene acceso al módulo productos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarProducto(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            if request.method == "POST":
                p = Producto(
                    nombre= request.POST["nombre"],
                    descripcion = request.POST["descripcion"],
                    precio = request.POST["precio"],
                    categoria = Categoria.objects.get(pk = request.POST["categoria"])
                )
                p.save()
                messages.success(request, "Producto guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarProductos')        
    else:
        if login and(login[1] == "A"):
            messages.warning(request, "No tiene acceso al módulo productos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
        
def editarProducto(request):  
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):           
        try:
            if request.method == "POST":
                p = Producto.objects.get(pk = request.POST["id"])
                c = Categoria.objects.get(pk = request.POST["categoria"])

                p.nombre= request.POST["nombre"]
                p.descripcion = request.POST["descripcion"]
                p.precio = request.POST["precio"]
                p.categoria = c
                
                p.save()
                messages.success(request, "Producto actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")    
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarProductos')    
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo productos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarProducto(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"): 
        try:
            p = Producto.objects.get(pk = id)

            p.delete()
            messages.success(request, "Producto eliminado correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este producto porque otros registros están relacionados con él....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarProductos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo productos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarProducto(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        if request.method == "POST":
            dato = request.POST["buscar"]
            p = Producto.objects.filter( Q(nombre__icontains = dato) | Q(descripcion__icontains = dato) )
            
            paginator = Paginator(p, 4) # Mostrar 4 registros por página...

            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            p = paginator.get_page(page_number)
            
            contexto = { "datos": p }
            return render(request, 'geprapapp/producto/listar_producto_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarProductos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo productos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

# CRUD Servicio---------------------------------------------------------------------------------------------------------------------
def listaServicio(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        servicio = Servicio.objects.all()

        paginator = Paginator(servicio, 4)
        page_number = request.GET.get('page')
        servicio = paginator.get_page(page_number)

        contexto = {"datos":servicio}
        return render(request, 'geprapapp/servicios/listarServicio.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioServicio(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        return render(request, 'geprapapp/servicios/nuevoServicio.html')
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarServicio(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            if request.method == "POST":
                servicio = Servicio(
                    descripcion = request.POST["descripcion"]
                )
                servicio.save()
                messages.success(request, "Servicio guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarServicio')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionServicio(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        servicio = Servicio.objects.get(id=id)
        return render(request, 'geprapapp/servicios/edicionServicio.html', {"servicio":servicio})
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarServicio(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):      
        try:
            if request.method == "POST":
                id = request.POST["id"]
                descripcion = request.POST["descripcion"]
                
                servicio = Servicio.objects.get(id=id)
                servicio.descripcion = descripcion
                servicio.save()
                messages.success(request, "Servicio actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarServicio')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarServicio(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"): 
        try:
            servicio = Servicio.objects.get(id=id)
            servicio.delete()
            messages.success(request, "El servicio se eliminó correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este servicio porque otros registros están relacionados con él....")
        except Exception as e: 
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarServicio')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarServicio(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        if request.method == "POST":
            dato = request.POST["buscar"]
            s = Servicio.objects.filter( Q(descripcion__icontains = dato))
                
            paginator = Paginator(s, 4) # Mostrar 4 registros por página...
            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            s = paginator.get_page(page_number)
                    
            contexto = { "datos": s }
            return render(request, 'geprapapp/servicios/listar_servicio_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarServicio')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo servicios...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

# CRUD Pedido---------------------------------------------------------------------------------------------------------------------
def listaPedido(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1] == "C"):
        p = Pedido.objects.all()

        paginator = Paginator(p, 4)
        page_number = request.GET.get('page')
        p = paginator.get_page(page_number)

        contexto = {"datos":p }
        return render(request, 'geprapapp/pedido/listarPedidoAdmin.html', contexto)

    elif login and(login[1] == "O" or login[1] == "I"):
        p = Pedido.objects.all()

        paginator = Paginator(p, 4)
        page_number = request.GET.get('page')
        p = paginator.get_page(page_number)

        contexto = {"datos":p }
        return render(request, 'geprapapp/pedido/listarPedidoOperarioInstalador.html', contexto)
    
    elif login and(login[1] == "C"):
        p = Pedido.objects.filter(usuario = request.session.get('logueo')[3])

        paginator = Paginator(p, 4)
        page_number = request.GET.get('page')
        p = paginator.get_page(page_number)

        contexto = {"datos": p }
        return render(request, 'geprapapp/pedido/listarPedido.html', contexto)
    else:
        messages.warning(request, "Inicie sesión...")
        return redirect('geprapapp:loginFormulario')

def formularioPedido(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1] == "C"):
        u = Usuario.objects.all()
        contexto = {"usu": u}
        return render(request, 'geprapapp/pedido/nuevoPedido.html', contexto)
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permiso para agregar pedidos...")
            return redirect('geprapapp:listarPedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
        
        
        
     
            
            
                     

def guardarPedido(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A" or login[1] == "C"): 
        try:
            if request.method == "POST":
                p = Pedido(
                    fecha_pedido = request.POST["fecha_pedido"],
                    total = request.POST["total"],
                    usuario = Usuario.objects.get(pk = request.POST["usuario"]),
                    estado = request.POST["estado"]
                )
                p.save()
                messages.success(request, "Pedido guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarPedidos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para agregar pedidos...")
            return redirect('geprapapp:listarPedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionPedido(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        p = Pedido.objects.get(pk = id)
        u = Usuario.objects.all()
        contexto = {"usu": u, "pedido": p}
        return render(request, 'geprapapp/pedido/edicionPedido.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para editar pedidos...")
            return redirect('geprapapp:listarPedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarPedido(request):  
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):                 
        try:
            if request.method == "POST":
                p = Pedido.objects.get(pk = request.POST["id"])
                u = Usuario.objects.get(pk = request.POST["usuario"])
                
                p.fecha_pedido = request.POST["fecha_pedido"]
                p.total = request.POST["total"]
                p.estado = request.POST["estado"]
                p.usuario = u
                
                p.save()
                messages.success(request, "Pedido actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....") 
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarPedidos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para editar pedidos...")
            return redirect('geprapapp:listarPedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarPedido(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"): 
        try:
            p = Pedido.objects.get(pk = id)

            p.delete()
            messages.success(request, "Pedido eliminado correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este pedido porque otros registros están relacionados con él....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarPedidos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permisos para eliminar pedidos...")
            return redirect('geprapapp:listarPedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarPedido(request):
    login = request.session.get('logueo', False)
    if login:
        if request.method == "POST":
            dato = request.POST["buscar"]
            p = Pedido.objects.filter( Q(id__icontains = dato))
            
            paginator = Paginator(p, 4) # Mostrar 4 registros por página...

            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            p = paginator.get_page(page_number)
            
            contexto = { "datos": p }
            return render(request, 'geprapapp/pedido/listar_pedido_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarPedidos')
    else:
        messages.warning(request, "Inicie sesión...")
        return redirect('geprapapp:loginFormulario')
        
# CRUD DetallePedido-----------------------------------------------------------------------------------------------------------
def listaDetallePedido(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1]== "C"):
        pd = Detalle_Pedido.objects.all()

        paginator = Paginator(pd, 4)
        page_number = request.GET.get('page')
        pd = paginator.get_page(page_number)

        contexto = {"datos":pd}
        return render(request, 'geprapapp/detallePedido/listarDetallePedidoAdmin.html', contexto)
    elif login and(login[1] == "O" or login[1] == "I"):
        pd = Detalle_Pedido.objects.all()

        paginator = Paginator(pd, 4)
        page_number = request.GET.get('page')
        pd = paginator.get_page(page_number)

        contexto = {"datos":pd}
        return render(request, 'geprapapp/detallePedido/listarDetallePedidoOperarioInsta.html', contexto)
    elif login and(login[1] == "C"):
        pd = Detalle_Pedido.objects.filter(usuario = request.session.get('logueo')[3])
        
        paginator = Paginator(pd, 4)
        page_number = request.GET.get('page')
        pd = paginator.get_page(page_number)

        contexto = {"datos":pd}
        return render(request, 'geprapapp/detallePedido/listarDetallePedido.html', contexto)
    else:
        messages.warning(request, "Inicie sesión...")
        return redirect('geprapapp:loginFormulario')

def formularioDetallePedido(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1] == "C"):
        ped = Pedido.objects.all()
        pro = Producto.objects.all()
        ser = Servicio.objects.all()
        u = Usuario.objects.all()
        contexto = {"pedido":ped, "producto":pro, "servicio":ser, "usuario":u}
        return render(request, 'geprapapp/detallePedido/nuevoDetallePedido.html', contexto)
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permiso para agregar detalle de pedidos...")
            return redirect('geprapapp:listarDetallePedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarDetallePedido(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A" or login[1] == "C"): 
        try:
            if request.method == "POST":
                p = Detalle_Pedido(
                    id_pedido = Pedido.objects.get(pk = request.POST["id_pedido"]),
                    id_producto = Producto.objects.get(pk = request.POST["id_producto"]),
                    id_servicio = Servicio.objects.get(pk = request.POST["id_servicio"]),
                    usuario = Usuario.objects.get(pk = request.POST["usuario"]),
                    cantidad = request.POST["cantidad"]
                )
                p.save()
                messages.success(request, f"Detalle de pedido guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarDetallePedidos')
    else:    
        if login and(login[1] != "A"):
                messages.warning(request, "No tiene permiso para agregar detalle de pedidos...")
                return redirect('geprapapp:listarDetallePedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionDetallePedido(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        p = Detalle_Pedido.objects.get(pk = id)
        ped = Pedido.objects.all()
        pro = Producto.objects.all()
        ser = Servicio.objects.all()
        u = Usuario.objects.all()

        contexto = {"pedido":ped, "producto":pro, "servicio":ser, "detalle":p, "usuario":u}
        return render(request, 'geprapapp/detallePedido/edicionDetallePedido.html', contexto)
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permiso para editar detalle de pedidos...")
            return redirect('geprapapp:listarDetallePedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarDetallePedido(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        try:
            if request.method == "POST":
                p = Detalle_Pedido.objects.get(pk = request.POST["id"])
                pedido = Pedido.objects.get(pk = request.POST["id_pedido"])
                producto = Producto.objects.get(pk = request.POST["id_producto"])
                servicio = Servicio.objects.get(pk = request.POST["id_servicio"])
                usuario = Usuario.objects.get(pk = request.POST["usuario"])

                p.id_pedido = pedido
                p.id_producto = producto
                p.id_servicio = servicio
                p.cantidad = request.POST["cantidad"]
                p.usuario = usuario

                p.save()
                messages.success(request, f"Detalle del pedido {pedido.id} actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")     
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarDetallePedidos')
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permiso para editar detalle de pedidos...")
            return redirect('geprapapp:listarDetallePedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarDetallePedido(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        try:
            p = Detalle_Pedido.objects.get(id=id)
            p.delete()
            messages.success(request, f"El Detalle del Pedido se eliminó correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este Detalle de Pedido porque otros registros están relacionados con él....")
        except Exception as e: 
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarDetallePedidos')
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene permiso para eliminar detalle de pedidos...")
        
            return redirect('geprapapp:listarDetallePedidos')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarDetallePedido(request):
    login = request.session.get('logueo', False)
    if login:
        if request.method == "POST":
            dato = request.POST["buscar"]
            p = Detalle_Pedido.objects.filter( Q(id__icontains = dato))
            
            paginator = Paginator(p, 4) # Mostrar 4 registros por página...

            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            p = paginator.get_page(page_number)
            
            contexto = { "datos": p }
            return render(request, 'geprapapp/detallePedido/listar_detallePedido_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarDetallePedidos')
    else:
        messages.warning(request, "Inicie sesión...")
        return redirect('geprapapp:loginFormulario')

#CRUD Agenda-------------------------------------------------------------------------------------------------------------------------------
def listaAgenda(request):
    login = request.session.get('logueo',False)
    if login and(login[1] == "A"):
        agenda = Agenda.objects.all()

        paginator = Paginator(agenda, 4)
        page_number = request.GET.get('page')
        agenda = paginator.get_page(page_number)

        contexto = {"datos":agenda}
        return render(request, 'geprapapp/agenda/listarAgendaAdmin.html', contexto)
    elif login and(login[1] == "I"):
        agenda = Agenda.objects.all()

        paginator = Paginator(agenda, 4)
        page_number = request.GET.get('page')
        agenda = paginator.get_page(page_number)

        contexto = {"datos":agenda}
        return render(request, 'geprapapp/agenda/listarAgenda.html', contexto)
    else:
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")   
            return redirect('geprapapp:loginFormulario')

def formularioAgenda(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        p = Pedido.objects.all()
        contexto = {"pedido":p}
        return render(request, 'geprapapp/agenda/nuevaAgenda.html', contexto)
    elif login and(login[1] == "I"):
        messages.warning(request, "No tiene permiso para agregar agenda...")
        return redirect('geprapapp:listarAgenda')
    else:    
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarAgenda(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        try:
            if request.method == "POST":
                agenda = Agenda(
                    fecha_asignada = request.POST["fecha_asignada"],
                    pedido =Pedido.objects.get(pk = request.POST["pedido"])
                )
                agenda.save()
                messages.success(request, "Agenda programada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarAgenda')
    elif login and(login[1] == "I"):
        messages.warning(request, "No tiene permiso para agregar agenda...")
        return redirect('geprapapp:listarAgenda')
    else:    
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionAgenda(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        a = Agenda.objects.get(pk = id)
        p = Pedido.objects.all()
        contexto = {"pedido": p, "agenda": a}
        return render(request, 'geprapapp/agenda/edicionAgenda.html', contexto)
    elif login and(login[1] == "I"):
        messages.warning(request, "No tiene permiso para editar agenda...")
        return redirect('geprapapp:listarAgenda')
    else:    
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarAgenda(request): 
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):            
        try:
            if request.method == "POST":
                a = Agenda.objects.get(pk = request.POST["id"])
                p = Pedido.objects.get(pk = request.POST["pedido"])

                a.fecha_asignada = request.POST["fecha_asignada"]
                a.pedido = p
                a.save()
                messages.success(request, "Agenda actualizada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")            
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarAgenda')
    elif login and(login[1] == "I"):
        messages.warning(request, "No tiene permiso para editar agenda...")
        return redirect('geprapapp:listarAgenda')
    else:    
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarAgenda(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):     
        try:
            a = Agenda.objects.get(pk = id)
            a.delete()
            messages.success(request, "Agenda eliminada correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar esta Agenda porque otros registros están relacionados con ella....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarAgenda')
    elif login and(login[1] == "I"):
        messages.warning(request, "No tiene permiso para eliminar agenda...")
        return redirect('geprapapp:listarAgenda')
    else:    
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarAgenda(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A" or login[1] == "I"): 
        if request.method == "POST":
            dato = request.POST["buscar"]
            a = Agenda.objects.filter( Q(id__icontains = dato) | Q(fecha_asignada__icontains = dato))
                
            paginator = Paginator(a, 4) # Mostrar 4 registros por página...
            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            a = paginator.get_page(page_number)
                    
            contexto = { "datos": a }
            return render(request, 'geprapapp/agenda/listar_agenda_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarAgenda')
    else:
        if login and(login[1] != "A" or login[1] != "I"):
            messages.warning(request, "No tiene acceso al módulo agenda...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')  

#CRUD Metodo Pago---------------------------------------------------------------------------------------------------------------------
def listaMetodoPago(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        metodoPago = Metodo_Pago.objects.all()

        paginator = Paginator(metodoPago, 4)
        page_number = request.GET.get('page')
        metodoPago = paginator.get_page(page_number)

        contexto = {"datos":metodoPago} 
        return render(request, 'geprapapp/metodoPago/listarMetodoPago.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioMetodoPago(request):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        return render(request, 'geprapapp/metodoPago/nuevoMetodoPago.html')
    else:    
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarMetodoPago(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            if request.method == "POST":
                metodo_Pago = Metodo_Pago(
                    metodoPago = request.POST["metodo"]
                )
                metodo_Pago.save()
                messages.success(request, "Metodo de Pago guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarMetodoPago')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionMetodoPago(request, id):
    login = request.session.get('logueo', False)
    if login and(login[1] == "A"):
        metodo_Pago = Metodo_Pago.objects.get(id=id)
        return render(request, 'geprapapp/metodoPago/edicionMetodoPago.html', {"metodoPago":metodo_Pago})
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarMetodoPago(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        try:
            if request.method == "POST":
                id = request.POST["id"]
                metodoPago = request.POST["metodo"]
                        
                metodo_Pago = Metodo_Pago.objects.get(id=id)
                metodo_Pago.metodoPago = metodoPago
                metodo_Pago.save()
                messages.success(request, "Metodo de Pago actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")        
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarMetodoPago')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarMetodoPago(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        try:
            metodo_Pago = Metodo_Pago.objects.get(id=id)
            metodo_Pago.delete()
            messages.success(request, "El Método de Pago se eliminó correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este metodo de pago porque otros registros están relacionados con él....")
        except Exception as e: 
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarMetodoPago')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarMetodoPago(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        if request.method == "POST":
            dato = request.POST["buscar"]
            m = Metodo_Pago.objects.filter( Q(id__icontains = dato) | Q(metodoPago__icontains = dato))
                
            paginator = Paginator(m, 4) # Mostrar 4 registros por página...
            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            m = paginator.get_page(page_number)
                    
            contexto = { "datos": m }
            return render(request, 'geprapapp/metodoPago/listar_metodo_pago_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarMetodoPago')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo métodos de pago...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

#CRUD Pagos---------------------------------------------------------------------------------------------------------------------------
def listaPagos(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        pago = Pago.objects.all()

        paginator = Paginator(pago, 4)
        page_number = request.GET.get('page')
        pago = paginator.get_page(page_number)

        contexto = {"datos":pago}
        return render(request, 'geprapapp/pagos/listarPagos.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioPagos(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        p = Pedido.objects.all()
        mp = Metodo_Pago.objects.all()
        contexto = {"pedido":p, "metodo":mp}
        return render(request, 'geprapapp/pagos/nuevoPago.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarPagos(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        try:
            if request.method == "POST":
                p = Pago(
                    plazos = request.POST["plazos"],
                    pedido = Pedido.objects.get(pk = request.POST["pedido"]),
                    formaPago = Metodo_Pago.objects.get(pk = request.POST["formaPago"])
                )
                p.save()
                messages.success(request, "Pago guardado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarPagos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionPago(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):
        p = Pago.objects.get(pk = id)
        pd = Pedido.objects.all()
        mp = Metodo_Pago.objects.all()
        contexto = {"pago": p, "metodo": mp, "pedido":pd}
        return render(request, 'geprapapp/pagos/edicionPagos.html', contexto)
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarPago(request): 
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):            
        try:
            if request.method == "POST":
                p = Pago.objects.get(pk = request.POST["id"])
                mp = Metodo_Pago.objects.get(pk = request.POST["formaPago"])
                pd = Pedido.objects.get(pk = request.POST["pedido"])

                p.plazos = request.POST["plazos"]
                p.formaPago = mp
                p.pedido = pd
                p.save()
                messages.success(request, "Pago actualizado correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")           
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarPagos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarPago(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            p = Pago.objects.get(id=id)
            p.delete()
            messages.success(request, "El Pago se eliminó correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar este pago porque otros registros están relacionados con él....")
        except Exception as e: 
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarPagos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarPago(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        if request.method == "POST":
            dato = request.POST["buscar"]
            p = Pago.objects.filter( Q(id__icontains = dato) | Q(plazos__icontains = dato))
                
            paginator = Paginator(p, 4) # Mostrar 4 registros por página...
            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            p = paginator.get_page(page_number)
                    
            contexto = { "datos": p }
            return render(request, 'geprapapp/pagos/listar_pagos_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarPagos')
    else:
        if login and(login[1] != "A"):
            messages.warning(request, "No tiene acceso al módulo de pagos...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

#CRUD Evaluación--------------------------------------------------------------------------------------------------------------------------
def listaEvaluacion(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        e = Evaluacion.objects.all()

        paginator = Paginator(e, 4)
        page_number = request.GET.get('page')
        e = paginator.get_page(page_number)

        contexto = {"datos":e}
        return render(request, 'geprapapp/evaluacion/listarEvaluacion.html', contexto)  
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para ver las evaluaciones...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioEvaluacion(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A" or login[1] == "C" ): 
        p = Pedido.objects.all()
        u = Usuario.objects.all()
        contexto = {"pedido":p, "usuario": u}
        return render(request, 'geprapapp/evaluacion/nuevaEvaluacion.html', contexto)
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarEvaluacion(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            if request.method == "POST":
                e = Evaluacion(
                    pedido = Pedido.objects.get(pk = request.POST["pedido"]),
                    usuario = Usuario.objects.get(pk = request.POST["usuario"]),
                    calificacionEvaluacion = request.POST["calificacionEvaluacion"],
                    comentarios = request.POST["comentarios"]
                )
                e.save()
                messages.success(request, "Evaluación guardada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarEvaluaciones')
    elif login and (login[1] == "C"):
        try:
            if request.method == "POST":
                e = Evaluacion(
                    pedido = Pedido.objects.get(pk = request.POST["pedido"]),
                    usuario = Usuario.objects.get(pk = request.POST["usuario"]),
                    calificacionEvaluacion = request.POST["calificacionEvaluacion"],
                    comentarios = request.POST["comentarios"]
                )
                e.save()
                messages.success(request, "Muchas gracias, tu opinión vale mucho para nosotros!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionEvaluacion(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        e = Evaluacion.objects.get(pk = id)
        p = Pedido.objects.all()
        u = Usuario.objects.all()
        contexto = {"pedido": p, "evaluacion": e, "usuario": u}
        return render(request, 'geprapapp/evaluacion/edicionEvaluacion.html', contexto)
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para editar las evaluaciones...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarEvaluacion(request):  
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):            
        try:
            if request.method == "POST":
                e = Evaluacion.objects.get(pk = request.POST["id"])
                p = Pedido.objects.get(pk = request.POST["pedido"])
                u = Usuario.objects.get(pk = request.POST["usuario"])

                e.comentarios = request.POST["comentarios"]
                e.calificacionEvaluacion = request.POST["calificacionEvaluacion"]
                e.pedido = p
                e.usuario = u
                e.save()
                messages.success(request, "Evaluación actualizada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")           
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarEvaluaciones')
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para editar las evaluaciones...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarEvaluacion(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            e = Evaluacion.objects.get(pk = id)
            e.delete()
            messages.success(request, "Evaluación eliminada correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar esta Evaluación porque otros registros están relacionados con ella....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarEvaluaciones')
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para eliminar las evaluaciones...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarEvaluacion(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        if request.method == "POST":
            dato = request.POST["buscar"]
            e = Evaluacion.objects.filter( Q(id__icontains = dato) | Q(calificacionEvaluacion__icontains = dato))

            paginator = Paginator(e, 4) # Mostrar 4 registros por página...
            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            e = paginator.get_page(page_number)
                    
            contexto = { "datos": e }
            return render(request, 'geprapapp/evaluacion/listar_evaluacion_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarEvaluaciones')
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para buscar evaluaciones...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de evaluación...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

#CRUD Garantía----------------------------------------------------------------------------------------------------------------------------
def listaGarantia(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        g = Garantia.objects.all()

        paginator = Paginator(g, 4)
        page_number = request.GET.get('page')
        g = paginator.get_page(page_number)

        contexto = {"datos":g}
        return render(request, 'geprapapp/garantia/listarGarantia.html', contexto)
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para ver las garantías...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def formularioGarantia(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A" or login[1] == "C" ): 
        p = Pedido.objects.all()
        contexto = {"pedido":p}
        return render(request, 'geprapapp/garantia/nuevaGarantia.html', contexto)
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def guardarGarantia(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            if request.method == "POST":
                g = Garantia(
                    fechaGarantia = request.POST["fechaGarantia"],
                    descripcion = request.POST["descripcion"],
                    pedido = Pedido.objects.get(pk = request.POST["pedido"])
                )
                g.save()
                messages.success(request, "Garantía guardada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarGarantias')
    elif login and (login[1] == "C"):
        try:
            if request.method == "POST":
                g = Garantia(
                    fechaGarantia = request.POST["fechaGarantia"],
                    descripcion = request.POST["descripcion"],
                    pedido = Pedido.objects.get(pk = request.POST["pedido"])
                )
                g.save()
                messages.success(request, f"Garantía Enviada satisfactoriamente!!\nSe enviara una respuesta al correo electrónico registrado lo mas pronto posible")
            else:
                messages.warning(request, "Usted no ha enviado datos....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def edicionGarantia(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        g = Garantia.objects.get(pk = id)
        p = Pedido.objects.all()
        contexto = {"pedido": p, "garantia": g}
        return render(request, 'geprapapp/garantia/edicionGarantia.html', contexto)
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para editar las garantías...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def editarGarantia(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"):              
        try:
            if request.method == "POST":
                g = Garantia.objects.get(pk = request.POST["id"])
                p = Pedido.objects.get(pk = request.POST["pedido"])

                g.fechaGarantia = request.POST["fechaGarantia"]
                g.descripcion = request.POST["descripcion"]
                g.pedido = p
                g.save()
                messages.success(request, "Garantía actualizada correctamente!!")
            else:
                messages.warning(request, "Usted no ha enviado datos....")         
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarGarantias')
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para editar las garantías...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def eliminarGarantia(request, id):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        try:
            g = Garantia.objects.get(pk = id)
            g.delete()
            messages.success(request, "Garantía eliminada correctamente!!")
        except IntegrityError:
            messages.warning(request, "No puede eliminar esta Garantía porque otros registros están relacionados con ella....")
        except Exception as e :
            messages.error(request, f"Error: {e}")
        return redirect('geprapapp:listarGarantias')
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para eliminar las garantías...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')

def buscarGarantia(request):
    login = request.session.get('logueo', False)
    if login and (login[1] == "A"): 
        if request.method == "POST":
            dato = request.POST["buscar"]
            g = Garantia.objects.filter( Q(id__icontains = dato) | Q(fechaGarantia__icontains = dato))
                
            paginator = Paginator(g, 4) # Mostrar 4 registros por página...
            page_number = request.GET.get('page')
            #Sobreescribir la salida de la consulta.......
            g = paginator.get_page(page_number)
                    
            contexto = { "datos": g }
            return render(request, 'geprapapp/garantia/listar_garantia_ajax.html', contexto)
        else:
            messages.error(request, "Error no envió datos...")
            return redirect('geprapapp:listarGarantias')
    elif login and (login[1] == "C"): 
        messages.warning(request, "No tiene permiso para buscar garantías...")
        return redirect('geprapapp:index')
    else:
        if login and(login[1] != "A" or login[1] != "C"):
            messages.warning(request, "No tiene acceso al módulo de garantías...")
            return redirect('geprapapp:index')
        else:
            messages.warning(request, "Inicie sesión...")
            return redirect('geprapapp:loginFormulario')
