def total_carrito(request):
    total=0
    if request.session.__contains__("carrito"): 
        for key, value in request.session["carrito"].items():
            total=total+float(value["precio"])
        
    return {"total_carrito":total}   

  
            