import json
import random
from datetime import datetime, timedelta
import os

LOG_FILE = "ssh_logs.json"

# Fake attacker IP pool
FAKE_IPS = [
    "45.83.12.91",
    "103.221.234.17",
    "185.220.101.42",
    "91.240.118.172",
    "203.0.113.55",
    "192.168.1.15"
]

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def simulate_attacks(count=50):
    logs = load_logs()
    now = datetime.now()

    for i in range(count):
        event = {
            "timestamp": (now - timedelta(seconds=random.randint(1, 3600)))
            .strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": random.choice(FAKE_IPS),
            "source_port": random.randint(20000, 65000),
            "destination_port": 2222,
            "service": "SSH",
            "event": "connection_attempt"
        }
        logs.append(event)

    save_logs(logs)
    print(f"[+] Simulated {count} SSH attack attempts")

if __name__ == "__main__":
    simulate_attacks()
