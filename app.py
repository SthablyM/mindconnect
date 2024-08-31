from flask import Flask, jsonify, request 

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def home():
    return "Hello world"

@app.route('/login', methods = ['GET'])
def login():
    return "Hello world login"


app.run(debug=True)