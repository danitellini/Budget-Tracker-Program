# Budget Tracker

import json
import os
import time
from datetime import datetime, timedelta
import csv

DATA_FILE = "budget_data.json"

total_income = 0
total_expenses = 0
balance = total_income - total_expenses

income_list = {}
expense_list = {}

# CSV Functions

def export_data_to_csv():
    with open("budget_report.csv", 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Amount", "Description", "Timestamp", "Date"])
        for amount, details in data["income_list"].items():
            description = details["description"]
            timestamp = details["timestamp"]
            writer.writerow(["Income", amount, description, timestamp])
        for amount, details in data["expense_list"].items():
            description = details["description"]
            timestamp = details["timestamp"]
            writer.writerow(["Expense", amount, description, timestamp])
        for name, details in data["bill_calendar"].items():
            due_date = details["due_date"].strftime('%y-%m-%d')
            amount = details["amount"]
            writer.writerow(["Bill", amount, name, "", due_date])
        for account, details in data["savings_accounts"].items():
            remaining_balance = details["remaining_balance"]
            writer.writerow(["Savings", remaining_balance, account])
    print("Data exported to budget_report.csv")

# JSON Functions

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {
            "balance": 0,
            "total_income": 0,
            "total_expenses": 0,
            "income_list": {},
            "expense_list": {},
            "bill_calendar": {},
            "savings_accounts": {}
        }
    
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Delete Functions

def delete_income(amount, description):
    global total_income, balance
    if amount in data["income_list"] and data["income_list"][amount] == description:
        data["income_list"].pop(amount)
        total_income -= amount
        balance -= amount
        save_data(data)
        print(f"Income '{description} of ${amount:.2f} deleted.")
    else:
        print("Income entry not found.")
    return_to_menu_or_exit()

def delete_expense(amount, description):
    global total_expenses, balance
    if amount in data["expense_list"] and data["expense_list"][amount] == description:
        data["expense_list"].pop(amount)
        total_expenses -= amount
        balance -= amount
        save_data(data)
        print(f"Expense '{description}' of ${amount:.2f} deleted.")
    else:
        print("Expense entry not found.")
    return_to_menu_or_exit()

def delete_bill(name):
    if name in data["bill_calendar"]:
        data["bill_calendar"].pop(name)
        save_data(data)
        print(f"Bill '{name}' deleted.")
    else:
        print("Bill not found.")
    return_to_menu_or_exit()

def delete_savings_account(account_name):
    global total_income, balance
    if account_name in data["savings_accounts"]:
        saved_amount = data["savings_accounts"][account_name]["goal"] - data["savings_accounts"][account_name]["remaining_balance"]
        total_income += saved_amount
        balance += saved_amount
        data["income_list"][saved_amount] = f"Saved amount from {account_name} savings account."
        data["savings_accounts"].pop(account_name)
        save_data(data)
        print(f"Savings account '{account_name}' deleted.")
        time.sleep(0.5)
        print(f"Saved amount of ${saved_amount:.2f} added to income.")
    else:
        print("Savins account not found.")
    return_to_menu_or_exit()

# Display Functions

def display_income():
    print("\nIncome List:")
    if not data["income_list"]:
        print("No income records.")
    else:
        for i, (amount, description, date) in enumerate(data["income_list"].items(), start=1):
            print(f"{i}. Amount: ${amount:.2f}, Description: {description}, Date: {date}")
    time.sleep(1)
    choice = input("\nWould you like to delete an income entry? (yes/no): ").strip().lower()
    if choice == "yes":
        index = int(input("Enter the number of the income entry you want to delete: ")) - 1
        if 0 <= index < len(data["income_list"]):
            amount, description = list(data["income_list"].items())[index]
            delete_income(amount, description)
        else:
            print("Invalid entry number.")
    return_to_menu_or_exit()

def display_expenses():
    print("\nExpense List:")
    if not data["expense_list"]:
        print("No expense records.")
    else:
        for i, (amount, description) in enumerate(data["expense_list"].items(), start=1):
            print(f"{i}. Amount: ${amount:.2f}, Description: {description}")
    choice = input("\nWould you like to delete an expense entry? (yes/no):").strip().lower()
    if choice == "no":
        index = int(input("Enter the number of the expense entry you want to delete: ")) - 1
        if 0 <= index < len(data["expense_list"]):
            amount, description = list(data["expense_list"].items())[index]
            delete_expense(amount, description)
        else:
            print("Invalid entry number.")
    return_to_menu_or_exit()

# Functions

def return_to_menu_or_exit():
    while True:
        choice = input("Would you like to return to the main menu, or exit? (Enter 'menu' or 'exit'): ")
        if choice.lower() == "menu":
            main_menu()
            break
        elif choice.lower() == "exit":
            print("Exiting the program...")
            exit()
    else:
        print("Invalid choice. Please try again: ")

def add_income(amount = 0, description = "item"):
    global income_list, total_income, balance
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["income_list"][amount] = {"description": description, "timestamp": timestamp}
    total_income += amount
    balance += amount
    save_data(data)
    time.sleep(1)
    print("\nIncome Summary:")
    time.sleep(0.5)
    print(display_income())
    time.sleep(0.5)
    print(f"{description} successfully added to your income. Your new balance is {balance:.2f}.")
    time.sleep(1)
    return_to_menu_or_exit()

def add_expense(amount = 0, description = "item"):
    global expense_list, total_expenses, balance
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data["expense_list"][amount] = {"description": description, "timestamp": timestamp}
    total_expenses += amount
    balance -= amount
    save_data(data)
    time.sleep(1)
    print("\nExpense Summary:")
    time.sleep(0.5)
    print(display_expenses())
    time.sleep(0.5)
    print(f"{description} successfully added to your expenses. Your new balance is {balance:.2f}.")
    return_to_menu_or_exit()

def view_balance():
    global balance
    print(f"Your balance is {balance:.2f}.")
    return_to_menu_or_exit()

def view_summary():
    print("\nComplete Budget Summary:")
    print(view_balance())
    print(display_income())
    print(display_expenses())
    print(view_bills())
    print(view_savings_accounts())
    return_to_menu_or_exit()

# Bill Calendar

bill_calendar = {}

def add_bill(name, date_str, amount):
    due_date = datetime.strptime(date_str, '%Y-%m-%d')
    bill_calendar[name] = (due_date, amount)
    save_data(data)
    time.sleep(1)
    print(f"Your bill '{name}' has been successfully added to your bill calendar!")
    return_to_menu_or_exit()

def view_bills():
    sorted_bills = sorted(data["bill_calendar"].items(), key=lambda x: x[1]["due_date"])
    print("Bill Calendar:")
    if not sorted_bills:
        print("No bills available.")
    else:
        for name, details in sorted_bills:
            due_date = details["due_date"]
            amount = details["amount"]
            print(f"Bill: {name}, Due: {due_date.strftime('%Y-%m-%d')}, Amount: ${amount:.2f}")
    choice = input("\n Would you like to delete a bill? (yes/no): ").strip().lower()
    if choice == "yes":
        name = input("Enter the name of the bill you want to delete: ")
        delete_bill(name)
    return_to_menu_or_exit()

def view_upcoming_bills():
    today = datetime.now()
    upcoming_date = today + timedelta(days=15)
    sorted_bills = sorted(
        ((name,details) for name, details in data["bill_calendar"].items() if today <= details["due_date"] <= upcoming_date),
        key=lambda x: x[1]["due_date"]
        )
    print("Upcoming Bills (Next 15 Days):")
    if not sorted_bills:
        print("No bills due in the next 15 days.")
    else:
        for name, details in sorted_bills:
            due_date = details["due_date"]
            amount = details["amount"]
            print(f"Bill: {name}, Due: {due_date.strftime('%Y-%m=%d')}, Amount: {amount:.2f}")
    return_to_menu_or_exit()

# Savings Account

savings_accounts = {}

def add_savings_account(account_name, goal_amount, contribution_per_period):
    remaining_balance = goal_amount
    time_needed = remaining_balance / contribution_per_period
    savings_accounts[account_name] = {
        'goal': goal_amount,
        'remaining_balance': remaining_balance,
        'contribution': contribution_per_period,
        'time_needed': time_needed
    }
    save_data(data)
    time.sleep(1)
    print(f"Savings account '{account_name}' created!")
    time.sleep(0.5)
    print(f"It will take {time_needed} months to save {goal_amount} with contributions of {contribution_per_period} per month.")
    return_to_menu_or_exit()
    #give deletion function that moves remaining balance to income

def view_savings_accounts():
    print("\nSavings Accounts:")
    if not data["savings_accounts"]:
        print("No savings accounts available.")
    else:
        for account_name, details in data["savings_accounts"].items():
            print(f"Account Name: {account_name}")
            print(f" - Goal Amount: {details['goal']:.2f}")
            print(f" - Remaining Balance: {details['remaining_balance']:.2f}")
            print(f" - Contribution per Month: {details['contribution']:.2f}")
            print(f" - Time Needed to Reach Goal: {details['time_needed']} months")
            print()
    choice = input("\nWould you like to delete a savings account? (yes/no): ").strip().lower()
    if choice == "yes":
        account_name = input("Enter the name of the savings account you want to delete: ")
        delete_savings_account(account_name)
    return_to_menu_or_exit()

def transfer_to_savings(account_name, transfer_amount):
    if account_name in savings_accounts:
        global total_income, total_expenses
        if transfer_amount > total_income:
            print(f"Error: Insufficient Funds")
        total_income -= transfer_amount
        print(f"${transfer_amount} transferred from income.")
        total_expenses += transfer_amount
        expense_list[account_name] = transfer_amount
        print(f"${transfer_amount} added to expenses.")
        savings_accounts[account_name]['remaining_balance'] -= transfer_amount
        if savings_accounts[account_name]['remaining_balance'] <= 0:
            savings_accounts[account_name]['remaining_balance'] = 0
            print(f"Congratulations! You've reached your savings goal for '{account_name}!")
        remaining_balance = savings_accounts[account_name]['remaining_balance']
        contribution_per_period = savings_accounts[account_name]['contribution']
        savings_accounts[account_name]['time_needed'] = remaining_balance / contribution_per_period if remaining_balance > 0 else 0
        save_data(data)
        print(f"${transfer_amount} successfully transferred to the savings account '{account_name}'.")
        print(f"New remaining balance: {remaining_balance}")
        print(f"New time to reach goal: {savings_accounts[account_name]['time_needed']} per month.")
    else:
        print(f"Savings account '{account_name}' not found.")
    return_to_menu_or_exit()

def transfer_from_savings(account_name, transfer_amount):
    if account_name in savings_accounts:
        global total_income, total_expenses
        if transfer_amount > (account_name['goal'] - account_name['remaining_balance']):
            print(f"Error: Insufficient Funds")
        balance += transfer_amount
        print(f"{transfer_amount} transferred from income.")
        income_list[account_name] = transfer_amount
        print(f"{transfer_amount} added to income.")
        savings_accounts[account_name]['remaining_balance'] += transfer_amount
        remaining_balance = savings_accounts[account_name]['remaining_balance']
        contribution_per_period = savings_accounts[account_name]['contribution']
        savings_accounts[account_name]['time_needed'] = remaining_balance / contribution_per_period
        save_data(data)
        print(f"${transfer_amount} successfully transferred to your available balance.")
        print(f"New remaining balance: {remaining_balance}")
        print(f"New time to reach goal: {savings_accounts[account_name]['time_needed']} per month.")
    else:
        print(f"Savings account '{account_name}' not found.")
    return_to_menu_or_exit()

# Menu

def main_menu():
    global data
    data = load_data()
    while True:
        print("\nMain Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance and Summary")
        print("4. Add Bill to Calendar")
        print("5. View Bills/Upcoming Bills")
        print("6. Create Savings Account")
        print("7. View Savings Account Details")
        print("8. Add to Savings")
        print("9. Transfer from Savings")
        print("10. Exit")

        choice = input("What would you like to do?: ")

        if choice == "1":
            amount = float(input("Amount (in USD): $"))
            description = input("Provide a brief, 1-3 word description: ")
            add_income(amount, description)
        elif choice == "2":
            amount = float(input("Amount (in USD): $"))
            description = input("Provide a brief, 1-3 word description: ")
            add_expense(amount, description)
        elif choice == "3":
            print("1. View Balance")
            print("2. View Summary")
            choice2 = input("Choose 1 or 2: ")
            if choice2 == "1":
                view_balance()
            elif choice2 == "2":
                view_summary()
        elif choice == "4":
            name = input("What is the name for this bill? ")
            date_str = input("What is the due date? Enter YYYY, DD, MM: ")
            amount = input("What is the amount (in USD)? $")
            add_bill(name, date_str, amount)
        elif choice == "5":
            print("1. View Bills")
            print("2. View Upcoming Bills")
            choice3 = input("Choose 1 or 2: ")
            if choice3 == "1":
                view_bills()
            elif choice3 == "2":
                view_upcoming_bills()
        elif choice == "6":
            account_name = input("What would you like to name this account? ")
            goal_amount = input("What is the amount (in USD) you'd like to save? $")
            contribution_per_period = input("How much would you like to save (in USD) towards this goal, per month? $")
            add_savings_account(account_name, goal_amount, contribution_per_period)
        elif choice == "7":
            view_savings_accounts()
        elif choice == "8":
            account_name = input("What account would you like to transfer money to? ")
            transfer_amount = input("What amount (in USD) would you like to transfer? $")
            transfer_to_savings(account_name, transfer_amount)
        elif choice == "9":
            account_name = input("What account would you like to transfer money out of? ")
            transfer_amount = input("What amount (in USD) would you like to transfer to your available balance? $")
            transfer_from_savings(account_name, transfer_amount)
        elif choice == "10":
            print("Exiting from program...")
            exit()
    else:
        print("Invalid choice. Please try again: ")

# Run Budget Tracker
main_menu()

# NOTES
#
# 
# 
#
#