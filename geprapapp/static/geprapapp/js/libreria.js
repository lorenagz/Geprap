function buscarUsuario(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarCategoria(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarProducto(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarPedido(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarDetallePedido(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarProductoPedido(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarServicio(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarServicioPedido(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarVenta(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarAgenda(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarFactura(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarMetodoPago(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarPago(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarEvaluacion(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}

function buscarGaratntia(url){
    respuesta = $('#respuesta');
    buscar = $('#buscar').val();
    token = $('input[name="csrfmiddlewaretoken"]').val();
    
    $.ajax({
        url: url,
        type: 'post',
        data: { "buscar": buscar, "csrfmiddlewaretoken": token},
        //dataType: 'json',
        success: function(r){
            respuesta.html(r);
        },
        error: function(error){
            console.log("Error" + error);
        }
    });
}