db = db.getSiblingDB('ecommerce');

// Create collections with validation
db.createCollection('products', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'price', 'description', 'category'],
      properties: {
        name: { bsonType: 'string' },
        price: { bsonType: 'number', minimum: 0 },
        description: { bsonType: 'string' },
        category: { bsonType: 'string' },
        image: { bsonType: 'string' }
      }
    }
  }
});

db.createCollection('stock', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['product_id', 'quantity'],
      properties: {
        product_id: { bsonType: 'string' },
        quantity: { bsonType: 'int', minimum: 0 }
      }
    }
  }
});

db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'email'],
      properties: {
        user_id: { bsonType: 'string' },
        email: { bsonType: 'string' },
        name: { bsonType: 'string' },
        address: { bsonType: 'string' },
        phone: { bsonType: 'string' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

// Insert some sample products
db.products.insertMany([
  {
    name: 'Premium Wireless Headphones',
    price: 199.99,
    description: 'High-quality wireless headphones with noise cancellation',
    category: 'Electronics',
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80'
  },
  {
    name: 'Smart Watch Pro',
    price: 299.99,
    description: 'Advanced smartwatch with health monitoring features',
    category: 'Electronics',
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80'
  },
  {
    name: 'Designer Backpack',
    price: 79.99,
    description: 'Stylish and functional backpack for everyday use',
    category: 'Fashion',
    image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80'
  }
]);