import db_utils
from user import User
from list import GroceryList
from product import Product
from datetime import datetime, timezone, timedelta
import uuid

def run_demo():
    print("--- Starting Database Demo ---")

    # 1. Initialize and Create Tables
    print("\n--- Step 1: Creating Tables ---")
    db_utils.create_tables()

    # 2. Add Users
    print("\n--- Step 2: Adding Users ---")
    user1_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc)
    expiry_time = current_time + timedelta(hours=1)
    user1 = User(user_ID=user1_id, username="alice_smith", email="alice@example.com",
                 password="password123", list_of_list_ids=[], access_token="token_alice_123",
                 refresh_token="refresh_alice_abc", token_type="Bearer", token_expiry=expiry_time,
                 preferred_location="Seattle")

    db_utils.add_user_to_db(user1)

    # 3. Get User Details
    print("\n--- Step 3: Getting User Details ---")
    retrieved_user1 = db_utils.get_user_by_id(user1_id)

    # 4. Add Grocery Lists for User 1
    print("\n--- Step 4: Creating Products for Grocery List---")
    product_apple = Product(
        name="Apple", price=1.50, promo_price=1.20, fufillment_type="In-Store",
        aisle="Produce", inventory=100, size="Medium", last_updated=datetime.now(timezone.utc),
        location_ID="LocA", upc="123456789012"
    )
    product_milk = Product(
        name="Milk (Whole)", price=3.99, promo_price=3.50, fufillment_type="Delivery",
        aisle="Dairy", inventory=50, size="Gallon", last_updated=datetime.now(timezone.utc),
        location_ID="LocB", upc="987654321098"
    )
    product_bread = Product(
        name="Whole Wheat Bread", price=2.75, promo_price=None, fufillment_type="In-Store",
        aisle="Bakery", inventory=30, size="Standard", last_updated=datetime.now(timezone.utc),
        location_ID="LocC", upc="555444333222"
    )

    print("\n--- Step 5: Adding Products for Grocery List---")
 
    # List 1 for User 1
    list1_id = str(uuid.uuid4())
    grocery_list1 = GroceryList(list_ID=list1_id, user_ID=user1_id, timestamp=datetime.now(timezone.utc))
    grocery_list1.products_on_list.append((product_apple, 5))
    grocery_list1.products_on_list.append((product_milk, 1))
    db_utils.add_grocery_list_to_db(grocery_list1)

    # List 2 for User 1
    list2_id = str(uuid.uuid4())
    grocery_list2 = GroceryList(list_ID=list2_id, user_ID=user1_id, timestamp=datetime.now(timezone.utc))
    grocery_list2.products_on_list.append((product_bread, 2))
    grocery_list2.products_on_list.append((product_apple, 3))
    db_utils.add_grocery_list_to_db(grocery_list2)

    # 5. Get Grocery List IDs for User
    print("\n--- Step 5: Getting Grocery List IDs for User 1 ---")
    user1_list_ids = db_utils.get_grocery_list_ids_for_user(user1_id)
    print(f"User 1's list IDs: {user1_list_ids}")

    # 6. Get Grocery List Details
    print("\n--- Step 6: Getting Grocery List Details ---")
    retrieved_list1 = db_utils.get_grocery_list_details(list1_id)
    print(f"Retrieved List 1 ID: {retrieved_list1.list_id}, User ID: {retrieved_list1.user_id}, Items: {len(retrieved_list1.products_on_list)}")
    for prod, qty in retrieved_list1.products_on_list:
        print(f"  - {prod.name} (Qty: {qty}, Price: ${prod.price:.2f}, UPC: {prod.upc})")

    # 7. Update User Details
    print("\n--- Step 7: Updating User Details ---")
    retrieved_user1.preferred_location = "Redmond"
    retrieved_user1.username = "alice_wonderland"
    db_utils.update_user_details(retrieved_user1)

    updated_user1 = db_utils.get_user_by_id(user1_id)
    if updated_user1:
        print(f"Updated User 1: {updated_user1.username} (Location: {updated_user1.preferred_location})")



    # 10. Remove Grocery List
    print("\n--- Step 8: Removing a Grocery List ---")
    db_utils.remove_grocery_list(list1_id)
    check_list3 = db_utils.get_grocery_list_details(list1_id)
    if not check_list3:
        print(f"Verification: Grocery list '{list1_id}' is indeed removed.")



    # 11. Remove User
    print("\n--- Step 9: Removing a User ---")
    db_utils.remove_user(user1_id)

    # Verify user and their lists are gone
    check_user1 = db_utils.get_user_by_id(user1_id)
    if not check_user1:
        print(f"Verification: User '{user1_id}' is indeed removed.")
    check_list1 = db_utils.get_grocery_list_details(list1_id)
    if not check_list1:
        print(f"Verification: Grocery list '{list1_id}' (associated with user1) is also removed.")

    # 12. Drop Tables (Cleanup)
    print("\n--- Step 10: Dropping Tables (Cleanup) ---")
    db_utils.drop_tables()
    print("\n--- Database Demo Finished ---")
if __name__ == "__main__":
    run_demo()