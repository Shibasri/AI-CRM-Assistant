from database import get_connection


def find_customer(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE name LIKE ?",
        (f"%{name}%",)
    )

    customer = cursor.fetchone()
    conn.close()

    return dict(customer) if customer else None


def get_customer_details(name):
    customer = find_customer(name)

    if not customer:
        return {
            "success": False,
            "message": f"Customer '{name}' was not found in the CRM."
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM deals WHERE customer_id = ?",
        (customer["id"],)
    )
    deals = [dict(row) for row in cursor.fetchall()]

    cursor.execute(
        "SELECT * FROM notes WHERE customer_id = ? ORDER BY created_at DESC",
        (customer["id"],)
    )
    notes = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "success": True,
        "customer": customer,
        "deals": deals,
        "notes": notes
    }


def get_deals_by_status(status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT deals.*, customers.name AS customer_name
        FROM deals
        JOIN customers ON deals.customer_id = customers.id
        WHERE deals.status = ?
    """, (status,))

    deals = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return deals


def get_deals_above_amount(amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT deals.*, customers.name AS customer_name
        FROM deals
        JOIN customers ON deals.customer_id = customers.id
        WHERE deals.amount > ?
    """, (amount,))

    deals = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return deals


def update_deal_status(deal_id, new_status):
    allowed_statuses = ["New", "Contacted", "Won", "Lost"]

    if new_status not in allowed_statuses:
        return {
            "success": False,
            "message": "Invalid status."
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM deals WHERE id = ?",
        (deal_id,)
    )

    deal = cursor.fetchone()

    if not deal:
        conn.close()
        return {
            "success": False,
            "message": f"Deal ID {deal_id} was not found."
        }

    cursor.execute("""
        UPDATE deals
        SET status = ?, last_updated = DATE('now')
        WHERE id = ?
    """, (new_status, deal_id))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Deal {deal_id} has been moved to {new_status}."
    }


def add_note(customer_name, note):
    customer = find_customer(customer_name)

    if not customer:
        return {
            "success": False,
            "message": f"Customer '{customer_name}' was not found in the CRM."
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (customer_id, note, created_at)
        VALUES (?, ?, DATE('now'))
    """, (customer["id"], note))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Note added successfully for {customer_name}."
    }


def assign_lead(customer_name, salesperson):
    customer = find_customer(customer_name)

    if not customer:
        return {
            "success": False,
            "message": f"Customer '{customer_name}' was not found in the CRM."
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE customers
        SET salesperson = ?
        WHERE id = ?
    """, (salesperson, customer["id"]))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"{customer_name}'s lead has been assigned to {salesperson}."
    }
def get_old_deals(days=14, amount=10000):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT deals.*, customers.name AS customer_name
        FROM deals
        JOIN customers ON deals.customer_id = customers.id
        WHERE deals.amount > ?
        AND deals.last_updated <= DATE('now', ?)
    """, (amount, f"-{days} days"))

    deals = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return deals
def get_customer_history(customer_name):
    customer = find_customer(customer_name)

    if not customer:
        return []

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT notes.*
        FROM notes
        WHERE notes.customer_id = ?
        ORDER BY notes.created_at ASC
    """, (customer["id"],))

    notes = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return notes
if __name__ == "__main__":
    print("Testing CRM tools...")

    print("\nCustomer:")
    print(find_customer("Rahul"))

    print("\nContacted deals:")
    print(get_deals_by_status("Contacted"))

    print("\nDeals above 10000:")
    print(get_deals_above_amount(10000))