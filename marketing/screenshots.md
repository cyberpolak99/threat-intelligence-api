# 📸 DEMO SCREENSHOTS — Threat Intelligence API

---

## **SCREENSHOT #1: HEALTH CHECK ENDPOINT**

### **DOSTAĆ:**
```bash
curl http://localhost:10000/api/health
```

### **WYGLĄD:**
```json
{
  "status": "healthy",
  "version": "1.0",
  "timestamp": "2026-02-20T21:05:21.542296",
  "db_exists": true
}
```

**SCREENSHOT TROCH:** Wizytualizacja JSON response w terminalu z zielony tekstem

---

## **SCREENSHOT #2: THREATS ENDPOINT**

### **DOSTAĆ:**
```bash
curl http://localhost:10000/api/threats?limit=10
```

### **WYGLĄD:**
```json
{
  "status": "success",
  "count": 10,
  "data": [
    {
      "id": 1,
      "incident_id": "INC_20260220_210238",
      "severity": "HIGH",
      "threat_type": "SHELLSHOCKexploit",
      "source_ip": "192.168.1.100",
      "detected_at": "2026-02-20 21:02:38",
      "status": "OPEN"
    },
    {
      "id": 2,
      "incident_id": "INC_20260220_210039",
      "severity": "CRITICAL",
      "threat_type": "DATA_EXFILTRATION",
      "source_ip": "10.0.0.50",
      "detected_at": "2026-02-20 21:00:39",
      "status": "OPEN"
    },
    {
      "id": 3,
      "incident_id": "INC_20260220_210140",
      "severity": "HIGH",
      "threat_type": "DDOS_ATTACK",
      "source_ip": "172.16.0.25",
      "detected_at": "2026-02-20 21:01:40",
      "status": "OPEN"
    },
    {
      "id": 4,
      "incident_id": "INC_20260220_210241",
      "severity": "MEDIUM",
      "threat_type": "PHISHING_CAMPAIGN",
      "source_ip": "203.0.113.1",
      "detected_at": "2026-02-20 21:02:41",
      "status": "OPEN"
    }
  ]
}
```

**SCREENSHOT TROCH:** Terminal z 4 threats display, each na własnej linijce

---

## **SCREENSHOT #3: STATS ENDPOINT**

### **DOSTAĆ:**
```bash
curl http://localhost:10000/api/threats/stats
```

### **WYGLĄD:**
```json
{
  "total_incidents": 4,
  "total_blocks": 0,
  "response_actions": 3
}
```

**SCREENSHOT TROCH:** Compact stats display

---

## **SCREENSHOT #4: PYTHON INTEGRATION**

### **DOSTAĆ:**
```python
import requests

response = requests.get("http://localhost:10000/api/threats?limit=10")
threats = response.json()

print(f"Found {threats['count']} threats")

for threat in threats['data']:
    severity = threat['severity']
    threat_type = threat['threat_type']
    ip = threat['source_ip']
    
    if severity == 'CRITICAL':
        print(f"🔴 CRITICAL: {threat_type} from {ip}")
    elif severity == 'HIGH':
        print(f"🟠 HIGH: {threat_type} from {ip}")
    else:
        print(f"🟡 {severity}: {threat_type} from {ip}")
```

### **WYGLĄD:**
Found 10 threats
🔴 CRITICAL: DATA_EXFILTRATION from 10.0.0.50
🟠 HIGH: SHELLSHOCKexploit from 192.168.1.100
🟠 HIGH: DDOS_ATTACK from 172.16.0.25
🟡 MEDIUM: PHISHING_CAMPAIGN from 203.0.113.1
...

**SCREENSHOT TROCH:** Python terminal output z color-coded severity

---

## **SCREENSHOT #5: WEB BROWSER API CALL**

### **DOSTAĆ:**
Browser wchodzi: `http://localhost:10000/api/threats?limit=5`

### **WYGLĄD (API Response):**
**Dokument JSON wyświetla w browser z kolorowe syntax highlighting**

**SCREENSHOT TROCH:** Browser with Firefox/Chrome DevTools panel showing endpoint response

---

## **SCREENSHOT #6: POSTMAN API TESTING**

### **DOSTAĆ:**
Postman application → GET Request: `http://localhost:10000/api/threats?limit=10`

### **WYGLĄD (Postman):**
- URL: `http://localhost:10000/api/threats?limit=10`
- Method: GET
- Headers:
  - Content-Type: application/json
- Response Body: JSON formatted
- Response Time: 120ms
- Response Status: 200 OK

**SCREENSHOT TROCH:** Postman interface z request/response

---

## **SCREENSHOT #7: CURL WITH ERROR CASE**

### **DOSTAĆ:**
```bash
curl http://localhost:10000/api/threats?limit=99999999
```

### **WYGLĄD:**
```json
{
  "status": "error",
  "error": "limit parameter exceeds maximum of 100"
}
```

**SCREENSHOT TROCH:** Handling invalid requests gracefully

---

## **SCREENSHOT #8: JAVASCRIPT FETCH**

### **DOSTAĆ:**
```javascript
fetch('http://localhost:10000/api/threats?limit=10')
  .then(res => res.json())
  .then(data => {
    console.log(`Found ${data.count} threats`);
    
    data.data.forEach(threat => {
      const icon = {
        'CRITICAL': '🔴',
        'HIGH': '🟠',
        'MEDIUM': '🟡',
        'LOW': '🟢'
      }[threat.severity] || '⚪';
      
      console.log(`${icon} ${threat.threat_type}: ${threat.source_ip}`);
    });
  });
```

### **WYGLĄD (Browser Console):**
Found 10 threats
🔴 DATA_EXFILTRATION: 10.0.0.50
🟠 SHELLSHOCKexploit: 192.168.1.100
🟠 DDOS_ATTACK: 172.16.0.25
🟡 PHISHING_CAMPAIGN: 203.0.113.1
...

**SCREENSHOT TROCH:** Chrome DevTools console output

---

## **SCREENSHOT #9: BULK EXPORT TO CSV**

### **DOSTAĆ:**
```python
import requests
import pandas as pd

response = requests.get("http://localhost:10000/api/threats?limit=100")
threats = response.json()['data']

df = pd.DataFrame(threats)
df.to_csv('threats.csv', index=False)
print(f"Exported {len(threats)} threats to CSV")
```

### **WYGLĄD:**
Exported 4 threats to CSV

**CSV FILE:**
id | incident_id | severity | threat_type | source_ip | detected_at | status
---|-------------|----------|-------------|-----------|-------------|--------
1  | INC_20260220_210238 | HIGH | SHELLSHOCKexploit | 192.168.1.100 | 2026-02-20 21:02:38 | OPEN
2  | INC_20260220_210039 | CRITICAL | DATA_EXFILTRATION | 10.0.0.50 | 2026-02-20 21:00:39 | OPEN
3  | INC_20260220_210140 | HIGH | DOSS_ATTACK | 172.16.0.25 | 2026-02-20 21:01:40 | OPEN
4  | INC_20260220_210241 | MEDIUM | PHISHING_CAMPAIGN | 203.0.113.1 | 2026-02-20 21:02:41 | OPEN

---

## **SCREENSHOT #10: REAL-TIME MONITORING DASHBOARD**

### **DOSTAĆ:**
Dashboard app uruchomiony → `http://localhost:8080`

### **WYGLĄD (Dashboard):**
- **Stats Panel:**
  - Total Incidents: 4
  - Active Threats: 4
  - Response Actions: 3

- **Threat Table:**
  - ID | Severity | Threat Type | Source IP | Time
  - 1 | HIGH | DOSS_ATTACK | 172.16.0.25 | 21:01:40
  - 2 | CRITICAL | DATA_EXFILTRATION | 10.0.0.50 | 21:00:39

- **Charts:**
  - Threat Distribution Pie Chart
  - Severity Bar Chart
  - Timeline Line Chart

**SCREENSHOT TROCH:** Dashboard with stats table + visual charts

---

## **SCREENSHOT #11: ERROR 404 DATABASE NOT FOUND**

### **DOSTAĆ:**
```bash
curl http://localhost:10000/api/threats
```

### **WYGLĄD:**
```json
{
  "error": "Database not found"
}
```

**SCREENSHOT TROCH:** Graceful error handling

---

## **SCREENSHOT #12: RATE LIMIT EXCEEDED**

### **DOSTAĆ:**
```bash
# After reaching request limit
curl -H "X-RateLimit-Remaining: 0" http://localhost:10000/api/threats
```

### **WYGLĄD:**
```json
{
  "status": "error",
  "error": "Rate limit exceeded. Please wait before making more requests."
}
```

**SCREENSHOT TROCH:** Rate limiting feedback

---

## **TWOJI SCREENSHOTS:**

### **INSTRUKCJE:**

1. **Otwórz terminal**
2. **Uruchom API:** `cd threat_intelligence_api && python threat_api.py`
3. **W drugim terminal,** wykonaj commands powyżej
4. **Zrób screenshot:** `Win + Shift + S` (Windows) lub `Cmd + Shift + 4` (Mac)
5. **Zapisz:** `screenshots/`

### **DO ZAPISANIA:**
```bash
# Stwórz folder
mkdir screenshots

# Zapisz jako:
screenshots/01_health_check.png
screenshots/02_threats_endpoint.png
screenshots/03_stats_endpoint.png
screenshots/04_python_integration.png
screenshots/05_browser_api.png
screenshots/06_postman.png
screenshots/07_error_case.png
screenshots/08_javascript_console.png
screenshots/09_csv_export.png
screenshots/10_dashboard.png
screenshots/11_error_404.png
screenshots/12_rate_limit.png
```

---

## **SCREENSHOT DO LANDING PAGE:**

**Add to index.html:** Add screenshot section with actual images

```html
<div class="screenshot-grid">
    <img src="screenshots/01_health_check.png" alt="Health Check">
    <img src="screenshots/02_threats_endpoint.png" alt="Threats Endpoint">
    <img src="screenshots/03_stats_endpoint.png" alt="Stats Endpoint">
    <img src="screenshots/04_python_integration.png" alt="Python Integration">
</div>
```

---

## **VIDEO TUTORIAL (2-MINUTE):**

### **SCRIPT:**
1. **Intro:** "Welcome to Threat Intelligence API"
2. **Demo 1:** Endpoint call (3 min)
3. **Demo 2:** Python integration (30 sec)
4. **Demo 3:** Real-time monitoring (30 sec)
5. **Outro:** "Try it now" + CTA

### **SUGGESTION:** Use OBS Studio + voice narration

---

*Screenshots Reference Guide* | Version: 1.0 | Update: 2026-02-21

---
