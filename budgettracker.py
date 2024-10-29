# Budget Tracker

import json
import os
import time
from datetime import datetime

DATA_FILE = "budget_data.json"

total_income = 0
total_expenses = 0
balance = total_income - total_expenses

income_list = {}
expense_list = {}

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

# Display Functions

def display_income():
    print("\nIncome List:")
    if not data["income_list"]:
        print("No income records.")
    else:
        for i, entry in enumerate(data["income_list"], start=1):
            print(f"{i}. Amount: ${entry['amount']:.2f}, Description: {entry['description']}")

def display_expenses():
    print("\nExpense List:")
    if not data["expense_list"]:
        print("No expense records.")
    else:
        for i, entry in enumerate(data["expense_list"], start=1):
            print(f"{i}. Amount: ${entry['amount']:.2f}, Description: {entry['description']}")

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
    income_list[amount] = description
    total_income += amount
    balance += amount
    save_data(data)
    time.sleep(1)
    print("\nIncome Summary:")
    time.sleep(0.5)
    print(income_list)
    time.sleep(0.5)
    print(f"{description} successfully added to your income. Your new balance is {balance:.2f}.")
    time.sleep(1)
    return_to_menu_or_exit()

def add_expense(amount = 0, description = "item"):
    global expense_list, total_expenses, balance
    expense_list[amount] = description
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
    print("\nComplete Budget Data:")
    print(json.dumps(data,indent=4))
    return_to_menu_or_exit()

# Bill Calendar

bill_calendar = {}

def add_bill(name, date_str, amount):
    due_date = datetime.strptime(date_str, '%Y-%m-%d')
    bill_calendar[name] = (due_date, amount)
    save_data(data)
    return_to_menu_or_exit()

def view_bills():
    for bill, details in bill_calendar.items():
        print(f"Bill: {bill}, Due: {details[0]}, Amount: {details[1]}")
        return_to_menu_or_exit()

def view_upcoming_bills():
    sorted_bills = sorted(bill_calendar.items(), key=lambda x: x[1][0])
    print("Upcoming Bills:")
    for name, (due_date, amount) in sorted_bills:
            print(f"Bill: {name}, Due: {due_date.strftime('%Y-%m=%d')}, Amount: {amount}")
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
    print(f"Savings account '{account_name}' created!")
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
            print(f" - Goal Amount: {details['goal']}:.2f")
            print(f" - Remaining Balance: {details['remaining_balance']}:.2f")
            print(f" - Contribution per Month: {details['contribution']}:.2f")
            print(f" - Time Needed to Reach Goal: {details['time_needed']} months")
            print()
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
            add_bill()
        elif choice == "5":
            print("1. View Bills")
            print("2. View Upcoming Bills")
            choice3 = input("Choose 1 or 2: ")
            if choice3 == "1":
                view_bills()
            elif choice3 == "2":
                view_upcoming_bills()
        elif choice == "6":
            add_savings_account()
        elif choice == "7":
            view_savings_accounts()
        elif choice == "8":
            transfer_to_savings()
        elif choice == "9":
            transfer_from_savings()
        elif choice == "10":
            print("Exiting from program...")
            exit()
    else:
        print("Invalid choice. Please try again: ")
# 4. Add bill to calendar - date format must be YYYY, DD, MM
# Run Budget Tracker
main_menu()