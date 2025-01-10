# My Project For Pearson Accredition "U18 IoT", Network & Cybersecurity Specialization
# Rawan Amr Abdelsattar @ WE Zayed ATS

from flask import Flask, request, jsonify
from flask import Flask, render_template
import sqlite3
from flask_cors import CORS
from datetime import datetime
import pytz

import requests
import json

app = Flask(__name__)
CORS(app)

AUTHORIZED_PASSWORD = "mypasswd"

# Function to send Email to my account by triggering the Webhook
def send_email(recepient_email, timestamp):

    url = "https://hook.eu2.make.com/7ublywlgv7c1rk4m6hnod8wstwowbn3b"
    data = {"event": "motion_detected", "message": "PIR detected motion!!", 'email': recepient_email, 'timestamp': timestamp}
    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.text)


# Create SQLite database and logs table if they don't exist
def init_db():
    conn = sqlite3.connect('/home/rawanamr/my_iot_api_flask_app/logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY, timestamp TEXT, message TEXT, email TEXT)''')
    conn.commit()
    conn.close()

# Function to insert log into the database
def insert_log(message, email, timestamp):
    conn = sqlite3.connect('/home/rawanamr/my_iot_api_flask_app/logs.db')
    c = conn.cursor()
    c.execute('INSERT INTO logs (timestamp, message, email) VALUES (?, ?, ?)', (timestamp, message, email))
    conn.commit()
    conn.close()

# API route to receive and store logs
@app.route('/log', methods=['POST'])
def log():
    timestamp = datetime.now(pytz.timezone("Africa/Cairo")).strftime('%Y-%m-%d %H:%M:%S')
    data = request.get_json()
    message = data.get('message')
    email = data.get('email')
    if message:
        insert_log(message, email, timestamp)
        print(email, type(email))
        send_email(email, timestamp)
        return jsonify({"status": "success", "message": "Log added."}), 200
    else:
        return jsonify({"status": "error", "message": "No message provided."}), 400


# API route to get and retrieve logs
@app.route('/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('/home/rawanamr/my_iot_api_flask_app/logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM logs ORDER BY id ASC')
    logs = [{"id": row[0], "timestamp": row[1], "message": row[2], "email": row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(logs)

@app.route('/logs', methods=['DELETE'])
def delete_logs():
    data = request.json
    if not data or 'password' not in data:
        return jsonify({"error": "Password required"}), 401

    if data['password'] != AUTHORIZED_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403

    # Clear the logs
    conn = sqlite3.connect('/home/rawanamr/my_iot_api_flask_app/logs.db')
    c = conn.cursor()
    c.execute('DELETE FROM logs')
    conn.commit()
    conn.close()
    return jsonify({"message": "All logs deleted"}), 200


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
