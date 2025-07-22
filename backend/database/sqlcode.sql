CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE GroceryLists (
    list_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    list_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE products (
    upc VARCHAR(14) PRIMARY KEY,
    name TEXT NOT NULL,
    brand VARCHAR(255),
    kroger_product_id VARCHAR(13) UNIQUE
);

CREATE TABLE stores (
    location_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    zip_code VARCHAR(10)
);

CREATE TABLE store_products (
    store_id VARCHAR(10),
    product_upc VARCHAR(14),
    regular_price DECIMAL(10, 2),
    promo_price DECIMAL(10, 2),
    stock_level VARCHAR(24) CHECK (stock_level IN ('HIGH', 'LOW', 'TEMPORARILY_OUT_OF_STOCK')),
    is_available_instore BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (store_id, product_upc),
    FOREIGN KEY (store_id) REFERENCES stores(location_id),
    FOREIGN KEY (product_upc) REFERENCES products(upc)
);

CREATE TABLE GroceryListItems (
    list_id INT NOT NULL,
    product_upc VARCHAR(14) NOT NULL,
    quantity INT DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (list_id, product_upc), -- Prevents adding the same item twice
    FOREIGN KEY (list_id) REFERENCES GroceryLists(list_id) ON DELETE CASCADE,
    FOREIGN KEY (product_upc) REFERENCES products(upc) ON DELETE CASCADE
);