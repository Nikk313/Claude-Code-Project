import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DATABASE_PATH = Path(__file__).parent / "spendly.db"


def get_db():
    """Return SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_user(name: str, email: str, password: str) -> int:
    """Create a new user. Returns user id. Raises IntegrityError if email exists."""
    db = get_db()
    password_hash = generate_password_hash(password)
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    db.commit()
    return cursor.lastrowid


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
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
        ("Demo User", "demo@spendly.com", "demo123"),
        ("Alice Sharma", "alice.sharma@example.com", "password123"),
        ("Bob Verma", "bob.verma@example.com", "bobpass"),
    ]

    for name, email, password in sample_users:
        cursor.execute(
            "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password),
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
