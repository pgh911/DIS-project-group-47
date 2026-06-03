# from flask import Flask, render_template
# from controllers import ledger
# import sqlite3 

# init_db()

# app = Flask(__name__)

# @app.route("/")
# def home():
#     values = [{
#         "name": "test",
#         "age": 17
#     },
#     {
#         "name": "test2",
#         "age": 24
#     }]
#     return render_template("pages/test.html", values=values)

# app.register_blueprint(ledger.bp)
# from database import init_db
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

if app.debug:
    init_db()

def get_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()

    ledgers = conn.execute(
        "SELECT * FROM ledgers ORDER BY lid"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        ledgers=ledgers
    )

if __name__ == "__main__":
    app.run(debug=True)