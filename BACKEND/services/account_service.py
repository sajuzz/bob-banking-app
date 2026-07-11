from database import get_db


def get_balance(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, balance FROM customers WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return {"full_name": row["full_name"], "balance": round(row["balance"], 2)}


def deposit(user_id, amount):
    if amount is None:
        return {"success": False, "error": "Amount is required"}
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return {"success": False, "error": "Invalid amount"}

    if amount <= 0:
        return {"success": False, "error": "Deposit amount must be greater than zero"}

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET balance = balance + ? WHERE id = ?", (amount, user_id))
    cursor.execute(
        "INSERT INTO transactions (customer_id, type, amount) VALUES (?, 'deposit', ?)",
        (user_id, amount),
    )
    conn.commit()
    cursor.execute("SELECT balance FROM customers WHERE id = ?", (user_id,))
    new_balance = cursor.fetchone()["balance"]
    conn.close()
    return {"success": True, "message": f"Deposited ${amount:.2f}", "balance": round(new_balance, 2)}


def withdraw(user_id, amount):
    if amount is None:
        return {"success": False, "error": "Amount is required"}
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return {"success": False, "error": "Invalid amount"}

    if amount <= 0:
        return {"success": False, "error": "Withdrawal amount must be greater than zero"}

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM customers WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    if row["balance"] < amount:
        conn.close()
        return {"success": False, "error": "Insufficient funds"}

    cursor.execute("UPDATE customers SET balance = balance - ? WHERE id = ?", (amount, user_id))
    cursor.execute(
        "INSERT INTO transactions (customer_id, type, amount) VALUES (?, 'withdrawal', ?)",
        (user_id, amount),
    )
    conn.commit()
    cursor.execute("SELECT balance FROM customers WHERE id = ?", (user_id,))
    new_balance = cursor.fetchone()["balance"]
    conn.close()
    return {"success": True, "message": f"Withdrew ${amount:.2f}", "balance": round(new_balance, 2)}
