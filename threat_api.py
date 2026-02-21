from flask import Flask, jsonify, request
from datetime import datetime
import os

app = Flask(__name__)

# Mock database for RapidAPI deployment
THREAT_DATA = [
    {"id": 1, "type": "Phishing", "severity": "HIGH", "ip_address": "192.168.1.100", "detected_at": "2026-02-21 12:00:00"},
    {"id": 2, "type": "Malware", "severity": "CRITICAL", "ip_address": "45.133.1.20", "detected_at": "2026-02-21 11:30:00"},
    {"id": 3, "type": "Brute Force", "severity": "MEDIUM", "ip_address": "185.220.101.5", "detected_at": "2026-02-21 10:15:00"},
    {"id": 4, "type": "DDoS", "severity": "HIGH", "ip_address": "103.212.223.4", "detected_at": "2026-02-20 23:45:00"},
    {"id": 5, "type": "SQL Injection", "severity": "CRITICAL", "ip_address": "91.240.118.12", "detected_at": "2026-02-20 22:10:00"}
]

@app.route('/')
def home():
    return "<h1>Threat Intelligence API</h1><p>Use /api/threats to fetch data.</p>"

@app.route('/api/threats', methods=['GET'])
def get_threats():
    limit = request.args.get('limit', 50, type=int)
    limit = min(limit, 100)
    return jsonify({
        'status': 'success',
        'count': len(THREAT_DATA[:limit]),
        'data': THREAT_DATA[:limit]
    })

@app.route('/api/threats/stats', methods=['GET'])
def get_stats():
    stats = {
        'total_incidents': len(THREAT_DATA),
        'severity_distribution': {
            'CRITICAL': len([t for t in THREAT_DATA if t['severity'] == 'CRITICAL']),
            'HIGH': len([t for t in THREAT_DATA if t['severity'] == 'HIGH']),
            'MEDIUM': len([t for t in THREAT_DATA if t['severity'] == 'MEDIUM'])
        }
    }
    return jsonify(stats)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
