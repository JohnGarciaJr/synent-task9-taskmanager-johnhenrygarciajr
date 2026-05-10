from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

import os
app.secret_key = os.urandom(24)

# Initialize the limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


# -------------------------
# REGISTER PAGE
# -------------------------
@app.route("/register", methods=["GET", "POST"])
@limiter.limit("3 per minute")
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        cur = conn.cursor()

        # Check if username already exists
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Username already exists. Please choose another.", "danger")
            conn.close()
            return redirect(url_for("register"))

        # Insert new user
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password))
        conn.commit()
        conn.close()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------------
# LOGIN PAGE
# -------------------------
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))

        flash("Invalid username or password", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# -------------------------
# DASHBOARD
# -------------------------
from datetime import date

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    filter_option = request.args.get("filter", "all")

    conn = get_db()
    cur = conn.cursor()

    if filter_option == "completed":
        cur.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND completed = 1",
            (session["user_id"],)
        )
    elif filter_option == "pending":
        cur.execute(
            "SELECT * FROM tasks WHERE user_id = ? AND completed = 0",
            (session["user_id"],)
        )
    else:
        cur.execute(
            "SELECT * FROM tasks WHERE user_id = ?",
            (session["user_id"],)
        )

    tasks = cur.fetchall()
    conn.close()

    # Pass today's date to the template for overdue comparison
    return render_template(
        "dashboard.html",
        tasks=tasks,
        filter_option=filter_option,
        current_date=str(date.today())
    )


# -------------------------
# ADD TASK
# -------------------------
@app.route("/add", methods=["GET", "POST"])
@limiter.limit("20 per minute")
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"] or None

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO tasks (user_id, title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, ?, 0)",
            (session["user_id"], title, description, priority, due_date)
        )
        conn.commit()
        conn.close()

        flash("Task added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("add_task.html")


# -------------------------
# EDIT TASK
# -------------------------
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
@limiter.limit("20 per minute")
def edit_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()

    # Fetch the task
    cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", 
                (task_id, session["user_id"]))
    task = cur.fetchone()

    if not task:
        flash("Task not found", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        due_date = request.form["due_date"] or None

        cur.execute(
            "UPDATE tasks SET title = ?, description = ?, priority = ?, due_date = ? WHERE id = ?",
            (title, description, priority, due_date, task_id)
        )
        conn.commit()
        conn.close()

        flash("Task updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_task.html", task=task)


# -------------------------
# DELETE TASK
# -------------------------
@app.route("/delete/<int:task_id>", methods=["GET", "POST"])
@limiter.limit("20 per minute")
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", 
                (task_id, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -------------------------
# MARK TASK AS COMPLETE
# -------------------------
@app.route("/complete/<int:task_id>", methods=["GET", "POST"])
@limiter.limit("20 per minute")
def complete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?", 
                (task_id, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -------------------------
# CUSTOM 404 PAGE
# -------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# -------------------------
# CUSTOM 500 PAGE
# -------------------------
@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

# -------------------------
# CUSTOM 403 PAGE
# -------------------------
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


# -------------------------
# RUN THE APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
