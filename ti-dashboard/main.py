from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import os

app = FastAPI(title="Threat Intelligence Dashboard", version="1.0")

# Templates
templates = Jinja2Templates(directory="templates")

# Event data model
class Event(BaseModel):
    ip: str = Field(..., description="IP address")
    source: str = Field(..., description="Source: nginx, fw, etc.")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp")
    meta: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")

# Events storage (in-memory)
events_store = []

# Threat Database (import from parent directory if needed, or inline)
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
    return templates.TemplateResponse("index.html", {"request": request, "stats": stats})

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
        "total": len(TREAT_DATA),
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
    """Create new event (ingest from nginx, fw, etc.)"""
    event_timestamp = event.timestamp if event.timestamp else datetime.now().isoformat()

    event_data = {
        "id": len(events_store) + 1,
        "ip": event.ip,
        "source": event.source,
        "timestamp": event_timestamp,
        "meta": event.meta or {},
        "created_at": datetime.now().isoformat()
    }

    events_store.append(event_data)

    return {
        "status": "success",
        "event_id": event_data["id"],
        "message": "Event received",
        "event": event_data
    }

@app.get("/events")
async def get_events(limit: int = 50, source: str = None):
    """Get events with optional filtering"""
    filtered_events = events_store

    if source:
        filtered_events = [e for e in events_store if e['source'] == source]

    return {
        "total": len(events_store),
        "filtered": len(filtered_events),
        "limit": limit,
        "events": filtered_events[:limit]
    }

@app.get("/events/stats")
async def get_events_stats():
    """Get events statistics"""
    total = len(events_store)

    by_source = {}
    for event in events_store:
        src = event['source']
        by_source[src] = by_source.get(src, 0) + 1

    return {
        "total_events": total,
        "by_source": by_source,
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
