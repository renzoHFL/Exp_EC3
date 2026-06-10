from flask import Blueprint, jsonify, request
import json
import os
from models.product import Producto
from models.transaction import Transaccion

purchase_bp = Blueprint('purchase', __name__)

PRODUCTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')
TRANSACTIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'transactions.json')

dinero_insertado = 0.0

def leer_productos():
    with open(PRODUCTS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_productos(data):
    with open(PRODUCTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def leer_transacciones():
    with open(TRANSACTIONS_PATH, 'r', encoding='utf-8') as f:
        contenido = f.read().strip()
        if not contenido:
            return {"transacciones": []}
        return json.loads(contenido)

def guardar_transaccion(transaccion):
    data = leer_transacciones()
    data["transacciones"].append(transaccion.to_dict())
    with open(TRANSACTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@purchase_bp.route('/insertar-dinero', methods=['POST'])
def insertar_dinero():
    global dinero_insertado
    body = request.get_json()
    monto = body.get('monto', 0)
    dinero_insertado += monto
    return jsonify({"dinero_insertado": dinero_insertado})

@purchase_bp.route('/comprar/<int:producto_id>', methods=['POST'])
def comprar(producto_id):
    global dinero_insertado
    data = leer_productos()
    productos = data["productos"]

    producto = next((p for p in productos if p["id"] == producto_id), None)

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404

    p = Producto(**producto)

    if not p.tiene_stock():
        return jsonify({"error": "Producto sin stock"}), 400

    if dinero_insertado < p.precio:
        return jsonify({"error": "Dinero insuficiente"}), 400

    vuelto = round(dinero_insertado - p.precio, 2)
    p.reducir_stock()

    for prod in productos:
        if prod["id"] == producto_id:
            prod["stock"] = p.stock

    guardar_productos(data)

    transaccion = Transaccion(
        id=len(leer_transacciones()["transacciones"]) + 1,
        producto_id=producto_id,
        monto_pagado=dinero_insertado,
        vuelto=vuelto
    )
    guardar_transaccion(transaccion)

    dinero_insertado = 0.0

    return jsonify({
        "mensaje": f"Compra exitosa: {p.nombre} {p.marca}",
        "vuelto": vuelto
    })

@purchase_bp.route('/cancelar', methods=['GET'])
def cancelar():
    global dinero_insertado
    devuelto = dinero_insertado
    dinero_insertado = 0.0
    return jsonify({"devuelto": devuelto})