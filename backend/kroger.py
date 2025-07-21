from kroger_api import KrogerAPI
import os
from dotenv import load_dotenv

load_dotenv("../.env")  
client_id = os.getenv("KROGER_CLIENT_ID")
client_secret = os.getenv("KROGER_CLIENT_SECRET")
zip_code = os.getenv("ZIP_CODE")


kroger = KrogerAPI()
tok = kroger.authorization.get_token_with_client_credentials("product.compact")

locs = kroger.location.search_locations(zip_code=zip_code, radius_in_miles=10, limit=5)
print(f"Found {len(locs.get('data', []))} stores")

if locs.get("data") and len(locs["data"]) > 0:
    store = locs["data"][0]
    location_id = store["locationId"]
    store_name = store.get("name", "Unknown Store")
    print(f"Using store: {store_name} (ID: {location_id})")
    
    products = kroger.product.search_products(term="milk", location_id=location_id, limit=5)
    print(f"Found {len(products.get('data', []))} products:")
    
    for product in products.get("data", []):
        name = product.get("description", "Unknown Product")
        price = product.get("items", [{}])[0].get("price", {}).get("regular", "N/A")
        print(f"  - {name}: ${price}")
else:
    print("❌ No stores found in the area")

