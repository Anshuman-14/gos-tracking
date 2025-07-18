from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

DB_NAME = "location.db"

# Initialize database with device_id as PRIMARY KEY
def init_db():
    with sqlite3.connect(DB_NAME) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            device_id TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL,
            timestamp TEXT
        )
        """)

# Route to save or update location
@app.route('/api/location', methods=['POST'])
def save_location():
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    device_id = request.form.get("id")
    ts = datetime.now().isoformat()

    if lat and lon and device_id:
        try:
            with sqlite3.connect(DB_NAME) as con:
                con.execute("""
                    INSERT OR REPLACE INTO locations (device_id, latitude, longitude, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (device_id, lat, lon, ts))
            return jsonify({"status": "success"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Missing lat, lon, or id"}), 400

# Route to get all current device locations
@app.route('/api/locations', methods=['GET'])
def get_all_locations():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM locations ORDER BY timestamp DESC")
        rows = cur.fetchall()
        devices = [
            {"device_id": r[0], "latitude": r[1], "longitude": r[2], "timestamp": r[3]}
            for r in rows
        ]
    return jsonify(devices)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

    
@app.route('/')
def home():
    return '🚀 GPS Tracking Server is Running!'
