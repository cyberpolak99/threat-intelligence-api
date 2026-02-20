from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.getcwd(), 'threats.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS incident_reports (id INTEGER PRIMARY KEY AUTOINCREMENT, ip_address TEXT, threat_type TEXT, severity TEXT, source TEXT, detected_at TEXT, description TEXT)')
    conn.commit()
    conn.close()

def run_scraper():
    try:
        from threat_feed_scraper import fetch_and_save
        fetch_and_save()
    except Exception as e:
        print(f"Scraper error: {e}")

init_db()
run_scraper()
