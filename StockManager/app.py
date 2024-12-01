from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/ecommerce")
mongo = PyMongo(app)

@app.route('/api/health')
def health_check():
    try:
        mongo.db.command('ping')
        return jsonify({
            "status": "healthy",
            "service": "StockManager",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "StockManager",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/api/stock/<product_id>', methods=['GET'])
def get_stock(product_id):
    try:
        stock = mongo.db.stock.find_one({'product_id': product_id})
        if stock:
            stock['_id'] = str(stock['_id'])
            return jsonify(stock)
        return jsonify({'quantity': 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stock/<product_id>', methods=['PUT'])
def update_stock(product_id):
    try:
        data = request.get_json()
        if 'quantity' not in data:
            return jsonify({"error": "Quantity is required"}), 400
            
        if not isinstance(data['quantity'], int) or data['quantity'] < 0:
            return jsonify({"error": "Invalid quantity value"}), 400

        result = mongo.db.stock.update_one(
            {'product_id': product_id},
            {'$set': {'quantity': data['quantity']}},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stock/batch', methods=['POST'])
def check_stock_batch():
    try:
        data = request.get_json()
        if not data or 'product_ids' not in data:
            return jsonify({"error": "Product IDs are required"}), 400

        product_ids = data['product_ids']
        stock_levels = {}
        for product_id in product_ids:
            stock = mongo.db.stock.find_one({'product_id': product_id})
            stock_levels[product_id] = stock['quantity'] if stock else 0
        return jsonify(stock_levels)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stock/reserve', methods=['POST'])
def reserve_stock():
    try:
        data = request.get_json()
        if not data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({"error": "Product ID and quantity are required"}), 400

        product_id = data['product_id']
        quantity = data['quantity']

        stock = mongo.db.stock.find_one({'product_id': product_id})
        if not stock or stock['quantity'] < quantity:
            return jsonify({"error": "Insufficient stock"}), 400

        result = mongo.db.stock.update_one(
            {'product_id': product_id},
            {'$inc': {'quantity': -quantity}}
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)