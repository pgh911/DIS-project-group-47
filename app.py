from flask import request, redirect, session, url_for, Flask, render_template
from controllers import ledger
from database import init_db, db_connection
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)

init_db()

# print(app.url_map)

@app.route("/login")
def login():
    # if request.method == "POST":
    #     username = request.form["username"]
    #     password = request.form["password"]

    #     user = users.get(username)

    #     if user and user["password"] == password:
    #         session["user_id"] = user["id"]
    #         session["username"] = username
    #         return redirect(url_for("dashboard"))

    #     return "Invalid login", 401
    return render_template("pages/login.html")


@app.route("/home")
def index():
    conn = db_connection()

    ledgers = conn.execute(
        "SELECT * FROM ledgers ORDER BY lid"
    ).fetchall()

    conn.close()

    return render_template(
        "pages/index.html",
        ledgers=ledgers
    )

app.register_blueprint(ledger.bp)

if __name__ == "__main__":
    app.run(debug=True)