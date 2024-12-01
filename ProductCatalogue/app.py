from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId
import os

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/ecommerce")
mongo = PyMongo(app)

@app.route('/api/health')
def health_check():
    try:
        # Test MongoDB connection
        mongo.db.command('ping')
        return jsonify({
            "status": "healthy",
            "service": "ProductCatalogue",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "ProductCatalogue",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = list(mongo.db.products.find())
        for product in products:
            product['_id'] = str(product['_id'])
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<id>', methods=['GET'])
def get_product(id):
    try:
        product = mongo.db.products.find_one({'_id': ObjectId(id)})
        if product:
            product['_id'] = str(product['_id'])
            return jsonify(product)
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ['name', 'price', 'description', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = mongo.db.products.insert_one(data)
        return jsonify({'_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    try:
        products = list(mongo.db.products.find({'category': category}))
        for product in products:
            product['_id'] = str(product['_id'])
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)