from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime
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
            "service": "UserProfile",
            "database": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "service": "UserProfile",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/api/profile/<user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        profile = mongo.db.users.find_one({'user_id': user_id})
        if profile:
            profile['_id'] = str(profile['_id'])
            return jsonify(profile)
        return jsonify({'error': 'Profile not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/profile/<user_id>', methods=['PUT'])
def update_profile(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        data['updated_at'] = datetime.utcnow()
        result = mongo.db.users.update_one(
            {'user_id': user_id},
            {'$set': data},
            upsert=True
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/profile/<user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    try:
        orders = list(mongo.db.orders.find({'user_id': user_id}))
        for order in orders:
            order['_id'] = str(order['_id'])
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/profile/<user_id>/orders', methods=['POST'])
def create_order(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ['items', 'total_amount', 'shipping_address']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        order = {
            'user_id': user_id,
            'items': data['items'],
            'total_amount': data['total_amount'],
            'shipping_address': data['shipping_address'],
            'status': 'pending',
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db.orders.insert_one(order)
        return jsonify({'order_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)