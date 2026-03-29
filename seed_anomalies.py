import sqlite3
import os
import random
from datetime import datetime, timedelta

# Unified path resolution
DB_PATH = os.environ.get("DATABASE_URL", "data/cyber_shield.db")

ATTACKER_IPS = [
    "45.133.1.20", "185.220.101.5", "89.248.165.59", "193.32.162.87",
    "171.25.193.78", "162.247.74.27", "185.243.218.50", "45.155.205.233",
    "103.251.167.20", "37.120.247.199", "94.102.49.190", "212.70.149.150",
    "45.95.169.11", "80.82.77.139", "198.98.51.189",
]

# (Type, Desc, Severity, BaseScore, TypicalPort)
ATTACK_TYPES = [
    ("SSH_BRUTE_FORCE", "SSH brute force login attempt", "HIGH", 0.85, 22),
    ("PORT_SCAN",       "Aggressive port scan detected", "MEDIUM", 0.55, None),
    ("HONEYPOT_HIT",    "Honeypot interaction triggered", "HIGH", 0.90, 80),
    ("MALWARE_C2",      "Known malware C2 callback detected", "CRITICAL", 1.0, 443),
    ("WEB_EXPLOIT",     "Web application exploit attempt (SQLi/XSS)", "HIGH", 0.80, 80),
    ("CREDENTIAL_STUFF","Credential stuffing on login page", "HIGH", 0.75, 443),
    ("DNS_TUNNEL",      "DNS tunneling activity detected", "MEDIUM", 0.60, 53),
    ("SMB_SCAN",        "SMB/EternalBlue scan attempt", "CRITICAL", 0.95, 445),
    ("TELNET_BRUTE",    "Telnet brute force (IoT-style)", "MEDIUM", 0.65, 23),
    ("RDP_BRUTE_FORCE", "RDP brute force login attempt", "HIGH", 0.82, 3389),
]

DST_IPS = ["10.0.0.1", "10.0.0.5", "10.0.0.10", "192.168.1.100", "172.16.0.50"]
PROTOCOLS = ["TCP", "UDP", "TCP"]

def seed():
    print(f"Seeding database: {DB_PATH}")
    is_postgres = DB_PATH.startswith(("postgres://", "postgresql://"))
    
    if is_postgres:
        import psycopg2
        conn = psycopg2.connect(DB_PATH)
    else:
        # Resolve relative path for SQLite if needed
        full_path = DB_PATH
        if not os.path.isabs(full_path) and "data" in full_path:
             os.makedirs(os.path.dirname(full_path), exist_ok=True)
        conn = sqlite3.connect(full_path)
    
    cursor = conn.cursor()

    # Clear table before seeding if --force
    if "--force" in __import__("sys").argv:
        print("  Force flag set - clearing existing anomalies...")
        cursor.execute("DELETE FROM anomalies")
    else:
        try:
            cursor.execute("SELECT COUNT(*) FROM anomalies")
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"  DB already has {count} anomalies. Use --force to re-seed.")
                conn.close()
                return
        except Exception:
            pass

    now = datetime.now()
    records = []
    for ip in ATTACKER_IPS:
        num_events = random.randint(5, 15)
        for _ in range(num_events):
            attack = random.choice(ATTACK_TYPES)
            ts = now - timedelta(days=random.uniform(0, 10))
            score = max(0.0, min(1.0, attack[3] + random.uniform(-0.05, 0.05)))
            
            # Map port
            port = attack[4]
            if port is None:
                port = random.choice([21, 25, 110, 143, 3306, 5432, 8080])

            records.append((
                ts, ip, random.choice(DST_IPS), port,
                random.choice(PROTOCOLS), attack[0], attack[2],
                round(score, 4), random.randint(100, 50000), attack[1], 1
            ))

    query = """
        INSERT INTO anomalies 
        (timestamp, src_ip, dst_ip, dst_port, protocol, type, severity, score, bytes_transferred, description, label)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """ if is_postgres else """
        INSERT INTO anomalies 
        (timestamp, src_ip, dst_ip, dst_port, protocol, type, severity, score, bytes_transferred, description, label)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.executemany(query, records)
    conn.commit()
    conn.close()
    print(f"  ✅ Successfully seeded {len(records)} anomalies.")

if __name__ == "__main__":
    seed()
