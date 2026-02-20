"""
API FLASK ENDPOINT - POPRAWIONE
==================
Udostępnij dane o zagrożeniach
"""

from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Poprawiona ścieżka do bazy
DB_PATH = os.path.join(os.getcwd(), 'cyber_sheld', 'data', 'cyber_shield.db')

@app.route('/')
def home():
    return "<h1>Threat Intelligence API</h1><p>Uzywaj /api/threats do pobrania danych</p>"


@app.route('/api/threats', methods=['GET'])
def get_threats():
    """Pobierz 50 ostatnich zagroze"""
    limit = request.args.get('limit', 50, type=int)
    limit = min(limit, 100)
    
    if not os.path.exists(DB_PATH):
        return jsonify({'error': 'Database not found'}), 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM incident_reports
            ORDER BY detected_at DESC
            LIMIT ?
        ''', (limit,))
        
        threats = []
        for row in cursor.fetchall():
            threats.append(dict(row))
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(threats),
            'data': threats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/threats/stats', methods=['GET'])
def get_stats():
    """Statystyki bazy"""
    if not os.path.exists(DB_PATH):
        return jsonify({'error': 'Database not found'}), 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        stats = {
            'total_incidents': cursor.execute('SELECT COUNT(*) FROM incident_reports').fetchone()[0],
            'total_blocks': cursor.execute('SELECT COUNT(*) FROM active_blocks').fetchone()[0],
            'response_actions': cursor.execute('SELECT COUNT(*) FROM response_actions').fetchone()[0]
        }
        
        conn.close()
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'db_path': DB_PATH,
        'db_exists': os.path.exists(DB_PATH)
    })


if __name__ == '__main__':
    app.run(port=10000, debug=False)
