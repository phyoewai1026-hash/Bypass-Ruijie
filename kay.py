# ... (အပေါ်က import အပိုင်းတွေ အတူတူပါပဲ)

def start_engine():
    os.system('clear')
    print(f"{bcyan}╔════════════════════════════════════════════════╗")
    print(f"║          TURBO BYPASS V4 (MANUAL MODE)         ║")
    print(f"╚════════════════════════════════════════════════╝{reset}")
    
    print(f"{cyan}[*] Detecting Portal Automatically...{reset}")
    sid = None
    gw_ip = "192.168.110.1" # Default Ruijie IP

    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        parsed = urlparse(r.url)
        sid = parse_qs(parsed.query).get('sessionId', [None])[0]
        if parsed.netloc: gw_ip = parsed.netloc.split(':')[0]
    except: pass

    # အကယ်၍ အလိုအလျောက် ရှာမရရင် Manual တောင်းမယ်
    if not sid:
        print(f"{yellow}[!] Auto-detection failed.{reset}")
        print(f"{white}Browser URL ထဲက sessionId (သို့မဟုတ်) token ကို ကူးပြီး ဒီမှာထည့်ပေးပါ။{reset}")
        sid = input(f"{bcyan}[?] Enter SID/Token: {reset}").strip()

    if sid:
        print(f"{green}[✓] Using SID: {sid}{reset}")
        auth_link = f"http://{gw_ip}:2060/wifidog/auth?token={sid}"
        
        # Engine စတင်ခြင်း
        print(f"{purple}[!] Engine Starting...{reset}")
        for _ in range(12):
            threading.Thread(target=high_speed_ping, args=(auth_link,), daemon=True).start()
        
        # နောက်ကွယ်ကနေ Key စစ်မယ်
        threading.Thread(target=background_verify, daemon=True).start()
        
        while True: time.sleep(1)
    else:
        print(f"{red}[X] Error: SID မရှိဘဲ Engine မောင်းလို့မရပါ။{reset}")
        
