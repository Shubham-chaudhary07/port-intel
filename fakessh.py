import socket
import json
from datetime import datetime

HOST = "0.0.0.0"
PORT = 2222
LOG_FILE = "ssh_logs.json"

def log_event(data):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(data)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def start_ssh_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[+] Fake SSH running on port {PORT}")

    while True:
        client, addr = server.accept()

        print(f"[!] SSH connection attempt from {addr[0]}")

        # Send fake SSH banner
        banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4\r\n"
        client.send(banner.encode())

        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": addr[0],
            "source_port": addr[1],
            "destination_port": PORT,
            "service": "SSH",
            "event": "connection_attempt"
        }

        log_event(event)

        client.close()

if __name__ == "__main__":
    start_ssh_honeypot()
