# Rutas de compra
# Este archivo maneja la logica de insertar dinero, comprar y cancelar

from flask import Blueprint, jsonify, request
import json
import os
from models.product import tiene_stock, reducir_stock
from models.transaction import crear_transaccion

# Creamos el blueprint de compras
purchase_bp = Blueprint('purchase', __name__)

# Rutas de los archivos JSON
RUTA_PRODUCTOS = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
RUTA_TRANSACCIONES = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.json')

# Variable global que guarda el dinero insertado por el usuario
dinero_insertado = 0.0

# --- FUNCIONES AUXILIARES ---

def leer_productos():
    archivo = open(RUTA_PRODUCTOS, 'r', encoding='utf-8')
    datos = json.load(archivo)
    archivo.close()
    return datos

def guardar_productos(datos):
    archivo = open(RUTA_PRODUCTOS, 'w', encoding='utf-8')
    json.dump(datos, archivo, ensure_ascii=False, indent=2)
    archivo.close()

def leer_transacciones():
    archivo = open(RUTA_TRANSACCIONES, 'r', encoding='utf-8')
    contenido = archivo.read().strip()
    archivo.close()
    if not contenido:
        return {"transacciones": []}
    return json.loads(contenido)

def guardar_transaccion(transaccion):
    datos = leer_transacciones()
    datos["transacciones"].append(transaccion)
    archivo = open(RUTA_TRANSACCIONES, 'w', encoding='utf-8')
    json.dump(datos, archivo, ensure_ascii=False, indent=2)
    archivo.close()

# --- ENDPOINTS ---

# POST /insertar-dinero
# El usuario inserta una moneda o billete
@purchase_bp.route('/insertar-dinero', methods=['POST'])
def insertar_dinero():
    global dinero_insertado
    cuerpo = request.get_json()
    monto = cuerpo.get('monto', 0)
    dinero_insertado = dinero_insertado + monto
    return jsonify({"dinero_insertado": dinero_insertado})

# POST /comprar/<id>
# El usuario selecciona un producto para comprar
@purchase_bp.route('/comprar/<int:producto_id>', methods=['POST'])
def comprar(producto_id):
    global dinero_insertado

    # Leemos los productos del archivo
    datos = leer_productos()
    lista_productos = datos["productos"]

    # Buscamos el producto seleccionado
    producto_encontrado = None
    for p in lista_productos:
        if p["id"] == producto_id:
            producto_encontrado = p

    # Si no existe el producto
    if producto_encontrado is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Verificamos si hay stock
    if not tiene_stock(producto_encontrado):
        return jsonify({"error": "Producto sin stock"}), 400

    # Verificamos si el dinero es suficiente
    if dinero_insertado < producto_encontrado["precio"]:
        return jsonify({"error": "Dinero insuficiente"}), 400

    # Calculamos el vuelto
    vuelto = round(dinero_insertado - producto_encontrado["precio"], 2)

    # Reducimos el stock del producto
    reducir_stock(producto_encontrado)

    # Actualizamos el stock en la lista
    for p in lista_productos:
        if p["id"] == producto_id:
            p["stock"] = producto_encontrado["stock"]

    # Guardamos los productos actualizados
    guardar_productos(datos)

    # Creamos y guardamos la transaccion
    total_transacciones = len(leer_transacciones()["transacciones"])
    nueva_transaccion = crear_transaccion(
        id = total_transacciones + 1,
        producto_id = producto_id,
        monto_pagado = dinero_insertado,
        vuelto = vuelto
    )
    guardar_transaccion(nueva_transaccion)

    # Reiniciamos el dinero insertado
    dinero_insertado = 0.0

    nombre_producto = producto_encontrado["nombre"] + " " + producto_encontrado["marca"]
    return jsonify({
        "mensaje": "Compra exitosa: " + nombre_producto,
        "vuelto": vuelto
    })

# para cancelar la compra
# El usuario cancela y recupera su dinero
@purchase_bp.route('/cancelar', methods=['GET'])
def cancelar():
    global dinero_insertado
    monto_devuelto = dinero_insertado
    dinero_insertado = 0.0
    return jsonify({"devuelto": monto_devuelto})