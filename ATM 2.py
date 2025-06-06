def show_balance():
    print(f"Balance is ₹{balance:.2f}")

def deposit():
    amount = float(input("Enter amount to deposit: "))
    if amount <= 0:
        print("Invalid amount. Try again.")
        return 0
    return amount

def withdraw():
    amount = float(input("Enter amount to withdraw: "))
    if amount > balance:
        print("Insufficient balance.")
        return 0
    elif amount <= 0:
        print("Invalid amount. Try again.")
        return 0
    return amount

user_pin = input("Set your 4-digit PIN: ")

for i in range(3):
    pin = input("Enter your PIN: ")
    if pin == user_pin:
        break
    else:
        print("Wrong PIN.")
else:
    print("Too many wrong attempts. Access denied.")
    exit()

balance = 0
while True:
    print("\n1. Show balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Enter choice (1-4): ")

    if choice == "1":
        show_balance()
    elif choice == "2":
        balance += deposit()
    elif choice == "3":
        balance -= withdraw()
    elif choice == "4":
        print("Thank you!")
        break
    else:
        print("Invalid choice.")
