#!/usr/bin/env python3
"""
Test script to verify Flask app functionality without running the server.
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add the Database directory to sys.path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database'))

from Database import db_utils
from kroger import KrogerAPI

def test_components():
    """Test individual components."""
    print("🧪 Testing Backend Components")
    print("=" * 50)
    
    # Test 1: Database Connection
    print("1. Testing database connection...")
    conn = db_utils.get_db_connection()
    if conn:
        print("   ✅ Database connection successful")
        conn.close()
    else:
        print("   ❌ Database connection failed")
    
    # Test 2: Kroger API
    print("\n2. Testing Kroger API...")
    kroger_api = KrogerAPI()
    if kroger_api._service_token:
        print("   ✅ Kroger API authentication successful")
        
        # Test product search
        try:
            products = kroger_api.productSearch("milk", limit=1)
            if products:
                product = products[0]
                print(f"   ✅ Product search successful: {product.name} - ${product.price}")
            else:
                print("   ❌ Product search returned no results")
        except Exception as e:
            print(f"   ❌ Product search failed: {e}")
    else:
        print("   ❌ Kroger API authentication failed")
    
    # Test 3: Frontend Static Files
    print("\n3. Testing frontend static files...")
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/out")
    index_path = os.path.join(frontend_path, "index.html")
    
    if os.path.exists(frontend_path):
        print(f"   ✅ Frontend directory exists: {frontend_path}")
        if os.path.exists(index_path):
            print("   ✅ index.html found")
        else:
            print("   ❌ index.html not found")
    else:
        print(f"   ❌ Frontend directory not found: {frontend_path}")
    
    print("\n" + "=" * 50)
    print("✅ Component testing complete!")
    
def test_flask_locally():
    """Test Flask app by importing it directly."""
    print("\n🧪 Testing Flask App Locally")
    print("=" * 50)
    
    try:
        # Import the Flask app
        from app import app, grocery_app
        
        print("   ✅ Flask app imported successfully")
        
        # Test with Flask test client
        client = app.test_client()
        
        # Test health endpoint
        print("\n1. Testing /api/health endpoint...")
        response = client.get('/api/health')
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Health check successful: {data}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
        
        # Test product search endpoint
        print("\n2. Testing /api/products/search endpoint...")
        search_data = {"query": "milk", "limit": 1}
        response = client.post('/api/products/search', 
                             json=search_data,
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success') and data.get('products'):
                product = data['products'][0]
                print(f"   ✅ Product search successful: {product['name']} - ${product['price']}")
            else:
                print(f"   ❌ Product search returned no results: {data}")
        else:
            print(f"   ❌ Product search failed: {response.status_code} - {response.data}")
        
        # Test static file serving
        print("\n3. Testing static file serving...")
        response = client.get('/')
        if response.status_code == 200:
            if b'GroceryAI' in response.data or b'DOCTYPE html' in response.data:
                print("   ✅ Static frontend served successfully")
            else:
                print("   ❌ Static frontend content unexpected")
        else:
            print(f"   ❌ Static file serving failed: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("✅ Flask app testing complete!")
        
    except Exception as e:
        print(f"   ❌ Flask app testing failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests."""
    print(f"🧪 FLASK INTEGRATION TEST")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    test_components()
    test_flask_locally()
    
    print("\n🎉 All tests completed!")
    print("🌐 To run the full application:")
    print("   cd backend && python3 app.py")
    print("   Then visit: http://localhost:5001")

if __name__ == "__main__":
    main()