import psycopg2
import psycopg2.extras # For DictCursor
from datetime import datetime, timezone, timedelta
import json # For serializing/deserializing list of list IDs
from .list import GroceryList
from .product import Product
from .user import User
DB_NAME = "grocery_app"
DB_USER = "samavramov" # Current user
DB_PASSWORD = "" # Leave empty if you don't have a password set for your user
DB_HOST = "localhost"
DB_PORT = "5432"
 
# Connection/Setup Methods:
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
    """Creates the necessary tables in the database.
    Drops existing tables first to ensure a clean schema.
    """
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            # Drop tables in reverse dependency order to avoid foreign key issues
            print("Attempting to drop existing tables for a clean slate...")
            cur.execute("DROP TABLE IF EXISTS grocery_list_items CASCADE;") # Drop this first as it depends on grocery_lists
            cur.execute("DROP TABLE IF EXISTS grocery_lists CASCADE;")
            cur.execute("DROP TABLE IF EXISTS users CASCADE;")
            # The 'products' table is no longer needed, so we explicitly drop it if it existed
            cur.execute("DROP TABLE IF EXISTS products CASCADE;")
            print("Existing tables dropped (if they existed).")


            # Create users table (One-to-One: user_ID -> User details)
            cur.execute("""
                CREATE TABLE users (
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
            print("Table 'users' created.")

            # Create grocery_lists table (One-to-One: list_ID -> GroceryList metadata)
            cur.execute("""
                CREATE TABLE grocery_lists (
                    list_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(user_id),
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
            print("Table 'grocery_lists' created.")

            # Create grocery_list_items table (Now contains all product details directly)
            cur.execute("""
                CREATE TABLE grocery_list_items (
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
                    upc TEXT, -- UPC is now just a descriptive column, not a FK
                    quantity INTEGER NOT NULL DEFAULT 1
                    -- UNIQUE (list_id, upc) is removed as UPC is not guaranteed to be unique across lists
                    -- if the same product is added with different details (e.g., price change)
                );
            """)
            print("Table 'grocery_list_items' created (with embedded product details).")

        conn.commit()
        print("All tables created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        conn.close()

def drop_tables():
    """Drops all created tables. Use with caution!"""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                DROP TABLE IF EXISTS grocery_list_items CASCADE;
                DROP TABLE IF EXISTS grocery_lists CASCADE;
                DROP TABLE IF EXISTS users CASCADE;
                DROP TABLE IF EXISTS products CASCADE; -- Ensure old products table is dropped
            """)
            print("All tables dropped.")
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error dropping tables: {e}")
        conn.rollback()
    finally:
        conn.close()

# User Methods:
def get_user_by_id(user_id):
    """
    Queries the 'users' table for a user object by user_ID (One-to-One).
    Returns a User object or None.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        # Use DictCursor to get results as dictionaries (column_name: value)
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                print(f"\n--- Querying User (One-to-One) for user_ID: {user_id} ---")
                # psycopg2.extras.DictCursor already deserializes JSONB columns
                list_of_list_ids = user_data['list_of_list_ids'] if user_data['list_of_list_ids'] is not None else []
                user = User(
                    user_ID=user_data['user_id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    list_of_list_ids=list_of_list_ids,
                    access_token=user_data['access_token'],
                    refresh_token=user_data['refresh_token'],
                    token_type=user_data['token_type'],
                    token_expiry=user_data['token_expiry'],
                    preferred_location=user_data['preferred_location']
                )
                print(f"Found User: {user.username} (Email: {user.email})")
                return user
            else:
                print(f"\n--- Querying User (One-to-One) for user_ID: {user_id} ---")
                print(f"User with ID '{user_id}' not found.")
                return None
    except psycopg2.Error as e:
        print(f"Error querying user by ID: {e}")
        return None
    finally:
        conn.close()

def get_grocery_list_ids_for_user(user_id):
    """
    Queries the 'grocery_lists' table for all list_IDs associated with a user_ID (One-to-Many).
    Returns a list of list_IDs or an empty list if none found/user doesn't exist.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT list_id FROM grocery_lists WHERE user_id = %s ORDER BY timestamp DESC;", (user_id,))
            list_ids = [row[0] for row in cur.fetchall()]
            print(f"\n--- Querying List IDs (One-to-Many) for user_ID: {user_id} ---")
            if list_ids:
                print(f"Found List IDs for user '{user_id}': {list_ids}")
            else:
                print(f"User '{user_id}' has no grocery lists or user not found in grocery_lists table.")
            return list_ids
    except psycopg2.Error as e:
        print(f"Error querying list IDs for user: {e}")
        return []
    finally:
        conn.close()

def get_grocery_list_details(list_id):
    """
    Retrieves a complete GroceryList object, including its products, by list_ID.
    This now fetches product details directly from grocery_list_items.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            print(f"\n--- Retrieving Grocery List Details for list_ID: {list_id} ---")

            # First, get the grocery list metadata
            cur.execute("SELECT list_id, user_id, timestamp FROM grocery_lists WHERE list_id = %s;", (list_id,))
            list_data = cur.fetchone()

            if not list_data:
                print(f"Grocery list with ID '{list_id}' not found.")
                return None

            # Now, get all products associated with this grocery list directly from grocery_list_items
            cur.execute("""
                SELECT
                    list_item_id, list_id, name, price, promo_price, fufillment_type, aisle,
                    inventory, size, last_updated, location_id, upc, quantity
                FROM grocery_list_items
                WHERE list_id = %s;
            """, (list_id,))
            product_items_data = cur.fetchall()

            products_on_list = []
            for item_data in product_items_data:
                product = Product(
                    name=item_data['name'],
                    price=item_data['price'],
                    promo_price=item_data['promo_price'],
                    fufillment_type=item_data['fufillment_type'],
                    brand=item_data['aisle'],  # Using aisle column for brand data
                    inventory=item_data['inventory'],
                    size=item_data['size'],
                    last_updated=item_data['last_updated'],
                    location_ID=item_data['location_id'],
                    upc=item_data['upc']
                )
                products_on_list.append((product, item_data['quantity']))

            grocery_list = GroceryList(
                list_ID=list_data['list_id'],
                user_ID=list_data['user_id'],
                timestamp=list_data['timestamp'],
                products_on_list=products_on_list
            )
            print(f"Found Grocery List '{grocery_list.list_id}' for user '{grocery_list.user_id}'.")
            print(f"  Items ({len(grocery_list.products_on_list)}):")
            for prod, qty in grocery_list.products_on_list:
                print(f"    - {prod.name} (UPC: {prod.upc}, Quantity: {qty}, Price: ${prod.price:.2f})")
            return grocery_list

    except psycopg2.Error as e:
        print(f"Error retrieving grocery list details: {e}")
        return None
    finally:
        conn.close()

def add_user_to_db(user_obj):
    """
    Adds a new user or updates an existing user in the 'users' table.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn.cursor() as cur:
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
        print(f"User '{user_obj.username}' ({user_obj.user_id}) added/updated in the database.")
        return True
    except psycopg2.Error as e:
        print(f"Error adding/updating user '{user_obj.username}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def add_grocery_list_to_db(grocery_list_obj):
    """
    Adds a new grocery list and its items to the database.
    Also updates the user's list_of_list_ids.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # 1. Insert/Update grocery_lists metadata
            cur.execute("""
                INSERT INTO grocery_lists (list_id, user_id, timestamp)
                VALUES (%s, %s, %s)
                ON CONFLICT (list_id) DO UPDATE SET
                    user_id = EXCLUDED.user_id, timestamp = EXCLUDED.timestamp;
            """, (grocery_list_obj.list_id, grocery_list_obj.user_id, grocery_list_obj.timestamp))
            print(f"Grocery list '{grocery_list_obj.list_id}' metadata added/updated.")

            # 2. Delete existing items for this list to prevent duplicates on re-insertion
            # This is important if you're re-adding a list that might have changed items.
            cur.execute("DELETE FROM grocery_list_items WHERE list_id = %s;", (grocery_list_obj.list_id,))
            print(f"Existing items for list '{grocery_list_obj.list_id}' cleared.")

            # 3. Insert grocery_list_items
            for product, quantity in grocery_list_obj.products_on_list:
                # Convert inventory string to integer for database
                inventory_int = None
                if product.inventory:
                    if isinstance(product.inventory, str):
                        inventory_map = {"HIGH": 100, "MEDIUM": 50, "LOW": 10, "OUT_OF_STOCK": 0, "UNKNOWN": None}
                        inventory_int = inventory_map.get(product.inventory.upper(), None)
                    else:
                        inventory_int = product.inventory
                
                cur.execute("""
                    INSERT INTO grocery_list_items (list_id, name, price, promo_price, fufillment_type, aisle, inventory, size, last_updated, location_id, upc, quantity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    grocery_list_obj.list_id,
                    product.name,
                    product.price,
                    product.promo_price,
                    product.fufillment_type,
                    product.brand,  # Using brand field for aisle column
                    inventory_int,  # Converted to integer
                    product.size,
                    product.last_updated,
                    product.location_ID,
                    product.upc,
                    quantity
                ))
            print(f"Items for grocery list '{grocery_list_obj.list_id}' inserted.")

            # 4. Update the user's list_of_list_ids in the users table
            # Fetch current list_of_list_ids
            cur.execute("SELECT list_of_list_ids FROM users WHERE user_id = %s;", (grocery_list_obj.user_id,))
            user_data = cur.fetchone()
            if user_data:
                current_list_ids = user_data['list_of_list_ids'] if user_data['list_of_list_ids'] is not None else []
                if grocery_list_obj.list_id not in current_list_ids:
                    current_list_ids.append(grocery_list_obj.list_id)
                    cur.execute("""
                        UPDATE users
                        SET list_of_list_ids = %s
                        WHERE user_id = %s;
                    """, (json.dumps(current_list_ids), grocery_list_obj.user_id))
                    print(f"User '{grocery_list_obj.user_id}' list_of_list_ids updated.")
            else:
                print(f"Warning: User '{grocery_list_obj.user_id}' not found when trying to update list_of_list_ids.")


        conn.commit()
        print(f"Grocery list '{grocery_list_obj.list_id}' and its items successfully added to the database.")
        return True
    except psycopg2.Error as e:
        print(f"Error adding grocery list '{grocery_list_obj.list_id}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
def remove_grocery_list(list_id):
    """
    Removes a specific grocery list and all its items from the database.
    Also removes the list ID from the associated user's list_of_list_ids.
    Due to ON DELETE CASCADE on grocery_list_items, deleting the list
    will automatically delete its items.
    """
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT user_id FROM grocery_lists WHERE list_id = %s;", (list_id,))
            result = cur.fetchone()
            if not result:
                print(f"Grocery list with ID '{list_id}' not found. Cannot remove.")
                return False
            user_id = result['user_id']
            cur.execute("DELETE FROM grocery_lists WHERE list_id = %s;", (list_id,))
            print(f"Grocery list '{list_id}' and its items successfully removed.")
            cur.execute("SELECT list_of_list_ids FROM users WHERE user_id = %s;", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                current_list_ids = user_data['list_of_list_ids'] if user_data['list_of_list_ids'] is not None else []
                if list_id in current_list_ids:
                    current_list_ids.remove(list_id)
                    cur.execute("""
                        UPDATE users
                        SET list_of_list_ids = %s
                        WHERE user_id = %s;
                    """, (json.dumps(current_list_ids), user_id))
                    print(f"User '{user_id}' list_of_list_ids updated to remove '{list_id}'.")
                else:
                    print(f"Warning: List ID '{list_id}' not found in user '{user_id}'s list_of_list_ids, but list was deleted.")
            else:
                print(f"Warning: User '{user_id}' not found when trying to update list_of_list_ids after list deletion.")

            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Error removing grocery list '{list_id}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def remove_user(user_id):
    """
    Removes a user and all their associated grocery lists and list items from the database.
    Due to CASCADE DELETE on foreign keys, deleting a user will automatically
    delete their grocery lists and their associated items.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_id,))
            if not cur.fetchone():
                print(f"User with ID '{user_id}' not found. Cannot remove.")
                return False

            cur.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
            conn.commit()
            print(f"User '{user_id}' and all associated data successfully removed from the database.")
            return True
    except psycopg2.Error as e:
        print(f"Error removing user '{user_id}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_user_details(user_obj):
    """
    Updates the details of an existing user in the 'users' table.
    The user_obj should contain the user_ID of the user to update,
    and all other fields with their desired new values.
    """
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_obj.user_id,))
            if not cur.fetchone():
                print(f"User with ID '{user_obj.user_id}' not found. Cannot update.")
                return False

            cur.execute("""
                UPDATE users
                SET username = %s,
                    email = %s,
                    password = %s,
                    preferred_location = %s,
                    access_token = %s,
                    refresh_token = %s,
                    token_type = %s,
                    token_expiry = %s,
                    list_of_list_ids = %s
                WHERE user_id = %s;
            """, (user_obj.username, user_obj.email, user_obj.password, user_obj.preferred_location,
                  user_obj.access_token, user_obj.refresh_token, user_obj.token_type, user_obj.token_expiry,
                  json.dumps(user_obj.list_of_list_ids), user_obj.user_id))
        conn.commit()
        print(f"User '{user_obj.username}' ({user_obj.user_id}) details updated successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error updating user '{user_obj.username}' ({user_obj.user_id}): {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

