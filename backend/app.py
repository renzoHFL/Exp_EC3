# Archivo principal del servidor Flask
# Aqui se crea la aplicacion y se registran las rutas

from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.products import products_bp
from routes.purchase import purchase_bp
import os

# Creamos la aplicacion Flask
app = Flask(__name__)

# Habilitamos CORS para que el frontend pueda comunicarse con el backend
CORS(app)

# Registramos las rutas de productos y compras
app.register_blueprint(products_bp)
app.register_blueprint(purchase_bp)

# Ruta donde esta el frontend
CARPETA_FRONTEND = os.path.join(os.path.dirname(__file__), '..', 'frontend')

# Ruta principal - muestra la pagina web
@app.route('/')
def index():
    return send_from_directory(CARPETA_FRONTEND, 'index.html')

# Ruta para los archivos estaticos (CSS, JS, imagenes)
@app.route('/<path:nombre_archivo>')
def archivos_estaticos(nombre_archivo):
    return send_from_directory(CARPETA_FRONTEND, nombre_archivo)

# Iniciamos el servidor
if __name__ == "__main__":
    app.run(debug=True)