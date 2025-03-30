import json
import datetime

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Format as "YYYY-MM-DD"

file_path = "/Users/jackhildebrand/Documents/Code/python projects/Expense Tracker/expenses.json"

# Initialize expenses
try:
    # Load existing data from the file if it exists
    with open(file_path, "r") as file:
        data = json.load(file)
        expenses = data.get("expenses", {})
except FileNotFoundError:
    # If the file doesn't exist, start fresh
    expenses = {}

def get_next_expense_id():
    """Calculate the next available expense ID dynamically."""
    if expenses:
        return max(map(int, expenses.keys())) + 1
    return 1

def add_expense(expense_date, expense_description, expense_amount):
    """Add a new expense to the dictionary."""
    expense_id = get_next_expense_id()
    expenses[expense_id] = {
        "date": expense_date,  # Use the provided date
        "description": expense_description,
        "amount": expense_amount
    }
    print(f"Expense added successfully (ID: {expense_id})")

def delete_expense(expense_id):
    """Delete an expense by its ID."""
    if expense_id in expenses:
        del expenses[expense_id]
        print(f"Expense with ID {expense_id} deleted successfully.")
    else:
        print(f"Expense with ID {expense_id} not found.")

def save_data():
    """Save the current state of expenses to the file."""
    with open(file_path, "w") as file:
        json.dump({"expenses": expenses}, file, indent=4)

def list_expenses():
    if not expenses:
        print("No expenses found.")
        return
    else:
        # Calculate dynamic column widths with extra padding for gaps
        id_width = max(len(str(expense_id)) for expense_id in expenses) + 4  # Add 4 for padding
        date_width = max(len(expense['date']) for expense in expenses.values()) + 4
        description_width = max(len(expense['description']) for expense in expenses.values()) + 4
        amount_width = max(len(expense['amount']) for expense in expenses.values()) + 4

        # Print the headers with dynamic widths and gaps
        print(f"{'ID'.ljust(id_width)}{'Date'.ljust(date_width)}{'Description'.ljust(description_width)}{'Amount'.ljust(amount_width)}")
        print("-" * (id_width + date_width + description_width + amount_width))  # Separator line

        # Print each expense with aligned columns and gaps
        for expense_id, expense in expenses.items():
            print(f"{str(expense_id).ljust(id_width)}{expense['date'].ljust(date_width)}{expense['description'].ljust(description_width)}{expense['amount'].ljust(amount_width)}")

# Main program loop
command = input("Enter command (add/delete/view/exit): ").strip().lower()

while command != "exit":
    if command == "add":
        expense_description = input("Enter expense description: ")
        expense_amount = input("Enter expense amount: ")
        add_expense(current_date, expense_description, expense_amount)  # Pass the current date
        save_data()
    elif command == "delete":
        try:
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)
            save_data()
        except ValueError:
            print("Invalid expense ID. Please enter a number.")
    elif command == "list":
        list_expenses()
    else:
        print("Invalid command. Please enter 'add', 'delete', 'view', or 'exit'.")
    
    command = input("Enter command (add/delete/view/exit): ").strip().lower()