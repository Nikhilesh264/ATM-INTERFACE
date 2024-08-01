def authenticate(user_data, entered_pin):
    return user_data["pin"] == entered_pin

def perform_transaction(user_data, choice, amount=None, recipient_user_id=None):
    if choice == "1":
        print(f"Current balance: {user_data['balance']}")
    
    elif choice == "2":
        if amount > user_data["balance"]:
            print("Insufficient funds")
        else:
            user_data["balance"] -= amount
            user_data["transaction_history"].append(f"Withdrawal of {amount}")
            print(f"Withdrawal successful. Current balance: {user_data['balance']}")
    
    elif choice == "3":
        user_data["balance"] += amount
        user_data["transaction_history"].append(f"Deposit of {amount}")
        print(f"Deposit successful. Current balance: {user_data['balance']}")
    
    elif choice == "4":
        if not recipient_user_id:
            print("Invalid recipient user ID")
            return

        recipient_user = users.get(recipient_user_id)

        if not recipient_user:
            print("Recipient's account not found.")
            return

        if amount > user_data["balance"]:
            print("Insufficient funds")
        else:
            user_data["balance"] -= amount
            user_data["transaction_history"].append(f"Transfer of {amount} to {recipient_user_id}")
            recipient_user["balance"] += amount
            recipient_user["transaction_history"].append(f"Transfer received from {user_data['user_id']}")
            print(f"Transfer successful. Current balance: {user_data['balance']}")
    
    elif choice == "5":
        print("\n".join(user_data["transaction_history"]))
    
    else:
        print("Invalid choice. Please try again.")

def create_user(user_id, pin, balance):
    return {
        "user_id": user_id,
        "pin": pin,
        "balance": balance,
        "transaction_history": []
    }

def main():
    global users
    users = {
        "user1": create_user("user1", "12345", 0),
        "user2": create_user("user2", "67890", 1000),
        "user3": create_user("user3", "01234", 32000),
        "user4": create_user("user4", "56789", 400000),
    }

    user_id = input("Enter your user ID: ")
    pin = input("Enter your PIN: ")

    user_data = users.get(user_id)

    if user_data and authenticate(user_data, pin):
        while True:
            print("\nATM Menu:")
            print("1. View Balance")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. View Transaction History")
            print("6. Quit")

            choice = input("Enter your choice: ")

            if choice == "6":
                print("Thank you for using the ATM.\n----- Have a nice day -----!")
                break
            elif choice in ("2", "3", "4"):
                try:
                    amount = float(input("Enter amount: "))
                except ValueError:
                    print("Invalid amount. Please enter a number.")
                    continue
                if choice == "4":
                    recipient_user_id = input("Enter recipient's user ID: ")
                    perform_transaction(user_data, choice, amount, recipient_user_id)
                else:
                    perform_transaction(user_data, choice, amount)
            else:
                perform_transaction(user_data, choice)

    else:
        print("Invalid user ID or PIN. Please try again.")

if __name__ == "__main__":
    main()