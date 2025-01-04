# My Project For Pearson Accredition "U18 IoT", Network & Cybersecurity Specialization
# Rawan Amr Abdelsattar @ WE Zayed ATS

from flask import Flask, request, jsonify
from flask import Flask, render_template
import sqlite3
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

# Create SQLite database and logs table if they don't exist
def init_db():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY, timestamp TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# Function to insert log into the database
def insert_log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute('INSERT INTO logs (timestamp, message) VALUES (?, ?)', (timestamp, message))
    conn.commit()
    conn.close()

# API route to receive and store logs
@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    message = data.get('message')
    if message:
        insert_log(message)
        return jsonify({"status": "success", "message": "Log added."}), 200
    else:
        return jsonify({"status": "error", "message": "No message provided."}), 400


# API route to get and retrieve logs
@app.route('/logs', methods=['GET'])
def get_logs():
    conn = sqlite3.connect('logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM logs ORDER BY id ASC')
    logs = [{"id": row[0], "timestamp": row[1], "message": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(logs)

# API route to delete logs
@app.route('/logs', methods=['DELETE'])
def delete_logs():
    try:
        conn = sqlite3.connect('logs.db')
        c = conn.cursor()
        c.execute('DELETE FROM logs')  # Delete all rows in the logs table
        conn.commit()
        conn.close()
        return jsonify({"message": "All logs deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
