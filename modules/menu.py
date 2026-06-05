#!/usr/bin/env python3
# Vortex DDoS Tool - Main Menu System

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
RESET = "\033[0m"

def clear_screen():
    os.system('clear')

def banner():
    print(f"{CYAN}{BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print(f"║                         {RED}VORTEX DDOS TOOL v13.0{CYAN}                             ║")
    print(f"║                   {YELLOW}Minecraft | Website | TCP | UDP | Amplification{CYAN}            ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

def menu():
    print(f"{CYAN}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║                         {BOLD}{WHITE}ATTACK MENU{CYAN}                                    ║{RESET}")
    print(f"{CYAN}╠════════════════════════════════════════════════════════════════════════════╣{RESET}")
    print(f"{CYAN}║  {GREEN}[1]{RESET}  MINECRAFT Java Server                                    {CYAN}║{RESET}")
    print(f"{CYAN}║  {GREEN}[2]{RESET}  MINECRAFT Bedrock Server                                 {CYAN}║{RESET}")
    print(f"{CYAN}║  {GREEN}[3]{RESET}  WEBSITE DDoS (Cloudflare Bypass)                         {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[4]{RESET}  TCP FLOOD                                              {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[5]{RESET}  UDP FLOOD                                              {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[6]{RESET}  AMPLIFICATION (DNS/NTP)                                 {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[7]{RESET}  SLOWLORIS                                              {CYAN}║{RESET}")
    print(f"{CYAN}║  {BLUE}[8]{RESET}  VIEW ATTACK LOGS                                        {CYAN}║{RESET}")
    print(f"{CYAN}║  {BLUE}[9]{RESET}  CLEAR LOGS                                              {CYAN}║{RESET}")
    print(f"{CYAN}║  {RED}[0]{RESET}  EXIT                                                    {CYAN}║{RESET}")
    print(f"{CYAN}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")

def footer():
    import platform
    import datetime
    
    now = datetime.datetime.now().strftime("%H:%M:%S")
    system = platform.system()
    if system == "Android":
        system = "Termux"
    
    print(f"\n┌────────────────────────────────────────────────────────────────────────────────┐")
    print(f"│  🕐 {now}  │  💻 {system}  │  🐍 Python {platform.python_version()}  │  🔥 Vortex DDoS v13.0  │")
    print(f"└────────────────────────────────────────────────────────────────────────────────┘")

def main_menu():
    while True:
        clear_screen()
        banner()
        menu()
        footer()
        
        choice = input(f"\n{BOLD}{YELLOW}ENTER YOUR CHOICE: {RESET}")
        
        if choice == "1":
            print(f"{GREEN}[+] Loading Minecraft Java Attack...{RESET}")
            minecraft_attack("java")
        elif choice == "2":
            print(f"{GREEN}[+] Loading Minecraft Bedrock Attack...{RESET}")
            minecraft_attack("bedrock")
        elif choice == "3":
            print(f"{GREEN}[+] Loading Website DDoS with Cloudflare Bypass...{RESET}")
            website_attack()
        elif choice == "4":
            print(f"{GREEN}[+] Loading TCP Flood...{RESET}")
            tcp_attack()
        elif choice == "5":
            print(f"{GREEN}[+] Loading UDP Flood...{RESET}")
            udp_attack()
        elif choice == "6":
            print(f"{GREEN}[+] Loading Amplification Attack...{RESET}")
            amp_attack()
        elif choice == "7":
            print(f"{GREEN}[+] Loading Slowloris...{RESET}")
            slowloris()
        elif choice == "8":
            print(f"{GREEN}[+] Loading Attack Logs...{RESET}")
            view_logs()
        elif choice == "9":
            print(f"{GREEN}[+] Clearing Logs...{RESET}")
            clear_logs()
        elif choice == "0":
            print(f"\n{YELLOW}[!] Shutting down Vortex DDoS Tool...{RESET}")
            time.sleep(1)
            print(f"{GREEN}[+] Goodbye!{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[!] Invalid choice! Please select 0-9{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
