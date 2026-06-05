import socket
import subprocess
from modules.utils import pcolor, resolve

def scan_network():
    pcolor("b", "\n[ NETWORK SCANNER ]\n")
    network = input("Network (192.168.1.0/24): ")
    try:
        subprocess.run(["nmap", "-sn", network])
    except:
        pcolor("r", "[-] nmap not installed")
    input("\nPress Enter...")

def ip_lookup():
    pcolor("b", "\n[ IP LOOKUP ]\n")
    target = input("IP or Domain: ")
    if not target.replace('.', '').isdigit():
        ip = resolve(target)
        if not ip:
            input("Press Enter...")
            return
    else:
        ip = target
    
    import urllib.request, json
    try:
        data = json.loads(urllib.request.urlopen(f"http://ip-api.com/json/{ip}").read())
        if data['status'] == 'success':
            print(f"\nCountry: {data['country']}")
            print(f"City: {data['city']}")
            print(f"ISP: {data['isp']}")
            print(f"Location: {data['lat']}, {data['lon']}")
    except:
        pcolor("r", "[-] Lookup failed")
    input("\nPress Enter...")
