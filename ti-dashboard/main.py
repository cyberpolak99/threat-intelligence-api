from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import os
import sqlite3
import json

app = FastAPI(title="Threat Intelligence Dashboard", version="1.0")

# Templates
templates = Jinja2Templates(directory="templates")

# SQLite database
DB_PATH = os.environ.get("DB_PATH", "ti_dashboard.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize SQLite database with events table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            source TEXT NOT NULL,
            timestamp TEXT,
            meta TEXT,
            is_malicious INTEGER DEFAULT 0,
            severity TEXT DEFAULT 'LOW',
            threats TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Event data model
class Event(BaseModel):
    ip: str = Field(..., description="IP address")
    source: str = Field(..., description="Source: nginx, fw, etc.")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp")
    meta: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")

# Initialize database on startup
init_db()

# Threat Database
THREAT_DATA = [
    {"id": 1, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.112.0", "detected_at": "2025-11-20 14:30:00", "source": "CERT PL"},
    {"id": 2, "type": "CERT_PL_BAD_RANGE", "severity": "HIGH", "ip_address": "185.242.113.0", "detected_at": "2025-11-20 15:45:00", "source": "CERT PL"},
    {"id": 3, "type": "KNOWN_MALWARE_HOST", "severity": "CRITICAL", "ip_address": "185.220.101.5", "detected_at": "2025-11-20 10:00:00", "source": "Known Bad IPs"},
    {"id": 4, "type": "PHISHING_CAMPAIGN", "severity": "HIGH", "ip_address": "198.51.100.10", "detected_at": "2015-03-22 14:30:00", "source": "Historical"},
    {"id": 5, "type": "DDOS_ATTACK", "severity": "CRITICAL", "ip_address": "203.0.113.1", "detected_at": "2014-06-15 12:00:00", "source": "Historical"},
    {"id": 6, "type": "BRUTE_FORCE", "severity": "MEDIUM", "ip_address": "203.0.113.120", "detected_at": "2019-10-05 08:00:00", "source": "Historical"},
    {"id": 7, "type": "ZERO_DAY", "severity": "CRITICAL", "ip_address": "192.0.2.150", "detected_at": "2017-08-15 13:30:00", "source": "Historical"},
]

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard main page"""
    stats = get_stats_data()
    THREAT_DATA_global = THREAT_DATA # for template access
    return templates.TemplateResponse("index.html", {"request": request, "stats": stats, "THREAT_DATA": THREAT_DATA_global})

@app.get("/threats")
async def threats_page(request: Request, page: int = 1, limit: int = 50, severity: str = None):
    """Threats list page"""
    filtered_data = THREAT_DATA
    if severity:
        filtered_data = [t for t in THREAT_DATA if t['severity'] == severity.upper()]

    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_data = filtered_data[start:end]

    total_pages = (len(filtered_data) + limit - 1) // limit

    return templates.TemplateResponse("threats.html", {
        "request": request,
        "threats": paginated_data,
        "page": page,
        "total_pages": total_pages,
        "severity": severity
    })

@app.get("/api/stats")
async def get_stats():
    """Get statistics data (JSON API)"""
    return get_stats_data()

@app.get("/api/threats")
async def api_threats(severity: str = None, limit: int = 100):
    """Get threats data (JSON API)"""
    filtered_data = THREAT_DATA
    if severity:
        filtered_data = [t for t in THREAT_DATA if t['severity'] == severity.upper()]

    return {
        "total": len(THREAT_DATA),
        "filtered": len(filtered_data),
        "data": filtered_data[:limit]
    }

@app.get("/api/dashboard/stats")
async def dashboard_stats():
    """Dashboard-specific stats"""
    stats = get_stats_data()
    latest = THREAT_DATA[:5]
    return {
        "stats": stats,
        "latest_threats": latest,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/events")
async def create_event(event: Event):
    """Create new event with automatic threat analysis (adds is_malicious, severity, threats) - SQLite"""
    event_timestamp = event.timestamp if event.timestamp else datetime.now().isoformat()

    # Check against THREAT_DATA
    matching_threats = [t for t in THREAT_DATA if t['ip_address'] == event.ip]

    # Determine severity (max if multiple, else "LOW")
    is_malicious = len(matching_threats) > 0
    if is_malicious:
        severity_order = {'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        severities = [t['severity'] for t in matching_threats]
        severity = sorted(severities, key=lambda s: severity_order.get(s, 0), reverse=True)[0]
    else:
        severity = "LOW"

    # Insert into SQLite
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (ip, source, timestamp, meta, is_malicious, severity, threats, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        event.ip,
        event.source,
        event_timestamp,
        json.dumps(event.meta or {}),
        1 if is_malicious else 0,
        severity,
        json.dumps(matching_threats),
        datetime.now().isoformat()
    ))
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()

    event_data = {
        "id": event_id,
        "ip": event.ip,
        "source": event.source,
        "timestamp": event_timestamp,
        "meta": event.meta or {},
        "is_malicious": is_malicious,
        "severity": severity,
        "threats": matching_threats,
        "created_at": datetime.now().isoformat()
    }

    return {
        "status": "success",
        "event_id": event_id,
        "message": "Event received with threat analysis",
        "event": event_data
    }

@app.get("/events")
async def get_events(limit: int = 50, source: str = None):
    """Get events from SQLite with optional filtering"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if source:
        cursor.execute('SELECT * FROM events WHERE source = ? ORDER BY id DESC LIMIT ?', (source, limit))
    else:
        cursor.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?', (limit,))

    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "ip": row[1],
            "source": row[2],
            "timestamp": row[3],
            "meta": json.loads(row[4]) if row[4] else {},
            "is_malicious": bool(row[5]),
            "severity": row[6],
            "threats": json.loads(row[7]) if row[7] else [],
            "created_at": row[8]
        })

    # Get total count
    conn = get_db_connection()
    cursor = conn.cursor()
    if source:
        cursor.execute('SELECT COUNT(*) FROM events')
        total_rows = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM events WHERE source = ?', (source,))
        filtered_rows = cursor.fetchone()[0]
    else:
        cursor.execute('SELECT COUNT(*) FROM events')
        total_rows = filtered_rows = cursor.fetchone()[0]
    conn.close()

    return {
        "total": total_rows,
        "filtered": filtered_rows,
        "limit": limit,
        "events": events
    }

@app.get("/events/stats")
async def get_events_stats():
    """Get events statistics from SQLite"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM events')
    total = cursor.fetchone()[0]

    cursor.execute('SELECT source, COUNT(*) FROM events GROUP BY source')
    by_source_raw = cursor.fetchall()
    conn.close()

    by_source = {row[0]: row[1] for row in by_source_raw}

    return {
        "total_events": total,
        "by_source": by_source,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/events/recent")
async def get_recent_events(limit: int = 50):
    """Get recent N events from SQLite (events already contain is_malicious, severity, threats)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?', (limit,))
    rows = cursor.fetchall()
    conn.close()

    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "ip": row[1],
            "source": row[2],
            "timestamp": row[3],
            "meta": json.loads(row[4]) if row[4] else {},
            "is_malicious": bool(row[5]),
            "severity": row[6],
            "threats": json.loads(row[7]) if row[7] else [],
            "created_at": row[8]
        })

    return {
        "total_events": len(events),  # Will match limit if enough events exist
        "limit": limit,
        "events": events,
        "timestamp": datetime.now().isoformat()
    }

def get_stats_data() -> Dict[str, Any]:
    """Calculate statistics"""
    total = len(THREAT_DATA)
    by_severity = {
        "CRITICAL": len([t for t in THREAT_DATA if t['severity'] == 'CRITICAL']),
        "HIGH": len([t for t in THREAT_DATA if t['severity'] == 'HIGH']),
        "MEDIUM": len([t for t in THREAT_DATA if t['severity'] == 'MEDIUM']),
        "LOW": len([t for t in THREAT_DATA if t['severity'] == 'LOW'])
    }
    by_type = {}
    for t in THREAT_DATA:
        t_type = t['type']
        by_type[t_type] = by_type.get(t_type, 0) + 1

    return {
        "total_threats": total,
        "by_severity": by_severity,
        "by_type": by_type,
        "updated_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
