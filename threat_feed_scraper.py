import requests
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), 'threats.db')
ABUSEIPDB_KEY = "TWOJ_API_KEY_TUTAJ"

def fetch_and_save():
    headers = {
        "Key": ABUSEIPDB_KEY,
        "Accept": "application/json"
    }
    params = {
        "confidenceMinimum": 50,
        "limit": 50
    }
    r = requests.get("https://api.abuseipdb.com/api/v2/blacklist", headers=headers, params=params)
    data = r.json()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incident_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT, threat_type TEXT, severity TEXT,
        source TEXT, detected_at TEXT, description TEXT)''')

    for item in data.get("data", []):
        cursor.execute('''INSERT INTO incident_reports 
            (ip_address, threat_type, severity, source, detected_at, description)
            VALUES (?,?,?,?,?,?)''', (
            item["ipAddress"], "blacklisted",
            "high" if item["abuseConfidenceScore"] > 80 else "medium",
            "AbuseIPDB", datetime.now().isoformat(),
            f"Abuse score: {item['abuseConfidenceScore']}%"
        ))
    conn.commit()
    conn.close()
    print(f"Zapisano {len(data.get('data',[]))} zagrożeń")

if __name__ == "__main__":
    fetch_and_save()
