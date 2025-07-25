#!/usr/bin/env python3
"""
Flask web application that serves the Next.js frontend and provides API endpoints
for the grocery optimization platform. Integrates the GroceryOptimizationApp logic.
"""

import os
import sys
import uuid
from datetime import datetime, timezone
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

sys.path.append(os.path.join(os.path.dirname(__file__), 'Database'))

from Database import db_utils
from Database.user import User
from Database.list import GroceryList
from kroger import KrogerAPI

class GroceryOptimizationApp:
    """Main application class for grocery optimization platform - from main.py"""
    
    def __init__(self):
        """Initialize the application."""
        self.kroger_api = KrogerAPI()
        self.current_user = None
        self.current_list = None
        
    def find_user_by_email(self, email):
        """Check if user exists by email."""
        conn = db_utils.get_db_connection()
        if conn is None:
            return None
            
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM users WHERE email = %s;", (email,))
                result = cur.fetchone()
                if result:
                    user_id = result[0]
                    return db_utils.get_user_by_id(user_id)
                return None
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None
        finally:
            conn.close()
    
    def create_new_user(self, email, password):
        """Create a new user with unique ID."""
        user_id = str(uuid.uuid4())
        username = email.split('@')[0]
        
        user = User(
            user_ID=user_id,
            username=username,
            email=email,
            password=password,
            list_of_list_ids=[],
            access_token=None,
            refresh_token=None,
            token_type=None,
            token_expiry=None,
            preferred_location="98075"
        )
        
        if db_utils.add_user_to_db(user):
            return user
        return None
    
    def get_or_create_user(self, email, password):
        """Get existing user or create new one."""
        existing_user = self.find_user_by_email(email)
        
        if existing_user:
            return existing_user
        else:
            return self.create_new_user(email, password)
    
    def get_user_grocery_lists(self, user_id):
        """Fetch existing grocery lists for user."""
        list_ids = db_utils.get_grocery_list_ids_for_user(user_id)
        
        if list_ids:
            lists = []
            for list_id in list_ids:
                grocery_list = db_utils.get_grocery_list_details(list_id)
                if grocery_list:
                    lists.append(grocery_list)
            return lists
        else:
            return []
    
    def create_new_grocery_list(self, user_id):
        """Create a new grocery list for the user."""
        list_id = str(uuid.uuid4())
        
        grocery_list = GroceryList(
            list_ID=list_id,
            user_ID=user_id,
            timestamp=datetime.now(timezone.utc),
            products_on_list=[]
        )
        
        if db_utils.add_grocery_list_to_db(grocery_list):
            return grocery_list
        return None
    
    def get_or_create_grocery_list(self, user_id):
        """Get existing grocery list or create new one."""
        existing_lists = self.get_user_grocery_lists(user_id)
        
        if existing_lists:
            return existing_lists[0]
        else:
            return self.create_new_grocery_list(user_id)
    
    def search_products(self, search_term, limit=5):
        """Search for products using Kroger API."""
        try:
            products = self.kroger_api.productSearch(search_term, limit=limit)
            return products
        except Exception as e:
            print(f"Error searching for products: {e}")
            return []
    
    def add_product_to_list(self, grocery_list, product, quantity=1):
        """Add a product to grocery list."""
        grocery_list.products_on_list.append((product, quantity))
        
        if db_utils.add_grocery_list_to_db(grocery_list):
            return True
        return False

# Initialize Flask app
app = Flask(
    __name__,
    static_folder='../frontend/out',
    static_url_path=''
)

# Enable CORS for all domains and routes
CORS(app)

# Initialize the grocery optimization app instance
grocery_app = GroceryOptimizationApp()

# Database setup on startup
def init_database():
    """Initialize database tables if they don't exist."""
    try:
        conn = db_utils.get_db_connection()
        if conn:
            conn.close()
            print("✅ Database connection verified")
        else:
            print("❌ Database connection failed")
    except Exception as e:
        print(f"Database initialization error: {e}")

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if db_utils.get_db_connection() else 'disconnected',
        'kroger_api': 'connected' if grocery_app.kroger_api._service_token else 'disconnected'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User authentication endpoint."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = grocery_app.get_or_create_user(email, password)
        
        if user:
            return jsonify({
                'success': True,
                'user': {
                    'id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'preferred_location': user.preferred_location
                }
            })
        else:
            return jsonify({'error': 'Failed to authenticate or create user'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Authentication failed: {str(e)}'}), 500

@app.route('/api/products/search', methods=['POST'])
def search_products():
    """Search for products using Kroger API."""
    try:
        data = request.get_json()
        search_term = data.get('query', '').strip()
        limit = data.get('limit', 5)
        
        if not search_term:
            return jsonify({'error': 'Search query is required'}), 400
        
        products = grocery_app.search_products(search_term, limit=limit)
        
        # Convert products to JSON-serializable format
        product_list = []
        for product in products:
            product_list.append({
                'name': product.name,
                'price': float(product.price) if product.price else None,
                'promo_price': float(product.promo_price) if product.promo_price else None,
                'brand': product.brand,
                'upc': product.upc,
                'size': product.size,
                'inventory': product.inventory,
                'fulfillment_type': product.fufillment_type,
                'location_id': product.location_ID
            })
        
        return jsonify({
            'success': True,
            'products': product_list,
            'count': len(product_list)
        })
        
    except Exception as e:
        return jsonify({'error': f'Product search failed: {str(e)}'}), 500

@app.route('/api/lists', methods=['POST'])
def create_list():
    """Create a new grocery list."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        grocery_list = grocery_app.create_new_grocery_list(user_id)
        
        if grocery_list:
            return jsonify({
                'success': True,
                'list': {
                    'id': grocery_list.list_id,
                    'user_id': grocery_list.user_id,
                    'timestamp': grocery_list.timestamp.isoformat(),
                    'items': []
                }
            })
        else:
            return jsonify({'error': 'Failed to create grocery list'}), 500
            
    except Exception as e:
        return jsonify({'error': f'List creation failed: {str(e)}'}), 500

@app.route('/api/lists/<list_id>/items', methods=['POST'])
def add_item_to_list(list_id):
    """Add an item to a grocery list."""
    try:
        data = request.get_json()
        
        # Get the grocery list
        grocery_list = db_utils.get_grocery_list_details(list_id)
        if not grocery_list:
            return jsonify({'error': 'Grocery list not found'}), 404
        
        # Search for the product
        search_term = data.get('item_name')
        if not search_term:
            return jsonify({'error': 'Item name is required'}), 400
        
        products = grocery_app.search_products(search_term, limit=1)
        if not products:
            return jsonify({'error': 'Product not found'}), 404
        
        product = products[0]
        quantity = data.get('quantity', 1)
        
        # Add product to list using the existing method
        if grocery_app.add_product_to_list(grocery_list, product, quantity):
            return jsonify({
                'success': True,
                'item': {
                    'name': product.name,
                    'price': float(product.price) if product.price else None,
                    'brand': product.brand,
                    'upc': product.upc,
                    'quantity': quantity
                }
            })
        else:
            return jsonify({'error': 'Failed to add item to list'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to add item: {str(e)}'}), 500

@app.route('/api/lists/user/<user_id>', methods=['GET'])
def get_user_lists(user_id):
    """Get all grocery lists for a user."""
    try:
        lists = grocery_app.get_user_grocery_lists(user_id)
        
        result_lists = []
        for grocery_list in lists:
            # Calculate total cost
            total_cost = 0
            items = []
            for product, quantity in grocery_list.products_on_list:
                item_cost = float(product.price) * quantity if product.price else 0
                total_cost += item_cost
                items.append({
                    'name': product.name,
                    'price': float(product.price) if product.price else None,
                    'brand': product.brand,
                    'upc': product.upc,
                    'quantity': quantity,
                    'subtotal': item_cost
                })
            
            result_lists.append({
                'id': grocery_list.list_id,
                'timestamp': grocery_list.timestamp.isoformat(),
                'items': items,
                'total_cost': total_cost,
                'item_count': len(items)
            })
        
        return jsonify({
            'success': True,
            'lists': result_lists,
            'count': len(result_lists)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get user lists: {str(e)}'}), 500

# Static file serving
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the Next.js build output."""
    full_path = os.path.join(app.static_folder, path)
    
    # If the file exists, serve it
    if path and os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    
    # For routes that don't match files, serve index.html (SPA routing)
    return send_from_directory(app.static_folder, 'index.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by serving the React app."""
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

# Initialize and run
if __name__ == '__main__':
    print("🚀 Starting Grocery Optimization Platform (Merged)")
    print("=" * 50)
    
    # Initialize database
    init_database()
    
    # Initialize Kroger API
    if grocery_app.kroger_api._service_token:
        print("✅ Kroger API initialized")
    else:
        print("❌ Kroger API initialization failed")
    
    print(f"📁 Serving frontend from: {app.static_folder}")
    print("🌐 Server starting on http://localhost:5001")
    print("🔧 Using merged GroceryOptimizationApp logic from main.py")
    print("=" * 50)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)