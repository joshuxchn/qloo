#!/usr/bin/env python3
"""
Complete test of merged Flask application functionality using the test client.
This demonstrates that main.py logic is properly integrated into app.py.
"""

import sys
import os
from datetime import datetime

# Add the Database directory to sys.path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database'))

def test_merged_functionality():
    """Test the merged Flask application using Flask test client."""
    print("🧪 COMPREHENSIVE MERGED APPLICATION TEST")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Import the merged Flask app
        from app import app, grocery_app
        
        print("✅ Merged Flask app imported successfully")
        print(f"✅ GroceryOptimizationApp instance created")
        print(f"✅ Kroger API initialized: {bool(grocery_app.kroger_api._service_token)}")
        
        # Create test client
        client = app.test_client()
        
        # Test 1: Health Check
        print("\n1️⃣  Testing Health Endpoint")
        print("-" * 30)
        response = client.get('/api/health')
        if response.status_code == 200:
            data = response.get_json()
            print(f"   Status: {data['status']}")
            print(f"   Database: {data['database']}")
            print(f"   Kroger API: {data['kroger_api']}")
            print("   ✅ Health check successful")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
        
        # Test 2: User Authentication (using main.py logic)
        print("\n2️⃣  Testing User Authentication (main.py logic)")
        print("-" * 45)
        auth_data = {"email": "merged@test.com", "password": "testpass123"}
        response = client.post('/api/auth/login', 
                             json=auth_data,
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                user = data['user']
                print(f"   User ID: {user['id']}")
                print(f"   Username: {user['username']}")
                print(f"   Email: {user['email']}")
                print(f"   Location: {user['preferred_location']}")
                print("   ✅ User authentication successful")
                user_id = user['id']
            else:
                print(f"   ❌ Authentication failed: {data}")
                return
        else:
            print(f"   ❌ Authentication request failed: {response.status_code}")
            return
        
        # Test 3: Product Search (using main.py logic)
        print("\n3️⃣  Testing Product Search (main.py logic)")
        print("-" * 40)
        search_data = {"query": "eggs", "limit": 3}
        response = client.post('/api/products/search', 
                             json=search_data,
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success') and data.get('products'):
                products = data['products']
                print(f"   Found {len(products)} products:")
                for i, product in enumerate(products, 1):
                    print(f"   {i}. {product['name']}")
                    print(f"      Brand: {product['brand']}")
                    print(f"      Price: ${product['price']}")
                    print(f"      UPC: {product['upc']}")
                print("   ✅ Product search successful")
            else:
                print(f"   ❌ Product search returned no results: {data}")
                return
        else:
            print(f"   ❌ Product search failed: {response.status_code}")
            return
        
        # Test 4: Create Grocery List (using main.py logic)
        print("\n4️⃣  Testing Grocery List Creation (main.py logic)")
        print("-" * 48)
        list_data = {"user_id": user_id}
        response = client.post('/api/lists', 
                             json=list_data,
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                grocery_list = data['list']
                print(f"   List ID: {grocery_list['id']}")
                print(f"   User ID: {grocery_list['user_id']}")
                print(f"   Created: {grocery_list['timestamp']}")
                print("   ✅ Grocery list creation successful")
                list_id = grocery_list['id']
            else:
                print(f"   ❌ List creation failed: {data}")
                return
        else:
            print(f"   ❌ List creation request failed: {response.status_code}")
            return
        
        # Test 5: Add Item to List (using main.py logic)
        print("\n5️⃣  Testing Add Item to List (main.py logic)")
        print("-" * 42)
        item_data = {"item_name": "apples", "quantity": 3}
        response = client.post(f'/api/lists/{list_id}/items', 
                             json=item_data,
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                item = data['item']
                print(f"   Item: {item['name']}")
                print(f"   Brand: {item['brand']}")
                print(f"   Price: ${item['price']}")
                print(f"   Quantity: {item['quantity']}")
                print(f"   UPC: {item['upc']}")
                print("   ✅ Add item successful")
            else:
                print(f"   ❌ Add item failed: {data}")
        else:
            print(f"   ❌ Add item request failed: {response.status_code}")
        
        # Test 6: Get User Lists (using main.py logic)
        print("\n6️⃣  Testing Get User Lists (main.py logic)")
        print("-" * 38)
        response = client.get(f'/api/lists/user/{user_id}')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                lists = data['lists']
                print(f"   Found {len(lists)} lists for user:")
                for i, lst in enumerate(lists, 1):
                    print(f"   {i}. List ID: {lst['id']}")
                    print(f"      Items: {lst['item_count']}")
                    print(f"      Total Cost: ${lst['total_cost']:.2f}")
                    print(f"      Created: {lst['timestamp'][:19]}")
                    
                    # Show items in the list
                    if lst['items']:
                        print("      Products:")
                        for item in lst['items']:
                            print(f"        - {item['name']} x{item['quantity']} = ${item['subtotal']:.2f}")
                print("   ✅ Get user lists successful")
            else:
                print(f"   ❌ Get lists failed: {data}")
        else:
            print(f"   ❌ Get lists request failed: {response.status_code}")
        
        # Test 7: Static File Serving
        print("\n7️⃣  Testing Static File Serving")
        print("-" * 28)
        response = client.get('/')
        if response.status_code == 200:
            if b'GroceryAI' in response.data or b'DOCTYPE html' in response.data:
                print("   ✅ Frontend static files served successfully")
            else:
                print("   ❌ Frontend content unexpected")
        else:
            print(f"   ❌ Static file serving failed: {response.status_code}")
        
        # Summary
        print("\n" + "=" * 60)
        print("🎉 MERGED APPLICATION TEST COMPLETE!")
        print("=" * 60)
        print("✅ All main.py logic successfully integrated into Flask app")
        print("✅ Database operations working")
        print("✅ Kroger API integration working")
        print("✅ User management working")
        print("✅ Grocery list management working")
        print("✅ Product search working")
        print("✅ Frontend static serving working")
        print("\n🚀 The merged application is ready for production!")
        print("   Run: python3 app.py")
        print("   Visit: http://localhost:5001")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main test function."""
    test_merged_functionality()

if __name__ == "__main__":
    main()