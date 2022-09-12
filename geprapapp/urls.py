from unicodedata import name
from django.urls import path
from . import views

app_name= "geprapapp"
urlpatterns = [
    path('', views.index, name = "index"),
    # rol--------------------------------------------------------------------------
    path('roles/', views.listaRol, name="listarRol"),
    path('formularioRol/', views.formularioRol, name="formularioRol"),
    path('guardarRol/',views.guardarRol, name="guardarRol"),
    path('edicionRol/<id>', views.edicionRol ,name="edicionRol"),
    path('editarRol/', views.editarRol, name="editarRol"),
    path('eliminarRol/<id>', views.eliminarRol, name="eliminarRol"),

    # permisos----------------------------------------------------------------------
    path('permisos/', views.listaPermiso, name="listarPermiso"),
    path('formularioPermiso/', views.formularioPermiso, name="formularioPermiso"),
    path('guardarPermiso/',views.guardarPermiso, name="guardarPermiso"),
    path('edicionPermiso/<id>', views.edicionPermiso ,name="edicionPermiso"),
    path('editarPermiso/', views.editarPermiso, name="editarPermiso"),
    path('eliminarPermiso/<id>', views.eliminarPermiso, name="eliminarPermiso"),

    # permisosRol----------------------------------------------------------------------
    path('permisosRol/', views.listaPermisoRol, name="listarPermisoRol"),
    path('formularioPermisoRol/', views.formularioPermisoRol, name="formularioPermisoRol"),
    path('guardarPermisoRol/',views.guardarPermisoRol, name="guardarPermisoRol"),
]