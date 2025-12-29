import socket
import json
import os
from datetime import datetime
from collections import defaultdict

HOST = "0.0.0.0"
PORT = 2222
LOG_FILE = "ssh_logs.json"

attempts = defaultdict(int)

def log_event(event):
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    logs.append(event)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("[+] SSH Honeypot running on port 2222")

    while True:
        client, addr = server.accept()
        ip = addr[0]
        attempts[ip] += 1

        severity = "LOW"
        if attempts[ip] > 5:
            severity = "MEDIUM"
        if attempts[ip] > 10:
            severity = "HIGH"

        banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu\r\n"
        client.send(banner.encode())

        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": ip,
            "source_port": addr[1],
            "destination_port": PORT,
            "service": "SSH",
            "severity": severity
        }

        log_event(event)
        client.close()

if __name__ == "__main__":
    start_honeypot()
