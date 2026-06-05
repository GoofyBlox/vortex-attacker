#!/usr/bin/env python3
import os
import socket

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def clear():
    os.system('clear')

def pcolor(color, text):
    colors = {
        "g": GREEN, "r": RED, "y": YELLOW, 
        "b": BLUE, "p": PURPLE, "c": CYAN,
        "w": WHITE, "bold": BOLD, "dim": DIM
    }
    print(colors.get(color, GREEN) + str(text) + RESET)

def resolve(domain):
    try:
        ip = socket.gethostbyname(domain)
        pcolor("g", f"[✓] {domain} → {ip}")
        return ip
    except:
        pcolor("r", f"[✗] Cannot resolve {domain}")
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
