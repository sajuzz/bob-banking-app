from flask import session
from werkzeug.security import check_password_hash
from database import get_db


def login_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"success": False, "error": "Invalid username or password"}

    if not check_password_hash(user["password"], password):
        return {"success": False, "error": "Invalid username or password"}

    return {"success": True, "user_id": user["id"], "username": user["username"]}


def logout_user():
    session.clear()
