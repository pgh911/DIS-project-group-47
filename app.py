import sqlite3
from flask import request, redirect, session, url_for, Flask, render_template
from controllers import ledger
from database import init_db, db_connection
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User, get_user, create_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

init_db()

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route("/")
def index():
    return redirect("/ledgers")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        print(request.form)
        if request.form['password'] != request.form['password_repeat']:
            return 401 
        
        password = request.form['password']
        username = request.form['email']
        user_id = create_user(email=username, password=password)
        
        if user_id:
            conn = db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE username = ? AND password = ?",
                    (username, password)
                )
                row = cursor.fetchone()
                if row is None:
                    return render_template("pages/login.html", error="Invalid credentials")
                user = User(row)
                login_user(user)
                return redirect(url_for("ledger.ledgers"))
            finally:
                    conn.close()
        return redirect(url_for('ledger.ledgers'))

    return render_template("pages/register.html")



@login_manager.user_loader
def load_user(user_id):
    conn = db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return User(row)

    finally:
        conn.close()

@app.route("/back", methods=["GET", "POST"])
def back():
    return redirect("/ledgers")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    conn = db_connection()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        row = cursor.fetchone()

        if row is None:
            return render_template("pages/login.html", error="Invalid credentials")

        user = User(row)
        login_user(user)

        return redirect(url_for("ledger.ledgers"))

    finally:
        conn.close()

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


app.register_blueprint(ledger.bp)

if __name__ == "__main__":
    app.run(debug=True)