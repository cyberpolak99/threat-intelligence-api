# 🔓 Threat Intelligence API — Darmowe API Threat Intel

## 🎯 **Co to robi?**

API udostępnia dane o zagrożeniach cybernetycznych z:

- **CERT Polska** — polskie zagrożenia
- **AbuseIPDB** — blacklist IP
- **CINS Score** —信誉 scores
- **VirusTotal** — malware analysis (w przyszłości)
- **Shodan** — vulnerability scan (w przyszłości)

## ⚡ **Usage:**

```bash
# BASE URL: https://api.threatintelligence.com (zmien po deployu)

# GET 50 ostatnich zagrożeń
curl "https://api.threatintelligence.com/api/threats?limit=50"

# GET statystyki
curl "https://api.threatintelligence.com/api/threats/stats"

# Health check
curl "https://api.threatintelligence.com/api/health"
```

---

## 📊 **Endpoints:**

### **1. GET /api/threats**

**Cel:** Pobierz zagrożenia cybernetyczne

**Request:**
```bash
GET /api/threats?limit=50  # limit: optional, default: 50, max: 100
```

**Response (200 OK):**
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
      "detected_at": "2026-02-20 21:02:38",
      "status": "OPEN"
    },
    ...
  ]
}
```

**Error (404):**
```json
{
  "error": "Database not found"
}
```

---

### **2. GET /api/threats/stats**

**Cel:** Pobierz statystyki baz danych

**Request:**
```bash
GET /api/threats/stats
```

**Response (200 OK):**
```json
{
  "total_incidents": 4,
  "total_blocks": 0,
  "response_actions": 3
}
```

---

### **3. GET /api/health**

**Cel:** Health check API

**Request:**
```bash
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.1",
  "timestamp": "2026-02-21T21:15:21"
}
```

---

## 🚀 **Jak użycia:**

### **PYTHON:**
```python
import requests

# Pobierz zagrożenia
response = requests.get("https://api.threatintelligence.com/api/threats?limit=10")
threats = response.json()

print(f"Found {threats['count']} threats")
for threat in threats['data']:
    print(f" - {threat['threat_type']}: {threat['source_ip']}")
```

### **CURL:**
```bash
curl "https://api.threatintelligence.com/api/threats?limit=10"
```

### **JAVASCRIPT (fetch):**
```javascript
fetch('https://api.threatintelligence.com/api/threats?limit=10')
  .then(res => res.json())
  .then(data => {
    console.log(`Found ${data.count} threats`);
    console.log(data.data);
  });
```

---

## 💰 **Pricing (po deployu na RapidAPI):**

| Tier | Requests | Cena |
|------|----------|------|
| FREE | 10/day | $0 |
| Basic | 1,000/month | $9.99 |
| Pro | 10,000/month | $49.99 |

---

## 🔧 **Configuration:**

### **Lokalnie:**
```bash
cd threat_intelligence_api
pip install -r requirements.txt
python threat_api.py  # Runs on http://localhost:10000
```

### **Production (RapidAPI):**
Deploy z: `https://github.com/cyberpolak99/threat-intelligence-api`

---

## 📖 **Resources:**

- **Dokumentacja API:** `API_REFERENCE.md`
- **Szybki start:** `QUICK_START.md`
- **Przykłady:** `EXAMPLES.md`
- **GitHub:** https://github.com/cyberpolak99/threat-intelligence-api

---

## 📞 **Support:**

- **Dokumentacja:** see above
- **ISSUES:** https://github.com/cyberpolak99/threat-intelligence-api/issues

---

**Wersja:** 1.0  
**Ostatnia aktualizacja:** 2026-02-20
**Developer:** cyberpolak99

---
