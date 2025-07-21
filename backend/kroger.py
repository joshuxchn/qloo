import requests
import base64
import os
import json
from urllib.parse import urlencode
from dotenv import load_dotenv

class KrogerAPI:
    def __init__(self):
        load_dotenv("../.env")
        self.client_id = os.getenv("KROGER_CLIENT_ID")
        self.client_secret = os.getenv("KROGER_CLIENT_SECRET")
        self.redirect_uri = os.getenv("KROGER_REDIRECT_URI")
        self.zip_code = os.getenv("ZIP_CODE", "98075")
        self.base_url = "https://api.kroger.com"
        self.token_file = "kroger_tokens.json"
        
        # Initialize service token for product search
        self._service_token = None
        self._get_service_token()
    
    def _get_auth_header(self):
        """Create base64 encoded authorization header."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def _get_service_token(self):
        """Get service-to-service token for product search."""
        token_url = f"{self.base_url}/v1/connect/oauth2/token"
        
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'scope': 'product.compact'
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data)
            if response.status_code == 200:
                token_info = response.json()
                self._service_token = token_info.get('access_token')
            else:
                print(f"Failed to get service token: {response.status_code}")
        except Exception as e:
            print(f"Error getting service token: {e}")
    
    def productSearch(self, search_term="milk", limit=3, zip_code=None):
        """
        Search for products using Kroger API and print detailed product information.
        
        Args:
            search_term (str): Product to search for
            limit (int): Maximum number of products to return
            zip_code (str): ZIP code for store search, uses env variable if not provided
        """
        if not zip_code:
            zip_code = self.zip_code
        
        if not self._service_token:
            print("No service token available")
            return
        
        # Find stores
        locations_url = f"{self.base_url}/v1/locations"
        headers = {'Authorization': f'Bearer {self._service_token}'}
        params = {
            'filter.zipCode.near': zip_code,
            'filter.radiusInMiles': 10,
            'filter.limit': 5
        }
        
        try:
            locs_response = requests.get(locations_url, headers=headers, params=params)
            locs = locs_response.json()
            
            print(f"Found {len(locs.get('data', []))} stores")
            
            if locs.get("data") and len(locs["data"]) > 0:
                store = locs["data"][0]
                location_id = store["locationId"]
                store_name = store.get("name", "Unknown Store")
                print(f"Using store: {store_name} (ID: {location_id})")
                
                # Search products
                products_url = f"{self.base_url}/v1/products"
                product_params = {
                    'filter.term': search_term,
                    'filter.locationId': location_id,
                    'filter.limit': limit
                }
                
                products_response = requests.get(products_url, headers=headers, params=product_params)
                products = products_response.json()
                
                print(f"Found {len(products.get('data', []))} products:")
                print("=" * 80)
                
                for i, product in enumerate(products.get("data", []), 1):
                    print(f"\nPRODUCT {i}")
                    print("-" * 40)
                    
                    # Basic product info
                    name = product.get("description", "Unknown Product")
                    brand = product.get("brand", "Unknown Brand")
                    upc = product.get("upc", "N/A")
                    product_id = product.get("productId", "N/A")
                    
                    print(f"Name: {name}")
                    print(f"Brand: {brand}")
                    print(f"UPC: {upc}")
                    print(f"Product ID: {product_id}")
                    
                    # Get item details
                    items = product.get("items", [])
                    if items:
                        item = items[0]
                        
                        # PRICING
                        print(f"\nPRICING:")
                        price_info = item.get("price", {})
                        if price_info:
                            regular_price = price_info.get("regular")
                            promo_price = price_info.get("promo")
                            print(f"  Regular Price: ${regular_price}" if regular_price else "  Regular Price: N/A")
                            print(f"  Promo Price: ${promo_price}" if promo_price else "  Promo Price: None")
                        
                        # FULFILLMENT
                        print(f"\nFULFILLMENT:")
                        fulfillment = item.get("fulfillment", {})
                        print(f"  In-Store: {'Yes' if fulfillment.get('instore') else 'No'}")
                        print(f"  Ship to Home: {'Yes' if fulfillment.get('shiptohome') else 'No'}")
                        print(f"  Delivery: {'Yes' if fulfillment.get('delivery') else 'No'}")
                        print(f"  Curbside: {'Yes' if fulfillment.get('curbside') else 'No'}")
                        
                        # INVENTORY
                        stock_level = item.get("inventory", {}).get("stockLevel")
                        if stock_level:
                            print(f"\nINVENTORY:")
                            print(f"  Stock Level: {stock_level}")
                        else:
                            print(f"\nINVENTORY: Not available")
                        
                        # SIZE
                        size = item.get("size", "N/A")
                        if size != "N/A":
                            print(f"\nSIZE: {size}")
                    
                    print("-" * 40)
            else:
                print("No stores found in the area")
                
        except Exception as e:
            print(f"Error during product search: {e}")
    
    def getAuthorizationUrl(self, scopes="cart.basic:write profile.compact", state="auth_state"):
        """
        Generate authorization URL for cart access.
        
        Args:
            scopes (str): OAuth scopes to request
            state (str): State parameter for CSRF protection
            
        Returns:
            str: Authorization URL
        """
        params = {
            'scope': scopes,
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': state
        }
        
        auth_url = f"{self.base_url}/v1/connect/oauth2/authorize"
        full_url = f"{auth_url}?{urlencode(params)}"
        
        print("CART AUTHORIZATION REQUIRED")
        print("=" * 50)
        print("To use cart functionality, visit this URL in your browser:")
        print(f"\n{full_url}\n")
        print("After authorization, copy the 'code' parameter from the redirect URL")
        print("=" * 50)
        
        return full_url
    
    def exchangeAuthCode(self, authorization_code):
        """
        Exchange authorization code for access tokens.
        
        Args:
            authorization_code (str): Code received from authorization callback
            
        Returns:
            dict: Token information or None if failed
        """
        token_url = f"{self.base_url}/v1/connect/oauth2/token"
        
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_info = response.json()
                
                # Add timestamp for expiration tracking
                import time
                token_info['expires_at'] = time.time() + token_info.get('expires_in', 1800)
                
                # Save tokens
                with open(self.token_file, 'w') as f:
                    json.dump(token_info, f, indent=2)
                
                print("SUCCESS: Authorization complete!")
                print("Tokens saved. You can now use cart functions.")
                return token_info
            else:
                print(f"Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error exchanging authorization code: {e}")
            return None
    
    def _refresh_token(self):
        """
        Refresh access token using refresh token.
        
        Returns:
            bool: True if refresh successful, False otherwise
        """
        try:
            with open(self.token_file, 'r') as f:
                token_info = json.load(f)
        except FileNotFoundError:
            return False
        
        refresh_token = token_info.get('refresh_token')
        if not refresh_token:
            print("No refresh token available")
            return False
        
        token_url = f"{self.base_url}/v1/connect/oauth2/token"
        
        headers = {
            'Authorization': self._get_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        
        try:
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                new_token_info = response.json()
                
                # Add timestamp for expiration tracking
                import time
                new_token_info['expires_at'] = time.time() + new_token_info.get('expires_in', 1800)
                
                # Preserve refresh token if not returned
                if 'refresh_token' not in new_token_info:
                    new_token_info['refresh_token'] = refresh_token
                
                # Save new tokens
                with open(self.token_file, 'w') as f:
                    json.dump(new_token_info, f, indent=2)
                
                print("Token refreshed successfully")
                return True
            else:
                print(f"Token refresh failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return False
    
    def _get_valid_token(self):
        """
        Get a valid access token, refreshing if necessary.
        
        Returns:
            str: Valid access token or None if unavailable
        """
        try:
            with open(self.token_file, 'r') as f:
                token_info = json.load(f)
        except FileNotFoundError:
            return None
        
        access_token = token_info.get('access_token')
        expires_at = token_info.get('expires_at', 0)
        
        import time
        current_time = time.time()
        
        # Check if token is expired (with 5 minute buffer)
        if current_time >= (expires_at - 300):
            print("Access token expired, refreshing...")
            if self._refresh_token():
                # Re-read the refreshed token
                try:
                    with open(self.token_file, 'r') as f:
                        token_info = json.load(f)
                    access_token = token_info.get('access_token')
                except:
                    return None
            else:
                print("Token refresh failed. Re-authorization required.")
                return None
        
        return access_token
    
    def addToCart(self, upc, quantity=1, modality="PICKUP"):
        """
        Add item to user's Kroger cart.
        
        Args:
            upc (str): UPC code of the product to add
            quantity (int): Quantity to add
            modality (str): "PICKUP" or "DELIVERY"
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Get valid access token (automatically refreshes if needed)
        access_token = self._get_valid_token()
        if not access_token:
            print("No valid access token. Complete authorization first using getAuthorizationUrl()")
            return False
        
        cart_url = f"{self.base_url}/v1/cart/add"
        
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        
        payload = {
            "items": [
                {
                    "upc": upc,
                    "quantity": quantity,
                    "modality": modality
                }
            ]
        }
        
        try:
            response = requests.put(cart_url, headers=headers, json=payload)
            
            if response.status_code == 204:
                print(f"SUCCESS: Added {quantity}x item (UPC: {upc}) to cart for {modality}")
                print("Check your Kroger app or website to verify.")
                return True
            else:
                print(f"Failed to add item: {response.status_code}")
                if response.status_code == 401:
                    print("Authorization expired. Get new authorization code.")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return False

# Example usage
if __name__ == "__main__":
    kroger = KrogerAPI()
    kroger.productSearch("milk", 3)