from auth import signup, login
from product import add_product, view_products, edit_product, delete_product

print("1. Sign Up")
print("2. Log In")
choice = input("Choose: ")

username = input("Username: ")
password = input("Password: ")

if choice == '1':
    signup(username, password)
elif choice == '2':
    if login(username, password):
        print("Login successful!")
        while True:
            print("\n1. Add Product\n2. View Products\n3. Edit Product\n4. Delete Product\n5. Exit")
            option = input("Choose: ")

            if option == '1':
                name = input("Product name: ")
                quantity = int(input("Quantity: "))
                price = float(input("Price: "))
                add_product(name, quantity, price)

            elif option == '2':
                view_products()

            elif option == '3':
                product_id = int(input("Enter product ID to edit: "))
                new_name = input("New name: ")
                new_quantity = int(input("New quantity: "))
                new_price = float(input("New price: "))
                edit_product(product_id, new_name, new_quantity, new_price)

            elif option == '4':
                product_id = int(input("Enter product ID to delete: "))
                delete_product(product_id)

            elif option == '5':
                break

            else:
                print("Invalid choice.")
