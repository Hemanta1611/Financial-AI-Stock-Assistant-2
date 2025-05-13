from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORY = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.now().strftime(date_format)
    try:
        return datetime.strptime(date_str, date_format).strftime(date_format)
    except ValueError:
        print("Invalid date format. Please use dd-mm-yyyy.")
        return get_date(prompt, allow_default)
        

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            print("Amount must be a positive number.")
            return get_amount()
        return amount
    except ValueError:
        print("Invalid amount format. Please enter a number.")
        return get_amount()

def get_category():
    category = input("Enter the category: ('I' for income, 'E' for expense)").upper()
    if category not in ['I', 'E']:
        print("Invalid category. Please enter 'I' for income or 'E' for expense.")
        return get_category()
    return CATEGORY[category]

def get_description():
    description = input("Enter the description: ")
    if not description:
        print("Description can't be empty.")
        return get_description()
    return description



        





