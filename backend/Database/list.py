# backend/database/list.py

class GroceryList:
    def __init__(self, list_id, user_id, timestamp, name="Untitled List", products_on_list=None):
        self.list_id = list_id
        self.user_id = user_id
        self.name = name  # ADDED
        self.timestamp = timestamp
        # This will be a list of (Product, quantity) tuples
        self.products_on_list = products_on_list if products_on_list is not None else []