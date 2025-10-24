#!/usr/bin/env python3
"""
Defense AI: Monitors traffic, detects anomalies, auto-blocks aggressive IPs.
"""
import time, json, os
from collections import defaultdict, deque
from pathlib import Path

TRAFFIC_FILE = Path("/shared/traffic.log")
ALERT_FILE = Path("/shared/alerts.json")
BLACKLIST_FILE = Path("/shared/blacklist.json")

# Detection thresholds
MAX_FAILS = 5           # Number of failed logins
WINDOW_SECONDS = 60     # Time window to check
SLEEP_INTERVAL = 3      # Check frequency

# Load blacklist
def load_blacklist():
    if BLACKLIST_FILE.exists():
        try:
            return set(json.load(open(BLACKLIST_FILE)))
        except json.JSONDecodeError:
            return set()
    return set()

# Save blacklist
def save_blacklist(bset):
    json.dump(sorted(list(bset)), open(BLACKLIST_FILE, "w"), indent=2)

# Save alert
def add_alert(message, src_ip):
    ts = int(time.time())
    alert = {"timestamp": ts, "src_ip": src_ip, "message": message}
    try:
        existing = json.load(open(ALERT_FILE)) if ALERT_FILE.exists() else []
    except json.JSONDecodeError:
        existing = []
    existing.append(alert)
    json.dump(existing[-50:], open(ALERT_FILE, "w"), indent=2)
    print("⚠️ ALERT:", message)

# Detection engine
def run_defense():
    recent = defaultdict(lambda: deque())
    last_size = 0
    blacklist = load_blacklist()
    print("🧠 Defense AI running...")

    while True:
        if TRAFFIC_FILE.exists():
            data = TRAFFIC_FILE.read_text().splitlines()
            if len(data) > last_size:
                new_lines = data[last_size:]
                last_size = len(data)
                for line in new_lines:
                    try:
                        ev = json.loads(line)
                        ip = ev.get("src_ip")
                        typ = ev.get("type")

                        # Ignore blacklisted IPs
                        if ip in blacklist:
                            continue

                        # Record failed logins
                        if typ == "auth_fail":
                            recent[ip].append(ev["ts"])
                            # Clean old entries
                            while recent[ip] and ev["ts"] - recent[ip][0] > WINDOW_SECONDS:
                                recent[ip].popleft()

                            # Trigger block if too many failures
                            if len(recent[ip]) >= MAX_FAILS:
                                msg = f"Auto-blocked {ip}: {len(recent[ip])} failed logins in {WINDOW_SECONDS}s"
                                add_alert(msg, ip)
                                blacklist.add(ip)
                                save_blacklist(blacklist)
                                print("🚫 IP blocked:", ip)
                    except Exception as e:
                        print("Parse error:", e)
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    try:
        run_defense()
    except KeyboardInterrupt:
        print("Defense AI stopped.")
