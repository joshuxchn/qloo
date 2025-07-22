#!/usr/bin/env python3
"""
Main application for Qloo grocery optimization platform.
Integrates Kroger API product search with PostgreSQL database storage.
"""

import os
from datetime import datetime, timezone
from dotenv import load_dotenv

from kroger import KrogerAPI
from backend.database.databaseInteractions import Database

# Load environment variables
load_dotenv("../.env")

# Database configuration
DB_PARAMS = {
    "dbname": "grocery_app",
    "user": os.getenv("DB_USER", "joshuachen"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

class GroceryService:
    """
    Service class that integrates Kroger API with database operations.
    Handles product search, store management, and data persistence.
    """
    
    def __init__(self):
        """Initialize Kroger API and database connection parameters."""
        self.kroger_api = KrogerAPI()
        self.db_params = DB_PARAMS
    
    def search_and_store_products(self, search_term, limit=5, zip_code=None, print_results=True):
        """
        Search for products using Kroger API and store results in database.
        
        Args:
            search_term (str): Product search query
            limit (int): Maximum number of products to return
            zip_code (str): ZIP code for store location
            print_results (bool): Whether to print search results
            
        Returns:
            dict: Search results with database storage status
        """
        if print_results:
            print(f"\nSearching for '{search_term}' (limit: {limit})")
            print("=" * 60)
        
        # Search products using Kroger API
        search_results = self.kroger_api.productSearch(
            search_term=search_term,
            limit=limit,
            zip_code=zip_code
        )
        
        if not search_results:
            return {"success": False, "message": "No search results from Kroger API"}
        
        # Store results in database
        try:
            with Database(self.db_params) as db:
                # Create tables if they don't exist
                db.create_tables()
                
                # Store store information
                store_info = search_results['store']
                db.add_or_update_store(
                    location_id=store_info['location_id'],
                    name=store_info['name'],
                    address=store_info['address'],
                    zip_code=store_info['zip_code']
                )
                
                stored_products = []
                
                # Store each product and its pricing information
                for product in search_results['products']:
                    if product['upc'] != 'N/A':  # Only store products with valid UPC
                        # Store product information
                        db.add_or_update_product(
                            upc=product['upc'],
                            name=product['name'],
                            brand=product['brand'],
                            kroger_product_id=product['kroger_product_id']
                        )
                        
                        # Store store-specific pricing and availability
                        db.add_or_update_store_product(
                            store_id=store_info['location_id'],
                            product_upc=product['upc'],
                            regular_price=product['regular_price'],
                            promo_price=product['promo_price'],
                            stock_level=product['stock_level'],
                            is_available=product['is_available_instore']
                        )
                        
                        stored_products.append({
                            'upc': product['upc'],
                            'name': product['name'],
                            'brand': product['brand'],
                            'regular_price': product['regular_price'],
                            'promo_price': product['promo_price']
                        })
                
                if print_results:
                    print(f"\nDatabase Storage Results:")
                    print(f"Store: {store_info['name']} (ID: {store_info['location_id']})")
                    print(f"Products stored: {len(stored_products)}")
                    print(f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
                
                return {
                    "success": True,
                    "search_results": search_results,
                    "stored_products": stored_products,
                    "store_info": store_info,
                    "message": f"Successfully stored {len(stored_products)} products from {store_info['name']}"
                }
                
        except Exception as e:
            error_msg = f"Database error: {str(e)}"
            if print_results:
                print(f"Error: {error_msg}")
            return {
                "success": False,
                "search_results": search_results,
                "message": error_msg
            }
    
    def get_product_pricing(self, product_upc, store_id):
        """
        Retrieve product pricing and availability from database.
        
        Args:
            product_upc (str): Product UPC code
            store_id (str): Store location ID
            
        Returns:
            dict: Product pricing and availability information
        """
        try:
            with Database(self.db_params) as db:
                store_product = db.get_store_product_info(store_id, product_upc)
                if store_product:
                    return {
                        "success": True,
                        "product_upc": product_upc,
                        "store_id": store_id,
                        "regular_price": float(store_product['regular_price']) if store_product['regular_price'] else None,
                        "promo_price": float(store_product['promo_price']) if store_product['promo_price'] else None,
                        "stock_level": store_product['stock_level'],
                        "is_available": store_product['is_available_instore'],
                        "last_updated": store_product['last_updated'].isoformat()
                    }
                else:
                    return {"success": False, "message": "Product not found in specified store"}
                    
        except Exception as e:
            return {"success": False, "message": f"Database error: {str(e)}"}
    
    def get_cheapest_products(self, search_term, limit=3):
        """
        Search for products and return them sorted by price (cheapest first).
        
        Args:
            search_term (str): Product search query
            limit (int): Maximum number of products to return
            
        Returns:
            list: Products sorted by regular price (ascending)
        """
        result = self.search_and_store_products(search_term, limit=limit * 2, print_results=False)
        
        if not result['success']:
            return []
        
        # Sort products by regular price (cheapest first)
        products_with_prices = [
            p for p in result['stored_products'] 
            if p['regular_price'] is not None
        ]
        
        cheapest_products = sorted(
            products_with_prices,
            key=lambda x: float(x['regular_price'])
        )
        
        return cheapest_products[:limit]

def demo_functionality():
    """Demonstrate the integrated grocery service functionality."""
    print("QLOO GROCERY OPTIMIZATION PLATFORM")
    print("=" * 60)
    print("Demonstrating Kroger API + Database Integration")
    
    service = GroceryService()
    
    # Demo 1: Search and store milk products
    print("\nDEMO 1: Search and Store Products")
    milk_results = service.search_and_store_products("milk", limit=3)
    
    if milk_results['success']:
        print(f"Success: {milk_results['message']}")
    else:
        print(f"Failed: {milk_results['message']}")
    
    # Demo 2: Find cheapest products
    print("\nDEMO 2: Cost Optimization")
    print("Finding cheapest milk products...")
    cheapest_milk = service.get_cheapest_products("milk", limit=3)
    
    if cheapest_milk:
        print("Cheapest milk products:")
        for i, product in enumerate(cheapest_milk, 1):
            price = f"${product['regular_price']}" if product['regular_price'] else "N/A"
            promo = f" (Promo: ${product['promo_price']})" if product['promo_price'] else ""
            print(f"  {i}. {product['name']} - {price}{promo}")
    else:
        print("No pricing data available")

if __name__ == "__main__":
    demo_functionality()