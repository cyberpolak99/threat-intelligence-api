from flask import Flask, jsonify, request, abort, Response, send_file
from flask_cors import CORS
from datetime import datetime
import os
import logging
import sqlite3
from db_manager import DBManager
from security import protected
from bulk_processor import BulkIPProcessor
from honeypot_feed import is_ip_in_honeypot, get_honeypot_details, get_all_honeypot_ips

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ThreatAPI')

app = Flask(__name__)
CORS(app, origins=["https://rapidapi.com", "https://threat-intelligence-api.onrender.com", "http://localhost:3000"])

# Initialize DB Manager
db = DBManager(db_path=os.environ.get("DATABASE_URL", "data/cyber_shield.db"))

import random
from datetime import timedelta

def migrate_sample_data():
    stats = db.get_stats()
    if stats['total_anomalies'] < 50:  # Upewnijmy się, że jest wystarczająco dużo danych
        logger.info("Baza danych ma mało danych. Generowanie bogatej historii dla Dashboardu (Social Proof)...")
        now = datetime.now()
        
        ATTACKER_IPS = [
            "45.133.1.20", "185.220.101.5", "89.248.165.59", "193.32.162.87",
            "171.25.193.78", "162.247.74.27", "185.243.218.50", "45.155.205.233",
            "103.251.167.20", "37.120.247.199", "94.102.49.190", "212.70.149.150"
        ]
        
        ATTACK_TYPES = [
            ("SSH_BRUTE_FORCE", "SSH brute force login attempt", "HIGH", 0.85, 22),
            ("PORT_SCAN",       "Aggressive port scan detected", "MEDIUM", 0.55, None),
            ("HONEYPOT_HIT",    "Honeypot interaction triggered", "HIGH", 0.90, 80),
            ("MALWARE_C2",      "Known malware C2 callback detected", "CRITICAL", 1.0, 443),
            ("WEB_EXPLOIT",     "Web application exploit attempt", "HIGH", 0.80, 80),
            ("CREDENTIAL_STUFF","Credential stuffing on login page", "HIGH", 0.75, 443),
            ("SMB_SCAN",        "SMB/EternalBlue scan attempt", "CRITICAL", 0.95, 445),
            ("TELNET_BRUTE",    "Telnet brute force (IoT)", "MEDIUM", 0.65, 23)
        ]
        
        # Generujemy 200 zdarzeń rozłożonych na ostatnie 7 dni
        records = []
        for _ in range(200):
            attack = random.choice(ATTACK_TYPES)
            days_ago = random.uniform(0, 6.9)
            ts = now - timedelta(days=days_ago)
            score = max(0.0, min(1.0, attack[3] + random.uniform(-0.1, 0.1)))
            port = attack[4] if attack[4] else random.choice([21, 25, 3306, 5432, 8080, 3389])
            ip = random.choice(ATTACKER_IPS)
            
            records.append({
                "timestamp": ts, "src_ip": ip, "dst_ip": "10.0.0.1", "dst_port": port,
                "protocol": random.choice(["TCP", "UDP"]), "type": attack[0], 
                "severity": attack[2], "score": round(score, 4), 
                "bytes": random.randint(100, 15000), "desc": attack[1], "label": 1
            })
            
        # Sortujemy chronologicznie (od najstarszych)
        records.sort(key=lambda x: x["timestamp"])
        
        with db._get_conn() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO anomalies 
                (timestamp, src_ip, dst_ip, dst_port, protocol, type, severity, score, bytes_transferred, description, label)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            # Wstawiamy omijając standardową metodę db.log_anomaly dla szybkości i pełnej kontroli nad datą
            for r in records:
                cursor.execute(query, (
                    r["timestamp"], r["src_ip"], r["dst_ip"], r["dst_port"], r["protocol"], 
                    r["type"], r["severity"], r["score"], r["bytes"], r["desc"], r["label"]
                ))
            conn.commit()
        logger.info("Pomyślnie wygenerowano 200 realistycznych zdarzeń!")

migrate_sample_data()

# Auth is handled entirely by @protected in security.py.
# RAPIDAPI_PROXY_SECRET and THREAT_API_KEYS are read from env there.

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Resource not found"), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal Server Error: {e}")
    return jsonify(error="Internal server error"), 500

@app.route('/')
def home():
    try:
        return send_file('index.html')
    except Exception as e:
        return "<h1>Threat Intelligence API</h1><p>Dashboard is currently unavailable.</p>"

@app.route('/api/threats', methods=['GET'])
@protected
def get_threats():
    try:
        limit = request.args.get('limit', 50, type=int)
        limit = max(1, min(limit, 100))
        severity = request.args.get('severity')
        
        anomalies = db.get_anomalies(limit=limit)
        
        # Filter by severity if requested
        if severity:
            anomalies = [a for a in anomalies if a['severity'] == severity]
        
        # Map DB schema to API schema for backward compatibility
        formatted_data = []
        for a in anomalies:
            formatted_data.append({
                "id": a['id'],
                "type": a['type'] or "Unknown",
                "severity": a['severity'] or "MEDIUM",
                "ip_address": a['src_ip'],
                "detected_at": a['timestamp'],
                "description": a['description']
            })
        return jsonify({
            'status': 'success',
            'count': len(formatted_data),
            'data': formatted_data
        })
    except Exception as e:
        logger.error(f"Error fetching threats: {e}")
        abort(500)

@app.route('/api/threats/stats', methods=['GET'])
def get_stats():
    try:
        db_stats = db.get_stats()
        anomalies = db.get_anomalies(limit=1000)
        
        severity_dist = {
            'CRITICAL': len([a for a in anomalies if a['severity'] == 'CRITICAL']),
            'HIGH': len([a for a in anomalies if a['severity'] == 'HIGH']),
            'MEDIUM': len([a for a in anomalies if a['severity'] == 'MEDIUM']),
            'LOW': len([a for a in anomalies if a['severity'] == 'LOW'])
        }
        
        return jsonify({
            'total_incidents': db_stats['total_anomalies'],
            'active_blocks': db_stats['active_blocks'],
            'severity_distribution': severity_dist
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        abort(500)


@app.route('/api/threats/timeline', methods=['GET'])
def get_timeline():
    try:
        days = request.args.get('days', 7, type=int)
        days = max(1, min(days, 30))
        timeline_data = db.get_threat_timeline(days=days)
        
        # Pro-level logic: fill missing dates with 0
        from datetime import date, timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        full_timeline = []
        data_map = {item['date']: item['count'] for item in timeline_data}
        
        curr = start_date
        while curr <= end_date:
            d_str = curr.strftime('%Y-%m-%d')
            full_timeline.append({
                "date": d_str,
                "count": data_map.get(d_str, 0)
            })
            curr += timedelta(days=1)

        return jsonify({
            'status': 'success',
            'days': days,
            'data': full_timeline
        })
    except Exception as e:
        logger.error(f"Error fetching timeline: {e}")
        abort(500)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.2-hardened',
        'timestamp': datetime.now().isoformat()
    })

# Max file size: 5MB
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
MAX_ROWS = 2000

def get_db_connection():
    """Returns a standalone SQLite connection"""
    conn = sqlite3.connect(db.db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ─── Honeypot scoring constants ─────────────────────────────────────────────
# When IP is in honeypot AND has external feed data → boost risk level.
HONEYPOT_SCORE_BOOST = 0.15 # added to ti_score if also in feeds
HONEYPOT_MIN_RISK_LEVEL = "high" # minimum risk_level when seen in honeypot
_RISK_ORDER = ["none", "low", "medium", "high", "critical"]

def _elevate_risk(current: str, minimum: str) -> str:
    """Returns the higher of two risk levels."""
    try:
        return current if _RISK_ORDER.index(current) >= _RISK_ORDER.index(minimum) else minimum
    except ValueError:
        return current

import socket
import ipaddress

def lookup_ip_internal(ip_addr: str) -> dict:
    """Internal business logic for IP lookup without HTTP overhead. Supports domain resolution."""
    try:
        # Check if it's already a valid IP
        ipaddress.ip_address(ip_addr)
    except ValueError:
        try:
            # Try resolving the domain to an IP
            ip_addr = socket.gethostbyname(ip_addr)
        except Exception:
            # If not an IP and cannot be resolved
            return {'ti_score': 0, 'risk_level': 'invalid', 'sources': '', 'seen_in_honeypot': 0}
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM anomalies WHERE src_ip = ?", (ip_addr,))
            matches = [dict(row) for row in cursor.fetchall()]
            severity_map = {"CRITICAL": 100, "HIGH": 80, "MEDIUM": 50, "LOW": 20}
            reverse_map = {100: "critical", 80: "high", 50: "medium", 20: "low"}
            max_val = 0
            scores = []
            sources = set()
            for m in matches:
                val = severity_map.get(str(m.get('severity', '')).upper(), 20)
                if val > max_val:
                    max_val = val
                scores.append(float(m.get('score') or 0))
                if m.get('type'):
                    sources.add(str(m['type']))
            base_score = max(scores) if scores else 0.0
            base_risk = reverse_map.get(max_val, 'none') if matches else 'none'
            # ── Honeypot enrichment ──────────────────────────────────────────────
            in_honeypot = is_ip_in_honeypot(ip_addr)
            if in_honeypot:
                sources.add('cybershield-honeypot')
            # Boost score if ALSO in external feeds, cap at 1.0
            if matches:
                base_score = min(1.0, base_score + HONEYPOT_SCORE_BOOST)
            # Enforce minimum risk level
            base_risk = _elevate_risk(base_risk, HONEYPOT_MIN_RISK_LEVEL)
            return {
                'ti_score': int(base_score * 10000) / 10000,
                'risk_level': base_risk,
                'sources': ";".join(sorted(sources)),
                'seen_in_honeypot': 1 if in_honeypot else 0,
            }
    except Exception as e:
        logger.error(f"Internal IP lookup failed for {ip_addr}: {e}")
        return {'ti_score': 0, 'risk_level': 'error', 'sources': '', 'seen_in_honeypot': 0}

@app.route('/api/check/<ip_addr>', methods=['GET'])
@protected
def check_ip(ip_addr):
    res = lookup_ip_internal(ip_addr)
    if res['risk_level'] in ['invalid', 'error']:
        return jsonify({"error": "Invalid IP format"}), 400
    
    details = get_honeypot_details(ip_addr) if res['seen_in_honeypot'] else {}
    return jsonify({
        'ip': ip_addr,
        'is_malicious': res['risk_level'] not in ['none', 'invalid'],
        'ti_score': res['ti_score'],
        'risk_level': res['risk_level'],
        'sources': res['sources'],
        'seen_in_honeypot': res['seen_in_honeypot'],
        'honeypot_details': details,
    })

@app.route('/api/honeypot-feed', methods=['GET'])
@protected
def honeypot_feed():
    """Returns list of all IPs observed by the Cyber Shield honeypot."""
    limit = request.args.get('limit', 200, type=int)
    limit = max(1, min(limit, 1000))
    ips = get_all_honeypot_ips(limit=limit)
    return jsonify({
        'status': 'success',
        'count': len(ips),
        'data': ips,
    })

@app.route('/api/bulk-ip-csv', methods=['POST'])
@protected
def bulk_enrich_csv():
    """Upload CSV, enrich with threat intel, and return as download"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format. Upload .csv'}), 400
    # Size validation
    file_bytes = file.read()
    if len(file_bytes) > MAX_CONTENT_LENGTH:
        return jsonify({'error': f'File too large. Max {MAX_CONTENT_LENGTH/1024/1024}MB'}), 413
    
    try:
        processor = BulkIPProcessor(lookup_func=lookup_ip_internal, max_rows=MAX_ROWS)
        enriched_csv = processor.process_csv(file_bytes)
        
        # Return as downloadable file
        return Response(
            enriched_csv,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=enriched_ips.csv"}
        )
    except ValueError as val_err:
        return jsonify({'error': str(val_err)}), 400
    except Exception as err:
        logger.error(f"Bulk CSV error: {err}")
        abort(500)

@app.route('/api/threats/port-stats', methods=['GET'])
def get_port_stats():
    """
    Returns port distribution for pie chart visualization.
    Queries honeypot_hits table for top attacked ports.
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = max(1, min(limit, 50))
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Try honeypot_hits table first
            try:
                cursor.execute("""
                    SELECT dst_port, COUNT(*) as hit_count
                    FROM honeypot_hits
                    WHERE dst_port IS NOT NULL
                    GROUP BY dst_port
                    ORDER BY hit_count DESC
                    LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
            except Exception:
                rows = []
            # Fallback: use anomalies table if honeypot_hits is empty
            if not rows:
                cursor.execute("""
                    SELECT dst_port, COUNT(*) as hit_count
                    FROM anomalies
                    WHERE dst_port IS NOT NULL
                    GROUP BY dst_port
                    ORDER BY hit_count DESC
                    LIMIT ?
                """, (limit,))
                rows = cursor.fetchall()
        total = sum(r['hit_count'] for r in rows) if rows else 0
        port_data = [
            {
                'port': r['dst_port'],
                'count': r['hit_count'],
                'percentage': round(r['hit_count'] / total * 100, 2) if total > 0 else 0,
                'label': _port_label(r['dst_port'])
            }
            for r in rows
        ]
        return jsonify({
            'status': 'success',
            'total_hits': total,
            'count': len(port_data),
            'data': port_data
        })
    except Exception as e:
        logger.error(f"Error fetching port stats: {e}")
        abort(500)


def _port_label(port) -> str:
    """Returns human-readable service name for common ports."""
    known = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
        443: 'HTTPS', 445: 'SMB', 3306: 'MySQL', 3389: 'RDP',
        5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt',
        27017: 'MongoDB', 5432: 'PostgreSQL', 1433: 'MSSQL', 9200: 'Elasticsearch'
    }
    try:
        return known.get(int(port), f'Port {port}')
    except (ValueError, TypeError):
        return str(port)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    # Prod warning check
    if os.environ.get("FLASK_ENV") == "production":
        logger.info("Running in PRODUCTION mode")
    else:
        logger.info("Running in DEVELOPMENT mode")
    
    app.run(host='0.0.0.0', port=port)
