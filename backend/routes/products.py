from flask import Blueprint, jsonify
import json
import os

products_bp = Blueprint('products', __name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')

def leer_productos():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@products_bp.route('/productos', methods=['GET'])
def get_productos():
    data = leer_productos()
    return jsonify(data)