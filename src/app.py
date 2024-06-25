# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get('/email')
def post_email():
    return jsonify(message="POST EMAIL"), 200


@app.post('/email')
def get_email():
    data = request.json
    return jsonify(message="GET EMAIL"), 200
