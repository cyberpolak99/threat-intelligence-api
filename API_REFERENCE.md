# 📋 API REFERENCE — Threat Intelligence API

---

## BASE URL
```
https://api.threatintelligence.com  (zmien po deployu na RapidAPI)
```

---

## ENDPOINT #1: GET /api/threats

**Cel:** Pobierz listę zagrożeń cybernetycznych

### ✅ Request Parameters

| Parameter | Type | Required | Default | Max | Opis |
|-----------|------|----------|---------|-----|------|
| limit | integer | Nie | 50 | 100 | Ile threatów zwrócić |

### ✅ Request Examples

```bash
# Default (50)
curl "https://api.threatintelligence.com/api/threats"

# Custom limit
curl "https://api.threatintelligence.com/api/threats?limit=10"

# Maximum limit
curl "https://api.threatintelligence.com/api/threats?limit=100"
```

### ✅ Response (200 OK)

```json
{
  "status": "success",
  "count": 50,
  "data": [
    {
      "id": 1,
      "incident_id": "INC_20260220_210238",
      "severity": "HIGH",
      "threat_type": "SHELLSHOCK",
      "source_ip": "192.168.1.100",
      "detected_at": "2026-02-20 21:02:38.221332",
      "status": "OPEN",
      "response_actions": ""
    },
    {
      "id": 2,
      "incident_id": "INC_20260220_210039",
      "severity": "CRITICAL",
      "threat_type": "DATA_EXFILTRATION",
      "source_ip": "10.0.0.50",
      "detected_at": "2026-02-20 21:00:39.123456",
      "status": "OPEN",
      "response_actions": ""
    },
    {
      "id": 3,
      "incident_id": "INC_20260220_210140",
      "severity": "HIGH",
      "threat_type": "DDOS_ATTACK",
      "source_ip": "172.16.0.25",
      "detected_at": "2026-02-20 21:01:40.456789",
      "status": "OPEN",
      "response_actions": ""
    },
    {
      "id": 4,
      "incident_id": "INC_20260220_210241",
      "severity": "MEDIUM",
      "threat_type": "PHISHING_CAMPAIGN",
      "source_ip": "203.0.113.1",
      "detected_at": "2026-02-20 21:02:41.789012",
      "status": "OPEN",
      "response_actions": ""
    }
  ]
}
```

### ❌ Error Responses

**404 Database Not Found**
```json
{
  "error": "Database not found"
}
```

**500 Server Error**
```json
{
  "error": "Internal server error details..."
}
```

---

## ENDPOINT #2: GET /api/threats/stats

**Cel:** Pobierz statystyki bazy danych zagrożeń

### ✅ Request Parameters
None

### ✅ Request Example
```bash
curl "https://api.threatintelligence.com/api/threats/stats"
```

### ✅ Response (200 OK)
```json
{
  "total_incidents": 4,
  "total_blocks": 0,
  "response_actions": 3
}
```

### ❌ Error Responses

**404 Database Not Found**
```json
{
  "error": "Database not found"
}
```

---

## ENDPOINT #3: GET /api/health

**Cel:** Health check endpoint

### ✅ Request Parameters
None

### ✅ Request Example
```bash
curl "https://api.threatintelligence.com/api/health"
```

### ✅ Response (200 OK)
```json
{
  "status": "healthy",
  "version": "1.0",
  "timestamp": "2026-02-20T21:05:21.542296",
  "db_path": "/app/cyber_sheld/data/cyber_shield.db",
  "db_exists": true
}
```

### ❌ Error Responses

**503 Service Unavailable (jeśli API w maintenance)**
```json
{
  "status": "maintenance",
  "message": "API is currently under maintenance"
}
```

---

## 📊 DATA MODEL

### Incident Object
```json
{
  "id": integer,
  "incident_id": string,
  "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "threat_type": string,
  "source_ip": string,
  "detected_at": string (ISO 8601 datetime),
  "status": "OPEN" | "IN_PROGRESS" | "RESOLVED",
  "response_actions": string (JSON-serialized if needed)
}
```

### Severity Levels

| Level | Opis |
|-------|------|
| CRITICAL | Bezpośrednie zagrożenie — podejrzywane do natychmiastowej reakcji |
| HIGH | Zagrożenie wysokiego priorytetu |
| MEDIUM | Znane zagrożenie, monitorowane |
| LOW | Niskie zagrożenie, może być ignorowane |

### Threat Types (przykłady)

- MALWARE_HOST
- PHISHING_CAMPAIGN
- DDOS_ATTACK
- DATA_EXFILTRATION
- SHELLSHOCKexploit
- UNKNOWN
- C2_SERVER
- VULNERABILITY_SCAN

---

## 🔎 Filters (W przyszłości)

Planowane filtry:
- `?severity=HIGH` — tylko high severity
- `?type=MALWARE` — tylko malware threats
- `?date_range=2024-01-01_2024-12-31` — range dat
- `?ip=1.2.3.4` — search po IP
- `?country=pl` — po kraju (jeśli geolokacja dodana)

---

## 📊 Rate Limiting

Jakie planowane:
- Tier Free: 10 request/dzień
- Tier Basic: 1000 request/miesiąc
- Tier Pro: 10000 request/miesiąc

W headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1645459200
```

---

## 🔐 Authentication (w przyszłości)

API keys required dla premium tierów

Header:
```
X-API-Key: your_api_key_here
```

---

**Wersja:** 1.0  
**Ostatnia aktualizacja:** 2026-02-20

---
