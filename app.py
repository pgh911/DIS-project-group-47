import sqlite3
from flask import request, redirect, session, url_for, Flask, render_template
from controllers import ledger
from database import init_db, db_connection
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.user import User, get_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

init_db()

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

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


# @app.route("/home")
# def index():
#     conn = db_connection()

#     ledgers = conn.execute(
#         "SELECT * FROM ledgers ORDER BY lid"
#     ).fetchall()

#     conn.close()

#     return render_template(
#         "pages/index.html",
#         ledgers=ledgers
#     )

@app.route("/register")
def register():
    return render_template("pages/register.html")

app.register_blueprint(ledger.bp)

if __name__ == "__main__":
    app.run(debug=True)