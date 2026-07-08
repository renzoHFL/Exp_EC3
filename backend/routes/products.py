# Rutas de productos
# Este archivo maneja todo lo relacionado a mostrar productos

from flask import Blueprint, jsonify
import json
import os

# Creamos el blueprint de productos
products_bp = Blueprint('products', __name__)

# Ruta donde esta guardado el archivo de productos
RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')

# Funcion para leer los productos del archivo JSON
def leer_productos():
    archivo = open(RUTA_PRODUCTOS, 'r', encoding='utf-8')
    datos = json.load(archivo)
    archivo.close()
    return datos

# Endpoint GET /productos
# Devuelve la lista completa de productos
@products_bp.route('/productos', methods=['GET'])
def get_productos():
    datos = leer_productos()
    return jsonify(datos)