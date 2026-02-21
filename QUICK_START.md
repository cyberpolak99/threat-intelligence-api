# 🚀 QUICK START — Threat Intelligence API

---

## **STEP 1: UZYSKAC DOSTĘP**

### **OPTION A: LOKALNIE (Python)**

```bash
# 1. Przejdź do folderu
cd threat_intelligence_api

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Uruchom API
python threat_api.py

# 4. Otwórz w przeglądarce
# http://localhost:10000/api/threats
```

### **OPTION B: PRODUCTION (RapidAPI)**

1. Otwórz: https://rapidapi.com/
2. Szukaj "Threat Intelligence API"
3. Zarejestrój, pobierz API key
4. Zaimplementuj client z API key

---

## **STEP 2: ZAINTERPRETUJ DANE**

### **BASIC REQUEST**

```bash
# Pobierz 10 ostatnich threatów
curl "https://api.threatintelligence.com/api/threats?limit=10"
```

### **JAK ZROBIĆ W PYTHON:**

```python
import requests

# Pobierz threatów
response = requests.get("https://api.threatintelligence.com/api/threats?limit=10")

# Sprawdź odpowiedź
if response.status_code == 200:
    data = response.json()
    threats = data['data']
    
    print(f"Found {data['count']} threats")
    
    # Iteruj przez threats
    for threat in threats:
        print(f" - {threat['threat_type']}: {threat['source_ip']} ({threat['severity']})")
else:
    print(f"Error: {response.status_code}")
```

---

## **STEP 3: INTEGUJ Z APLIKACJĄ**

### **W DZIEŁALNOŚCI (monitoring):**

```python
def check_threats():
    response = requests.get("https://api.threatintelligence.com/api/threats?limit=10")
    
    if response.status_code == 200:
        threats = response.json()['data']
        
        for threat in threats:
            if threat['severity'] == 'CRITICAL':
                # Wyslij alert
                send_sms_alert(f"CRITICAL: {threat['threat_type']} from {threat['source_ip']}")
            elif threat['severity'] == 'HIGH':
                # Wyslij email
                send_email_alert(f"HIGH threat: {threat['threat_type']}")
```

### **W BLOCKLIST SYSTEM:**

```python
def update_blocklist():
    response = requests.get("https://api.threatintelligence.com/api/threats?limit=100")
    
    if response.status_code == 200:
        threats = response.json()['data']
        
        for threat in threats:
            if threat['severity'] in ['CRITICAL', 'HIGH']:
                # Dodaj do blocklist
                add_ip_to_blocklist(threat['source_ip'])
                update_firewall(threat['source_ip'])
```

---

## **STEP 4: MONITOROWANIE W CZASIE RZECZYWISTYM**

### **SCRIPT (auto-check):**

```python
import time
import requests

while True:
    # Pobierz stats
    stats = requests.get("https://api.threatintelligence.com/api/threats/stats").json()
    
    # Jeśli nowe threats
    if stats['total_incidents'] > LAST_KNOWN_INCIDENTS:
        # Pobierz nowe threats
        response = requests.get("https://api.threatintelligence.com/api/threats?limit=5")
        threats = response.json()['data']
        
        for threat in threats:
            print(f"[{threat['severity']}] {threat['threat_type']}: {threat['source_ip']}")
    
    # Czekaj 5 minut
    time.sleep(300)
```

---

## **STEP 5: DODAJ ERROR HANDLING**

```python
import requests
from requests.exceptions import RequestException

def get_threats(limit=50):
    try:
        response = requests.get(f"https://api.threatintelligence.com/api/threats?limit={limit}")
        response.raise_for_status()  # Raise 4XX/5XX errors
        return response.json()['data']
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except ValueError:
        print(f"Invalid JSON response")
    
    return []
```

---

## **STEP 6: UŻYJ W RÓŻNYCH PLATFORMACH**

### **NODE.JS:**

```javascript
const fetch = require('node-fetch');

async function getThreats() {
    const response = await fetch('https://api.threatintelligence.com/api/threats?limit=10');
    const data = await response.json();
    
    console.log(`Found ${data.count} threats`);
    console.log(data.data);
}

getThreats();
```

### **GO:**

```go
package main

import "encoding/json"
import "net/http"

type ThreatResponse struct {
    Status string  `json:"status"`
    Data   Threats `json:"data"`
}

func main() {
    resp, err := http.Get("https://api.threatintelligence.com/api/threats?limit=10")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    
    var data ThreatResponse
    json.NewDecoder(resp.Body).Decode(&data)
    
    fmt.Printf("Found %d threats\n", len(data.Data))
}
```

---

## **TROUBLESHOOTING**

### **Błąd: 404 Database Not Found**
- API jest w maintenance — spróbuj za godzinę

### **Błąd: Rate Limit Exceeded**
- Sprawdź tier upgrade

### **Błąd: Invalid JSON**
- Sprawdź API version — może to było v2

### **Kopiowanie local:**
- Pamiętaj o zmianie BASE URL z localhost:10000 na production URL

---

## **NEXT STEPS**

1. ✅ Pobierz pierwsze threatów
2. ✅ Implementuj w aplikacji
3. ✅ Rozwijaj do real-time monitoring
4. ✅ Rozważ upgrade to Basic/Pro tier dla większego limitu

---

**Wersja:** 1.0  
**Quick Start Guide** | Update: 2026-02-20

---
