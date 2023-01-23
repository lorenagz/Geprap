def total_carrito(request):
    total=0
    # if request.user.is_authenticated: // para cuando se este logeado o auntenticado
    for key, value in request.session["carrito"].items():
        total=total+float(value["precio"])
    return {"total_carrito":total}   

  
            