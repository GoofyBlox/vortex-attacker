import os
import socket

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def clear():
    os.system('clear')

def pcolor(color, text):
    colors = {"g": GREEN, "r": RED, "y": YELLOW, "b": BLUE, "c": CYAN}
    print(colors.get(color, GREEN) + text + RESET)

def banner():
    print(BOLD + CYAN + """
╔═══════════════════════════════════════════════════════════╗
║     VORTEX DDOS TOOL v13.0 - READY FOR ACTION            ║
╚═══════════════════════════════════════════════════════════╝
""" + RESET)

def resolve(domain):
    try:
        ip = socket.gethostbyname(domain)
        pcolor("g", f"[+] {domain} -> {ip}")
        return ip
    except:
        pcolor("r", f"[-] Cannot resolve {domain}")
        return None

def check_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        s.close()
        return True
    except:
        return False
