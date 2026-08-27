import sqlite3
from database import get_connection, init_db

init_db()

conn = get_connection()
cursor = conn.cursor()

# Customers
customers = [
    ("Rahul Kumar", "rahul@gmail.com", "9876543210", "Priya"),
    ("Priya Sharma", "priya@gmail.com", "9876543211", "Arun"),
    ("Arun Kumar", "arun@gmail.com", "9876543212", "Priya"),
    ("Meena Raj", "meena@gmail.com", "9876543213", "Karthik"),
    ("Sanjay Kumar", "sanjay@gmail.com", "9876543214", "Arun"),
    ("Divya Shah", "divya@gmail.com", "9876543215", "Karthik")
]

for customer in customers:
    cursor.execute("""
        INSERT INTO customers (name, email, phone, salesperson)
        VALUES (?, ?, ?, ?)
    """, customer)


# Deals
deals = [
    (1, "CRM Software", 25000, "Contacted", "2026-08-10"),
    (2, "AI Support System", 15000, "New", "2026-08-20"),
    (3, "Enterprise Plan", 50000, "Won", "2026-08-05"),
    (4, "Website Project", 12000, "Lost", "2026-07-15"),
    (5, "Cloud Migration", 30000, "Contacted", "2026-07-20"),
    (6, "AI Chatbot", 18000, "Contacted", "2026-08-01")
]

for deal in deals:
    cursor.execute("""
        INSERT INTO deals
        (customer_id, title, amount, status, last_updated)
        VALUES (?, ?, ?, ?, ?)
    """, deal)


# Notes
notes = [
    (1, "Demo completed. Customer is interested.", "2026-08-12"),
    (1, "Follow up next Monday.", "2026-08-15"),
    (2, "Initial enquiry received.", "2026-08-20"),
    (3, "Contract signed successfully.", "2026-08-05"),
    (5, "No response after multiple follow-ups.", "2026-07-25"),
    (6, "Customer requested product demo.", "2026-08-02")
]

for note in notes:
    cursor.execute("""
        INSERT INTO notes
        (customer_id, note, created_at)
        VALUES (?, ?, ?)
    """, note)


conn.commit()
conn.close()

print("Sample CRM data added successfully!")