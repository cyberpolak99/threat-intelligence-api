# Threat Intelligence API

[![RapidAPI](https://img.shields.io/badge/RapidAPI-Threat%20Intelligence%20API-blue)](https://rapidapi.com/darro2323/api/threat-intelligence-api1)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7)](https://render.com)

Real-time IP & Domain threat intelligence powered by a **live 24/7 honeypot network**.

## Live Stats (March 2026)

| Metric | Value |
|---|---|
| Total attacks detected | 211,356 |
| IPs blocked automatically | 3,697 |
| New blocks today | 330+ |
| Honeypot ports | SSH/22, RDP/3389, HTTP/80, SMB/445, Telnet/23 |

## What is this?

Cyber Shield AI is a honeypot + auto-defend system running 24/7. It detects, scores, and blocks malicious IPs automatically. This API exposes the threat intelligence data publicly.

**How it works:**
1. Honeypot sensors listen on common attack ports
2. Every connection is logged with IP, port, timestamp
3. IPs are scored 0.0-1.0 (ti_score)
4. High-risk IPs are auto-blocked via Windows Firewall
5. Blocks expire after 24h TTL
6. This API serves the intelligence data in real time

## API Endpoints

### Check IP or Domain Reputation
```
GET /api/check/{ip_or_domain}
```

**Response:**
```json
{
  "ip": "45.133.1.20",
  "is_malicious": true,
  "ti_score": 0.95,
  "risk_level": "critical",
  "sources": "Brute Force;cybershield-honeypot",
  "seen_in_honeypot": 1,
  "honeypot_details": {}
}
```

### Quick Start (Python)
```python
import requests

url = "https://threat-intelligence-api-1.onrender.com/api/check/45.133.1.20"
headers = {"X-API-Key": "YOUR_API_KEY"}

response = requests.get(url, headers=headers)
print(response.json())
```

### Quick Start (curl)
```bash
curl -H "X-API-Key: YOUR_KEY" \
  https://threat-intelligence-api-1.onrender.com/api/check/suspicious-domain.com
```

### Port Traffic Distribution (Pie Chart Data)
```
GET /api/threats/port-stats?limit=10
```
Returns top attacked ports with counts and percentages — ready for pie chart rendering.

**Response:**
```json
{
  "status": "success",
  "total_hits": 8432,
  "count": 10,
  "data": [
    {"port": 22, "count": 3120, "percentage": 37.0, "label": "SSH"},
    {"port": 3389, "count": 1850, "percentage": 21.94, "label": "RDP"},
    {"port": 445, "count": 980, "percentage": 11.62, "label": "SMB"}
  ]
}
```


## Pricing (via RapidAPI)

| Plan | Price | Rate Limit |
|---|---|---|
| Basic | Free | 50 req/hour |
| PRO | $9.99/month | 500 req/hour |
| ULTRA | $49.99/month | 10,000 req/hour |

**[Get API Key on RapidAPI](https://rapidapi.com/darro2323/api/threat-intelligence-api1)**

## Tech Stack

- **Backend:** Python, Flask, SQLite
- **Deployment:** Render (auto-deploy from GitHub)
- **Honeypot:** Custom multi-port sensor (Windows)
- **Auto-defense:** netsh Windows Firewall rules
- **API Distribution:** RapidAPI

## Architecture

```
[Honeypot Sensor] --> [SQLite DB] --> [Flask API] --> [RapidAPI] --> [Users]
       |                  |
[Auto-Defend Mgr]  [Cleanup Mgr]
(auto-block)       (TTL expiry)
```

## Web Dashboard

A built-in data visualization dashboard is now available directly at the root (`/`) endpoint of the API.
It features real-time threat counts, blocked IPs, and interactive charts (Port Distribution and Threat Severity) built with Chart.js using a responsive Glassmorphism design.

## Self-Hosting

```bash
git clone https://github.com/cyberpolak99/threat-intelligence-api
cd threat-intelligence-api
pip install -r requirements.txt
python threat_api.py
```

## License

MIT


---
*Last technical update: Added real-time HTML/Chart.js Dashboard and fixed internal routing for RapidAPI stability.*
