#!/usr/bin/env python3
# VORTEX DDOS TOOL v12.0 - Main Entry Point

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.menu import main_menu
from modules.utils import clear_screen, banner

if __name__ == "__main__":
    clear_screen()
    banner()
    main_menu()
