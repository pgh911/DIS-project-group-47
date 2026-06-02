from flask import Flask, render_template
from database import init_db
from controllers import ledger

init_db()

app = Flask(__name__)

@app.route("/")
def home():
    values = [{
        "name": "test",
        "age": 17
    },
    {
        "name": "test2",
        "age": 24
    }]
    return render_template("pages/test.html", values=values)

app.register_blueprint(ledger.bp)
