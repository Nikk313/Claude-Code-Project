#!/usr/bin/env python3
"""Seed a realistic random Indian user into the database."""

import random
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from werkzeug.security import generate_password_hash
from database.db import get_db

# Common Indian first names by region
FIRST_NAMES = {
    "north": ["Rahul", "Amit", "Rajesh", "Priya", "Neha", "Anjali", "Vikram", "Rohan", "Pooja", "Sneha"],
    "south": ["Arjun", "Karthik", "Lakshmi", "Divya", "Prakash", "Meera", "Suresh", "Kavita", "Ravi", "Anita"],
    "east": ["Sourav", "Debashish", "Mamata", "Ritwik", "Sreyoshi", "Tanushree", "Anirban", "Koel"],
    "west": ["Siddharth", "Pratiksha", "Sagar", "Rutuja", "Atharva", "Trupti", "Chinmay", "Swara"],
}

# Common Indian surnames by region
SURNAMES = {
    "north": ["Sharma", "Verma", "Gupta", "Agarwal", "Singh", "Kumar", "Malhotra", "Kapoor", "Chopra"],
    "south": ["Iyer", "Nair", "Reddy", "Rao", "Pillai", "Menon", "Krishnan", "Subramanian", "Gowda"],
    "east": ["Banerjee", "Chatterjee", "Ganguly", "Mukherjee", "Das", "Bose", "Sengupta", "Roy"],
    "west": ["Patel", "Desai", "Joshi", "Kulkarni", "Deshmukh", "Thakur", "Mehta", "Shah"],
}

def generate_indian_name():
    """Generate a realistic random Indian name."""
    region = random.choice(list(FIRST_NAMES.keys()))
    first_name = random.choice(FIRST_NAMES[region])
    last_name = random.choice(SURNAMES[region])
    return f"{first_name} {last_name}"

def generate_email_from_name(name):
    """Generate email from name with random 2-3 digit suffix."""
    first, last = name.lower().split()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    suffix = random.randint(10, 999)
    email = f"{first}.{last}{suffix}@{random.choice(domains)}"
    return email

def email_exists(email):
    """Check if email already exists in database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def seed_user():
    """Generate and insert a unique random Indian user."""
    # Generate unique name/email combination
    max_attempts = 10
    for attempt in range(max_attempts):
        name = generate_indian_name()
        email = generate_email_from_name(name)

        if not email_exists(email):
            break
    else:
        print(f"Could not generate unique email after {max_attempts} attempts")
        return None

    # Hash password
    password_hash = generate_password_hash("password123")

    # Insert user
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (email, password_hash)
    )
    conn.commit()

    user_id = cursor.lastrowid
    conn.close()

    print(f"User created successfully!")
    print(f"  id: {user_id}")
    print(f"  name: {name}")
    print(f"  email: {email}")

    return {"id": user_id, "name": name, "email": email}

if __name__ == "__main__":
    seed_user()
