import datetime
class Product:
    def __init__(self, name, price, promo_price, fufillment_type, brand, inventory, size, last_updated, location_ID, upc):
        self.name = name
        self.price = price
        self.promo_price = promo_price
        self.fufillment_type = fufillment_type
        self.brand = brand
        self.inventory = inventory 
        self.size = size
        self.last_updated = last_updated 
        self.location_ID = location_ID
        self.upc = upc 

    def to_dict(self):
        """Converts Product object to a dictionary for easier storage/transfer."""
        return {
            "name": self.name,
            "price": float(self.price),
            "promo_price": float(self.promo_price) if self.promo_price is not None else None,
            "fufillment_type": self.fufillment_type,
            "brand": self.brand,
            "inventory": self.inventory,
            "size": self.size,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "location_ID": self.location_ID,
            "upc": self.upc
        }

    @staticmethod
    def from_dict(data):
        """Creates a Product object from a dictionary."""
        return Product(
            name=data.get("name"),
            price=data.get("price"),
            promo_price=data.get("promo_price"),
            fufillment_type=data.get("fufillment_type"),
            brand=data.get("brand"),
            inventory=data.get("inventory"),
            size=data.get("size"),
            last_updated=datetime.fromisoformat(data["last_updated"]) if data.get("last_updated") else None,
            location_ID=data.get("location_ID"),
            upc=data.get("upc")
        )