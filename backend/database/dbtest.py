import os
import json
from databaseInteractions import Database, all_grocery_lists_to_json, user_grocery_lists_to_json
from datetime import datetime, timedelta, timezone

DB_PARAMS = {
    "dbname": "grocery_app",
    "user": "joshuachen",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

def test_all_methods():
    try:
        with Database(DB_PARAMS) as db:
            print("\nCreating tables...")
            db.create_tables()

            print("\nClearing all test data...")
            db.clear_all_data_for_testing()

            print("\nTesting user management...")
            user_id = db.add_user('testuser', 'test@example.com', 'supersecret')
            assert user_id is not None, "User creation failed"
            user = db.get_user_by_username('testuser')
            assert user['email'] == 'test@example.com'
            print(f"Added user: {user['username']}")

            print("\nTesting product/store creation...")
            db.add_or_update_product('0001111041700', 'Organic Whole Milk', 'Simple Truth', '0001111041700')
            db.add_or_update_product('0004133100040', 'Vitamin D Milk', 'Kroger', '0004133100040')
            db.add_or_update_store('70100123', 'QFC - U-Village', '2746 NE 45th St, Seattle, WA 98105', '98105')
            print("Products and store added.")

            print("\nTesting store product pricing...")
            db.add_or_update_store_product(
                store_id='70100123',
                product_upc='0001111041700',
                regular_price=6.99,
                promo_price=6.49,
                stock_level='HIGH',
                is_available=True
            )
            info = db.get_store_product_info('70100123', '0001111041700')
            assert info is not None
            print(f"Store product added with price: ${info['regular_price']}")

            print("\nTesting grocery list creation and items...")
            list_id = db.create_grocery_list(user_id, "Weekly List")
            assert list_id is not None
            print(f"Created list ID {list_id}")

            db.add_item_to_list(list_id, '0001111041700', quantity=1)
            db.add_item_to_list(list_id, '0004133100040', quantity=2)
            print("Items added to grocery list.")

            db.update_item_quantity(list_id, '0004133100040', 5)
            db.remove_item_from_list(list_id, '0001111041700')
            print("Updated and removed list items.")

            contents = db.get_list_contents(list_id)
            assert len(contents) == 1
            print(f"List contains {len(contents)} item(s):")
            for item in contents:
                print(f" - {item['name']} (x{item['quantity']})")

            print("\nTesting list retrieval...")
            lists = db.get_user_lists(user_id)
            assert len(lists) == 1
            print(f"User has {len(lists)} grocery list(s).")

            # ✅ Test: get_all_lists_with_details
            print("\nTesting get_all_lists_with_details()...")
            all_list_details = db.get_all_lists_with_details()
            assert any(d['username'] == 'testuser' for d in all_list_details), "User not found in all_list_details"
            print("Successfully fetched all grocery list details.")

            # ✅ Test: Export all grocery lists to JSON
            print("\nTesting all_grocery_lists_to_json()...")
            all_grocery_lists_to_json(db)
            assert os.path.exists("all_grocery_lists.json")
            with open("all_grocery_lists.json", "r") as f:
                data = json.load(f)
                assert any("items" in d for d in data.values())
            print("Exported all grocery lists to JSON.")

            # ✅ Test: Export specific user grocery lists to JSON
            print("\nTesting user_grocery_lists_to_json()...")
            user_grocery_lists_to_json(db, user_id)
            expected_file = f"user_{user_id}_lists.json"
            assert os.path.exists(expected_file)
            with open(expected_file, "r") as f:
                user_data = json.load(f)
                assert isinstance(user_data, list) and len(user_data) > 0
            print(f"Exported user {user_id} grocery lists to JSON.")

            print("\nTesting list deletion...")
            deleted = db.delete_grocery_list(list_id, user_id)
            assert deleted
            print("Grocery list deleted.")

            print("\n✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == '__main__':
    test_all_methods()
