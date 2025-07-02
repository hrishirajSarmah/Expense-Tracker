import json
from datetime import datetime
from collections import defaultdict

class Expense:
    def __init__(self, username: str):
        self.username = username
        self.expense = []

    def add_expenses(self, amount: int, category: str, description: str, date: str):
        self.expense.append({
            'amount' : amount,
            'category' : category,
            'description' : description,
            'date' : date
        })

    def __str__(self):
        return f'{self.username} expenses'

    def view_expenses(self):
        print(f'+---{self.username}\'s expenses---+\n')
        if not self.expense:
            print("No expenses recorded yet.")
            return

        for i, exp in enumerate(self.expense, 1):
            print(f"--- Expense {i} ---")
            print(f"Amount: {exp['amount']}")
            print(f"Category: {exp['category']}")
            print(f"Description: {exp['description']}")
            print(f"Date: {exp['date']}\n")

        print('+----------------------+\n')


    def filter_expenses(self, category: str = None, date: str = None):
        print(f"Filtering expenses for {self.username}...")

        if category and date:
            print(f'Category: {category} & date: {date}\n')
        elif category:
            print(f'Category: {category}\n')
        elif date:
            print(f'Date: {date}\n')

        if not self.expense:
            print("No expenses recorded yet.")
            return

        for i, exp in enumerate(self.expense, 1):
            if category and date:
                if exp['category'] == category and exp['date'] == date:
                    print(f"--- Expense {i} ---")
                    print(f"Amount: {exp['amount']}")
                    print(f"Description: {exp['description']}")
            elif category:
                if exp['category'] == category:
                    print(f"--- Expense {i} ---")
                    print(f"Amount: {exp['amount']}")
                    print(f"Description: {exp['description']}")
                    print(f"Date: {exp['date']}\n")
            elif date:
                if exp['date'] == date:
                    print(f"--- Expense {i} ---")
                    print(f"Amount: {exp['amount']}")
                    print(f"Category: {exp['category']}")
                    print(f"Description: {exp['description']}")


    def total_expenses(self, category: str = None, date: str = None):
        total = 0

        for exp in self.expense:
            if category and date:
                if exp['category'] == category and exp['date'] == date:
                    total += exp['amount']

            elif category:
                if exp['category'] == category:
                    total += exp['amount']

            elif date:
                if exp['date'] == date:
                    total += exp['amount']

            else:
                total += exp['amount']

        print(f"\n{self.username}'s Total Expense", end='')
        if category:
            print(f" in category '{category}'", end='')
        if date:
            print(f" on date {date}", end='')
        print(f": ₹{total}")


    def save_expenses_history(self):
        filename = f'{self.username.lower()}_expenses.json'
        try:
            with open(filename, 'w') as f:
                json.dump(self.expense, f)
        except FileNotFoundError:
            print(f"No file {filename} found.")


    def load_expenses_history(self):
        filename = f'{self.username.lower()}_expenses.json'
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                    self.expense = data
                    print(f"Loaded {len(data)} expense(s) for {self.username} from {f}")
                else:
                    print("Error: Invalid data format.")
        except FileNotFoundError:
            print(f"No previous expense file found for {self.username}. Starting fresh.")
        except json.JSONDecodeError:
            print("Error: File is not valid JSON.")



if __name__ == "__main__":
    today = datetime.now().strftime("%y-%m-%d")
    print("\n---WELCOME TO EXPENSE TRACKER---\n", "This is a CLI-based expense tracker program\nto track your daily expenses.\n", sep='\n')

    # Person1 = Expense("Alice")
    # Person2 = Expense("Bob")
    #
    # Person1.add_expenses(100, 'Food', 'Lunch', today)
    # Person1.add_expenses(250, 'Entertainment', 'Movie', today)
    # Person1.add_expenses(1200, 'Food', 'Dinner', today)
    # Person1.add_expenses(100, 'Food', 'Breakfast', "2025-06-18")
    # Person1.add_expenses(100, 'Food', 'Snacks', '2025-06-13')
    # Person1.add_expenses(100, 'Entertainment', 'AM park', '2025-06-21')
    #
    #
    # Person2.add_expenses(3000, 'Hobbies', 'Hiking', today)
    # Person2.add_expenses(100, 'Food', 'Lunch', today)
    # Person2.add_expenses(550, 'Entertainment', 'Water Park', today)

    # print(Person1)
    # Person1.view_expenses()
    # Person2.view_expenses()
    # Person1.filter_expenses('Food')
    #
    # Person1.total_expenses('Food', "2025-06-18")
    # Person1.save_expenses_history()
    # Person2.save_expenses_history()

    users = {}
    curr_user = None
    running = True

    def add_user():
        global curr_user
        username = input('Username: ')

        if username in users:
            print('User already exists!')
        else:
            users[username] = Expense(username)
        curr_user = users[username]

    def switch_user():
        global curr_user
        username = input("Enter username to switch: ")
        if username in users:
            curr_user = users[username]
            print(f"Switched to user: {username}")
        else:
            print("User not found.")


    def view_expenses():
        if curr_user:
            curr_user.view_expenses()
        else:
            print("No active user. Please add or switch user.")

    def add_expenses():
        if curr_user:
            amount = int(input("Amount: "))
            category = input("Category: ")
            description = input("Description: ")
            date = input("Date (YYYY-MM-DD): ")
            curr_user.add_expenses(amount, category, description, date)
        else:
            print("No active user. Please add or switch user.")


    def filter_expenses():
        if curr_user:
            category = input("Category: ")
            date = input("Date (YYYY-MM-DD): ")
            print('\n')
            category = category if category else None
            date = date if date else None
            curr_user.filter_expenses(category, date)
        else:
            print("No active user.")


    def total_expenses():
        if curr_user:
            category = input("Category: ")
            date = input("Date (YYYY-MM-DD): ")
            category = category if category else None
            date = date if date else None
            curr_user.total_expenses(category, date)
        else:
            print("No active user.")


    def save_expenses_history():
        if curr_user:
            curr_user.save_expenses_history()
        else:
            print("No active user.")

    def exit_program():
        print('Exiting program...')
        global running
        running = False

    menu = {
        '1' : add_user,
        '2' : switch_user,
        '3' : view_expenses,
        '4' : add_expenses,
        '5' : filter_expenses,
        '6' : total_expenses,
        '7' : save_expenses_history,
        '8' : exit_program
    }

    while running:
        print('---MENU---')
        print("\n1. Add user")
        print("2. Switch user")
        print("3. View expenses")
        print("4. Add expenses")
        print("5. Filter expenses")
        print("6. Total expenses")
        print("7. Save")
        print("8. Exit\n")
        choice = input("Enter your choice: ")
        print('\n')

        action = menu.get(choice)
        if action:
            action()
        else:
            print("\nInvalid choice, please try again!\n")
