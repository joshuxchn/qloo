import requests
import base64
import os
import json
from urllib.parse import urlencode
from dotenv import load_dotenv
from datetime import datetime
from Database.product import Product
from Database.user import User

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
        except Exception:
            pass
    
    def productSearch(self, search_term, limit=1, zip_code=None): #expand limit later with LLM and RAG
        """
        Search for products using Kroger API and return Product objects.
        
        Args:
            search_term (str): Product to search for
            limit (int): Maximum number of products to return
            zip_code (str): ZIP code for store search, uses env variable if not provided
            
        Returns:
            list: List of Product objects, or empty list if failed
        """
        if not zip_code:
            zip_code = self.zip_code
        
        if not self._service_token:
            return []
        
        # Find stores
        locations_url = f"{self.base_url}/v1/locations"
        headers = {'Authorization': f'Bearer {self._service_token}'}
        params = {
            'filter.zipCode.near': zip_code,
            'filter.radiusInMiles': 10,
            'filter.limit': 5 #expand later with LLM and RAG
        }
        
        try:
            locs_response = requests.get(locations_url, headers=headers, params=params)
            locs = locs_response.json()
            
            if locs.get("data") and len(locs["data"]) > 0:
                store = locs["data"][0]
                location_id = store["locationId"]
                store_name = store.get("name", "Unknown Store")
                
                # Search products
                products_url = f"{self.base_url}/v1/products"
                product_params = {
                    'filter.term': search_term,
                    'filter.locationId': location_id,
                    'filter.limit': limit
                }
                
                products_response = requests.get(products_url, headers=headers, params=product_params)
                products = products_response.json()
                
                # Create list of Product objects
                product_objects = []
                
                for product in products.get("data", []):
                    # Basic product info
                    name = product.get("description", "Unknown Product")
                    brand = product.get("brand", "Unknown Brand")
                    upc = product.get("upc", "N/A")
                    
                    # Get item details
                    items = product.get("items", [])
                    
                    # Initialize default values
                    regular_price = None
                    promo_price = None
                    stock_level = "UNKNOWN"
                    fulfillment_type = "UNKNOWN"
                    size = None
                    
                    if items:
                        item = items[0]
                        
                        # PRICING
                        price_info = item.get("price", {})
                        if price_info:
                            regular_price = price_info.get("regular")
                            promo_price = price_info.get("promo")
                        
                        # FULFILLMENT
                        fulfillment = item.get("fulfillment", {})
                        if fulfillment.get('instore', False):
                            fulfillment_type = "INSTORE"
                        elif fulfillment.get('delivery', False):
                            fulfillment_type = "DELIVERY"
                        elif fulfillment.get('pickup', False):
                            fulfillment_type = "PICKUP"
                        
                        # INVENTORY
                        inventory_info = item.get("inventory", {})
                        stock_level = inventory_info.get("stockLevel", "UNKNOWN")
                        
                        # SIZE
                        size = item.get("size", "N/A")
                        if size == "N/A":
                            size = None
                    
                    product_obj = Product(
                        name=name,
                        price=regular_price,
                        promo_price=promo_price,
                        fufillment_type=fulfillment_type,
                        brand=brand,
                        inventory=stock_level,
                        size=size,
                        last_updated=datetime.now(),
                        location_ID=location_id,
                        upc=upc
                    )
                    
                    product_objects.append(product_obj)
                
                return product_objects
            else:
                return []
                
        except Exception:
            return []
    
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
                
                return token_info
            else:
                return None
                
        except Exception:
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
                
                return True
            else:
                return False
                
        except Exception:
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
            if self._refresh_token():
                # Re-read the refreshed token
                try:
                    with open(self.token_file, 'r') as f:
                        token_info = json.load(f)
                    access_token = token_info.get('access_token')
                except:
                    return None
            else:
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
                return True
            else:
                return False
                
        except Exception:
            return False

# Example usage moved to test_kroger.py