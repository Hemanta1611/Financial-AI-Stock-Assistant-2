import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

df = pd.read_csv('finance_data.csv')

# print(df)

class CSV:
    CSV_FILE = 'finance_data.csv'
    COLUMNS = ['date', 'amount', 'category', 'description']
    FORMAT = "%d-%m-%Y"
    
    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_data(cls, data, amount, category, description):
        new_data = {
            "date": data,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
            writer.writerow(new_data)
        print("Data added successfully")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found for the given date range.")
            return None
        
        print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}:")
        print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))

        total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
        total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()

        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Balance: ${total_income - total_expense:.2f}")
        
        return filtered_df

def plot_transactions(df):
    df.set_index('date', inplace=True)
    income_df = df[df['category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0)
    expense_df = df[df['category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.plot(income_df.index, income_df['amount'], label='Income', color='green')
    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='red')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Daily Transaction Amounts')
    plt.legend()
    plt.show()

    
def add_data():
    CSV.initialize_csv()
    data = get_date("Enter the date (dd-mm-yyyy): ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_data(data, amount, category, description)
    
def main():
    while True:
        print("\n1. Add a new Transaction")
        print("2. View Transaction and summary within a the date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add_data()
        elif choice == "2":
            start_date = input("Enter the start date (dd-mm-yyyy): ")
            end_date = input("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if df is not None and input("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()

# add_data()

# CSV.get_transactions("16-11-2024", "16-11-2025")
# CSV.initialize_csv()
# CSV.add_data("2025-05-13", 100, "Food", "Dinner at the restaurant")



