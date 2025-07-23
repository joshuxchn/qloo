#!/usr/bin/env python3
"""
Main application entry point for the grocery optimization platform.
Structured user flow with clean database integration using db_utils.py
"""

import sys
import os
import uuid
from datetime import datetime, timezone

# Add the Database directory to sys.path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Database'))

from Database import db_utils
from Database.user import User
from Database.list import GroceryList
from kroger import KrogerAPI

class GroceryOptimizationApp:
    """Main application class for grocery optimization platform."""
    
    def __init__(self):
        """Initialize the application."""
        self.kroger_api = KrogerAPI()
        self.current_user = None
        self.current_list = None
        
    def get_user_credentials(self):
        """Get user email and password (will be Google auth later)."""
        print("\n" + "=" * 50)
        print("🔐 USER AUTHENTICATION")
        print("=" * 50)
        
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()
        
        if not email or not password:
            print("❌ Email and password are required!")
            return None, None
            
        return email, password
    
    def find_user_by_email(self, email):
        """Check if user exists by email (custom function since db_utils doesn't have this)."""
        # Since db_utils doesn't have find_by_email, we'll implement it here
        # This would normally be in db_utils.py but we'll add it temporarily
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
        """Create a new user with unique ID using demo.py pattern."""
        print("\n📝 Creating new user account...")
        
        # Generate unique user ID using UUID (demo.py pattern)
        user_id = str(uuid.uuid4())
        
        # Extract username from email
        username = email.split('@')[0]
        
        # Create User object with filler data (following demo.py structure)
        user = User(
            user_ID=user_id,
            username=username,
            email=email,
            password=password,  # In production, this would be hashed
            list_of_list_ids=[],
            access_token=None,  # Will be set when Kroger OAuth is implemented
            refresh_token=None,
            token_type=None,
            token_expiry=None,
            preferred_location="98075"  # Default ZIP code
        )
        
        # Save to database using db_utils
        if db_utils.add_user_to_db(user):
            print(f"   ✅ User created successfully!")
            print(f"   User ID: {user_id}")
            print(f"   Username: {username}")
            return user
        else:
            print("   ❌ Failed to create user in database")
            return None
    
    def get_or_create_user(self, email, password):
        """Get existing user or create new one."""
        print("\n🔍 Checking for existing user...")
        
        # Check if user exists
        existing_user = self.find_user_by_email(email)
        
        if existing_user:
            print(f"   ✅ Found existing user: {existing_user.username}")
            print(f"   User ID: {existing_user.user_id}")
            # In production, verify password here
            return existing_user
        else:
            print("   ℹ️  No existing user found")
            return self.create_new_user(email, password)
    
    def get_user_grocery_lists(self, user_id):
        """Fetch existing grocery lists for user."""
        print("\n🛒 Checking for existing grocery lists...")
        
        # Use db_utils to get list IDs for user
        list_ids = db_utils.get_grocery_list_ids_for_user(user_id)
        
        if list_ids:
            print(f"   ✅ Found {len(list_ids)} existing grocery list(s)")
            lists = []
            for list_id in list_ids:
                grocery_list = db_utils.get_grocery_list_details(list_id)
                if grocery_list:
                    lists.append(grocery_list)
                    print(f"   - List ID: {list_id} ({len(grocery_list.products_on_list)} items)")
            return lists
        else:
            print("   ℹ️  No existing grocery lists found")
            return []
    
    def create_new_grocery_list(self, user_id):
        """Create a new grocery list for the user."""
        print("\n📋 Creating new grocery list...")
        
        # Generate unique list ID using UUID (demo.py pattern)
        list_id = str(uuid.uuid4())
        
        # Create GroceryList object using demo.py structure
        grocery_list = GroceryList(
            list_ID=list_id,
            user_ID=user_id,
            timestamp=datetime.now(timezone.utc),
            products_on_list=[]
        )
        
        # Save to database using db_utils
        if db_utils.add_grocery_list_to_db(grocery_list):
            print(f"   ✅ Grocery list created successfully!")
            print(f"   List ID: {list_id}")
            return grocery_list
        else:
            print("   ❌ Failed to create grocery list")
            return None
    
    def get_or_create_grocery_list(self, user_id):
        """Get existing grocery list or create new one."""
        existing_lists = self.get_user_grocery_lists(user_id)
        
        if existing_lists:
            # Use the first existing list
            grocery_list = existing_lists[0]
            print(f"   ✅ Using existing list: {grocery_list.list_id}")
            return grocery_list
        else:
            # Create new list
            return self.create_new_grocery_list(user_id)
    
    def fetch_kroger_products_for_testing(self, num_products=5):
        """Fetch products from Kroger API for testing."""
        print("\n🛍️  Fetching products from Kroger API...")
        
        # Different search terms for variety
        search_terms = ["milk", "bread", "apples", "chicken", "rice", "eggs", "cheese", "bananas"]
        
        products = []
        
        for i in range(num_products):
            search_term = search_terms[i % len(search_terms)]
            print(f"   Searching for: {search_term}")
            
            try:
                # Get 1 product per search
                search_results = self.kroger_api.productSearch(search_term, limit=1)
                
                if search_results:
                    product = search_results[0]
                    products.append(product)
                    print(f"     ✅ Found: {product.name} - ${product.price}")
                else:
                    print(f"     ❌ No results for: {search_term}")
                    
            except Exception as e:
                print(f"     ❌ Error searching for {search_term}: {e}")
        
        print(f"   ✅ Successfully fetched {len(products)} products")
        return products
    
    def add_products_to_list(self, grocery_list, products):
        """Add Kroger products to grocery list."""
        print("\n➕ Adding products to grocery list...")
        
        # Add products to the list object (demo.py pattern)
        for product in products:
            grocery_list.products_on_list.append((product, 1))  # Quantity 1
            print(f"   ✅ Added: {product.name}")
        
        # Save updated list to database using db_utils
        if db_utils.add_grocery_list_to_db(grocery_list):
            print(f"   ✅ Updated grocery list saved to database")
            return True
        else:
            print("   ❌ Failed to save updated grocery list")
            return False
    
    def display_final_summary(self):
        """Display final summary of the user's data."""
        print("\n" + "=" * 60)
        print("📊 FINAL SUMMARY")
        print("=" * 60)
        
        if self.current_user:
            print(f"👤 User: {self.current_user.username} ({self.current_user.email})")
            print(f"🆔 User ID: {self.current_user.user_id}")
            
            if self.current_list:
                print(f"📋 Grocery List ID: {self.current_list.list_id}")
                print(f"🛒 Items in list: {len(self.current_list.products_on_list)}")
                
                if self.current_list.products_on_list:
                    total_cost = 0
                    print("\n📦 Products:")
                    for product, quantity in self.current_list.products_on_list:
                        cost = float(product.price) * quantity if product.price else 0
                        total_cost += cost
                        print(f"   • {product.name}")
                        print(f"     Brand: {product.brand} | Price: ${product.price} | Qty: {quantity}")
                        print(f"     UPC: {product.upc} | Subtotal: ${cost:.2f}")
                    
                    print(f"\n💰 Total estimated cost: ${total_cost:.2f}")
        
        print("\n🔍 You can now view this data in pgAdmin!")
        print("Tables: users, grocery_lists, grocery_list_items")
    
    def run(self):
        """Main application entry point."""
        print("=" * 60)
        print("🛒 GROCERY OPTIMIZATION PLATFORM")
        print("=" * 60)
        print("Structured user flow with database integration")
        
        try:
            # Step 1: Get user credentials
            email, password = self.get_user_credentials()
            if not email or not password:
                return
            
            # Step 2: Get or create user
            self.current_user = self.get_or_create_user(email, password)
            if not self.current_user:
                print("❌ Failed to authenticate or create user")
                return
            
            # Step 3: Get or create grocery list
            self.current_list = self.get_or_create_grocery_list(self.current_user.user_id)
            if not self.current_list:
                print("❌ Failed to get or create grocery list")
                return
            
            # Step 4: Add Kroger products for testing
            products = self.fetch_kroger_products_for_testing(5)
            if products:
                self.add_products_to_list(self.current_list, products)
            
            # Step 5: Display summary
            self.display_final_summary()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Application interrupted by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Application entry point."""
    app = GroceryOptimizationApp()
    app.run()

if __name__ == "__main__":
    main()