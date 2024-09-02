from datetime import timezone
from flask import Flask, render_template, request
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/mindconnect"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def home():
    return render_template("home.html")

@app.route('/signin', methods=["GET"])
def signin():
    return render_template("login.html")
        

@app.route('/signup', methods=["GET"])
def signup():
    return render_template("signup.html")

app.run(debug=True)