# Budget Tracker
import sqlite3
import time
import datetime

# Connect to SQLite database
conn = sqlite3.connect('BudgetTracker.db')
c = conn.cursor()

# Create table if not exists
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS stufftoplot(
            datestamp TEXT,
            Expenses REAL,
            Income REAL,
            RecurringCost REAL
        )
    ''')

# Insert data
def data_entry():
    datestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Income = int(input('Enter your income: '))
    Expenses = int(input('Enter your expenses: '))
    
    # Calculate recurring cost percentage
    if Income > 0:
        RecurringCost = ((Income - Expenses) / Income) * 100
    else:
        RecurringCost = 0
    
    print(f'The recurring cost in percentage is {RecurringCost:.2f}%')

    # Insert into database
    c.execute('INSERT INTO stufftoplot(datestamp, Expenses, Income, RecurringCost) VALUES (?, ?, ?, ?)',
              (datestamp, Expenses, Income, RecurringCost))
    conn.commit()

# Show data
def read_data():
    date_input = input('Enter date (YYYY-MM-DD HH:MM:SS) or press Enter to show all: ')
    if date_input.strip():
        query = "SELECT * FROM stufftoplot WHERE datestamp > ?"
        c.execute(query, (date_input,))
    else:
        c.execute("SELECT * FROM stufftoplot")
    
    data = c.fetchall()
    for row in data:
        print(row)

# Delete all data
def del_data():
    confirm = input("Are you sure you want to delete all data? (yes/no): ")
    if confirm.lower() == "yes":
        c.execute("DELETE FROM stufftoplot")
        conn.commit()
        print("All data deleted.")
    else:
        print("Operation cancelled.")

# Run the tracker
create_table()

choice = input('''
Choose:
1 - Enter data
2 - Show data
3 - Delete all data
Any other key - Exit
Your choice: ''')

if choice == '1':
    data_entry()
elif choice == '2':
    read_data()
elif choice == '3':
    del_data()
else:
    print("Exiting...")

# Close DB connection
c.close()
conn.close()
