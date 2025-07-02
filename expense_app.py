import tkinter as tk
from tkinter import messagebox
from expense_tracker import Expense

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker GUI")

        # User management
        self.users = {}
        self.curr_user = None

        # Build UI
        self.build_login_frame()
        self.build_expense_frame()
        self.build_buttons()
        self.build_output_area()

    def build_login_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Username:").grid(row=0, column=0, padx=5)
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Add/Switch User", command=self.login_user).grid(row=0, column=2, padx=5)

    def build_expense_frame(self):
        form = tk.LabelFrame(self.root, text="Expense Details")
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Amount:").grid(row=0, column=0, sticky="w")
        self.amount_entry = tk.Entry(form)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(form, text="Category:").grid(row=1, column=0, sticky="w")
        self.category_entry = tk.Entry(form)
        self.category_entry.grid(row=1, column=1)

        tk.Label(form, text="Description:").grid(row=2, column=0, sticky="w")
        self.desc_entry = tk.Entry(form)
        self.desc_entry.grid(row=2, column=1)

        tk.Label(form, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.date_entry = tk.Entry(form)
        self.date_entry.grid(row=3, column=1)

    def build_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="View Expenses", command=self.view_expenses).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Filter", command=self.filter_expenses).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Total", command=self.show_total).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Save", command=self.save_history).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.root.quit).grid(row=0, column=5, padx=5)

    def build_output_area(self):
        self.output = tk.Text(self.root, height=15, width=70)
        self.output.pack(padx=10, pady=5)

    def login_user(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return
        if username not in self.users:
            self.users[username] = Expense(username)
            # load history if exists
            self.users[username].load_expenses_history()
        self.curr_user = self.users[username]
        messagebox.showinfo("Success", f"Current user: {username}")
        self.output.delete(1.0, tk.END)

    def view_expenses(self):
        if not self.curr_user:
            messagebox.showerror("Error", "No active user.")
            return
        self.output.delete(1.0, tk.END)
        exps = self.curr_user.view_expenses()  # prints in CLI, but returns list? override to return
        # The CLI view_expenses prints. Instead directly use attribute:
        for i, exp in enumerate(self.curr_user.expense, 1):
            self.output.insert(tk.END,
                f"{i}. ₹{exp['amount']} | {exp['category']} | {exp['description']} | {exp['date']}\n")

    def add_expense(self):
        if not self.curr_user:
            messagebox.showerror("Error", "No active user.")
            return
        try:
            amt = int(self.amount_entry.get())
            cat = self.category_entry.get().strip()
            desc = self.desc_entry.get().strip()
            date = self.date_entry.get().strip()
            self.curr_user.add_expenses(amt, cat, desc, date)
            messagebox.showinfo("Added", "Expense added successfully.")
            # clear inputs
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Amount must be an integer.")

    def filter_expenses(self):
        if not self.curr_user:
            messagebox.showerror("Error", "No active user.")
            return
        cat = self.category_entry.get().strip() or None
        date = self.date_entry.get().strip() or None
        filtered = self.curr_user.filter_expenses(cat, date)
        self.output.delete(1.0, tk.END)
        for i, exp in enumerate(filtered, 1):
            self.output.insert(tk.END,
                f"{i}. ₹{exp['amount']} | {exp['category']} | {exp['description']} | {exp['date']}\n")

    def show_total(self):
        if not self.curr_user:
            messagebox.showerror("Error", "No active user.")
            return
        cat = self.category_entry.get().strip() or None
        date = self.date_entry.get().strip() or None
        total = self.curr_user.total_expenses(cat, date)
        self.output.delete(1.0, tk.END)
        label = f"Total Expense"
        if cat:
            label += f" in {cat}"
        if date:
            label += f" on {date}"
        self.output.insert(tk.END, f"{label}: ₹{total}\n")

    def save_history(self):
        if not self.curr_user:
            messagebox.showerror("Error", "No active user.")
            return
        self.curr_user.save_expenses_history()
        messagebox.showinfo("Saved", "Expenses saved.")

if __name__ == '__main__':
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()
