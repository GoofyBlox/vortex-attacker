#!/usr/bin/env python3
# Vortex DDoS Tool - Fixed Menu UI

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

def clear():
    os.system('clear')

def banner():
    print(f"{CYAN}{BOLD}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print(f"║     {RED}██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗{CYAN}              ║")
    print(f"║     {RED}██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝{CYAN}              ║")
    print(f"║     {RED}██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝{CYAN}               ║")
    print(f"║     {RED}╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗{CYAN}               ║")
    print(f"║     {RED} ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗{CYAN}              ║")
    print(f"║     {RED}  ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝{CYAN}              ║")
    print("║                                                                            ║")
    print(f"║                 {YELLOW}🔥 DDoS TOOL v13.0 - ULTIMATE EDITION 🔥{CYAN}                 ║")
    print(f"║               {GREEN}⚡ Minecraft | Website | TCP | UDP | Amplification ⚡{CYAN}        ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

def menu():
    print(f"{CYAN}╔════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║                         {BOLD}{WHITE}🔧 ATTACK MENU 🔧{CYAN}                          ║{RESET}")
    print(f"{CYAN}╠════════════════════════════════════════════════════════════════════════════╣{RESET}")
    print(f"{CYAN}║  {GREEN}[1]{RESET}  MINECRAFT Java Server      {DIM}Attack Java Edition servers{RESET}                              {CYAN}║{RESET}")
    print(f"{CYAN}║  {GREEN}[2]{RESET}  MINECRAFT Bedrock Server   {DIM}Attack Bedrock Edition servers{RESET}                           {CYAN}║{RESET}")
    print(f"{CYAN}║  {GREEN}[3]{RESET}  WEBSITE DDoS               {DIM}HTTP/HTTPS flood with Cloudflare bypass{RESET}                  {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[4]{RESET}  TCP FLOOD                  {DIM}Generic TCP connection flood{RESET}                             {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[5]{RESET}  UDP FLOOD                  {DIM}Generic UDP packet flood{RESET}                                 {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[6]{RESET}  AMPLIFICATION              {DIM}DNS/NTP amplification (50-500x multiplier){RESET}               {CYAN}║{RESET}")
    print(f"{CYAN}║  {YELLOW}[7]{RESET}  SLOWLORIS                  {DIM}Slowloris - keep connections open{RESET}                        {CYAN}║{RESET}")
    print(f"{CYAN}║  {BLUE}[8]{RESET}  VIEW LOGS                  {DIM}View attack history and statistics{RESET}                       {CYAN}║{RESET}")
    print(f"{CYAN}║  {BLUE}[9]{RESET}  CLEAR LOGS                 {DIM}Delete all attack logs{RESET}                                    {CYAN}║{RESET}")
    print(f"{CYAN}║  {RED}[0]{RESET}  EXIT                       {DIM}Exit the tool{RESET}                                             {CYAN}║{RESET}")
    print(f"{CYAN}╚════════════════════════════════════════════════════════════════════════════╝{RESET}")

def footer():
    import platform
    import datetime
    
    now = datetime.datetime.now().strftime("%H:%M:%S")
    system = platform.system()
    if system == "Android":
        system = "Termux"
    
    print(f"\n{DIM}┌────────────────────────────────────────────────────────────────────────────────┐{RESET}")
    print(f"{DIM}│  🕐 {now}  │  💻 {system}  │  🐍 Python {platform.python_version()}  │  🔥 Vortex DDoS v13.0  │{RESET}")
    print(f"{DIM}└────────────────────────────────────────────────────────────────────────────────┘{RESET}")

def loading(text):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for char in chars:
        sys.stdout.write(f"\r{char} {text}")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write(f"\r✓ {text}     \n")

def main_menu():
    while True:
        clear()
        banner()
        menu()
        footer()
        
        choice = input(f"\n{BOLD}{YELLOW}🎯 ENTER YOUR CHOICE: {RESET}")
        
        if choice == "1":
            loading("Loading Minecraft Java Attack...")
            minecraft_attack("java")
        elif choice == "2":
            loading("Loading Minecraft Bedrock Attack...")
            minecraft_attack("bedrock")
        elif choice == "3":
            loading("Loading Website DDoS with Cloudflare Bypass...")
            website_attack()
        elif choice == "4":
            loading("Loading TCP Flood...")
            tcp_attack()
        elif choice == "5":
            loading("Loading UDP Flood...")
            udp_attack()
        elif choice == "6":
            loading("Loading Amplification Attack...")
            amp_attack()
        elif choice == "7":
            loading("Loading Slowloris...")
            slowloris()
        elif choice == "8":
            loading("Loading Attack Logs...")
            view_logs()
        elif choice == "9":
            loading("Clearing Logs...")
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
