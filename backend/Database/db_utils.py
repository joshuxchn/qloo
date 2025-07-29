import psycopg2
import psycopg2.extras # For DictCursor
from datetime import datetime, timezone, timedelta
import json # For serializing/deserializing list of list IDs
from .list import GroceryList
from .product import Product
from .user import User

# --- Database Connection Constants ---
DB_NAME = "grocery_app"
DB_USER = "samavramov" # Current user
DB_PASSWORD = "" # Leave empty if you don't have a password set for your user
DB_HOST = "localhost"
DB_PORT = "5432"

# --- Connection/Setup Methods ---
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

def create_tables():
    """Creates the necessary tables in the database if they don't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    preferred_location TEXT,
                    access_token TEXT,
                    refresh_token TEXT,
                    token_type TEXT,
                    token_expiry TIMESTAMP WITH TIME ZONE,
                    list_of_list_ids JSONB DEFAULT '[]'::jsonb
                );
            """)
            # Create grocery_lists table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS grocery_lists (
                    list_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
            # Create grocery_list_items table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS grocery_list_items (
                    list_item_id SERIAL PRIMARY KEY,
                    list_id TEXT NOT NULL REFERENCES grocery_lists(list_id) ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    price NUMERIC(10, 2) NOT NULL,
                    promo_price NUMERIC(10, 2),
                    fufillment_type TEXT,
                    aisle TEXT,
                    inventory INTEGER,
                    size TEXT,
                    last_updated TIMESTAMP WITH TIME ZONE,
                    location_id TEXT,
                    upc TEXT,
                    quantity INTEGER NOT NULL DEFAULT 1
                );
            """)
        conn.commit()
        print("✅ Tables ensured to exist.")
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        conn.close()

def drop_tables():
    """Drops all created tables. Use with caution!"""
    conn = get_db_connection()
    if conn is None: return
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS grocery_list_items, grocery_lists, users CASCADE;")
            print("All tables dropped.")
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error dropping tables: {e}")
        conn.rollback()
    finally:
        conn.close()

# --- User Methods ---
def get_user_by_id(user_id):
    """Queries for a user by user_id and returns a User object."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                # Corrected: Instantiate User object with snake_case properties
                user = User(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    list_of_list_ids=user_data['list_of_list_ids'] or [],
                    access_token=user_data['access_token'],
                    refresh_token=user_data['refresh_token'],
                    token_type=user_data['token_type'],
                    token_expiry=user_data['token_expiry'],
                    preferred_location=user_data['preferred_location']
                )
                return user
            return None
    except psycopg2.Error as e:
        print(f"Error querying user by ID: {e}")
        return None
    finally:
        conn.close()

def add_user_to_db(user_obj):
    """Adds a new user or updates an existing user in the 'users' table."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            # Assumes user_obj properties are already in snake_case
            cur.execute("""
                INSERT INTO users (user_id, username, email, password, preferred_location, access_token, refresh_token, token_type, token_expiry, list_of_list_ids)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                    username = EXCLUDED.username, email = EXCLUDED.email, password = EXCLUDED.password,
                    preferred_location = EXCLUDED.preferred_location, access_token = EXCLUDED.access_token,
                    refresh_token = EXCLUDED.refresh_token, token_type = EXCLUDED.token_type,
                    token_expiry = EXCLUDED.token_expiry, list_of_list_ids = EXCLUDED.list_of_list_ids;
            """, (user_obj.user_id, user_obj.username, user_obj.email, user_obj.password, user_obj.preferred_location,
                  user_obj.access_token, user_obj.refresh_token, user_obj.token_type, user_obj.token_expiry,
                  json.dumps(user_obj.list_of_list_ids)))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error adding/updating user '{user_obj.username}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# --- Grocery List Methods ---
def get_grocery_list_details(list_id):
    """Retrieves a complete GroceryList object, including its products."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT list_id, user_id, timestamp FROM grocery_lists WHERE list_id = %s;", (list_id,))
            list_data = cur.fetchone()
            if not list_data: return None

            cur.execute("""
                SELECT * FROM grocery_list_items WHERE list_id = %s;
            """, (list_id,))
            product_items_data = cur.fetchall()

            products_on_list = []
            for item_data in product_items_data:
                # Corrected: Instantiate Product object with snake_case properties
                product = Product(
                    name=item_data['name'],
                    price=item_data['price'],
                    promo_price=item_data['promo_price'],
                    fufillment_type=item_data['fufillment_type'],
                    brand=item_data['aisle'],
                    inventory=item_data['inventory'],
                    size=item_data['size'],
                    last_updated=item_data['last_updated'],
                    location_id=item_data['location_id'], # Corrected from location_ID
                    upc=item_data['upc']
                )
                products_on_list.append((product, item_data['quantity']))

            # Corrected: Instantiate GroceryList object with snake_case properties
            grocery_list = GroceryList(
                list_id=list_data['list_id'],
                user_id=list_data['user_id'],
                timestamp=list_data['timestamp'],
                products_on_list=products_on_list
            )
            return grocery_list
    except psycopg2.Error as e:
        print(f"Error retrieving grocery list details: {e}")
        return None
    finally:
        conn.close()

def add_grocery_list_to_db(grocery_list_obj):
    """Adds a new grocery list and its items to the database."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # 1. Insert/Update grocery_lists metadata
            cur.execute("""
                INSERT INTO grocery_lists (list_id, user_id, timestamp)
                VALUES (%s, %s, %s)
                ON CONFLICT (list_id) DO UPDATE SET
                    user_id = EXCLUDED.user_id, timestamp = EXCLUDED.timestamp;
            """, (grocery_list_obj.list_id, grocery_list_obj.user_id, grocery_list_obj.timestamp))

            # 2. Clear existing items for this list before re-inserting
            cur.execute("DELETE FROM grocery_list_items WHERE list_id = %s;", (grocery_list_obj.list_id,))

            # 3. Insert new grocery_list_items
            for product, quantity in grocery_list_obj.products_on_list:
                inventory_int = None
                if isinstance(product.inventory, str):
                    inventory_map = {"HIGH": 100, "MEDIUM": 50, "LOW": 10, "OUT_OF_STOCK": 0}
                    inventory_int = inventory_map.get(product.inventory.upper())
                else:
                    inventory_int = product.inventory
                
                cur.execute("""
                    INSERT INTO grocery_list_items (list_id, name, price, promo_price, fufillment_type, aisle, inventory, size, last_updated, location_id, upc, quantity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    grocery_list_obj.list_id, product.name, product.price, product.promo_price,
                    product.fufillment_type, product.brand, inventory_int, product.size,
                    product.last_updated, product.location_id, product.upc, quantity # Corrected from product.location_ID
                ))

            # 4. Update the user's list_of_list_ids
            cur.execute("SELECT list_of_list_ids FROM users WHERE user_id = %s;", (grocery_list_obj.user_id,))
            user_data = cur.fetchone()
            if user_data:
                current_list_ids = user_data['list_of_list_ids'] or []
                if grocery_list_obj.list_id not in current_list_ids:
                    current_list_ids.append(grocery_list_obj.list_id)
                    cur.execute("UPDATE users SET list_of_list_ids = %s WHERE user_id = %s;",
                                (json.dumps(current_list_ids), grocery_list_obj.user_id))

        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error adding grocery list '{grocery_list_obj.list_id}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def remove_grocery_list(list_id):
    """Removes a grocery list and updates the user's list of IDs."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT user_id FROM grocery_lists WHERE list_id = %s;", (list_id,))
            result = cur.fetchone()
            if not result: return False
            user_id = result['user_id']
            
            # Deleting the list will cascade and delete its items
            cur.execute("DELETE FROM grocery_lists WHERE list_id = %s;", (list_id,))
            
            # Update the user's list of IDs
            cur.execute("SELECT list_of_list_ids FROM users WHERE user_id = %s;", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                current_list_ids = user_data['list_of_list_ids'] or []
                if list_id in current_list_ids:
                    current_list_ids.remove(list_id)
                    cur.execute("UPDATE users SET list_of_list_ids = %s WHERE user_id = %s;",
                                (json.dumps(current_list_ids), user_id))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Error removing grocery list '{list_id}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# The remaining functions `remove_user` and `update_user_details` from your original
# file are generally fine as they mostly deal with IDs, but I am including them
# here for completeness and ensuring they use consistent property access.
def remove_user(user_id):
    """Removes a user and all their associated data (lists, items) via CASCADE."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
            # The rowcount attribute tells us if a row was deleted
            if cur.rowcount == 0:
                print(f"User with ID '{user_id}' not found. Cannot remove.")
                return False
            conn.commit()
            print(f"User '{user_id}' and all associated data successfully removed.")
            return True
    except psycopg2.Error as e:
        print(f"Error removing user '{user_id}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_user_details(user_obj):
    """Updates the details of an existing user in the 'users' table."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users SET
                    username = %s, email = %s, password = %s, preferred_location = %s,
                    access_token = %s, refresh_token = %s, token_type = %s,
                    token_expiry = %s, list_of_list_ids = %s
                WHERE user_id = %s;
            """, (user_obj.username, user_obj.email, user_obj.password, user_obj.preferred_location,
                  user_obj.access_token, user_obj.refresh_token, user_obj.token_type, user_obj.token_expiry,
                  json.dumps(user_obj.list_of_list_ids), user_obj.user_id))
            if cur.rowcount == 0:
                print(f"User with ID '{user_obj.user_id}' not found. Cannot update.")
                return False
        conn.commit()
        print(f"User '{user_obj.username}' details updated successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error updating user '{user_obj.username}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()