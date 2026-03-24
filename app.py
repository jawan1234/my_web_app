import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Replace the string below with your actual MongoDB Connection String
# For security on Vercel, we use an Environment Variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/test")
client = MongoClient(MONGO_URI)
db = client.my_database

@app.route('/')
def index():
    # Pull all messages from the database
    messages = db.messages.find().sort("timestamp", -1)
    return render_template('index.html', messages=messages)

@app.route('/send', methods=['POST'])
def send():
    # Get the text from the form in our HTML
    user_text = request.form.get('content')
    if user_text:
        db.messages.insert_one({
            "content": user_text,
            "timestamp": datetime.now()
        })
    return redirect(url_for('index'))
