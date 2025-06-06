from db import connect_db

def add_product(name, quantity, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO products (name, quantity, price)
    VALUES (?, ?, ?)
    ''', (name, quantity, price))
    conn.commit()
    conn.close()
    print("Product added.")

from db import connect_db

LOW_STOCK_THRESHOLD = 5

def view_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    # Optional: log to console for debugging
    if not products:
        print("No products found.")
    else:
        for p in products:
            id_, name, quantity, price = p
            print(f"ID: {id_}, Name: {name}, Quantity: {quantity}, Price: {price}")
            if quantity < LOW_STOCK_THRESHOLD:
                print("  *** LOW STOCK ALERT! ***")

    return products


def edit_product(product_id, new_name, new_quantity, new_price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE products
    SET name = ?, quantity = ?, price = ?
    WHERE id = ?
    ''', (new_name, new_quantity, new_price, product_id))
    conn.commit()
    conn.close()
    print(f"Product ID {product_id} updated.")

def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    print(f"Product ID {product_id} deleted.")
