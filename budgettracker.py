# Budget Tracker

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

def bill_calendar(name, date, amount):
    bill_calendar[name] = date, amount
    #import a library for date/time

# Extra Income

extra_income = {}

def add_extra_income(amount, description):
    extra_income[amount] = description
    total_income += float(amount)
    return "Your new monthly total income is ", total_income

# Savings Account

savings_accounts = {}

def get_savings_timeframe(account_name, goal_amount, contribution_per_period):
    time_needed = goal_amount / contribution_per_period
    #add a transfer - subtract contribution from income
    #add account name to savings_accounts
    #give deletion function that moves remaining balance to income
    return time_needed

# Menu

# 1. Add income
# 2. Add expense
# 3. View balance and summary
# 4. Add bill to calendar
# 5. View bills
# 6. Add extra income
# 7. Create savings account - go to two options: get timeframe or manually create/add to savings account
# 8. View savings account details
# 9. Exit