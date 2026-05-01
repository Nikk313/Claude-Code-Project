from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
from database.db import create_user, get_db
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key-change-in-production"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        if not name or not email or not password:
            flash("All fields are required")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match")
            return render_template("register.html")

        try:
            create_user(name, email, password)
            flash("Account created! Please sign in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already registered")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required")
            return render_template("login.html")

        db = get_db()
        user = db.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["name"]
        flash("Welcome back!")
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Hardcoded data for Step 4 (Step 5 will replace with DB queries)
    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2025"
    }

    summary_stats = {
        "total_spent": 1250.00,
        "transaction_count": 5,
        "top_category": "Food"
    }

    transactions = [
        {"date": "2025-01-15", "description": "Grocery shopping", "category": "Food", "amount": 45.99},
        {"date": "2025-01-12", "description": "Uber ride", "category": "Transport", "amount": 15.00},
        {"date": "2025-01-10", "description": "Electric bill", "category": "Utilities", "amount": 120.00},
        {"date": "2025-01-08", "description": "Restaurant dinner", "category": "Food", "amount": 89.50},
    ]

    category_breakdown = [
        {"category": "Food", "amount": 135.49, "percentage": 45},
        {"category": "Utilities", "amount": 120.00, "percentage": 40},
        {"category": "Transport", "amount": 15.00, "percentage": 15},
    ]

    return render_template("profile.html",
                         user=user,
                         summary_stats=summary_stats,
                         transactions=transactions,
                         category_breakdown=category_breakdown)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False,port=5001)
