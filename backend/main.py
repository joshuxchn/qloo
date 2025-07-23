#!/usr/bin/env python3
"""
Main application entry point for the grocery optimization platform.
Creates a user, grocery list, and populates it with Kroger products.
"""

import uuid
import psycopg2
from kroger import KrogerAPI

# Database connection parameters
DB_NAME = "grocery_app"
DB_USER = "joshuachen"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_user_in_db():
    """Create a user directly in the database using the existing schema."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        with conn.cursor() as cur:
            # Insert user and get the auto-generated ID
            unique_suffix = uuid.uuid4().hex[:6]
            cur.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING user_id;
            """, (
                f"demo_user_{unique_suffix}",
                f"demo_{unique_suffix}@grocery-demo.com", 
                "demo_password_hash"
            ))
            
            user_id = cur.fetchone()[0]
            
        conn.commit()
        print(f"   ✅ Created user with ID: {user_id}")
        return user_id
        
    except Exception as e:
        print(f"   ❌ Error creating user: {e}")
        return None
    finally:
        conn.close()

def create_grocery_list_in_db(user_id):
    """Create a grocery list directly in the database."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        with conn.cursor() as cur:
            # Insert grocery list and get the auto-generated ID
            cur.execute("""
                INSERT INTO grocerylists (user_id, list_name)
                VALUES (%s, %s)
                RETURNING list_id;
            """, (user_id, f"Demo Grocery List"))
            
            list_id = cur.fetchone()[0]
            
        conn.commit()
        print(f"   ✅ Created grocery list with ID: {list_id}")
        return list_id
        
    except Exception as e:
        print(f"   ❌ Error creating grocery list: {e}")
        return None
    finally:
        conn.close()

def add_product_to_db(product):
    """Add a product to the products table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        with conn.cursor() as cur:
            # Insert product (ignore if already exists)
            cur.execute("""
                INSERT INTO products (upc, name, brand)
                VALUES (%s, %s, %s)
                ON CONFLICT (upc) DO NOTHING;
            """, (product.upc, product.name, product.brand))
            
        conn.commit()
        return True
        
    except Exception as e:
        print(f"   ⚠️  Error adding product {product.upc}: {e}")
        return False
    finally:
        conn.close()

def add_product_to_list(list_id, product, quantity=1):
    """Add a product to a grocery list."""
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        with conn.cursor() as cur:
            # Insert into grocery list items
            cur.execute("""
                INSERT INTO grocerylistitems (list_id, product_upc, quantity)
                VALUES (%s, %s, %s)
                ON CONFLICT (list_id, product_upc) DO UPDATE SET
                    quantity = grocerylistitems.quantity + EXCLUDED.quantity;
            """, (list_id, product.upc, quantity))
            
        conn.commit()
        return True
        
    except Exception as e:
        print(f"   ⚠️  Error adding product to list: {e}")
        return False
    finally:
        conn.close()

def get_list_details(list_id):
    """Get details of a grocery list with products."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        with conn.cursor() as cur:
            # Get list info
            cur.execute("""
                SELECT gl.list_id, gl.user_id, gl.list_name, gl.created_at
                FROM grocerylists gl
                WHERE gl.list_id = %s;
            """, (list_id,))
            
            list_data = cur.fetchone()
            if not list_data:
                return None
                
            # Get products in the list
            cur.execute("""
                SELECT p.upc, p.name, p.brand, gli.quantity
                FROM grocerylistitems gli
                JOIN products p ON gli.product_upc = p.upc
                WHERE gli.list_id = %s;
            """, (list_id,))
            
            products = cur.fetchall()
            
        return {
            'list_id': list_data[0],
            'user_id': list_data[1], 
            'list_name': list_data[2],
            'created_at': list_data[3],
            'products': products
        }
        
    except Exception as e:
        print(f"Error getting list details: {e}")
        return None
    finally:
        conn.close()

def fetch_kroger_products(num_products=5):
    """Fetch products from Kroger API using different search terms."""
    kroger_api = KrogerAPI()
    
    # Different search terms to get variety
    search_terms = ["milk", "bread", "apples", "chicken", "rice", "eggs", "cheese", "bananas"]
    
    products = []
    
    print(f"Fetching {num_products} products from Kroger API...")
    
    for i in range(num_products):
        search_term = search_terms[i % len(search_terms)]
        print(f"  Searching for: {search_term}")
        
        try:
            # Get 1 product per search (default limit is now 1)
            search_results = kroger_api.productSearch(search_term, limit=1)
            
            if search_results:
                product = search_results[0]  # Get first (and only) product
                products.append(product)
                print(f"    Found: {product.name} - ${product.price}")
            else:
                print(f"    No results for: {search_term}")
                
        except Exception as e:
            print(f"    Error searching for {search_term}: {e}")
    
    return products

def main():
    """Main application entry point."""
    print("=" * 60)
    print("GROCERY OPTIMIZATION PLATFORM - DEMO SETUP")
    print("=" * 60)
    
    # Step 1: Create user in database
    print("\n1. Creating demo user...")
    user_id = create_user_in_db()
    if not user_id:
        print("   ❌ Failed to create user")
        return
    
    # Step 2: Create grocery list
    print("\n2. Creating grocery list...")
    list_id = create_grocery_list_in_db(user_id)
    if not list_id:
        print("   ❌ Failed to create grocery list")
        return
    
    # Step 3: Fetch products from Kroger API
    print("\n3. Fetching products from Kroger API...")
    products = fetch_kroger_products(5)
    
    if not products:
        print("   ❌ No products fetched from Kroger API")
        return
    
    print(f"   ✅ Successfully fetched {len(products)} products")
    
    # Step 4: Add products to database and grocery list
    print("\n4. Adding products to database and grocery list...")
    added_count = 0
    
    for product in products:
        # Add product to products table
        if add_product_to_db(product):
            # Add product to grocery list
            if add_product_to_list(list_id, product, quantity=1):
                added_count += 1
                print(f"   ✅ Added: {product.name}")
            else:
                print(f"   ❌ Failed to add to list: {product.name}")
        else:
            print(f"   ❌ Failed to add to products table: {product.name}")
    
    print(f"   ✅ Successfully added {added_count} products to grocery list")
    
    # Step 5: Verify creation by retrieving from database
    print("\n5. Verifying creation...")
    list_details = get_list_details(list_id)
    
    if list_details:
        print(f"   ✅ Grocery list retrieved: {list_details['list_name']}")
        print(f"   User ID: {list_details['user_id']}")
        print(f"   List ID: {list_details['list_id']}")
        print(f"   Created: {list_details['created_at']}")
        print(f"   Number of products: {len(list_details['products'])}")
        
        if list_details['products']:
            print("\n   Products in list:")
            for upc, name, brand, quantity in list_details['products']:
                print(f"     • {name}")
                print(f"       Brand: {brand} | UPC: {upc} | Quantity: {quantity}")
    else:
        print("   ❌ Failed to retrieve grocery list details")
    
    print("\n" + "=" * 60)
    print("DEMO SETUP COMPLETE!")
    print("=" * 60)
    print(f"Created User ID: {user_id}")
    print(f"Created List ID: {list_id}")
    print(f"Products added: {added_count}")
    print("\nYou can now view this data in pgAdmin!")
    print("Check tables: users, grocerylists, products, grocerylistitems")

if __name__ == "__main__":
    main()