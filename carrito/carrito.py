class Carrito:
    def __init__(self,request):#se hace el request o peticion
        self.request = request
        self.session = request.session  #se iguala la session del user con el carrito
        carrito=self.session.get('carrito')
        if not carrito:                  #si no hay carrito lo crea
            carrito= self.session['carrito']= {}
        
        self.carrito=carrito  #si hay lo iguala 
            
            
    def agregar(self,producto):
        if(str(producto.id) not in self.carrito.keys()):
            self.carrito[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "descripcion":producto.descripcion,
                "precio":str(producto.precio),#se convierta a string
                #"categoria":producto.categoria,
                "cantidad": 1,
               # "imagen":producto.imagen.url #carpeta de imagenes
                    
            }
        else:
            for key, value in self.carrito.items():#para saber si ya lo ha agregado al carrito
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    value["precio"]= float(value["precio"])+producto.precio
                    break
        
        self.guardar_carrito()
        
    def guardar_carrito(self):
        self.session["carrito"]=self.carrito
        self.session.modified=True
        
        
    def eliminar(self,producto):
        producto.id = str(producto.id)
        if producto.id in self.carrito:
            del self.carrito[producto.id]
            self.guardar_carrito()
    
    
    def restar_producto(self,producto):
            for key, value in self.carrito.items():
                if key==str(producto.id):
                    value["cantidad"]=value["cantidad"]-1#para restar el producto del carrito
                    value["precio"]= float(value["precio"])-producto.precio
                    if value["cantidad"]<1: #para saber si hay algo en el carrito para eliminar
                        self.eliminar(producto)
                    break
            self.guardar_carrito()
            
        
    def limpiar_carrito(self):
        self.session["carrito"]={}
        self.session.modified=True            
            
            
                    
                    
                    
            
                        