#!/usr/bin/env python3
# Vortex DDoS Tool - Main Menu System

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utils import clear, banner, pcolor
from modules.logger import view_logs, clear_logs
from attacks.minecraft import minecraft_attack
from attacks.website import website_attack
from attacks.tcp import tcp_attack
from attacks.udp import udp_attack
from attacks.amplification import amp_attack
from attacks.slowloris import slowloris

def main_menu():
    while True:
        clear()
        banner()
        
        print("""
╔════════════════════════════════════════════════════════════════╗
║                     VORTEX DDOS TOOL v13.0                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║   1. MINECRAFT Java Server DDoS                               ║
║   2. MINECRAFT Bedrock Server DDoS                            ║
║   3. WEBSITE DDoS (HTTP/HTTPS)                                ║
║   4. TCP FLOOD (Generic)                                      ║
║   5. UDP FLOOD (Generic)                                      ║
║   6. AMPLIFICATION ATTACK (DNS/NTP)                           ║
║   7. SLOWLORIS ATTACK                                         ║
║   8. VIEW ATTACK LOGS                                         ║
║   9. CLEAR LOGS                                               ║
║  10. EXIT                                                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")
        
        choice = input("[?] Select (1-10): ")
        
        if choice == "1":
            minecraft_attack("java")
        elif choice == "2":
            minecraft_attack("bedrock")
        elif choice == "3":
            website_attack()
        elif choice == "4":
            tcp_attack()
        elif choice == "5":
            udp_attack()
        elif choice == "6":
            amp_attack()
        elif choice == "7":
            slowloris()
        elif choice == "8":
            view_logs()
        elif choice == "9":
            clear_logs()
        elif choice == "10":
            pcolor("g", "\n[+] Exiting Vortex DDoS Tool...")
            sys.exit(0)
        else:
            pcolor("r", "\n[-] Invalid choice. Press Enter...")
            input()

if __name__ == "__main__":
    main_menu()
