import json
import os
import matplotlib.pyplot as plt
from collections import Counter

LOG_FILE = "ssh_logs.json"
GRAPH_PATH = "static/graphs/attacks.png"

def generate_graph():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except:
            return

    if not logs:
        return

    ips = Counter(log["source_ip"] for log in logs)
    top = ips.most_common(5)

    labels = [x[0] for x in top]
    values = [x[1] for x in top]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Top Attacking IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Attempts")
    plt.tight_layout()
    plt.savefig(GRAPH_PATH)
    plt.close()
