class GroceryList:
    def __init__(self, list_ID, user_ID, timestamp, products_on_list=None):
        self.list_id = list_ID
        self.user_id = user_ID
        self.timestamp = timestamp
        self.products_on_list = products_on_list if products_on_list is not None else []
