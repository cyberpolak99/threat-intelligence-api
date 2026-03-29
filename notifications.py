"""
notifications.py
================
System powiadomień dla Cyber Shield AI.

Obsługuje:
  - Windows Toast (win10toast / plyer) dla zdarzeń CRITICAL
  - Fallback: zapis do pliku alerts.log jeśli toast niedostępny
  - Webhook opcjonalny (Discord / Slack)

Integracja z autodefend_mgr.py:
  from notifications import notify_critical, notify_block
"""

import os
import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
ALERT_LOG = LOG_DIR / "alerts.log"

# Opcjonalny webhook Discord/Slack (ustaw w zmiennej środowiskowej)
WEBHOOK_URL = os.environ.get("CYBER_SHIELD_WEBHOOK_URL", "")

logger = logging.getLogger("CyberShieldNotify")


def _toast(title: str, message: str, icon: str = "warning") -> bool:
    """Próbuje wysłać Windows Toast. Zwraca True jeśli się udało."""
    # Metoda 1: win10toast
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            title,
            message,
            duration=8,
            threaded=True,
        )
        return True
    except ImportError:
        pass
    except Exception as e:
        logger.debug(f"win10toast failed: {e}")

    # Metoda 2: plyer
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Cyber Shield AI",
            timeout=8,
        )
        return True
    except ImportError:
        pass
    except Exception as e:
        logger.debug(f"plyer failed: {e}")

    return False


def _write_alert_log(level: str, title: str, message: str):
    """Zapisuje alert do pliku logs/alerts.log"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {title} | {message}\n"
    with open(ALERT_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def _send_webhook(title: str, message: str, color: int = 0xFF0000):
    """Wysyła powiadomienie na Discord/Slack webhook jeśli skonfigurowany."""
    if not WEBHOOK_URL:
        return
    try:
        import urllib.request
        import json
        # Discord format
        payload = json.dumps({
            "embeds": [{
                "title": title,
                "description": message,
                "color": color,
                "footer": {"text": "Cyber Shield AI"}
            }]
        }).encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        logger.debug(f"Webhook failed: {e}")


def notify_critical(ip: str, score: float, reason: str = ""):
    """
    Wysyła powiadomienie CRITICAL — używane przez autodefend_mgr.
    Automatyczne blokowanie wysokiego ryzyka.
    """
    title = f"🚨 CYBER SHIELD: CRITICAL BLOCK"
    message = f"IP: {ip}\nScore: {score:.4f}\n{reason or 'High-risk activity detected'}"
    _toast(title, message)
    _write_alert_log("CRITICAL", title, message)
    _send_webhook(title, message, color=0xFF0000)
    logger.warning(f"CRITICAL BLOCK: {ip} score={score:.4f}")


def notify_block(ip: str, score: float, port: int = None, reason: str = ""):
    """
    Powiadomienie o zablokowaniu IP (nie koniecznie CRITICAL).
    """
    port_info = f" port={port}" if port else ""
    title = f"🛡️ CYBER SHIELD: IP Blocked"
    message = f"IP: {ip}{port_info}\nScore: {score:.4f}\n{reason}"
    _write_alert_log("BLOCK", title, message)
    _send_webhook(title, message, color=0xFFA500)
    logger.info(f"BLOCK: {ip} score={score:.4f}")


def notify_honeypot_hit(ip: str, port: int, proto: str = "TCP"):
    """
    Powiadomienie o nowym trafieniu do honeypota.
    """
    title = "🎯 CYBER SHIELD: Honeypot Hit"
    message = f"IP: {ip}\nPort: {port}/{proto}\nNew attack logged."
    _write_alert_log("HONEYPOT", title, message)
    # Toast tylko dla podejrzanych portów
    if port in (22, 3389, 445):
        _toast(title, message)
    _send_webhook(title, message, color=0x00BFFF)
    logger.info(f"HONEYPOT HIT: {ip}:{port}/{proto}")


if __name__ == "__main__":
    # Test
    print("Testowanie powiadomień Cyber Shield AI...")
    notify_critical("1.2.3.4", 0.9921, "Test: auto-block triggered")
    notify_block("5.6.7.8", 0.75, port=22, reason="SSH brute-force")
    notify_honeypot_hit("9.10.11.12", 3389)
    print(f"Logi zapisane w: {ALERT_LOG}")
