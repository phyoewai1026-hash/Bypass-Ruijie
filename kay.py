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

# URL ထဲမှ SID ကို ဖြတ်ထုတ်ရန် Function အသစ်
def extract_sid_from_url(url):
    # နည်းလမ်း ၁ - sessionId= ကို ရှာခြင်း
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    sid = params.get('sessionId', [None])[0]
    
    # နည်းလမ်း ၂ - Regex ဖြင့် ၃၂ လုံး ရှာခြင်း (Parameter name ကွဲနေပါက)
    if not sid:
        match = re.search(r'sessionId=([a-zA-Z0-9]{32})', url)
        if match:
            sid = match.group(1)
        else:
            # နောက်ဆုံး ၃၂ လုံးကို ယူကြည့်ခြင်း
            clean_url = url.strip()
            potential_sid = clean_url[-32:]
            if len(potential_sid
            
