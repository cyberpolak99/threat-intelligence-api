# 🔧 TROUBLESHOOTING — Threat Intelligence API

---

## **COMMON PROBLEMS**

---

## **PROBLEM 1: 404 Database Not Found**

### Symptom
```json
{
  "error": "Database not found"
}
```

### rozwiązania

**OPTION A: Check if database exists**
```bash
# Lokalnie
cd cyber_sheld/data
ls -la | grep cyber_shield.db

# Powinny widzieć:
# cyber_sheld.db
```

**OPTION B: Initialize database**
```bash
python -c "import sqlite3; sqlite3.connect('cyber_sheld/data/cyber_shield.db').execute('CREATE TABLE IF NOT EXISTS incident_reports (id INTEGER PRIMARY KEY, incident_id TEXT, severity TEXT, threat_type TEXT, source_ip TEXT, detected_at TEXT, status TEXT)').close()"
```

**OPTION C: Check permissions**
```bash
# Linux/Mac
chmod 644 cyber_sheld/data/cyber_shield.db

# Windows (Admin required)
# Prawoklik na file -> Properties -> Security -> Full Control
```

---

## **PROBLEM 2: Connection Refused / Cannot Connect**

### Symptom
```
ConnectionRefusedError: [WinError 10061] No connection could be made
```

### rozwiązania

**OPTION A: Check if API is running**
```bash
# Sprawdź process
ps aux | grep threat_api.py

# Windows
tasklist | findstr python
```

**OPTION B: Check port**
```bash
# Sprawdź czy port 10000 jest zajęty
netstat -an | grep 10000
```

**OPTION C: Restart API**
```bash
# Stop current (Ctrl+C)
# Restart
python threat_api.py
```

---

## **PROBLEM 3: Slow Response Time**

### Symptom
API response > 5 seconds

### rozwiązania

**OPTION A: Add timeout**
```python
import requests

response = requests.get("http://localhost:10000/api/threats?limit=10", timeout=5)
```

**OPTION B: Optimize queries**
W `threat_api.py`:
```python
# Use index
cursor.execute('CREATE INDEX IF NOT EXISTS idx_detected_at ON incident_reports(detected_at)')
```

**OPTION C: Add caching**
```python
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=100)
def get_cached_threats(limit=50):
    # Logic here...
```

---

## **PROBLEM 4: Rate Limiting (429 Too Many Requests)**

### Symptom
```json
{
  "error": "Rate limit exceeded"
}
```

### rozwiązania

**OPTION A: Upgrade tier**
Zobacz pricing page

**OPTION B: Implement retry**
```python
import time
import requests

def safe_request(url, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url)
        
        if response.status_code == 429:
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        
        return response
    
    return None
```

---

## **PROBLEM 5: Invalid JSON Response**

### Symptom
```python
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

### rozwiązania

**OPTION A: Check response content type**
```python
response = requests.get("http://localhost:10000/api/threats")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Raw: {response.text}")
```

**OPTION B: Validate response**
```python
def get_threats():
    response = requests.get("http://localhost:10000/api/threats?limit=10")
    
    if not response.ok:
        print(f"Error: HTTP {response.status_code}")
        return []
    
    try:
        return response.json()['data']
    except ValueError:
        print(f"Invalid JSON: {response.text}")
        return []
```

---

## **PROBLEM 6: CORS Error in Web Apps**

### Symptom
```
Access-Control-Allow-Origin: http://localhost:3000
```

### rozwiązania

**OPTION A: Enable CORS in Flask**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

**OPTION B: Restrict CORS**
```python
cors = CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
```

---

## **PROBLEM 7: API Key Not Working**

### Symptom
```json
{
  "error": "Invalid API key"
}
```

### rozwiązania

**OPTION A: Verify API key**
```bash
# Check if API key is correct
echo "YOUR_API_KEY" | tr -d '[:space:]'
```

**OPTION B: Regenerate API key**
W RapidAPI dashboard

**OPTION C: Add API key to headers**
```python
headers = {
    "X-RapidAPI-Key": "your_api_key"
}
response = requests.get("http://localhost:10000/api/threats", headers=headers)
```

---

## **PROBLEM 8: Database Lock Error**

### Symptom
```
sqlite3.OperationalError: database is locked
```

### rozwiązania

**OPTION A: Check for multiple processes**
```bash
ps aux | grep python | grep threat_api
```

**OPTION B: Use transaction mode**
```python
conn = sqlite3.connect('data/cyber_shield.db', timeout=30)  # 30 second timeout
```

**OPTION C: Implement connection pooling**
```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///data/cyber_shield.db', pool_size=5)
```

---

## **PROBLEM 9: Memory Leak**

### Symptom
Continuously increasing memory usage

### rozwiązania

**OPTION A: Add garbage collection**
```python
import gc

# After processing
gc.collect()
```

**OPTION B: Use generators**
```python
def stream_threats(limit=50):
    for threat in get_all_threats(limit):
        yield threat
        # Not store in memory all threats
```

---

## **PROBLEM 10: Production Deployment Fails**

### Symptom
Deploy na RapidAPI/Render fails

### rozwiązania

**OPTION A: Check requirements**
```bash
# Ensure all dependencies listed
pip freeze > requirements.txt
```

**OPTION B: Add start command**
```
Starting: gunicorn threat_api:app --bind 0.0.0.0:$PORT --workers 1
```

**OPTION C: Check environment variables**
```bash
# Ensure DB_PATH is set
export DB_PATH=/app/data/cyber_shield.db
```

---

## **DEBUGGING TIPS**

### **1. Enable debug mode:**
```python
app.run(debug=True)
```

### **2. Add logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### **3. Check logs:**
```bash
# Linux/Mac
tail -f /var/log/cyber_shield.log

# Windows (use Event Viewer)
```

### **4. Use Flask debugger:**
```python
@app.route('/debug')
def debug():
    import pdb; pdb.set_trace()  # Breakpoint
    return "Debug point"
```

---

## **WHERE TO GET HELP**

### **Official Channels:**
- GitHub Issues: https://github.com/cyberpolak99/threat-intelligence-api/issues
- Documentation: See README.md, API_REFERENCE.md

### **Community:**
- Reddit: r/APIg
- Stack Overflow: Tag: threat-intelligence-api

### **Debugging Tools:**
- curl: Test endpoints
- Postman: API testing
- Chrome DevTools: Network tab

---

**Troubleshooting Guide** | Version: 1.0 | Update: 2026-02-20

---
