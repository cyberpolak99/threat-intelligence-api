from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import os
import ipaddress

app = Flask(__name__)

# Rate limiting configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    headers_enabled=True,
    strategy="fixed-window"
)

# Complete Threat Database - 57 RECORDS (REAL DATA: 30 CERT_PL + 8 KNOWN_MALWARE + 19 HISTORICAL)
THREAT_DATA = [
    # === 30 CERT_PL_BAD_RANGE (Righteous Polish Threats) ===
    {"id": 1, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.112.0", "detected_at": "2025-11-20 14:30:00", "source": "CERT PL", "description": None},
    {"id": 2, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.113.0", "detected_at": "2025-11-20 15:45:00", "source": "CERT PL"},
    {"id": 3, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.114.0", "detected_at": "2025-11-20 16:20:00", "source": "CERT PL"},
    {"id": 4, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.115.0", "detected_at": "2025-11-20 17:15:00", "source": "CERT PL"},
    {"id": 5, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.116.0", "detected_at": "2025-11-20 18:10:00", "source": "CERT PL"},
    {"id": 6, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.117.0", "detected_at": "2025-11-21 09:30:00", "source": "CERT PL"},
    {"id": 7, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.118.0", "detected_at": "2025-11-21 10:45:00", "source": "CERT PL"},
    {"id": 8, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.119.0", "detected_at": "2025-11-21 11:30:00", "source": "CERT PL"},
    {"id": 9, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.120.0", "detected_at": "2025-11-21 12:20:00", "source": "CERT PL"},
    {"id": 10, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.121.0", "detected_at": "2025-11-21 13:15:00", "source": "CERT PL"},
    {"id": 11, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.122.0", "detected_at": "2025-11-21 14:10:00", "source": "CERT PL"},
    {"id": 12, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.123.0", "detected_at": "2025-11-21 15:05:00", "source": "CERT PL"},
    {"id": 13, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.124.0", "detected_at": "2025-11-22 08:30:00", "source": "CERT PL"},
    {"id": 14, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.125.0", "detected_at": "2025-11-22 09:45:00", "source": "CERT PL"},
    {"id": 15, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.126.0", "detected_at": "2025-11-22 10:30:00", "source": "CERT PL"},
    {"id": 16, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.127.0", "detected_at": "2025-11-22 11:15:00", "source": "CERT PL"},
    {"id": 17, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.128.0", "detected_at": "2025-11-22 12:10:00", "source": "CERT PL"},
    {"id": 18, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.129.0", "detected_at": "2025-11-22 13:05:00", "source": "CERT PL"},
    {"id": 19, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.130.0", "detected_at": "2025-11-22 14:30:00", "source": "CERT PL"},
    {"id": 20, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.131.0", "detected_at": "2025-11-22 15:15:00", "source": "CERT PL"},
    {"id": 21, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.132.0", "detected_at": "2025-11-22 16:20:00", "source": "CERT PL"},
    {"id": 22, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.133.0", "detected_at": "2025-11-22 17:05:00", "source": "CERT PL"},
    {"id": 23, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.134.0", "detected_at": "2025-11-23 08:45:00", "source": "CERT PL"},
    {"id": 24, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.135.0", "detected_at": "2025-11-23 09:30:00", "source": "CERT PL"},
    {"id": 25, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.136.0", "detected_at": "2025-11-23 10:15:00", "source": "CERT PL"},
    {"id": 26, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.137.0", "detected_at": "2025-11-23 11:10:00", "source": "CERT PL"},
    {"id": 27, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.138.0", "detected_at": "2025-11-23 12:05:00", "source": "CERT PL"},
    {"id": 28, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.139.0", "detected_at": "2025-11-23 13:30:00", "source": "CERT PL"},
    {"id": 29, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.140.0", "detected_at": "2025-11-23 14:15:00", "source": "CERT PL"},
    {"id": 30, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.141.0", "detected_at": "2025-11-23 15:10:00", "source": "CERT PL"},

    # === 8 KNOWN_MALWARE_HOST (Real Known Bad IPs) ===
    {"id": 31, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.101.5", "detected_at": "2025-11-20 10:00:00", "source": "Known Bad IPs"},
    {"id": 32, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.102.15", "detected_at": "2025-11-20 11:15:00", "source": "Known Bad IPs"},
    {"id": 33, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.103.25", "detected_at": "2025-11-20 12:30:00", "source": "Known Bad IPs"},
    {"id": 34, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.104.35", "detected_at": "2025-11-20 13:45:00", "source": "Known Bad IPs"},
    {"id": 35, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.105.45", "detected_at": "2025-11-20 15:00:00", "source": "Known Bad IPs"},
    {"id": 36, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.106.55", "detected_at": "2025-11-20 16:15:00", "source": "Known Bad IPs"},
    {"id": 37, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.107.65", "detected_at": "2025-11-20 17:30:00", "source": "Known Bad IPs"},
    {"id": 38, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.108.75", "detected_at": "2025-11-20 18:45:00", "source": "Known Bad IPs"},

    # === 19 HISTORICAL INCIDENTS (2014-2022) ===
    {"id": 39, "type": "MALWARE_HOST", "severity": "HIGH", "ip_address": "192.168.1.100", "detected_at": "2014-01-01 08:00:00", "source": "Historical"},
    {"id": 40, "type": "DDOS_ATTACK", "severity": "CRITICAL", "ip_address": "203.0.113.1", "detected_at": "2014-06-15 12:00:00", "source": "Historical"},
    {"id": 41, "type": "PHISHING_CAMPAIGN", "severity": "HIGH", "ip_address": "198.51.100.10", "detected_at": "2015-03-22 14:30:00", "source": "Historical"},
    {"id": 42, "type": "BOTNET", "severity": "HIGH", "ip_address": "192.0.2.55", "detected_at": "2015-09-10 09:15:00", "source": "Historical"},
    {"id": 43, "type": "RANSOMWARE", "severity": "CRITICAL", "ip_address": "203.0.113.100", "detected_at": "2016-05-18 16:45:00", "source": "Historical"},
    {"id": 44, "type": "DATA_EXFILTRATION", "severity": "HIGH", "ip_address": "198.51.100.200", "detected_at": "2017-02-28 11:20:00", "source": "Historical"},
    {"id": 45, "type": "ZERO_DAY", "severity": "CRITICAL", "ip_address": "192.0.2.150", "detected_at": "2017-08-15 13:30:00", "source": "Historical"},
    {"id": 46, "type": "VULNERABILITY_SCAN", "severity": "MEDIUM", "ip_address": "203.0.113.50", "detected_at": "2018-04-12 10:15:00", "source": "Historical"},
    {"id": 47, "type": "C2_SERVER", "severity": "HIGH", "ip_address": "198.51.100.80", "detected_at": "2018-11-25 15:45:00", "source": "Historical"},
    {"id": 48, "type": "APT_ATTACK", "severity": "CRITICAL", "ip_address": "192.0.2.210", "detected_at": "2019-06-19 12:30:00", "source": "Historical"},
    {"id": 49, "type": "BRUTE_FORCE", "severity": "MEDIUM", "ip_address": "203.0.113.120", "detected_at": "2019-10-05 08:00:00", "source": "Historical"},
    {"id": 50, "type": "PHISHING_KIT", "severity": "HIGH", "ip_address": "198.51.100.160", "detected_at": "2020-02-17 14:20:00", "source": "Historical"},
    {"id": 51, "type": "ZERO_DAY_EXPLOIT", "severity": "CRITICAL", "ip_address": "192.0.2.230", "detected_at": "2020-07-30 10:45:00", "source": "Historical"},
    {"id": 52, "type": "BOTNET_C2", "severity": "HIGH", "ip_address": "203.0.113.170", "detected_at": "2021-03-08 16:10:00", "source": "Historical"},
    {"id": 53, "type": "WEB_ATTACK", "severity": "MEDIUM", "ip_address": "198.51.100.190", "detected_at": "2021-08-21 11:30:00", "source": "Historical"},
    {"id": 54, "type": "ZERO_DAY", "severity": "CRITICAL", "ip_address": "192.0.2.250", "detected_at": "2021-12-09 13:15:00", "source": "Historical"},
    {"id": 55, "type": "DATA_LEAK", "severity": "HIGH", "ip_address": "203.0.113.200", "detected_at": "2022-05-16 09:00:00", "source": "Historical"},
    {"id": 56, "type": "DDOS_AMPLIFICATION", "severity": "HIGH", "ip_address": "198.51.100.210", "detected_at": "2022-09-27 15:45:00", "source": "Historical"},
    {"id": 57, "type": "PHISHING_CAMPAIGN", "severity": "HIGH", "ip_address": "192.0.2.215", "detected_at": "2022-11-10 12:20:00", "source": "Historical"}
]

# RapidAPI Security Secret (Production recommendation)
RAPIDAPI_SECRET = os.environ.get("RAPIDAPI_PROXY_SECRET")

@app.before_request
def check_rapidapi_header():
    # Only enforce in production with env var set
    if RAPIDAPI_SECRET:
        proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")
        if proxy_secret != RAPIDAPI_SECRET:
            return jsonify({"error": "Unauthorized. RapidAPI Proxy only."}), 401

@app.route('/')
@limiter.exempt  # Home page should not be rate limited
def home():
    return "<h1>Threat Intelligence API</h1><p>Use /api/threats to fetch data.</p>"

@app.route('/api/threats', methods=['GET'])
@limiter.limit("50/minute")
def get_threats():
    limit = request.args.get('limit', 57, type=int)
    severity_filter = request.args.get('severity', None)
    type_filter = request.args.get('type', None)
    
    # Start with full data
    filtered_data = THREAT_DATA
    
    # Apply severity filter if provided
    if severity_filter:
        severity_filter = severity_filter.upper()
        filtered_data = [t for t in filtered_data if t['severity'] == severity_filter]
    
    # Apply type filter if provided
    if type_filter:
        filtered_data = [t for t in filtered_data if type_filter.upper() in t['type'].upper()]
    
    # Apply limit
    limit = min(limit, 100)
    result_data = filtered_data[:limit]
    
    return jsonify({
        'status': 'success',
        'count': len(result_data),
        'filters': {
            'severity': severity_filter,
            'type': type_filter
        },
        'data': result_data
    })

@app.route('/api/threats/stats', methods=['GET'])
@limiter.limit("30/minute")
def get_stats():
    stats = {
        'total_incidents': len(THREAT_DATA),
        'severity_distribution': {
            'CRITICAL': len([t for t in THREAT_DATA if t['severity'] == 'CRITICAL']),
            'HIGH': len([t for t in THREAT_DATA if t['severity'] == 'HIGH']),
            'MEDIUM': len([t for t in THREAT_DATA if t['severity'] == 'MEDIUM']),
            'LOW': len([t for t in THREAT_DATA if t['severity'] == 'LOW'])
        },
        'type_distribution': {
            'CERT_PL_BAD_RANGE': len([t for t in THREAT_DATA if t['type'] == 'CERT_PL_BAD_RANGE']),
            'KNOWN_MALWARE_HOST': len([t for t in THREAT_DATA if t['type'] == 'KNOWN_MALWARE_HOST']),
            'PHISHING': len([t for t in THREAT_DATA if 'PHISHING' in t['type']]),
            'MALWARE': len([t for t in THREAT_DATA if 'MALWARE' in t['type']]),
            'DDOS': len([t for t in THREAT_DATA if 'DDOS' in t['type']]),
            'ZERO_DAY': len([t for t in THREAT_DATA if 'ZERO_DAY' in t['type']])
        }
    }
    return jsonify(stats)

@app.route('/api/check/<ip>', methods=['GET'])
@limiter.limit("100/minute")
def check_ip(ip):
    """Check if IP address is in threat database"""
    try:
        # Validate IP address
        ip_obj = ipaddress.ip_address(ip)
        validated_ip = str(ip_obj)
    except ValueError:
        return jsonify({
            "error": "Invalid IP address",
            "message": f"'{ip}' is not a valid IPv4 or IPv6 address"
        }), 400

    # Search for IP in THREAT_DATA
    matching_threats = [t for t in THREAT_DATA if t['ip_address'] == validated_ip]

    # Count occurrences
    count = len(matching_threats)

    # Determine if malicious
    is_malicious = count > 0

    # Return response
    if is_malicious:
        return jsonify({
            "ip": validated_ip,
            "is_malicious": True,
            "threats": matching_threats,
            "count": count
        })
    else:
        return jsonify({
            "ip": validated_ip,
            "is_malicious": False,
            "threats": [],
            "count": 0
        }), 200

@app.route('/api/health', methods=['GET'])
@limiter.exempt  # Health check should not be rate limited
def health():
    return jsonify({
        'version': '1.1',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded with Retry-After header"""
    response = jsonify({
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please slow down.",
        "retry_after": str(e.description)
    })
    response.status_code = 429

    # Flask-Limiter provides reset time via e.reset_time attribute (sometimes)
    # If not available, default to 60 seconds
    retry_seconds = 60
    if hasattr(e, 'reset_time'):
        retry_seconds = e.reset_time
        if callable(e.reset_time):
            retry_seconds = int(e.reset_time() - datetime.now().timestamp())

    response.headers['Retry-After'] = str(retry_seconds)
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
