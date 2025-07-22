flowchart TD
    H["Main Application Loop / User Interaction"] -- Manage Grocery Lists --> GL_START["Initialize Grocery List Management"]
    GL_START --> GL_CHOICE{"Select Grocery List Action"}
    GL_CHOICE -- Create New List --> GL_CREATE_IN["Input: User ID, Grocery List Name"]
    GL_CREATE_IN --> GL_CREATE_CALL["Call create_grocery_list(user_id, list_name)"]
    GL_CREATE_CALL --> GL_CREATE_RES["Display New Grocery List ID"]
    GL_CREATE_RES --> GL_END["End Grocery List Management"]
    GL_CHOICE -- Retrieve User Lists --> GL_GET_IN["Input: User ID"]
    GL_GET_IN --> GL_GET_CALL["Call get_user_lists(user_id)"]
    GL_GET_CALL --> GL_GET_RES@{ label: "Display User's Grocery Lists" }
    GL_GET_RES --> GL_END
    GL_CHOICE -- Delete Existing List --> GL_DELETE_IN["Input: Grocery List ID, User ID"]
    GL_DELETE_IN --> GL_DELETE_CALL["Call delete_grocery_list(list_id, user_id)"]
    GL_DELETE_CALL --> GL_DELETE_RES{"Was List Deleted Successfully?"}
    GL_DELETE_RES -- Yes --> GL_DELETE_SUCCESS["Show Success Message"]
    GL_DELETE_RES -- No --> GL_DELETE_FAIL["Show Failure Message"]
    GL_DELETE_SUCCESS --> GL_END
    GL_DELETE_FAIL --> GL_END
    GL_END --> H
    H -- Manage Grocery List Items --> LI_START["Initialize Grocery List Item Management"]
    LI_START --> LI_CHOICE{"Select Item Action"}
    LI_CHOICE -- Add Item to List --> LI_ADD_IN["Input: List ID, Product UPC, Quantity"]
    LI_ADD_IN --> LI_ADD_CALL["Call add_item_to_list(list_id, product_upc, quantity)"]
    LI_ADD_CALL --> LI_ADD_RES["Confirm Item Added"]
    LI_ADD_RES --> LI_END["End Grocery List Item Management"]
    LI_CHOICE -- Update Item Quantity --> LI_UPDATE_IN["Input: List ID, Product UPC, New Quantity"]
    LI_UPDATE_IN --> LI_UPDATE_CALL["Call update_item_quantity(list_id, product_upc, quantity)"]
    LI_UPDATE_CALL --> LI_UPDATE_RES["Confirm Quantity Updated"]
    LI_UPDATE_RES --> LI_END
    LI_CHOICE -- Remove Item from List --> LI_REMOVE_IN["Input: List ID, Product UPC"]
    LI_REMOVE_IN --> LI_REMOVE_CALL["Call remove_item_from_list(list_id, product_upc)"]
    LI_REMOVE_CALL --> LI_REMOVE_RES["Confirm Item Removed"]
    LI_REMOVE_RES --> LI_END
    LI_CHOICE -- Get List Contents with Product Details --> LI_GET_IN["Input: Grocery List ID"]
    LI_GET_IN --> LI_GET_CALL["Call get_list_contents(list_id)"]
    LI_GET_CALL --> LI_GET_RES["Display List Items with Product Name, Brand, Quantity"]
    LI_GET_RES --> LI_END
    LI_CHOICE -- Get Product Pricing and Availability at Store --> LI_GET_STORE_PROD_IN["Input: Store ID, Product UPC"]
    LI_GET_STORE_PROD_IN --> LI_GET_STORE_PROD_CALL["Call get_store_product_info(store_id, product_upc)"]
    LI_GET_STORE_PROD_CALL --> LI_GET_STORE_PROD_RES["Display Regular Price, Promo Price, Stock Level, Availability"]
    LI_GET_STORE_PROD_RES --> LI_END
    LI_END --> H
    H -- Generate Reports / Export Data --> REP_START["Initialize Reporting Module"]
    REP_START --> REP_CHOICE{"Choose Report Type"}
    REP_CHOICE -- Export User Grocery Lists to JSON --> REP_USER_IN["Input: User ID"]
    REP_USER_IN --> REP_USER_CALL["Call user_grocery_lists_to_json(db, user_id)"]
    REP_USER_CALL --> REP_USER_RES@{ label: "Confirm File 'user_{ID}_lists.json' Created" }
    REP_USER_RES --> REP_END["Feed Reports to LLMs"]
    REP_CHOICE -- Export All Grocery Lists to JSON --> REP_ALL_CALL["Call all_grocery_lists_to_json(db)"]
    REP_ALL_CALL --> REP_ALL_RES@{ label: "Confirm File 'all_grocery_lists.json' Created" }
    REP_ALL_RES --> REP_END
    REP_END --> H
    H --> Z["Exit Application"]
    Z --> END["End Program"]
    GL_GET_RES@{ shape: rect}
    REP_USER_RES@{ shape: rect}
    REP_ALL_RES@{ shape: rect}


