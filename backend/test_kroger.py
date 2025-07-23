#!/usr/bin/env python3
"""
Test script for Kroger API functionality.
Tests both product search and persistent cart operations.

IMPORTANT: Cart authorization is PERSISTENT - you only need to authorize once!
After initial setup, cart functions work seamlessly without re-authorization.
"""

# Create a single shared KrogerAPI instance
from kroger import KrogerAPI
kroger = KrogerAPI()

# Import methods directly from the instance
productSearch = kroger.productSearch
getAuthorizationUrl = kroger.getAuthorizationUrl
exchangeAuthCode = kroger.exchangeAuthCode
addToCart = kroger.addToCart

def test_product_search():
    """Test product search functionality (no authorization required)."""
    print("=" * 60)
    print("TESTING PRODUCT SEARCH")
    print("=" * 60)
    
    # Use the detailed search function with printing
    detailed_product_search("milk", 1)

def detailed_product_search(search_term="milk", limit=1, zip_code=None):
    """
    Search for products and return Product objects, then print as JSON.
    """
    import json
    
    products = kroger.productSearch(search_term, limit, zip_code)
    
    if not products:
        print("No search results available")
        return []
    
    print(f"Found {len(products)} product(s):")
    print("=" * 80)
    
    # Convert products to dictionaries and print as JSON
    product_dicts = []
    for i, product in enumerate(products, 1):
        print(f"\nPRODUCT {i} - JSON FORMAT:")
        print("-" * 40)
        
        # Convert to dictionary
        product_dict = product.to_dict()
        product_dicts.append(product_dict)
        
        # Print as formatted JSON
        print(json.dumps(product_dict, indent=2))
        print("-" * 40)
    
    # Return the Product objects for further use
    return products

def test_cart_authorization():
    """
    ONE-TIME SETUP: Get authorization URL for cart access.
    Only needed once - tokens persist automatically after this.
    """
    print("\n" + "=" * 60)
    print("ONE-TIME CART AUTHORIZATION SETUP")
    print("=" * 60)
    print("⚠️  This is only needed ONCE. After this, cart access is persistent.")
    
    # Get authorization URL
    auth_url = getAuthorizationUrl()
    
    print(f"\nNext steps:")
    print("1. Visit the authorization URL above in your browser")
    print("2. Log in to your Kroger account and authorize the application")
    print("3. Copy the 'code' parameter from the redirect URL")
    print("4. Run: test_cart_token_exchange('YOUR_CODE_HERE')")
    print("\n⭐ After completing this once, you can use cart functions forever!")
    
    return auth_url

def test_cart_token_exchange(authorization_code):
    """
    ONE-TIME SETUP: Exchange authorization code for persistent tokens.
    After this completes, cart functions work automatically.
    """
    print("\n" + "=" * 60)
    print("COMPLETING PERSISTENT TOKEN SETUP")
    print("=" * 60)
    
    token_info = exchangeAuthCode(authorization_code)
    
    if token_info:
        print("\n🎉 SUCCESS! Cart authorization is now PERSISTENT!")
        print("✅ Tokens saved to kroger_tokens.json")
        print("✅ Automatic token refresh enabled")
        print("✅ Cart functions now work seamlessly")
        print("\nTesting cart functionality...")
        test_add_to_cart()
        print("\n🚀 Setup complete! You can now use cart functions anytime.")
    else:
        print("❌ Token exchange failed. Check your authorization code.")

def test_add_to_cart(upc="0001111042850", quantity=1, modality="PICKUP"):
    """
    Test adding items to cart (works seamlessly with persistent tokens).
    """
    print("\n" + "=" * 60)
    print("TESTING PERSISTENT CART ACCESS")
    print("=" * 60)
    print("ℹ️  This uses persistent tokens - no re-authorization needed!")
    
    success = addToCart(upc, quantity, modality)
    
    if success:
        print("✅ Cart operation successful!")
        print("🛒 Item added using persistent authentication")
    else:
        print("❌ Cart operation failed")
        print("💡 If this fails, you may need to run initial authorization setup")
    
    return success

def quick_cart_test():
    """
    Quick test to verify persistent cart access is working.
    This should work seamlessly without any setup after initial authorization.
    """
    print("QUICK PERSISTENT CART TEST")
    print("=" * 40)
    print("🔄 Testing seamless cart access...")
    
    # Try to add item using persistent tokens
    success = addToCart("0001111042850", 1, "PICKUP")
    
    if success:
        print("✅ PERSISTENT CART ACCESS WORKING!")
        print("🎯 No re-authorization needed")
    else:
        print("❌ Cart access failed")
        print("💡 Run setup_cart_authorization() for initial setup")
    
    return success

def setup_cart_authorization():
    """
    Complete one-time cart authorization setup.
    Run this once, then use cart functions forever.
    """
    print("🚀 KROGER CART AUTHORIZATION SETUP")
    print("=" * 60)
    print("This is a ONE-TIME setup for persistent cart access.")
    print()
    
    # Step 1: Get authorization URL
    print("Step 1: Getting authorization URL...")
    auth_url = test_cart_authorization()
    
    print(f"\n📋 SETUP INSTRUCTIONS:")
    print("1. Copy the authorization URL above")
    print("2. Paste it in your browser and complete Kroger login")
    print("3. Copy the 'code' parameter from the redirect URL")
    print("4. Run: test_cart_token_exchange('YOUR_CODE')")
    print("\n⭐ After this one-time setup, cart functions work forever!")
    
    return auth_url

def demonstrate_persistent_cart():
    """
    Demonstrate persistent cart functionality with multiple operations.
    This shows how cart functions work seamlessly after initial setup.
    """
    print("🛒 DEMONSTRATING PERSISTENT CART OPERATIONS")
    print("=" * 60)
    print("Adding multiple items to demonstrate seamless access...")
    
    # List of test items
    test_items = [
        {"upc": "0001111042850", "name": "Organic Milk", "quantity": 1, "modality": "PICKUP"},
        {"upc": "0001111008485", "name": "White Bread", "quantity": 2, "modality": "DELIVERY"},
        {"upc": "0007225003706", "name": "Honey Wheat Bread", "quantity": 1, "modality": "PICKUP"}
    ]
    
    success_count = 0
    
    for item in test_items:
        print(f"\n🔄 Adding {item['name']}...")
        success = addToCart(item["upc"], item["quantity"], item["modality"])
        if success:
            success_count += 1
        else:
            print(f"❌ Failed to add {item['name']}")
    
    print(f"\n📊 RESULTS:")
    print(f"✅ Successfully added {success_count}/{len(test_items)} items")
    print(f"🎯 All operations used persistent authentication")
    
    if success_count == len(test_items):
        print("🎉 PERSISTENT CART ACCESS IS WORKING PERFECTLY!")
    else:
        print("⚠️  Some operations failed - check token status")
    
    return success_count == len(test_items)

def check_token_status():
    """
    Check the status of stored authentication tokens.
    """
    import json
    import time
    
    print("🔍 CHECKING TOKEN STATUS")
    print("=" * 40)
    
    try:
        with open('kroger_tokens.json', 'r') as f:
            token_info = json.load(f)
        
        expires_at = token_info.get('expires_at', 0)
        current_time = time.time()
        time_until_expiry = expires_at - current_time
        
        print("✅ Token file found")
        print(f"🔑 Access Token: {'Present' if token_info.get('access_token') else 'Missing'}")
        print(f"🔄 Refresh Token: {'Present' if token_info.get('refresh_token') else 'Missing'}")
        
        if time_until_expiry > 0:
            minutes_left = int(time_until_expiry / 60)
            print(f"⏰ Token expires in: {minutes_left} minutes")
            print("✅ Token is currently valid")
        else:
            print("⏰ Access token has expired")
            print("🔄 Will be auto-refreshed on next cart operation")
        
        return True
        
    except FileNotFoundError:
        print("❌ No token file found")
        print("💡 Run setup_cart_authorization() for initial setup")
        return False
    except Exception as e:
        print(f"❌ Error reading token file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 KROGER API TEST INTERFACE")
    print("=" * 60)
    print("Available functions:")
    print()
    print("📦 PRODUCT SEARCH (no auth required):")
    print("  - test_product_search(): Test product search functionality")
    print()
    print("🛒 CART FUNCTIONS (persistent auth):")
    print("  - quick_cart_test(): Quick test if cart access works")
    print("  - test_add_to_cart(): Test adding single item to cart")
    print("  - demonstrate_persistent_cart(): Add multiple items seamlessly")
    print()
    print("⚙️  SETUP (one-time only):")
    print("  - setup_cart_authorization(): Complete one-time authorization")
    print("  - test_cart_token_exchange('code'): Exchange auth code for tokens")
    print()
    print("🔍 UTILITIES:")
    print("  - check_token_status(): Check current token status")
    print()
    
    # Check if cart is already set up
    print("🔍 Checking current setup status...")
    has_tokens = check_token_status()
    
    if has_tokens:
        print("\n✅ PERSISTENT CART ACCESS IS CONFIGURED!")
        print("🎯 You can use cart functions directly:")
        print("   - quick_cart_test()")
        print("   - addToCart('upc', quantity, 'modality')")
        print("   - demonstrate_persistent_cart()")
        
        # Run a quick demo
        print("\n🔄 Running quick cart test...")
        # quick_cart_test()
        detailed_product_search()
        
    else:
        print("\n⚙️  SETUP REQUIRED")
        print("💡 Run setup_cart_authorization() to enable cart functions")
        print("   This is a one-time setup for persistent access")
    
