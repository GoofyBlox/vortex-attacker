#!/usr/bin/env python3
# Vortex DDoS Tool - Main Menu System with Enhanced UI

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utils import clear, pcolor
from modules.logger import view_logs, clear_logs
from attacks.minecraft import minecraft_attack
from attacks.website import website_attack
from attacks.tcp import tcp_attack
from attacks.udp import udp_attack
from attacks.amplification import amp_attack
from attacks.slowloris import slowloris

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def center_text(text, width=70):
    """Center text for better UI"""
    return text.center(width)

def print_ascii_art():
    """Display cool ASCII art banner"""
    art = f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║      ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗                             ║
║      ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝                             ║
║      ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝                              ║
║      ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗                              ║
║       ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗                             ║
║        ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                             ║
║                                                                                      ║
║                      {RED}🔥 DDoS TOOL v13.0 - ULTIMATE EDITION 🔥{CYAN}                       ║
║                      {YELLOW}⚡ Minecraft | Website | TCP | UDP | Amplification ⚡{CYAN}        ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
{RESET}
"""
    print(art)

def print_menu_box():
    """Display menu options in a stylish box"""
    
    menu_items = [
        ("1", "MINECRAFT Java Server", "🎮", "Attack Java Edition servers on port 25565"),
        ("2", "MINECRAFT Bedrock Server", "🎮", "Attack Bedrock Edition servers on port 19132"),
        ("3", "WEBSITE DDoS", "🌐", "HTTP/HTTPS flood attack on websites"),
        ("4", "TCP FLOOD", "🔌", "Generic TCP connection flood"),
        ("5", "UDP FLOOD", "📡", "Generic UDP packet flood"),
        ("6", "AMPLIFICATION", "🚀", "DNS/NTP amplification (50-500x multiplier)"),
        ("7", "SLOWLORIS", "🐌", "Slowloris - keep connections open"),
        ("8", "VIEW LOGS", "📋", "View attack history and statistics"),
        ("9", "CLEAR LOGS", "🗑️", "Delete all attack logs"),
        ("0", "EXIT", "❌", "Exit the tool")
    ]
    
    print(f"{CYAN}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║                          {BOLD}{WHITE}🔧 ATTACK MENU 🔧{CYAN}                          ║{RESET}")
    print(f"{CYAN}╠════════════════════════════════════════════════════════════════════════════╣{RESET}")
    
    for num, name, icon, desc in menu_items:
        color = GREEN if num in ["1", "2", "3"] else YELLOW if num in ["4", "5", "6", "7"] else CYAN
        print(f"{CYAN}║  {color}{BOLD}{icon} [{num}] {name}{RESET}{DIM}{' ' * (45 - len(name))}{desc}{RESET}{CYAN} ║{RESET}")
    
    print(f"{CYAN}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")

def print_footer():
    """Display footer with system info"""
    import platform
    import datetime
    
    now = datetime.datetime.now().strftime("%H:%M:%S")
    system = platform.system()
    python_ver = platform.python_version()
    
    print(f"\n{DIM}┌────────────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{DIM}│  🕐 {now}  │  💻 {system}  │  🐍 Python {python_ver}  │  🔥 Vortex DDoS v13.0  │{RESET}")
    print(f"{DIM}└────────────────────────────────────────────────────────────────────────────────┘{RESET}")

def loading_animation(text, duration=0.5):
    """Simple loading animation"""
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(int(duration * 10)):
        for char in chars:
            sys.stdout.write(f"\r{char} {text}")
            sys.stdout.flush()
            time.sleep(0.05)
    sys.stdout.write("\r✓ " + text + "     \n")
    sys.stdout.flush()

def main_menu():
    while True:
        clear()
        print_ascii_art()
        print_menu_box()
        print_footer()
        
        # Animated prompt
        choice = input(f"\n{BOLD}{YELLOW}🎯 ENTER YOUR CHOICE: {RESET}")
        
        if choice == "1":
            loading_animation("Loading Minecraft Java Attack...", 0.3)
            minecraft_attack("java")
        elif choice == "2":
            loading_animation("Loading Minecraft Bedrock Attack...", 0.3)
            minecraft_attack("bedrock")
        elif choice == "3":
            loading_animation("Loading Website Attack...", 0.3)
            website_attack()
        elif choice == "4":
            loading_animation("Loading TCP Flood...", 0.3)
            tcp_attack()
        elif choice == "5":
            loading_animation("Loading UDP Flood...", 0.3)
            udp_attack()
        elif choice == "6":
            loading_animation("Loading Amplification Attack...", 0.3)
            amp_attack()
        elif choice == "7":
            loading_animation("Loading Slowloris...", 0.3)
            slowloris()
        elif choice == "8":
            loading_animation("Loading Attack Logs...", 0.3)
            view_logs()
        elif choice == "9":
            loading_animation("Clearing Logs...", 0.3)
            clear_logs()
        elif choice == "0":
            print(f"\n{YELLOW}🔥 Shutting down Vortex DDoS Tool...{RESET}")
            time.sleep(1)
            print(f"{GREEN}✓ Goodbye!{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}❌ Invalid choice! Please select 0-9{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
