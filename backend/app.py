from flask import Flask
from flask_cors import CORS
from routes.products import products_bp
from routes.purchase import purchase_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(products_bp)
app.register_blueprint(purchase_bp)

if __name__ == "__main__":
    app.run(debug=True)