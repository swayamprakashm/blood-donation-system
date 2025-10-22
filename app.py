from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, bcrypt
from datetime import date
from functools import wraps

app = Flask(__name__)
app.secret_key = "aceec027"

# ---------------------------
# Initialize Database
# ---------------------------
def init_db():
    conn = sqlite3.connect("donor.db")
    cursor = conn.cursor()

    # Users table with role column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    """)

    # Donors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        last_donation TEXT,
        contact TEXT,
        city TEXT,
        notes TEXT
    )
    """)

    # Add default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed_pw = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       ("admin", "admin@example.com", hashed_pw, "admin"))

    conn.commit()
    conn.close()

init_db()

# ---------------------------
# Database helper
# ---------------------------
def get_db():
    conn = sqlite3.connect("donor.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------
# Login Required Decorator
# ---------------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first!", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
@login_required
def index():
    return render_template("index.html", current_year=date.today().year)

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user["password"]):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash(f"Login successful! ({session['role']})", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

# -------- SIGNUP --------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"].encode("utf-8")
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_pw))
            conn.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "danger")
        finally:
            conn.close()

    return render_template("signup.html")

# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

# -------- DONOR MANAGEMENT --------
@app.route("/add_donor", methods=["GET", "POST"])
@login_required
def add_donor():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        blood_group = request.form["blood_group"]
        last_donation = request.form["last_donation"]
        contact = request.form["contact"]
        city = request.form["city"]
        notes = request.form["notes"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO donors (name, age, gender, blood_group, last_donation, contact, city, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, age, gender, blood_group, last_donation, contact, city, notes)
        )
        conn.commit()
        conn.close()
        flash("Donor added successfully!", "success")
        return redirect(url_for("view_donors"))

    return render_template("add_donor.html", current_date=date.today().isoformat())

@app.route("/view_donors")
@login_required
def view_donors():
    query = request.args.get("q", "").strip().lower()
    conn = get_db()
    cursor = conn.cursor()
    if query:
        cursor.execute("SELECT * FROM donors WHERE lower(name) LIKE ? OR lower(blood_group) LIKE ? OR lower(city) LIKE ?",
                       (f"%{query}%", f"%{query}%", f"%{query}%"))
    else:
        cursor.execute("SELECT * FROM donors")
    donors = cursor.fetchall()
    conn.close()
    return render_template("view_donors.html", donors=donors, search_query=query)

@app.route("/delete_donor/<int:donor_id>")
@login_required
def delete_donor(donor_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM donors WHERE id=?", (donor_id,))
    conn.commit()
    conn.close()
    flash("Donor deleted!", "info")
    return redirect(url_for("view_donors"))

# -------- EXTRA PAGES --------
@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html")

# ---------------------------
# Run Flask
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
