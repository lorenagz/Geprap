from unicodedata import name
from django.urls import path
from . import views

app_name= "geprapapp"
urlpatterns = [
    path('', views.index, name = "index"),

    #Login----------------------------------------------------------------------------------------
    path('loginFormulario/', views.loginFormulario, name="loginFormulario" ),
    path('login/', views.login, name="login" ),
    path('logout/', views.logout, name="logout" ),
     
    #Restablecer contraseña------------------------------------------------------------------------
    path('solicitudRestablecer/',views.solicitudRestablecer, name="solicitudRestablecer"),
    path('restablecer/',views.restablecerContrasena, name="restablecerContrasena"), 
    path('restablecerContrasena/<int:id>',views.cambiarContrasena, name="cambiarContrasena"),
    path('cambiarClave/',views.cambiarClave, name="cambiarClave"),

    # Usuarios--------------------------------------------------------------------------------------
    path('usuarios/', views.listaUsuarios, name="listarUsuarios"),
    path('formularioUsuario/', views.formularioUsuario, name="formularioUsuario"),
    path('guardarUsuario/',views.guardarUsuario, name="guardarUsuario"),
    path('edicionUsuario/<id>', views.edicionUsuario,name="edicionUsuario"),
    path('editarUsuario/', views.editarUsuario, name="editarUsuario"),
    path('eliminarUsuario/<id>', views.eliminarUsuario, name="eliminarUsuario"),
    path('buscarUsuario/', views.buscarUsuario, name="buscarUsuario"), 

    #Registrar cliente-------------------------------------------------------------------------------
    #path('formularioRegistro/', views.formularioRegistro, name="formularioRegistro"),
    #path('guardarRegistro/',views.guardarRegistro, name="guardarRegistro"),

    # Categoría--------------------------------------------------------------------------------------
    path('categorias/', views.listaCategoria, name="listarCategoria"),
    path('formularioCategoria/', views.formularioCategoria, name="formularioCategoria"),
    path('guardarCategoria/',views.guardarCategoria, name="guardarCategoria"),
    path('edicionCategoria/<id>', views.edicionCategoria, name="edicionCategoria"),
    path('editarCategoria/', views.editarCategoria, name="editarCategoria"),
    path('eliminarCategoria/<id>', views.eliminarCategoria, name="eliminarCategoria"),
    path('buscarCategoria/', views.buscarCategoria, name="buscarCategoria"),

    # Productos----------------------------------------------------------------------------------------
    path('productos/', views.listaProducto, name="listarProductos"),
    path('formularioProducto/', views.formularioProducto, name="formularioProducto"),
    path('guardarProducto/',views.guardarProducto, name="guardarProducto"),
    path('edicionProducto/<id>', views.edicionProducto, name="edicionProducto"),
    path('editarProducto/', views.editarProducto, name="editarProducto"),
    path('eliminarProducto/<id>', views.eliminarProducto, name="eliminarProducto"),
    path('buscarProducto/', views.buscarProducto, name="buscarProducto"),
    
    # Servicio------------------------------------------------------------------------------------------
    path('servicios/', views.listaServicio, name="listarServicio"),
    path('formularioServicio/', views.formularioServicio, name="formularioServicio"),
    path('guardarServicio/',views.guardarServicio, name="guardarServicio"),
    path('edicionServicio/<id>', views.edicionServicio, name="edicionServicio"),
    path('editarServicio/', views.editarServicio, name="editarServicio"),
    path('eliminarServicio/<id>', views.eliminarServicio, name="eliminarServicio"),
    path('buscarServicio/', views.buscarServicio, name="buscarServicio"),

    # Pedidos--------------------------------------------------------------------------------------------
    path('pedidos/', views.listaPedido, name="listarPedidos"),
    path('formularioPedido/', views.formularioPedido, name="formularioPedido"),
    path('guardarPedido/',views.guardarPedido, name="guardarPedido"),
    path('edicionPedido/<id>', views.edicionPedido, name="edicionPedido"),
    path('editarPedido/', views.editarPedido, name="editarPedido"),
    path('eliminarPedido/<id>', views.eliminarPedido, name="eliminarPedido"),
    path('buscarPedido/', views.buscarPedido, name="buscarPedido"),

    # DetallePedidos---------------------------------------------------------------------------------------
    path('DetallePedidos/', views.listaDetallePedido, name="listarDetallePedidos"),
    path('formularioDetallePedido/', views.formularioDetallePedido, name="formularioDetallePedido"),
    path('guardarDetallePedido/',views.guardarDetallePedido, name="guardarDetallePedido"),
    path('edicionDetallePedido/<id>', views.edicionDetallePedido, name="edicionDetallePedido"),
    path('editarDetallePedido/', views.editarDetallePedido, name="editarDetallePedido"),
    path('eliminarDetallePedido/<id>', views.eliminarDetallePedido, name="eliminarDetallePedido"),
    path('buscarDetallePedido/', views.buscarDetallePedido, name="buscarDetallePedido"),

    # Agenda-------------------------------------------------------------------------------------------------
    path('agenda/', views.listaAgenda, name="listarAgenda"),
    path('formularioAgenda/', views.formularioAgenda, name="formularioAgenda"),
    path('guardarAgenda/',views.guardarAgenda, name="guardarAgenda"),
    path('edicionAgenda/<id>', views.edicionAgenda, name="edicionAgenda"),
    path('editarAgenda/', views.editarAgenda, name="editarAgenda"),
    path('eliminarAgenda/<id>', views.eliminarAgenda, name="eliminarAgenda"),
    path('buscarAgenda/', views.buscarAgenda, name="buscarAgenda"),

    # Metodo_Pago--------------------------------------------------------------------------------------------
    path('metodosPago/', views.listaMetodoPago, name="listarMetodoPago"),
    path('formularioMetodoPago/', views.formularioMetodoPago, name="formularioMetodoPago"),
    path('guardarMetodoPago/',views.guardarMetodoPago, name="guardarMetodoPago"),
    path('edicionMetodoPago/<id>', views.edicionMetodoPago, name="edicionMetodoPago"),
    path('editarMetodoPago/', views.editarMetodoPago, name="editarMetodoPago"),
    path('eliminarMetodoPago/<id>', views.eliminarMetodoPago, name="eliminarMetodoPago"),
    path('buscarMetodoPago/', views.buscarMetodoPago, name="buscarMetodoPago"),

    # Pagos--------------------------------------------------------------------------------------------------
    path('pagos/', views.listaPagos, name="listarPagos"),
    path('formularioPagos/', views.formularioPagos, name="formularioPagos"),
    path('guardarPagos/',views.guardarPagos, name="guardarPago"),
    path('edicionPago/<id>', views.edicionPago, name="edicionPago"),
    path('editarPago/', views.editarPago, name="editarPago"),
    path('eliminarPago/<id>', views.eliminarPago, name="eliminarPago"),
    path('buscarPago/', views.buscarPago, name="buscarPago"),

   # Evaluación----------------------------------------------------------------------------------------------
    path('evaluaciones/', views.listaEvaluacion, name="listarEvaluaciones"),
    path('formularioEvaluacion/', views.formularioEvaluacion, name="formularioEvaluacion"),
    path('guardarEvaluacion/',views.guardarEvaluacion, name="guardarEvaluacion"),
    path('edicionEvaluacion/<id>', views.edicionEvaluacion, name="edicionEvaluacion"),
    path('editarEvaluacion/', views.editarEvaluacion, name="editarEvaluacion"),
    path('eliminarEvaluacion/<id>', views.eliminarEvaluacion, name="eliminarEvaluacion"),
    path('buscarEvaluacion/', views.buscarEvaluacion, name="buscarEvaluacion"),

   # Garantía-------------------------------------------------------------------------------------------------
   path('garantia/', views.listaGarantia, name="listarGarantias"),
   path('formularioGarantia/', views.formularioGarantia, name="formularioGarantia"),
   path('guardarGarantia/',views.guardarGarantia, name="guardarGarantia"),
   path('edicionGarantia/<id>', views.edicionGarantia, name="edicionGarantia"),
   path('editarGarantia/', views.editarGarantia, name="editarGarantia"),
   path('eliminarGarantia/<id>', views.eliminarGarantia, name="eliminarGarantia"),
   path('buscarGarantia/', views.buscarGarantia, name="buscarGarantia"),
]

