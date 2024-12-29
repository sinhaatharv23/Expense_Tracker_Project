import customtkinter as ctk
import tkinter as tk  # Import tkinter for Treeview
from tkinter import ttk  # Import ttk for themed widgets
import csv
import os
from tkinter import messagebox
# Function to add an expense entry
def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()

    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    # Write data to CSV file
    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

    messagebox.showinfo("Success", "Expense added successfully")
    refresh_expenses()


# Function to view all expenses
def refresh_expenses():
    for row in tree.get_children():
        tree.delete(row)

    if not os.path.exists('expenses.csv'):
        messagebox.showwarning("No Data", "No expenses recorded yet.")
        return

    with open('expenses.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            tree.insert("", "end", values=row)


# Function to clear input fields
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)


# Function to toggle between Dark and Light mode
def toggle_mode():
    current_mode = ctk.get_appearance_mode()  # Get current appearance mode
    new_mode = "light" if current_mode == "dark" else "dark"
    ctk.set_appearance_mode(new_mode)  # Set the new appearance mode


# Function to delete an expense
def delete_expense():
    selected_item = tree.selection()  # Get selected row
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete")
        return

    # Confirm the deletion
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?")
    if not confirm:
        return

    # Get the values of the selected row
    selected_expense = tree.item(selected_item, 'values')
    date, category, amount = selected_expense

    # Read all expenses and filter out the selected one
    expenses = []
    with open('expenses.csv', mode='r') as file:
        reader = csv.reader(file)
        expenses = [row for row in reader if row != list(selected_expense)]

    # Rewrite the CSV file without the deleted expense
    with open('expenses.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(expenses)

    # Remove the selected row from the treeview
    tree.delete(selected_item)

    messagebox.showinfo("Success", "Expense deleted successfully")
    refresh_expenses()


# Setting up the main GUI window
ctk.set_appearance_mode("dark")  # Start with dark mode
ctk.set_default_color_theme("green")  # Set default color theme

root = ctk.CTk()
root.title("Enhanced Expense Tracker")

# Configure the grid layout for responsiveness
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Labels and Entry fields
label_date = ctk.CTkLabel(root, text="Date (YYYY-MM-DD):")
label_date.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
entry_date = ctk.CTkEntry(root)
entry_date.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

label_category = ctk.CTkLabel(root, text="Category:")
label_category.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
entry_category = ctk.CTkEntry(root)
entry_category.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

label_amount = ctk.CTkLabel(root, text="Amount:")
label_amount.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
entry_amount = ctk.CTkEntry(root)
entry_amount.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Buttons
button_add = ctk.CTkButton(root, text="Add Expense", command=add_expense)
button_add.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

button_clear = ctk.CTkButton(root, text="Clear", command=clear_entries)
button_clear.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

# Toggle mode button
button_toggle_mode = ctk.CTkButton(root, text="Toggle Dark/Light Mode", command=toggle_mode)
button_toggle_mode.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Delete button
button_delete = ctk.CTkButton(root, text="Delete Selected Expense", command=delete_expense)
button_delete.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Table to view expenses using ttk's Treeview
columns = ("Date", "Category", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

# Configure the columns
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Expand the treeview and table
root.rowconfigure(5, weight=5)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Start the GUI with existing data
refresh_expenses()

root.mainloop()
