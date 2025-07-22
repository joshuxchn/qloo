#brew install postgresql
#pip install psycopg2-binary
#brew services start postgresql
# createdb grocery_app
# user = whoami
import psycopg2
import psycopg2.extras
from datetime import datetime, timezone
import json # This import should be at the module level

class Database:
    def __init__(self, db_params):
        """
        Initializes the Database object and stores connection parameters.
        Args:
            db_params (dict): A dictionary with database connection details
                              (e.g., dbname, user, password, host, port).
        """
        self.db_params = db_params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Establishes the database connection and returns the cursor."""
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return self
        except psycopg2.OperationalError as e:
            print(f"Error connecting to the database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits changes and closes the connection and cursor."""
        if self.conn:
            if exc_type: # If an exception occurred, rollback
                self.conn.rollback()
            else: # Otherwise, commit
                self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def create_tables(self):
        """Creates all necessary tables if they don't already exist."""
        print("Creating database tables...")
        commands = (
            """
            CREATE TABLE IF NOT EXISTS Users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                upc VARCHAR(14) PRIMARY KEY,
                name TEXT NOT NULL,
                brand VARCHAR(255),
                kroger_product_id VARCHAR(13) UNIQUE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS stores (
                location_id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address TEXT,
                zip_code VARCHAR(10)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS store_products (
                store_id VARCHAR(10),
                product_upc VARCHAR(14),
                regular_price DECIMAL(10, 2),
                promo_price DECIMAL(10, 2),
                stock_level VARCHAR(30) CHECK (stock_level IN ('HIGH', 'LOW', 'TEMPORARILY_OUT_OF_STOCK', 'UNKNOWN')),
                is_available_instore BOOLEAN DEFAULT FALSE,
                last_updated TIMESTAMP WITH TIME ZONE NOT NULL,
                PRIMARY KEY (store_id, product_upc),
                FOREIGN KEY (store_id) REFERENCES stores(location_id) ON DELETE CASCADE,
                FOREIGN KEY (product_upc) REFERENCES products(upc) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS GroceryLists (
                list_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                list_name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS GroceryListItems (
                list_id INT NOT NULL,
                product_upc VARCHAR(14) NOT NULL,
                quantity INT DEFAULT 1,
                added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (list_id, product_upc),
                FOREIGN KEY (list_id) REFERENCES GroceryLists(list_id) ON DELETE CASCADE,
                FOREIGN KEY (product_upc) REFERENCES products(upc) ON DELETE CASCADE
            );
            """
        )
        for command in commands:
            self.cursor.execute(command)
        print("Tables created successfully.")

    # --- User Management ---
    def add_user(self, username, email, password_hash):
        """Adds a new user and returns their ID."""
        sql = "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING user_id;"
        try:
            self.cursor.execute(sql, (username, email, password_hash))
            return self.cursor.fetchone()['user_id']
        except psycopg2.IntegrityError:
            return None # Indicates user already exists

    def get_user_by_username(self, username):
        """Fetches a user by their username."""
        self.cursor.execute("SELECT * FROM Users WHERE username = %s;", (username,))
        return self.cursor.fetchone()

    # --- Product & Store Data Management ---
    def add_or_update_product(self, upc, name, brand, kroger_product_id):
        """Adds a new product or updates it if it already exists."""
        sql = """
        INSERT INTO products (upc, name, brand, kroger_product_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (upc) DO UPDATE SET
            name = EXCLUDED.name,
            brand = EXCLUDED.brand;
        """
        self.cursor.execute(sql, (upc, name, brand, kroger_product_id))

    def add_or_update_store(self, location_id, name, address, zip_code):
        """Adds a new store or updates it if it already exists."""
        sql = """
        INSERT INTO stores (location_id, name, address, zip_code)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (location_id) DO UPDATE SET
            name = EXCLUDED.name,
            address = EXCLUDED.address,
            zip_code = EXCLUDED.zip_code;
        """
        self.cursor.execute(sql, (location_id, name, address, zip_code))

    def add_or_update_store_product(self, store_id, product_upc, regular_price, promo_price, stock_level, is_available):
        """Inserts or updates the price/availability info for a product at a specific store."""
        sql = """
        INSERT INTO store_products (store_id, product_upc, regular_price, promo_price, stock_level, is_available_instore, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (store_id, product_upc) DO UPDATE SET
            regular_price = EXCLUDED.regular_price,
            promo_price = EXCLUDED.promo_price,
            stock_level = EXCLUDED.stock_level,
            is_available_instore = EXCLUDED.is_available_instore,
            last_updated = EXCLUDED.last_updated;
        """
        self.cursor.execute(sql, (store_id, product_upc, regular_price, promo_price, stock_level, is_available, datetime.now(timezone.utc)))

    def get_store_product_info(self, store_id, product_upc):
        """
        Retrieves stored product info for a given store and UPC.
        This method does NOT check if the data is stale. The application
        layer is responsible for checking the 'last_updated' timestamp.
        """
        sql = "SELECT * FROM store_products WHERE store_id = %s AND product_upc = %s;"
        self.cursor.execute(sql, (store_id, product_upc))
        return self.cursor.fetchone()

    # --- Grocery List Management ---
    def create_grocery_list(self, user_id, list_name):
        """Creates a new grocery list for a user and returns the new list's ID."""
        sql = "INSERT INTO GroceryLists (user_id, list_name) VALUES (%s, %s) RETURNING list_id;"
        self.cursor.execute(sql, (user_id, list_name))
        return self.cursor.fetchone()['list_id']

    def get_user_lists(self, user_id):
        """Retrieves all grocery lists belonging to a user."""
        self.cursor.execute("SELECT * FROM GroceryLists WHERE user_id = %s;", (user_id,))
        return self.cursor.fetchall()
        
    def delete_grocery_list(self, list_id, user_id):
        """Deletes a grocery list, ensuring it belongs to the user."""
        self.cursor.execute("DELETE FROM GroceryLists WHERE list_id = %s AND user_id = %s;", (list_id, user_id))
        return self.cursor.rowcount > 0 # Returns True if a row was deleted

    # --- Grocery List Item Management ---
    def add_item_to_list(self, list_id, product_upc, quantity=1):
        """Adds a product to a grocery list. If it exists, does nothing."""
        sql = """
        INSERT INTO GroceryListItems (list_id, product_upc, quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (list_id, product_upc) DO NOTHING;
        """
        self.cursor.execute(sql, (list_id, product_upc, quantity))

    def update_item_quantity(self, list_id, product_upc, quantity):
        """Updates the quantity of an item on a list."""
        sql = "UPDATE GroceryListItems SET quantity = %s WHERE list_id = %s AND product_upc = %s;"
        self.cursor.execute(sql, (quantity, list_id, product_upc))

    def remove_item_from_list(self, list_id, product_upc):
        """Removes an item from a grocery list."""
        sql = "DELETE FROM GroceryListItems WHERE list_id = %s AND product_upc = %s;"
        self.cursor.execute(sql, (list_id, product_upc))

    def get_list_contents(self, list_id):
        """Retrieves all items on a grocery list with full product details."""
        sql = """
        SELECT
            gli.quantity,
            gli.product_upc,
            p.name,
            p.brand
        FROM GroceryListItems gli
        JOIN products p ON gli.product_upc = p.upc
        WHERE gli.list_id = %s;
        """
        self.cursor.execute(sql, (list_id,))
        return self.cursor.fetchall()
        
    def clear_all_data_for_testing(self):
        """DANGER: Deletes all data from all tables. For testing only."""
        print("\nWARNING: Deleting all data from tables.")
        self.cursor.execute("DELETE FROM GroceryListItems;")
        self.cursor.execute("DELETE FROM GroceryLists;")
        self.cursor.execute("DELETE FROM store_products;")
        self.cursor.execute("DELETE FROM stores;")
        self.cursor.execute("DELETE FROM products;")
        self.cursor.execute("DELETE FROM Users;")
        print("All data cleared.")

    def get_all_lists_with_details(self):
        """
        Retrieves all grocery lists along with user and item details.
        Returns a flat list of dictionaries for easier JSON structuring.
        """
        sql = """
        SELECT
            gl.list_id,
            gl.list_name,
            u.username,
            gli.quantity,
            p.name AS product_name,
            p.brand
        FROM GroceryLists gl
        JOIN Users u ON gl.user_id = u.user_id
        LEFT JOIN GroceryListItems gli ON gl.list_id = gli.list_id
        LEFT JOIN products p ON gli.product_upc = p.upc
        ORDER BY gl.list_id, gli.added_at;
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

# These functions should be outside the Database class
def user_grocery_lists_to_json(db: Database, user_id: int):
    """
    Fetches all grocery lists for a specific user and exports them to a JSON file.
    """
    print(f"\nExporting grocery lists for user {user_id} to JSON...")
    user_lists = db.get_user_lists(user_id)
    output_data = []

    for grocery_list in user_lists:
        list_id = grocery_list['list_id']
        list_contents = db.get_list_contents(list_id)
        output_data.append({
            "list_id": list_id,
            "list_name": grocery_list['list_name'],
            "created_at": grocery_list['created_at'].isoformat(),
            "items": [
                {
                    "product_upc": item['product_upc'],
                    "name": item['name'],
                    "brand": item['brand'],
                    "quantity": item['quantity']
                } for item in list_contents
            ]
        })

    file_path = f"user_{user_id}_lists.json"
    with open(file_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"Successfully exported user lists to {file_path}")

def all_grocery_lists_to_json(db: Database):
    """
    Fetches all grocery lists from all users and exports them to a JSON file.
    """
    print("\nExporting all grocery lists to JSON...")
    all_lists_raw = db.get_all_lists_with_details()
    
    structured_lists = {}
    for row in all_lists_raw:
        list_id = row['list_id']
        if list_id not in structured_lists:
            structured_lists[list_id] = {
                "list_name": row['list_name'],
                "owner": row['username'],
                "items": []
            }
        # Only add an item if product_name is not None (handles empty lists)
        if row['product_name'] is not None:
            structured_lists[list_id]['items'].append({
                "product_name": row['product_name'],
                "brand": row['brand'],
                "quantity": row['quantity']
            })

    file_path = "all_grocery_lists.json"
    with open(file_path, 'w') as f:
        json.dump(structured_lists, f, indent=4)
    print(f"Successfully exported all lists to {file_path}")