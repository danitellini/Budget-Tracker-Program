# Budget Tracker

from datetime import datetime

total_income = 0
total_expenses = 0

income_list = {}
expense_list = {}

def add_income(amount, description):
    income_list[amount] = description
    total_income += float(amount)

def add_expense(amount, description):
    expense_list[amount] = description
    total_expenses += float(amount)

def view_balance():
    return total_income - total_expenses 

def view_summary():
    print(income_list)
    print(expense_list)
    return view_balance()

# Bill Calendar

bill_calendar = {}

def add_bill(name, date_str, amount):
    due_date = datetime.strptime(date_str, '%Y-%m-%d')
    bill_calendar[name] = (due_date, amount)

def view_bills():
    for bill, details in bill_calendar.items():
        print(f"Bill: {bill}, Due: {details[0]}, Amount: {details[1]}")

def view_upcoming_bills():
    sorted_bills = sorted(bill_calendar.items(), key=lambda x: x[1][0])
    print("Upcoming Bills:")
    for name, (due_date, amount) in sorted_bills:
            print(f"Bill: {name}, Due: {due_date.strftime('%Y-%m=%d')}, Amount: {amount}")

# Extra Income

extra_income = {}

def add_extra_income(amount, description):
    extra_income[amount] = description
    total_income += float(amount)
    return "Your new monthly total income is ", total_income

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
    print(f"Savings account '{account_name}' created!")
    print(f"It will take {time_needed} months to save {goal_amount} with contributions of {contribution_per_period} per month.")
    #give deletion function that moves remaining balance to income

def view_savings_accounts():
    if not savings_accounts:
        print("No savings accounts available.")
        return
    for account_name, details in savings_accounts.items():
        print(f"Account Name: {account_name}")
        print(f" - Goal Amount: {details['goal']}")
        print(f" - Remaining Balance: {details['remaining_balance']}")
        print(f" - Contribution per Month: {details['contribution']}")
        print(f" - Time Needed to Reach Goal: {details['time_needed']} months")
        print()

def add_funds_savings(account_name, additional_contribution):
    if account_name in savings_accounts:
        account = savings_accounts[account_name]
        account['remaining_balance'] -= additional_contribution
        if account['remaining_balance'] <= 0:
            account['remaining_balance'] = 0
            print(f"Congratulations@ You've reached your savings goal for {account_name}!")
        else:
            account['time_needed'] = account['remaining_balance'] / account['contribution']
            print(f"New remaining balance for {account_name}: {account['remaining_balance']}")
            print(f"New time to reach goal: {account['time_needed']} per month.")
    else:
        print(f"Account '{account_name}' not found.")

def auto_transfer_to_savings(account_name, transfer_amount):
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
        print(f"${transfer_amount} successfully transferred to the savings account '{account_name}'.")
        print(f"New remaining balance: {remaining_balance}")
    else:
        print(f"Savings account '{account_name}' not found.")

# Menu

# 1. Add income
# 2. Add expense
# 3. View balance and summary
# 4. Add bill to calendar - date format must be YYYY, DD, MM
# 5. View bills/upcoming bills
# 6. Add extra income
# 7. Create savings account - contribution_per_period needs to be prompted as per month
# 8. View savings account details
# 9. Add to savings