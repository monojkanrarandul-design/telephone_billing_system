import sqlite3

# Connects to database (creates it if it doesn't exist)
conn = sqlite3.connect('telephone_billing_db.sqlite')
cursor = conn.cursor()

# Create Customer Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL
)
''')

# Create Billing Table with a foreign key to Customer
cursor.execute('''
CREATE TABLE IF NOT EXISTS Billing (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT NOT NULL,
    call_duration INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (phone) REFERENCES Customer(phone)
)
''')

# New Table for Authentication

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("Database schema successfully generated.")