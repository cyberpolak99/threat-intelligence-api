from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.getcwd(), 'threats.db')

def init_db():
from threat_feed_scraper import fetch_and_save
try:
    fetch_and_save()
except:
    pass

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incident_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            threat_type TEXT,
            severity TEXT,
            source TEXT,
            detected_at TEXT,
            description TEXT
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO incident_reports 
        (ip_address, threat_type, severity, source, detected_at, description)
        VALUES 
        ('192.168.1.100', 'malware', 'high', 'CERT-PL', datetime('now'), 'Suspicious activity'),
        ('10.0.0.55', 'phishing', 'medium', 'VirusTotal', datetime('now'), 'Phishing attempt'),
        ('172.16.0.1', 'brute_force', 'low', 'Honeypot', datetime('now'), 'SSH brute force')
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "<h1>Threat Intelligence API</h1><p>Use /api/threats to get data</p>"

@app.route('/api/threats', methods=['GET'])
def get_threats():
    limit = request.args.get('limit', 50, type=int)
    limit = min(limit, 100)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM incident_reports ORDER BY detected_at DESC LIMIT ?', (limit,))
    threats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({'status': 'success', 'count': len(threats), 'data': threats})

@app.route('/api/threats/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    total = cursor.execute('SELECT COUNT(*) FROM incident_reports').fetchone()[0]
    conn.close()
    return jsonify({'total_incidents': total, 'status': 'success'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'db_exists': os.path.exists(DB_PATH)
    })

if __name__ == '__main__':
    app.run(port=10000, debug=False)
