import flask
from flask import request, jsonify, render_template
import requests
import json

with open('users.json', 'r') as f:
    data = json.load(f)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html", data=data)

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template("analytics.html", data=data)
app.run()
