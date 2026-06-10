class Producto:
    def __init__(self, id, nombre, marca, precio, stock):
        self.id = id
        self.nombre = nombre
        self.marca = marca
        self.precio = precio
        self.stock = stock

    def tiene_stock(self):
        return self.stock > 0

    def reducir_stock(self):
        if self.tiene_stock():
            self.stock -= 1
            return True
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "marca": self.marca,
            "precio": self.precio,
            "stock": self.stock
        }