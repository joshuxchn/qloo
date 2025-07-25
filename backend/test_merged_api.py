#!/usr/bin/env python3
"""
Test script to verify the merged Flask API endpoints work correctly.
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the merged API endpoints."""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Merged API Endpoints")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check: {data}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: User Authentication
    print("\n2. Testing user authentication...")
    try:
        auth_data = {"email": "test@example.com", "password": "testpass"}
        response = requests.post(f"{base_url}/api/auth/login", 
                               json=auth_data, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user = data['user']
                print(f"   ✅ User authenticated: {user['username']} ({user['id']})")
                user_id = user['id']
            else:
                print(f"   ❌ Authentication failed: {data}")
                return
        else:
            print(f"   ❌ Authentication request failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Authentication error: {e}")
        return
    
    # Test 3: Product Search
    print("\n3. Testing product search...")
    try:
        search_data = {"query": "bread", "limit": 2}
        response = requests.post(f"{base_url}/api/products/search", 
                               json=search_data, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('products'):
                products = data['products']
                print(f"   ✅ Found {len(products)} products:")
                for product in products:
                    print(f"      - {product['name']} - ${product['price']}")
            else:
                print(f"   ❌ Product search returned no results: {data}")
        else:
            print(f"   ❌ Product search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Product search error: {e}")
    
    # Test 4: Create Grocery List
    print("\n4. Testing grocery list creation...")
    try:
        list_data = {"user_id": user_id}
        response = requests.post(f"{base_url}/api/lists", 
                               json=list_data, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                grocery_list = data['list']
                print(f"   ✅ Grocery list created: {grocery_list['id']}")
                list_id = grocery_list['id']
            else:
                print(f"   ❌ List creation failed: {data}")
                return
        else:
            print(f"   ❌ List creation request failed: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ List creation error: {e}")
        return
    
    # Test 5: Add Item to List
    print("\n5. Testing add item to list...")
    try:
        item_data = {"item_name": "milk", "quantity": 2}
        response = requests.post(f"{base_url}/api/lists/{list_id}/items", 
                               json=item_data, 
                               timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                item = data['item']
                print(f"   ✅ Item added: {item['name']} x{item['quantity']} - ${item['price']}")
            else:
                print(f"   ❌ Add item failed: {data}")
        else:
            print(f"   ❌ Add item request failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Add item error: {e}")
    
    # Test 6: Get User Lists
    print("\n6. Testing get user lists...")
    try:
        response = requests.get(f"{base_url}/api/lists/user/{user_id}", 
                              timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                lists = data['lists']
                print(f"   ✅ Found {len(lists)} lists for user:")
                for lst in lists:
                    print(f"      - List {lst['id']}: {lst['item_count']} items, ${lst['total_cost']:.2f}")
            else:
                print(f"   ❌ Get lists failed: {data}")
        else:
            print(f"   ❌ Get lists request failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Get lists error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Merged API testing complete!")

def main():
    """Main test function."""
    print("🔄 Waiting for server to be ready...")
    time.sleep(2)
    
    try:
        test_api_endpoints()
    except KeyboardInterrupt:
        print("\n⚠️  Testing interrupted by user")

if __name__ == "__main__":
    main()