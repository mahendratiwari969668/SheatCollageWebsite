from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

# ================= DATABASE SETUP =================
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= LANDING PAGE =================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "home":
            return redirect(url_for("home"))

    return render_template("index.html")

# ================= HOME PAGE =================
@app.route("/home")
def home():
    return render_template("home.html")

# ================= ABOUT PAGE =================
@app.route("/about")
def about():
    return render_template("about.html")

# ================= COURSES PAGE =================
@app.route("/courses")
def courses():
    return render_template("courses.html")

# ================= FACULTY PAGE =================
@app.route("/faculty")
def faculty():
    return render_template("faculty.html")

# ================= ADMISSION PAGE =================
@app.route("/admission", methods=["GET", "POST"])
def admission():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        course = request.form.get("course")
        qualification = request.form.get("qualification")
        percentage = request.form.get("percentage")
        city = request.form.get("city")
        state = request.form.get("state")
        message = request.form.get("message")

        print("===== NEW ADMISSION FORM SUBMISSION =====")
        print("Full Name:", full_name)
        print("Email:", email)
        print("Phone:", phone)
        print("Course:", course)
        print("Qualification:", qualification)
        print("Percentage:", percentage)
        print("City:", city)
        print("State:", state)
        print("Message:", message)
        print("========================================")

        return render_template("admission.html", success=True)

    return render_template("admission.html", success=False)

# ================= CONTACT PAGE =================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        message = request.form.get("message")

        print("===== NEW CONTACT FORM MESSAGE =====")
        print("Name:", name)
        print("Email:", email)
        print("Phone:", phone)
        print("Subject:", subject)
        print("Message:", message)
        print("====================================")

        return render_template("contact.html", success=True)

    return render_template("contact.html", success=False)

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()
        confirm_password = request.form.get("confirm_password").strip()

        if password != confirm_password:
            message = "Passwords do not match!"
            return render_template("register.html", message=message)

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            message = "Email already registered!"
            return render_template("register.html", message=message)

    return render_template("register.html", message=message)

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]

            return redirect(url_for("dashboard"))
        else:
            message = "Invalid email or password!"

    return render_template("login.html", message=message)

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        user_email=session.get("user_email")
    )

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)