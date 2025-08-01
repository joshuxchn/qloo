import psycopg2
import psycopg2.extras
import json
from .list import GroceryList
from .product import Product
from .user import User

DB_NAME = "grocery_app"
DB_USER = "joshuachen"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    conn = get_db_connection()
    if conn is None: return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    access_token TEXT,
                    refresh_token TEXT,
                    token_type TEXT,
                    token_expiry TIMESTAMP WITH TIME ZONE,
                    list_of_list_ids JSONB DEFAULT '[]'::jsonb,
                    first_name TEXT,
                    last_name TEXT,
                    preferred_location TEXT,
                    budget INTEGER,
                    shopping_frequency TEXT,
                    shopping_priority TEXT,
                    dietary_restrictions JSONB,
                    allergies JSONB,
                    health_goals TEXT,
                    favorite_cuisines JSONB,
                    cultural_background TEXT,
                    favorite_foods TEXT,
                    age INTEGER,
                    gender TEXT
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS grocery_lists (
                    list_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                    name TEXT NOT NULL DEFAULT 'My Grocery List',
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS grocery_list_items (
                    list_item_id SERIAL PRIMARY KEY,
                    list_id TEXT NOT NULL REFERENCES grocery_lists(list_id) ON DELETE CASCADE,
                    name TEXT NOT NULL,
                    price NUMERIC(10, 2),
                    promo_price NUMERIC(10, 2),
                    fulfillment_type TEXT,
                    brand TEXT,
                    inventory TEXT,
                    size TEXT,
                    last_updated TIMESTAMP WITH TIME ZONE,
                    location_id TEXT,
                    upc TEXT,
                    quantity INTEGER NOT NULL DEFAULT 1,
                    category TEXT
                );
            """)
        conn.commit()
        print("✅ Tables ensured to exist.")
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = get_db_connection()
    if conn is None: return None
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                return User(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    list_of_list_ids=user_data.get('list_of_list_ids') or [],
                    access_token=user_data.get('access_token'),
                    refresh_token=user_data.get('refresh_token'),
                    token_type=user_data.get('token_type'),
                    token_expiry=user_data.get('token_expiry'),
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                    preferred_location=user_data.get('preferred_location'),
                    budget=user_data.get('budget'),
                    shopping_frequency=user_data.get('shopping_frequency'),
                    shopping_priority=user_data.get('shopping_priority'),
                    dietary_restrictions=user_data.get('dietary_restrictions'),
                    allergies=user_data.get('allergies'),
                    health_goals=user_data.get('health_goals'),
                    favorite_cuisines=user_data.get('favorite_cuisines'),
                    cultural_background=user_data.get('cultural_background'),
                    favorite_foods=user_data.get('favorite_foods'),
                    age=user_data.get('age'),
                    gender=user_data.get('gender')
                )
            return None
    finally:
        conn.close()

def add_user_to_db(user_obj):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (user_id, username, email, password)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            """, (user_obj.user_id, user_obj.username, user_obj.email, user_obj.password))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print(f"Error adding user '{user_obj.username}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_user_details(user_obj):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users SET
                    username = %s, email = %s, first_name = %s, last_name = %s,
                    preferred_location = %s, budget = %s, shopping_frequency = %s,
                    shopping_priority = %s, dietary_restrictions = %s, allergies = %s,
                    health_goals = %s, favorite_cuisines = %s, cultural_background = %s,
                    favorite_foods = %s, age = %s, gender = %s
                WHERE user_id = %s;
            """, (
                user_obj.username, user_obj.email, user_obj.first_name, user_obj.last_name,
                user_obj.preferred_location, user_obj.budget, user_obj.shopping_frequency,
                user_obj.shopping_priority, json.dumps(user_obj.dietary_restrictions),
                json.dumps(user_obj.allergies), user_obj.health_goals,
                json.dumps(user_obj.favorite_cuisines), user_obj.cultural_background,
                user_obj.favorite_foods, user_obj.age, user_obj.gender,
                user_obj.user_id
            ))
        conn.commit()
        print(f"✅ User '{user_obj.username}' details updated successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error updating user '{user_obj.username}': {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def add_grocery_list_to_db(grocery_list_obj):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO grocery_lists (list_id, user_id, name, timestamp)
                VALUES (%s, %s, %s, %s);
            """, (grocery_list_obj.list_id, grocery_list_obj.user_id, grocery_list_obj.name, grocery_list_obj.timestamp))

            for product, quantity in grocery_list_obj.products_on_list:
                cur.execute("""
                    INSERT INTO grocery_list_items (
                        list_id, name, price, promo_price, fulfillment_type, brand,
                        inventory, size, last_updated, location_id, upc, quantity, category
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    grocery_list_obj.list_id, product.name, product.price, product.promo_price,
                    product.fulfillment_type, product.brand, product.inventory, product.size,
                    product.last_updated, product.location_ID, product.upc, quantity, product.category
                ))
        
        conn.commit()
        print(f"✅ Grocery list '{grocery_list_obj.name}' saved successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error adding grocery list: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_all_lists_for_user(user_id):
    conn = get_db_connection()
    if conn is None: return []
    
    lists = []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM grocery_lists WHERE user_id = %s ORDER BY timestamp DESC;", (user_id,))
            list_records = cur.fetchall()

            for list_record in list_records:
                cur.execute("SELECT * FROM grocery_list_items WHERE list_id = %s;", (list_record['list_id'],))
                item_records = cur.fetchall()
                items = [dict(item) for item in item_records]
                list_data = dict(list_record)
                list_data['items'] = items
                lists.append(list_data)
        return lists
    except psycopg2.Error as e:
        print(f"Error getting lists for user: {e}")
        return []
    finally:
        conn.close()

def remove_grocery_list(list_id, user_id):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM grocery_lists WHERE list_id = %s AND user_id = %s;", (list_id, user_id))
            conn.commit()
            if cur.rowcount > 0:
                print(f"✅ List {list_id} deleted successfully.")
                return True
            else:
                print(f"⚠️ Warning: List {list_id} not found or permission denied for user {user_id}.")
                return False
    except psycopg2.Error as e:
        print(f"Error removing grocery list: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_grocery_list(list_obj, user_id):
    conn = get_db_connection()
    if conn is None: return False
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM grocery_lists WHERE list_id = %s AND user_id = %s;", (list_obj.list_id, user_id))
            if cur.fetchone() is None:
                return False

            cur.execute("UPDATE grocery_lists SET name = %s WHERE list_id = %s;", (list_obj.name, list_obj.list_id))
            
            cur.execute("DELETE FROM grocery_list_items WHERE list_id = %s;", (list_obj.list_id,))

            for product, quantity in list_obj.products_on_list:
                cur.execute("""
                    INSERT INTO grocery_list_items (
                        list_id, name, price, promo_price, fulfillment_type, brand,
                        inventory, size, last_updated, location_id, upc, quantity, category
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    list_obj.list_id, product.name, product.price, product.promo_price,
                    product.fulfillment_type, product.brand, product.inventory, product.size,
                    product.last_updated, product.location_ID, product.upc, quantity, product.category
                ))

        conn.commit()
        print(f"✅ List {list_obj.list_id} updated successfully.")
        return True
    except psycopg2.Error as e:
        print(f"Error updating grocery list: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()