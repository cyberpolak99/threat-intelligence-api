"""
start_cyber_shield.py
=====================
Orchestrator dla Cyber Shield AI.
Uruchamia wszystkie moduły systemu jako procesy w tle:
  - Dashboard (Flask API + interfejs web)
  - Honeypot Sensor (nasłuch na portach)
  - Auto-Defend Manager (automatyczne blokowanie)
  - Cleanup Manager (wygaśanie blokad TTL)

Użycie:
  python start_cyber_shield.py          # uruchom wszystkie
  python start_cyber_shield.py --stop   # zatrzymaj wszystkie
  python start_cyber_shield.py --status # pokaż status
"""

import subprocess
import sys
import os
import time
import json
import signal
from pathlib import Path
from datetime import datetime

# ─── Konfiguracja modułów ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
PID_FILE = BASE_DIR / ".cyber_shield_pids.json"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

MODULES = [
    {
        "name": "Dashboard",
        "cmd": [sys.executable, "dashboard.py"],
        "log": "dashboard.log",
        "delay": 0,
    },
    {
        "name": "Honeypot Sensor",
        "cmd": [sys.executable, "honeypot_sensor.py"],
        "log": "honeypot_sensor.log",
        "delay": 2,
    },
    {
        "name": "Auto-Defend Manager",
        "cmd": [sys.executable, "autodefend_mgr.py"],
        "log": "autodefend.log",
        "delay": 3,
    },
    {
        "name": "Cleanup Manager",
        "cmd": [sys.executable, "cleanup_mgr.py"],
        "log": "cleanup.log",
        "delay": 4,
    },
]


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def start_all():
    pids = {}
    log("=" * 50)
    log("  CYBER SHIELD AI - START")
    log("=" * 50)

    for module in MODULES:
        time.sleep(module["delay"])
        log_path = LOG_DIR / module["log"]
        log_file = open(log_path, "a")

        try:
            proc = subprocess.Popen(
                module["cmd"],
                cwd=BASE_DIR,
                stdout=log_file,
                stderr=log_file,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
            )
            pids[module["name"]] = proc.pid
            log(f"[OK] {module['name']:25} PID={proc.pid:6}  log={module['log']}")
        except FileNotFoundError:
            log(f"[SKIP] {module['name']:22} - plik nie znaleziony: {module['cmd'][1]}")
        except Exception as e:
            log(f"[ERR] {module['name']:23} - {e}")

    # Zapisz PID-y do pliku
    with open(PID_FILE, "w") as f:
        json.dump(pids, f, indent=2)

    log("=" * 50)
    log(f"Uruchomiono {len(pids)} modułów. PID-y zapisane w {PID_FILE.name}")
    log("Dashboard:  http://localhost:5000")
    log("Zatrzymaj:  python start_cyber_shield.py --stop")
    log("=" * 50)


def stop_all():
    if not PID_FILE.exists():
        log("Brak pliku PIDów. Możliwe, że system nie jest uruchomiony.")
        return

    with open(PID_FILE) as f:
        pids = json.load(f)

    log("Zatrzymywanie Cyber Shield AI...")
    for name, pid in pids.items():
        try:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                               capture_output=True)
            else:
                os.kill(pid, signal.SIGTERM)
            log(f"[STOP] {name:25} PID={pid}")
        except (ProcessLookupError, PermissionError):
            log(f"[GONE] {name:25} PID={pid} (już nie działa)")
        except Exception as e:
            log(f"[ERR]  {name:25} - {e}")

    PID_FILE.unlink(missing_ok=True)
    log("System zatrzymany.")


def show_status():
    if not PID_FILE.exists():
        log("System nie jest uruchomiony (brak pliku PIDów).")
        return

    with open(PID_FILE) as f:
        pids = json.load(f)

    log("Status Cyber Shield AI:")
    for name, pid in pids.items():
        try:
            if sys.platform == "win32":
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {pid}"],
                    capture_output=True, text=True
                )
                running = str(pid) in result.stdout
            else:
                os.kill(pid, 0)  # Sygnał 0 = sprawdza czy proces żyje
                running = True
        except (ProcessLookupError, PermissionError):
            running = False

        status = "RUNNING" if running else "STOPPED"
        icon = "✅" if running else "❌"
        log(f"  {icon} {name:25} PID={pid:6}  [{status}]")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--stop" in args:
        stop_all()
    elif "--status" in args:
        show_status()
    else:
        start_all()
