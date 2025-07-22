from datetime import datetime
import json

class Product:
    def __init__(self, upc: str, name: str, brand: str = None, kroger_product_id: str = None, quantity: int = 1):
        if not upc or not name:
            raise ValueError("Product UPC and Name cannot be empty.")
        self.upc = upc
        self.name = name
        self.brand = brand
        self.kroger_product_id = kroger_product_id
        self.quantity = quantity

    def __repr__(self):
        return f"Product(UPC='{self.upc}', Name='{self.name}', Quantity={self.quantity})"

    def to_dict(self):
        """Converts the Product object to a dictionary for JSON serialization."""
        return {
            "upc": self.upc,
            "name": self.name,
            "brand": self.brand,
            "kroger_product_id": self.kroger_product_id,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Product object from a dictionary (e.g., loaded from JSON)."""
        return cls(
            upc=data['upc'],
            name=data['name'],
            brand=data.get('brand'),
            kroger_product_id=data.get('kroger_product_id'),
            quantity=data.get('quantity', 1)
        )

class GroceryList:
    def __init__(self, list_name: str, user_id: int, list_id: int = None, products: list = None, created_at: datetime = None):
        if not list_name:
            raise ValueError("Grocery list name cannot be empty.")
        if not isinstance(user_id, int):
            raise ValueError("User ID must be an integer.")

        self.list_id = list_id
        self.user_id = user_id
        self.list_name = list_name
        self.products = []
        if products:
            for p_data in products:
                if isinstance(p_data, Product):
                    self.products.append(p_data)
                elif isinstance(p_data, dict):
                    # Allow dicts to be passed, assuming they are compatible with Product.from_dict
                    self.products.append(Product.from_dict(p_data))
                else:
                    raise TypeError("Items in 'products' list must be Product objects or dictionaries convertible to Product.")

        self.created_at = created_at if created_at else datetime.now()

    def add_product(self, product: Product):
        """Adds a product to the list, or updates its quantity if already present."""
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to a grocery list.")
        
        for p in self.products:
            if p.upc == product.upc:
                p.quantity += product.quantity
                print(f"Updated quantity for {product.name}. New quantity: {p.quantity}")
                return
        self.products.append(product)
        print(f"Added {product.name} to the list.")

    def remove_product(self, upc: str):
        """Removes a product from the list by its UPC."""
        initial_len = len(self.products)
        self.products = [p for p in self.products if p.upc != upc]
        if len(self.products) < initial_len:
            print(f"Removed product with UPC {upc} from the list.")
        else:
            print(f"Product with UPC {upc} not found in the list.")

    def update_product_quantity(self, upc: str, new_quantity: int):
        """Updates the quantity of a product on the list. Removes if quantity is 0 or less."""
        if new_quantity <= 0:
            self.remove_product(upc)
            return

        for p in self.products:
            if p.upc == upc:
                p.quantity = new_quantity
                print(f"Updated quantity for product {p.name} (UPC: {upc}) to {new_quantity}.")
                return
        print(f"Product with UPC {upc} not found in the list.")

    def get_product(self, upc: str):
        """Retrieves a product object from the list by its UPC."""
        for p in self.products:
            if p.upc == upc:
                return p
        return None

    def to_dict(self):
        """Converts the GroceryList object to a dictionary for JSON serialization."""
        return {
            "list_id": self.list_id,
            "list_name": self.list_name,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "products": [product.to_dict() for product in self.products]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a GroceryList object from a dictionary (typically loaded from JSONB)."""
        products = [Product.from_dict(p_data) for p_data in data.get('products', [])]
        created_at_str = data.get('created_at')
        created_at = datetime.fromisoformat(created_at_str) if created_at_str else None
        
        return cls(
            list_name=data['list_name'],
            user_id=data['user_id'],
            list_id=data.get('list_id'),
            products=products,
            created_at=created_at
        )