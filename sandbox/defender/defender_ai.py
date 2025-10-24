import os
import time
import json
import random
from datetime import datetime

# Create sandbox folder safely
os.makedirs("sandbox/defender", exist_ok=True)

ALERTS_FILE = "data/alerts.jsonl"

# Function to log alerts to file
def log_alert(event_type, message, severity):
    alert = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": event_type,
        "message": message,
        "severity": severity
    }
    os.makedirs(os.path.dirname(ALERTS_FILE), exist_ok=True)
    with open(ALERTS_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")
    print(f"[{alert['timestamp']}] {event_type.upper()} - {message} ({severity})")

# Simulation loop
def simulate_threat_detection():
    events = [
        ("PORT_SCAN", "Multiple connection attempts detected from 192.168.1.10", "medium"),
        ("MALWARE", "Suspicious binary detected in /tmp/unknown.bin", "high"),
        ("LOGIN_FAIL", "Repeated failed SSH login attempts", "low"),
        ("INTRUSION", "Unauthorized access to /var/log/auth.log", "critical")
    ]
    while True:
        event = random.choice(events)
        log_alert(*event)
        time.sleep(random.randint(5, 15))  # random interval

if __name__ == "__main__":
    print("Defender AI is active and monitoring...")
    simulate_threat_detection()
