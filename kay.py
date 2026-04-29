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
from urllib.parse import urlparse, parse_qs

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
purple = "\033[0;35m"
white, reset = "\033[0;37m", "\033[00m"

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

def background_verify():
    """အင်တာနက်ရလာရင် နောက်ကွယ်ကနေ Key ကို စစ်ပေးမည့်အပိုင်း"""
    my_key = get_system_key()
    while True:
        if check_real_internet():
            try:
                r = requests.get(GITHUB_KEY_URL, timeout=10)
                if r.status_code == 200 and my_key in r.text:
                    with open(LOCAL_KEYS_FILE, 'w') as f: f.write(my_key)
                    break
            except: pass
        time.sleep(15)

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
    print(f"║          TURBO BYPASS V4 (HYBRID MODE)         ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    print(f"[*] ID: {byellow}{get_system_key()}{reset}\n")
    
    print(f"{cyan}[*] Attempting Auto-Detection...{reset}")
    sid = None
    gw_ip = "192.168.110.1"

    try:
        # Portal Redirect ကို ဖမ်းယူခြင်း
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        parsed = urlparse(r.url)
        params = parse_qs(parsed.query)
        sid = params.get('sessionId', [None])[0] or params.get('token', [None])[0]
        if parsed.netloc: gw_ip = parsed.netloc.split(':')[0]
    except: pass

    # အကယ်၍ Auto ရှာမရရင် Manual တောင်းမယ်
    if not sid:
        print(f"{yellow}[!] Auto-detection failed.{reset}")
        print(f"{white}Browser URL ထဲက {byellow}sessionId={white} (သို့မဟုတ်) {byellow}token={white} နောက်ကစာသားကို ကူးထည့်ပါ။{reset}")
        sid = input(f"{bcyan
        
