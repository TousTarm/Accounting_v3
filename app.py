from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os,csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]
    collection = db["data"]

@app.route('/')
def home():
    return render_template('index.j2')


if __name__ == "__main__":
    app.run(debug=True)