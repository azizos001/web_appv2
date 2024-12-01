from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

PRODUCT_SERVICE_URL = "http://product-catalogue:5001"
STOCK_SERVICE_URL = "http://stock-manager:5002"
USER_SERVICE_URL = "http://user-profile:5003"

@app.route('/')
def home():
    try:
        # Fetch products from ProductCatalogue service
        products_response = requests.get(f"{PRODUCT_SERVICE_URL}/api/products")
        products = products_response.json() if products_response.ok else []
        return render_template('index.html', products=products)
    except requests.RequestException:
        return render_template('index.html', products=[])

@app.route('/products')
def products():
    try:
        products_response = requests.get(f"{PRODUCT_SERVICE_URL}/api/products")
        products = products_response.json() if products_response.ok else []
        return render_template('products.html', products=products)
    except requests.RequestException:
        return render_template('products.html', products=[])

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "ShopFront",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)