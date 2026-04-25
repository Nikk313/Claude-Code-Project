import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "spendly.db"


def get_db():
    """Return SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development."""
    conn = get_db()
    cursor = conn.cursor()

    # Sample users (passwords are plaintext for dev - will hash in Step 3)
    sample_users = [
        ("demo_user", "demo123"),
        ("alice", "password123"),
        ("bob", "bobpass"),
    ]

    for username, password in sample_users:
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )

    # Sample expenses
    sample_expenses = [
        (1, 45.99, "Food", "Grocery shopping", "2025-01-15"),
        (1, 120.00, "Utilities", "Electric bill", "2025-01-10"),
        (1, 15.00, "Transport", "Uber ride", "2025-01-12"),
        (2, 89.50, "Food", "Restaurant dinner", "2025-01-14"),
        (2, 200.00, "Shopping", "New clothes", "2025-01-08"),
    ]

    for user_id, amount, category, description, date in sample_expenses:
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, description, date),
        )

    conn.commit()
    conn.close()
