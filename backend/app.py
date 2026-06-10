from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.products import products_bp
from routes.purchase import purchase_bp
import os

app = Flask(__name__)
CORS(app)

app.register_blueprint(products_bp)
app.register_blueprint(purchase_bp)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)