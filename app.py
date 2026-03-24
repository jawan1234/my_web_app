import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Replace with your actual string or set it in Vercel Environment Variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/test")
client = MongoClient(MONGO_URI)
db = client.my_database

@app.route('/')
def index():
    messages = db.messages.find().sort("timestamp", -1)
    return render_template('index.html', messages=messages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send', methods=['POST'])
def send():
    user_text = request.form.get('content')
    if user_text:
        db.messages.insert_one({
            "content": user_text,
            "timestamp": datetime.now()
        })
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)