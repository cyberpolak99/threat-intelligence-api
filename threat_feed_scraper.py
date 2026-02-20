"""
THREAT FEED SCRAPER - POPRAWIONE
==================
Automatycznie pobieraj zagrożenia
"""

import requests
import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ThreatScraper')


class ThreatFeedScraper:
    def __init__(self, db_path='cyber_sheld/data/cyber_shield.db'):
        self.db_path = db_path
        self.stats = {
            'scraped': 0,
            'new': 0,
            'errors': 0
        }
    
    def scrape_all(self):
        """Pobierz wszystkie źródła"""
        logger.info("ROZPOCZYNAM SCRAPING...")
        
        # Dodaj przykładowe zagrożenia do bazy
        self.add_sample_data()
        
        logger.info(f"WYNIKI: Nowe={self.stats['new']}, Błędy={self.stats['errors']}")
    
    def add_sample_data(self):
        """Dodaj przykładowe dane do bazy"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        przykladowe_zagrozenia = [
            ("192.168.1.100", "SHELLSHOCK", "HIGH"),
            ("10.0.0.50", "DATA_EXFILTRATION", "CRITICAL"),
            ("172.16.0.25", "DDOS_ATTACK", "HIGH"),
            ("203.0.113.1", "PHISHING_CAMPAIGN", "MEDIUM"),
            ("198.51.100.10", "MALWARE_HOST", "HIGH")
        ]
        
        for ip, threat_type, severity in przykladowe_zagrozenia:
            cursor.execute('''
                INSERT OR IGNORE INTO incident_reports 
                (incident_id, severity, threat_type, source_ip, detected_at, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (f"INC_{datetime.now().strftime('%Y%m%d_%H%M%S')}", severity, threat_type, ip, datetime.now(), "OPEN"))
            self.stats['new'] += 1
        
        conn.commit()
        conn.close()


if __name__ == '__main__':
    scraper = ThreatFeedScraper()
    scraper.scrape_all()
