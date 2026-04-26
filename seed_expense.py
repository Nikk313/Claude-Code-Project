#!/usr/bin/env python3
"""Seed realistic dummy expenses for a specific user."""

import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from database.db import get_db

# Category definitions with Indian context
CATEGORIES = {
    "Food": {"min": 50, "max": 800, "weight": 25, "descriptions": [
        "Grocery shopping", "Restaurant dinner", "Swiggy order", "Zomato delivery",
        "Tea and snacks", "Vegetables from market", "Biryani takeaway", "Street food"
    ]},
    "Transport": {"min": 20, "max": 500, "weight": 15, "descriptions": [
        "Uber ride", "Ola cab", "Auto rickshaw", "Metro card recharge",
        "Bus pass", "Fuel refill", "Parking fees", "Taxi fare"
    ]},
    "Bills": {"min": 200, "max": 3000, "weight": 12, "descriptions": [
        "Electricity bill", "Mobile recharge", "Internet bill", "DTH recharge",
        "Water bill", "Maintenance charges", "Gas cylinder", "Insurance premium"
    ]},
    "Health": {"min": 100, "max": 2000, "weight": 8, "descriptions": [
        "Pharmacy purchase", "Doctor consultation", "Medical test", "Gym membership",
        "Health supplements", "Physiotherapy session", "Dental checkup"
    ]},
    "Entertainment": {"min": 100, "max": 1500, "weight": 10, "descriptions": [
        "Movie tickets", "Netflix subscription", "Concert entry", "Gaming subscription",
        "Book purchase", "Amazon Prime", "Spotify premium", "Weekend outing"
    ]},
    "Shopping": {"min": 200, "max": 5000, "weight": 15, "descriptions": [
        "New clothes", "Festival shopping", "Electronics purchase", "Home decor",
        "Kitchen appliances", "Shoes and footwear", "Watch accessory", "Bag purchase"
    ]},
    "Other": {"min": 50, "max": 1000, "weight": 10, "descriptions": [
        "Miscellaneous expense", "Donation", "Gift purchase", "Stationery",
        "Pet supplies", "Car wash", "Laundry service", "Haircut"
    ]},
}

def parse_args(args):
    """Parse command line arguments."""
    if len(args) != 3:
        return None

    try:
        user_id = int(args[0])
        count = int(args[1])
        months = int(args[2])
        return {"user_id": user_id, "count": count, "months": months}
    except ValueError:
        return None

def verify_user(user_id):
    """Check if user exists in database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def select_category():
    """Select category based on weights for proportional distribution."""
    categories = list(CATEGORIES.keys())
    weights = [CATEGORIES[cat]["weight"] for cat in categories]
    return random.choices(categories, weights=weights)[0]

def generate_expense(user_id, start_date, end_date):
    """Generate a single random expense."""
    category = select_category()
    cat_data = CATEGORIES[category]

    amount = round(random.uniform(cat_data["min"], cat_data["max"]), 2)
    description = random.choice(cat_data["descriptions"])

    # Random date within range
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    date = start_date + timedelta(days=random_days)

    return {
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date.strftime("%Y-%m-%d"),
    }

def seed_expenses(user_id, count, months):
    """Generate and insert expenses for a user."""
    # Verify user exists
    user = verify_user(user_id)
    if not user:
        print(f"No user found with id {user_id}.")
        return None

    print(f"Seeding {count} expenses for user '{user['username']}' (id={user_id})...")

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)

    # Generate expenses
    expenses = [generate_expense(user_id, start_date, end_date) for _ in range(count)]

    # Insert in single transaction
    conn = get_db()
    cursor = conn.cursor()

    try:
        for exp in expenses:
            cursor.execute(
                """INSERT INTO expenses
                   (user_id, amount, category, description, date)
                   VALUES (?, ?, ?, ?, ?)""",
                (exp["user_id"], exp["amount"], exp["category"],
                 exp["description"], exp["date"])
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error inserting expenses: {e}")
        conn.close()
        return None

    # Fetch inserted expenses for confirmation
    cursor.execute(
        """SELECT id, amount, category, description, date
           FROM expenses
           WHERE user_id = ?
           ORDER BY date DESC
           LIMIT 5""",
        (user_id,)
    )
    sample = cursor.fetchall()

    # Get date range of inserted expenses
    cursor.execute(
        """SELECT MIN(date) as min_date, MAX(date) as max_date
           FROM expenses
           WHERE user_id = ?""",
        (user_id,)
    )
    date_range = cursor.fetchone()

    conn.close()

    # Print confirmation
    print(f"\nSuccessfully inserted {count} expenses!")
    print(f"Date range: {date_range['min_date']} to {date_range['max_date']}")
    print(f"\nSample records (most recent 5):")
    print("-" * 70)
    for row in sample:
        print(f"  ID: {row['id']:<5} | Rs {row['amount']:<7.2f} | {row['category']:<12} | {row['date']} | {row['description']}")

    return {"count": count, "sample": sample, "date_range": date_range}

if __name__ == "__main__":
    # Parse arguments from command line
    if len(sys.argv) != 4:
        print("Usage: python seed_expense.py <user_id> <count> <months>")
        print("Example: python seed_expense.py 1 50 6")
        sys.exit(1)

    params = parse_args(sys.argv[1:])
    if not params:
        print("Usage: python seed_expense.py <user_id> <count> <months>")
        print("Example: python seed_expense.py 1 50 6")
        sys.exit(1)

    seed_expenses(params["user_id"], params["count"], params["months"])
