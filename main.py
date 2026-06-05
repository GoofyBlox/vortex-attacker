#!/usr/bin/env python3
# VORTEX DDOS TOOL v13.0

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.menu import main_menu

if __name__ == "__main__":
    os.system('clear')
    main_menu()
