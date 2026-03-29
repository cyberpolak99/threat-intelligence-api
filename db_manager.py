import sqlite3
import os
import re
from datetime import datetime, timedelta

# Try to import psycopg2 for Postgres support (optional but needed for Render/Docker)
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

class DBManager:
    def __init__(self, db_path="data/cyber_shield.db"):
        self.db_url = os.environ.get("DATABASE_URL", db_path)
        self.is_postgres = self.db_url.startswith(("postgres://", "postgresql://"))
        
        if not self.is_postgres:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.db_path = db_path
            self._init_sqlite()
        else:
            if not HAS_POSTGRES:
                raise ImportError("PostgreSQL URL provided but psycopg2 not installed.")
            self._init_postgres()

    def _get_conn(self):
        if self.is_postgres:
            conn = psycopg2.connect(self.db_url)
            # Use RealDictCursor to mimic sqlite3.Row behavior
            return conn
        else:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn

    def _init_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS anomalies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    src_ip TEXT,
                    dst_ip TEXT,
                    dst_port INTEGER,
                    protocol TEXT,
                    type TEXT,
                    severity TEXT,
                    score REAL,
                    bytes_transferred INTEGER,
                    description TEXT,
                    label INTEGER DEFAULT 0
                )
            ''')
            # Add dst_port column if it doesn't exist (migration)
            try:
                cursor.execute("ALTER TABLE anomalies ADD COLUMN dst_port INTEGER")
            except sqlite3.OperationalError:
                pass # Already exists

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT UNIQUE,
                    reason TEXT,
                    blocked_at DATETIME,
                    expires_at DATETIME,
                    status TEXT DEFAULT 'active'
                )
            ''')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_anomalies_timestamp ON anomalies(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_anomalies_src ON anomalies(src_ip)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_blocks_ip ON blocks(ip)')
            
            # WAL mode
            cursor.execute('PRAGMA journal_mode = WAL')
            cursor.execute('PRAGMA synchronous = NORMAL')
            conn.commit()

    def _init_postgres(self):
        # Convert Render's 'postgres://' to 'postgresql://' if needed (psycopg2 preference)
        if self.db_url.startswith("postgres://"):
             self.db_url = self.db_url.replace("postgres://", "postgresql://", 1)
            
        with psycopg2.connect(self.db_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS anomalies (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                        src_ip TEXT,
                        dst_ip TEXT,
                        dst_port INTEGER,
                        protocol TEXT,
                        type TEXT,
                        severity TEXT,
                        score FLOAT8,
                        bytes_transferred BIGINT,
                        description TEXT,
                        label INTEGER DEFAULT 0
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS blocks (
                        id SERIAL PRIMARY KEY,
                        ip TEXT UNIQUE,
                        reason TEXT,
                        blocked_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMPTZ,
                        status TEXT DEFAULT 'active'
                    )
                ''')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_anomalies_ts ON anomalies(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_anomalies_sip ON anomalies(src_ip)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_blocks_ip_pg ON blocks(ip)')
            conn.commit()

    def log_anomaly(self, src_ip, dst_ip, protocol, threat_type, severity, score, bytes_val, desc, label=0, dst_port=None):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                query = '''
                    INSERT INTO anomalies (timestamp, src_ip, dst_ip, dst_port, protocol, type, severity, score, bytes_transferred, description, label)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''' if self.is_postgres else '''
                    INSERT INTO anomalies (timestamp, src_ip, dst_ip, dst_port, protocol, type, severity, score, bytes_transferred, description, label)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (datetime.now(), src_ip, dst_ip, dst_port, protocol, threat_type, severity, score, bytes_val, desc, label)
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            print(f"[DB ERROR] Log anomaly: {e}")
            return False

    def get_stats(self):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM anomalies")
                total = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM blocks WHERE status='active'")
                active = cursor.fetchone()[0]
                return {"total_anomalies": total, "active_blocks": active}
        except Exception:
            return {"total_anomalies": 0, "active_blocks": 0}

    def get_anomalies(self, limit=50):
        try:
            with self._get_conn() as conn:
                if self.is_postgres:
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                else:
                    cursor = conn.cursor()
                
                query = "SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT %s" if self.is_postgres else "SELECT * FROM anomalies ORDER BY timestamp DESC LIMIT ?"
                cursor.execute(query, (limit,))
                return [dict(row) for row in cursor.fetchall()]
        except Exception:
            return []

    def get_custom_port_stats(self):
        """Aggregate data for port chart"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                query = """
                    SELECT 
                        CASE 
                            WHEN dst_port = 22   THEN 'SSH (22)'
                            WHEN dst_port = 23   THEN 'Telnet (23)'
                            WHEN dst_port = 80   THEN 'HTTP (80)'
                            WHEN dst_port = 443  THEN 'HTTPS (443)'
                            WHEN dst_port = 3389 THEN 'RDP (3389)'
                            WHEN dst_port = 445  THEN 'SMB (445)'
                            ELSE 'Other'
                        END AS port_label,
                        COUNT(*) AS count
                    FROM anomalies
                    WHERE dst_port IS NOT NULL
                    GROUP BY port_label
                    ORDER BY count DESC
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                return {
                    "labels": [row[0] for row in rows],
                    "values": [row[1] for row in rows]
                }
        except Exception:
            return {"labels": [], "values": []}

    def get_threat_timeline(self, days=7):
        """Threat counts per day for timeline visualization"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                if self.is_postgres:
                    query = """
                        SELECT date_trunc('day', timestamp) as day, COUNT(*) 
                        FROM anomalies 
                        WHERE timestamp >= CURRENT_DATE - INTERVAL '%s day'
                        GROUP BY day ORDER BY day ASC
                    """
                    cursor.execute(query % (days,))
                else:
                    query = """
                        SELECT strftime('%Y-%m-%d', timestamp) as day, COUNT(*) 
                        FROM anomalies 
                        WHERE timestamp >= date('now', '-%s day')
                        GROUP BY day ORDER BY day ASC
                    """
                    cursor.execute(query % (days,))
                rows = cursor.fetchall()
                return [{"date": str(row[0]).split()[0], "count": row[1]} for row in rows]
        except Exception:
            return []

    def get_anomalies_with_geo(self, limit=20, use_geo=False):
        """Get anomalies with optional geolocation information"""
        try:
            with self._get_conn() as conn:
                if self.is_postgres:
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                else:
                    cursor = conn.cursor()
                
                query = """
                    SELECT timestamp, src_ip, dst_ip, description as explanation, score as iso_score, label
                    FROM anomalies
                    ORDER BY timestamp DESC LIMIT %s
                """ if self.is_postgres else """
                    SELECT timestamp, src_ip, dst_ip, description as explanation, score as iso_score, label
                    FROM anomalies
                    ORDER BY timestamp DESC LIMIT ?
                """
                cursor.execute(query, (limit,))

                anomalies = []
                geo_db_enabled = False
                geo_reader = None

                if use_geo:
                    try:
                        import geoip2.database
                        db_path = os.path.join(os.path.dirname(self.db_path) if not self.is_postgres else "data", "GeoLite2-City.mmdb")
                        if os.path.exists(db_path):
                            geo_db_enabled = True
                            geo_reader = geoip2.database.Reader(db_path)
                    except Exception:
                        pass

                for row in cursor.fetchall():
                    anomaly = dict(row)
                    if geo_db_enabled and geo_reader and anomaly.get('src_ip'):
                        try:
                            response = geo_reader.city(anomaly['src_ip'])
                            anomaly['country_code'] = response.country.iso_code
                            anomaly['country_name'] = response.country.name
                            anomaly['city'] = response.city.name
                        except Exception:
                            anomaly['country_code'] = None
                            anomaly['country_name'] = 'Unknown'
                            anomaly['city'] = 'Unknown'
                    else:
                        anomaly['country_code'] = None
                        anomaly['country_name'] = 'Unknown'
                        anomaly['city'] = 'Unknown'
                    anomalies.append(anomaly)

                if geo_reader:
                    geo_reader.close()
                return anomalies
        except Exception as e:
            print(f"[DB ERROR] get_anomalies_with_geo: {e}")
            return []

    def add_block(self, ip, reason, duration_sec=86400):
        """Add IP block"""
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                query = "INSERT INTO blocks (ip, reason, blocked_at, status) VALUES (%s, %s, %s, 'active') ON CONFLICT(ip) DO UPDATE SET status='active', blocked_at=%s" if self.is_postgres else "INSERT OR REPLACE INTO blocks (ip, reason, blocked_at, status) VALUES (?, ?, ?, 'active')"
                now = datetime.now()
                params = (ip, reason, now, now) if self.is_postgres else (ip, reason, now)
                cursor.execute(query, params)
                conn.commit()
                return True
        except Exception:
            return False
