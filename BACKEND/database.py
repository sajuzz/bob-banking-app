import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "banking.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            full_name   TEXT    NOT NULL,
            balance     REAL    NOT NULL DEFAULT 0.0
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id     INTEGER NOT NULL,
            type            TEXT    NOT NULL,   -- 'deposit' | 'withdrawal'
            amount          REAL    NOT NULL,
            timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
    """)

    # Seed demo accounts if not already present
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        from werkzeug.security import generate_password_hash
        demo_users = [
            ("alice", generate_password_hash("alice123"), "Alice Johnson", 5000.00),
            ("bob",   generate_password_hash("bob123"),   "Bob Smith",     3200.50),
            ("carol", generate_password_hash("carol123"), "Carol White",   8750.75),
        ]
        cursor.executemany(
            "INSERT INTO customers (username, password, full_name, balance) VALUES (?, ?, ?, ?)",
            demo_users,
        )

    conn.commit()
    conn.close()
