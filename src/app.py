from flask import Flask, render_template

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