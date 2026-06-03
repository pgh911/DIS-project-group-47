from flask import Flask, render_template
from controllers import ledger
from database import init_db, db_connection
import sqlite3

app = Flask(__name__)

if app.debug:
    init_db()

# print(app.url_map)

@app.route("/")
def index():
    conn = db_connection()

    ledgers = conn.execute(
        "SELECT * FROM ledgers ORDER BY lid"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        ledgers=ledgers
    )

app.register_blueprint(ledger.bp)

if __name__ == "__main__":
    app.run(debug=True)