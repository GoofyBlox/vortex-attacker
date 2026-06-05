import os
import json
import time
from datetime import datetime
from modules.utils import pcolor

LOG_FILE = "logs/attack_logs.json"

def save_log(target, port, method, threads, duration, packets, errors):
    os.makedirs("logs", exist_ok=True)
    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": f"{target}:{port}",
        "method": method,
        "threads": threads,
        "duration": duration,
        "packets": packets,
        "errors": errors,
        "status": "SUCCESS" if packets > 0 else "FAILED"
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append(log)
    if len(logs) > 100:
        logs = logs[-100:]
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def view_logs():
    pcolor("b", "\n[ ATTACK LOGS ]\n")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        for log in reversed(logs[-20:]):
            status = "SUCCESS" if log['status'] == "SUCCESS" else "FAILED"
            color = "g" if log['status'] == "SUCCESS" else "r"
            print(f"[{log['time']}] {log['target']} | {log['method']} | ", end="")
            pcolor(color, status)
            print(f"   Packets: {log['packets']}")
    else:
        print("No logs")
    input("\nPress Enter...")

def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        pcolor("g", "[+] Logs cleared")
    else:
        pcolor("y", "[-] No logs")
    time.sleep(1)
