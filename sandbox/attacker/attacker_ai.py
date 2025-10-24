tee sandbox/attacker/attacker_ai.py > /dev/null <<'PY'
#!/usr/bin/env python3
"""
Attacker: synthetic traffic generator.
If blocked (blacklist contains its current IP), attacker rotates to a new IP and backs off.
"""
import time, json, random, os, sys
from pathlib import Path

OUT = "/shared/traffic.log"
BLACKLIST = "/shared/blacklist.json"
SERVICES = ["ssh", "http", "ftp"]

def gen_ip():
    return f"10.0.0.{random.randint(2,250)}"

def read_blacklist():
    try:
        if Path(BLACKLIST).exists():
            return set(json.loads(Path(BLACKLIST).read_text()))
    except Exception:
        pass
    return set()

def append_event(ev):
    try:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "a") as f:
            f.write(json.dumps(ev) + "\n")
            f.flush()
        print(json.dumps(ev), flush=True)
    except Exception as e:
        print("ERROR writing event:", e, file=sys.stderr, flush=True)

def main_loop():
    ip = gen_ip()
    backoff = 0.5
    counter = 0
    while True:
        # if blacklisted, rotate IP and back off
        blocked = read_blacklist()
        if ip in blocked:
            print(f"[attacker] IP {ip} blocked, rotating", flush=True)
            ip = gen_ip()
            backoff = min(5.0, backoff * 2)  # exponential backoff up to 5s
            time.sleep(backoff)
            continue

        counter += 1
        action = random.choices(["scan", "auth_fail", "auth_success"], weights=[0.5, 0.45, 0.05])[0]
        ts = int(time.time())
        if action == "scan":
            ev = {"ts": ts, "src_ip": ip, "type": "scan", "service": random.choice(SERVICES)}
        else:
            ev = {"ts": ts, "src_ip": ip, "type": action, "user": random.choice(["admin","root","guest"]), "attempt": random.randint(1,9999)}
        append_event(ev)

        # gradually reduce backoff if healthy
        if backoff > 0.5:
            backoff = max(0.5, backoff / 1.5)

        # occasional burst
        sleep = random.uniform(0.5, 2.5) if counter % 20 != 0 else random.uniform(0.1, 0.4)
        time.sleep(sleep)

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("attacker stopped", flush=True)
PY
chmod +x sandbox/attacker/attacker_ai.py
