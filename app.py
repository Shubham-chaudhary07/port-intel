from flask import Flask, render_template, jsonify
import subprocess
import json
import os
from collections import Counter
from log_analyzer import generate_graph

app = Flask(__name__)
LOG_FILE = "ssh_logs.json"
honeypot_process = None

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    logs = load_logs()
    generate_graph()

    severity = Counter(log["severity"] for log in logs)
    ips = Counter(log["source_ip"] for log in logs)

    return jsonify({
        "total": len(logs),
        "severity": severity,
        "top_ips": ips.most_common(5)
    })

@app.route("/start")
def start():
    global honeypot_process
    if honeypot_process is None:
        honeypot_process = subprocess.Popen(["python3", "honeypot.py"])
    return "Honeypot Started"

@app.route("/stop")
def stop():
    global honeypot_process
    if honeypot_process:
        honeypot_process.terminate()
        honeypot_process = None
    return "Honeypot Stopped"

if __name__ == "__main__":
    app.run(debug=True)
