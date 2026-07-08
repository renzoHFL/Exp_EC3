# Modelo de Producto
# Un producto tiene: id, nombre, marca, precio y stock

def crear_producto(id, nombre, marca, precio, stock):
    producto = {
        "id": id,
        "nombre": nombre,
        "marca": marca,
        "precio": precio,
        "stock": stock
    }
    return producto

def tiene_stock(producto):
    if producto["stock"] > 0:
        return True
    else:
        return False

def reducir_stock(producto):
    if tiene_stock(producto):
        producto["stock"] = producto["stock"] - 1
        return True
    else:
        return False

def producto_a_diccionario(producto):
    resultado = {
        "id": producto["id"],
        "nombre": producto["nombre"],
        "marca": producto["marca"],
        "precio": producto["precio"],
        "stock": producto["stock"]
    }
    return resultado