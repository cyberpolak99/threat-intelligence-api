# 💡 EXAMPLES — Threat Intelligence API

---

## **EXAMPLE 1: BASIC INTEGRATION**

### **Python - Simple monitor**

```python
import requests
import time

def monitor_threats(interval_minutes=5):
    """Monitoruj threats i alert przy nowych"""
    
    last_count = 0
    
    while True:
        # Pobierz stats
        stats = requests.get("https://api.threatintelligence.com/api/threats/stats").json()
        current_count = stats['total_incidents']
        
        # Jeśli nowe threats
        if current_count > last_count:
            print(f"⚠️ NOWE THREATS DETECTED: {current_count - last_count}")
            
            # Pobierz nowe threats
            response = requests.get(f"https://api.threatintelligence.com/api/threats?limit={current_count - last_count + 10}")
            threats = response.json()['data']
            
            for threat in threats[:10]:
                severity_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(threat['severity'], "")
                print(f"{severity_icon} {threat['threat_type']}: {threat['source_ip']}")
        
        last_count = current_count
        time.sleep(interval_minutes * 60)

# Uruchom monitor
monitor_threats(interval_minutes=5)
```

---

## **EXAMPLE 2: INTEGRACJA Z FIREWALL**

### **Python - Auto-block critical/high threats**

```python
import requests
import subprocess

def get_critical_high_threats():
    """Pobierz CRITICAL i HIGH threats"""
    response = requests.get("https://api.threatintelligence.com/api/threats?limit=100")
    
    if response.status_code == 200:
        data = response.json()['data']
        return [t for t in data if t['severity'] in ['CRITICAL', 'HIGH']]
    return []

def block_ip(ip):
    """Zablokuj IP w iptables/Windows firewall"""
    try:
        # Linux (iptables)
        result = subprocess.run(
            f"sudo iptables -A INPUT -s {ip} -j DROP",
            shell=True,
            capture_output=True
        )
        
        if result.returncode == 0:
            print(f"✅ Zablokowano IP: {ip}")
            return True
    except:
        print(f"❌ Błąd blokowania IP: {ip}")
    
    return False

def auto_block_critical_threats():
    """Automatycznie blockuj CRITICAL/HIGH threats"""
    threats = get_critical_high_threats()
    
    print(f"Found {len(threats)} CRITICAL/HIGH threats")
    
    for threat in threats:
        ip = threat['source_ip']
        severity = threat['severity']
        threat_type = threat['threat_type']
        
        print(f"Blocking {severity} threat: {threat_type} ({ip})")
        block_ip(ip)
    
    print("Done blocking threats")

# Uruchom
auto_block_critical_threats()
```

---

## **EXAMPLE 3: EMAIL ALERTS**

### **Python - Wyslij emails przy nowych threats**

```python
import requests
import smtplib
from email.mime.text import MIMEText

def get_new_threats():
    """Pobierz ostatnie threats"""
    response = requests.get("https://api.threatintelligence.com/api/threats?limit=10")
    return response.json()['data'] if response.status_code == 200 else []

def send_email_alert(threats):
    """Wyslij email alert"""
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"
    recipient = "your_team@company.com"
    
    # Tresc
    body = "WYKRYTO NOWE ZAGROŻENIA:\n\n"
    for threat in threats:
        body += f"[{threat['severity']}] {threat['threat_type']}: {threat['source_ip']}\n"
    
    # Email
    msg = MIMEText(body)
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "⚠️ THREAT ALERT"
    
    # Wyslij
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    
    print("✅ Email alert wyslany")

# Uruchom
threats = get_new_threats()
if threats:
    send_email_alert(threats)
else:
    print("Brak nowych threats")
```

---

## **EXAMPLE 4: WEB DASHBOARD**

### **Flask - Web dashboard monitoringu threats**

```python
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Pobierz threats
    response = requests.get("https://api.threatintelligence.com/api/threats?limit=50")
    threats = response.json()['data'] if response.status_code == 200 else []
    
    # Pobierz stats
    stats = requests.get("https://api.threatintelligence.com/api/threats/stats").json()
    
    # Render template
    return render_template('dashboard.html', threats=threats, stats=stats)

@app.route('/stats')
def stats():
    # Stats API endpoint
    return requests.get("https://api.threatintelligence.com/api/threats/stats").json()

if __name__ == '__main__':
    app.run(port=8080, debug=True)
```

---

## **EXAMPLE 5: REAL-TIME MONITORING WITH WEBSOCKET**

### **JavaScript - WebSocket alert system**

```javascript
// clientside.js
const socket = new WebSocket('wss://your-server.com/ws');

socket.onmessage = function(event) {
    const threat = JSON.parse(event.data);
    
    // Pokaz alert
    const severityColors = {
        'CRITICAL': '#ff0000',
        'HIGH': '#ff9900',
        'MEDIUM': '#ffcc00',
        'LOW': '#00cc00'
    };
    
    const alertDiv = document.createElement('div');
    alertDiv.style.backgroundColor = severityColors[threat.severity];
    alertDiv.style.color = 'white';
    alertDiv.style.padding = '10px';
    alertDiv.style.margin = '5px';
    alertDiv.textContent = `[${threat.severity}] ${threat.threat_type}: ${threat.source_ip}`;
    
    document.getElementById('alerts').prepend(alertDiv);
};

// Pobieraj threats co 5 sekund
setInterval(() => {
    fetch('http://localhost:10000/api/threats?limit=5')
        .then(res => res.json())
        .then(data => console.log('Threats:', data));
}, 5000);
```

---

## **EXAMPLE 6: BATCH PROCESSING**

### **Python - Batch processing threats**

```python
import requests
import pandas as pd
from datetime import datetime

def export_threats_to_csv():
    """Export threats to CSV file"""
    response = requests.get("https://api.threatintelligence.com/api/threats?limit=100")
    
    if response.status_code == 200:
        threats = response.json()['data']
        df = pd.DataFrame(threats)
        
        # Dodaj columny
        df['export_time'] = datetime.now().isoformat()
        
        # Save to CSV
        filename = f"threats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ Exported {len(threats)} threats to {filename}")
    else:
        print("❌ Error exporting threats")

export_threats_to_csv()
```

---

## **EXAMPLE 7: CUSTOM FILTER**

### **Python - Filter threats by severity**

```python
import requests

def get_threats_by_category(severity, limit=50):
    """Pobierz threats po severity"""
    all_threats = requests.get(f"https://api.threatintelligence.com/api/threats?limit={limit}").json()['data']
    return [t for t in all_threats if t['severity'] == severity]

# Filter only CRITICAL
critical_threats = get_threats_by_category('CRITICAL', limit=100)

print(f"CRITICAL threats: {len(critical_threats)}")
for threat in critical_threats:
    print(f" - {threat['threat_type']}: {threat['source_ip']}")
```

---

## **EXAMPLE 8: CORRELATION ANALYSIS**

### **Python - Correlate threats (po IP)**

```python
import requests
from collections import Counter

def analyze_ip_correlation(limit=100):
    """Analiza correlation threats po IP"""
    threats = requests.get(f"https://api.threatintelligence.com/api/threats?limit={limit}").json()['data']
    
    # Zlicz threat types per IP
    ip_threats = {}
    for threat in threats:
        ip = threat['source_ip']
        threat_type = threat['threat_type']
        
        if ip not in ip_threats:
            ip_threats[ip] = []
        ip_threats[ip].append(threat_type)
    
    # Znajdz IPs z wieloma threat types
    multi_threat_ips = {ip: types for ip, types in ip_threats.items() if len(types) > 1}
    
    print(f"ZNALEZIONO {len(multi_threat_ips)} IPs z wieloma threat types")
    
    for ip, types in multi_threat_ips.items():
        print(f"  - {ip}: {len(types)} threat types")
    
    return multi_threat_ips

# Uruchom
multi_threat_ips = analyze_ip_correlation(limit=200)
```

---

## **EXAMPLE 9: SCHEDULED JOBS**

### **Python - Scheduled monitoring**

```python
import requests
import schedule
import time

def check_threats():
    """Scheduled check job"""
    print(f"🔍 Checking threats at {datetime.now()}...")
    
    stats = requests.get("https://api.threatintelligence.com/api/threats/stats").json()
    print(f"Total incidents: {stats['total_incidents']}")
    print(f"Total blocks: {stats['total_blocks']}")
    print(f"Response actions: {stats['response_actions']}")

# Schedule jobs
schedule.every(5).minutes.do(check_threats)  # Co 5 minut
schedule.every().hour.do(check_threats)      # Co godzinę
schedule.every().day.at("08:00").do(check_threats)  # Codziennie 8:00

# Uruchom scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## **EXAMPLE 10: INTEGRACJA Z SECURITY TOOLS**

### **Python - Integrate z Security Ops Center**

```python
import requests

def create_security_incident(threat):
    """Integrate z Security Ops Center (SOC)"""
    
    # Mock SOC API
    soc_url = "https://your-soc-platform.com/api/incidents"
    
    incident_data = {
        "title": f"Threat: {threat['threat_type']}",
        "severity": threat['severity'],
        "source": threat['source_ip'],
        "description": f"Threat detected: {threat['threat_type']}",
        "priority": "HIGH" if threat['severity'] in ['CRITICAL', 'HIGH'] else "LOW"
    }
    
    response = requests.post(soc_url, json=incident_data)
    
    if response.status_code == 201:
        print(f"✅ Incident created: {response.json()['incident_id']}")
    else:
        print(f"❌ Error creating incident")

# Dla każde CRITICAL/HIGH threat
for threat in get_critical_high_threats():
    create_security_incident(threat)
```

---

## **EXAMPLE 11: METRICS & ANALYTICS**

### **Python - Generate threat metrics**

```python
import requests
import pandas as pd
from datetime import datetime

def generate_threat_metrics():
    """Generuj metrics raport"""
    threats = requests.get("https://api.threatintelligence.com/api/threats?limit=100").json()['data']
    
    df = pd.DataFrame(threats)
    
    # Metrics
    metrics = {
        'total_count': len(df),
        'severity_distribution': df['severity'].value_counts().to_dict(),
        'threat_type_distribution': df['threat_type'].value_counts().to_dict(),
        'most_common_source': df['source_ip'].value_counts().head(5).to_dict(),
        'new_threats_last_hour': len(df[pd.to_datetime(df['detected_at']) > (datetime.now() - timedelta(hours=1))])
    }
    
    print("📊 THREAT METRICS:")
    print(f"Total threats: {metrics['total_count']}")
    print(f"Severity distribution: {metrics['severity_distribution']}")
    print(f"Threat types: {metrics['threat_type_distribution']}")
    print(f"Top sources: {metrics['most_common_source']}")
    
    return metrics

generate_threat_metrics()
```

---

## **EXAMPLE 12: AUTOMATED TESTING**

### **Python - Test API endpoints**

```python
import requests
import json

def test_api():
    """Test Threat Intelligence API"""
    
    base_url = "http://localhost:10000"
    
    tests = [
        ("health", f"{base_url}/api/health"),
        ("threats", f"{base_url}/api/threats?limit=10"),
        ("stats", f"{base_url}/api/threats/stats")
    ]
    
    print("🧪 Testing API endpoints...")
    
    for test_name, url in tests:
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {test_name}: OK (status: {response.status_code})")
            else:
                print(f"❌ {test_name}: FAILED (status: {response.status_code})")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("Testing complete")

# Uruchom test
test_api()
```

---

**Examples:** 12 real-world use cases  
**Wersja:** 1.0  
**Update:** 2026-02-20

---
