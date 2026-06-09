import requests
import json
import time
import sys
import os

# ============================================================
# 🎨 ANSI COLOR CODES
# ============================================================
class ANSI:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLUE = "\033[44m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================================================
# 🌐 LANGUAGE DICTIONARIES
# ============================================================
TEXTS = {
    "my": {
        "banner": "🚀 BYBIT AUTO BOT (မြန်မာ)",
        "cookie_loaded": "✅ Cookie ရှိသည်",
        "cookie_not_loaded": "❌ Cookie မရှိသေး - Option 1 သို့ 2 ကို အရင်လုပ်ပါ",
        "menu_title": "📋 MENU",
        "menu_items": [
            "🔐 Cookie ထည့်သွင်းရန် (Browser မှ Copy ကူးထည့်ပါ)",
            "📂 Cookie ဖိုင်မှ ပြန်ဖတ်ရန်",
            "🎁 Rewards ကြည့်ရှုခြင်း",
            "💰 Rewards Auto Claim",
            "📊 Positions ကြည့်ရှုခြင်း",
            "🔒 Position Close (တစ်ခုချင်း)",
            "🔐 Position Close (အားလုံး)",
            "🚪 ထွက်မည်"
        ],
        "prompt_choice": "👉 ရွေးချယ်ပါ (1-8): ",
        "enter_cookie_title": "📋 COOKIE ထည့်သွင်းခြင်း",
        "enter_cookie_info": [
            "Browser မှ Cookie String အပြည့်အစုံကို Paste လုပ်ပါ",
            "(F12 → Network Tab → Request Headers → Cookie တစ်ကြောင်းလုံး)"
        ],
        "enter_cookie_prompt": "Cookie ရိုက်ထည့်ပါ (ပြီးလျှင် Enter နှစ်ချက်နှိပ်ပါ):",
        "cookie_saved": "Cookie ကို 'bybit_cookies.txt' တွင် သိမ်းဆည်းပြီးပါပြီ",
        "cookie_not_entered": "Cookie ထည့်မထားပါ",
        "cookie_loaded_file": "Cookie ဖိုင်မှ ဖတ်ယူပြီးပါပြီ",
        "cookie_file_not_found": "bybit_cookies.txt ဖိုင် မတွေ့ပါ",
        "fetching_rewards": "Reward စာရင်းများ ရယူနေသည်...",
        "rewards_fetched": "Reward စာရင်းများ ရယူပြီးပါပြီ",
        "no_claimable": "Claim လုပ်နိုင်သော Reward မရှိပါ",
        "auto_claim_title": "🎁 AUTO CLAIM ပြုလုပ်နေသည်",
        "total_claimable": "စုစုပေါင်း: ",
        "claiming": "Claiming: ",
        "claim_success": "✅ Claim အောင်မြင်ပါသည်",
        "claim_fail": "❌ Claim မအောင်မြင်ပါ",
        "positions_title": "📊 ဖွင့်ထားသော POSITIONS များ",
        "no_positions": "ဖွင့်ထားသော Position မရှိပါ",
        "close_which": "Close လုပ်လိုသော Position နံပါတ်: ",
        "close_confirm": "Close {symbol}? (y/n): ",
        "close_success": "✅ {symbol} {side} Position Close အောင်မြင်ပါသည်",
        "close_fail": "Close မအောင်မြင်ပါ: ",
        "close_all_warning": "Position {n} ခုလုံး Close လုပ်ပါမည်",
        "close_all_confirm": "⚠️ အားလုံး Close လုပ်မှာသေချာပါသလား? (yes/no): ",
        "close_all_none": "ပိတ်ရန် Position မရှိပါ",
        "exit_msg": "Program မှ ထွက်ခွာပါပြီ 👋",
        "error_choice": "မှားယွင်းသော ရွေးချယ်မှု",
        "error_no_cookie": "Cookie မရှိသေးပါ။ Option 1/2 အရင်လုပ်ပါ",
        "error_api": "API Error: ",
        "error_http": "HTTP Error: ",
        "error_connection": "Connection Error: ",
        "error_invalid_num": "ဂဏန်းသာထည့်ပါ",
        "press_enter": "Enter နှိပ်၍ ဆက်သွားပါ...",
        "terminated": "Program ရပ်တန့်လိုက်ပါသည်",
        "success": "အောင်မြင်",
        "error": "အမှား",
        "warning": "သတိပေး",
        "info": "သတင်း"
    },
    "en": {
        "banner": "🚀 BYBIT AUTO BOT (English)",
        "cookie_loaded": "✅ Cookie Loaded",
        "cookie_not_loaded": "❌ Cookie Not Loaded - Use option 1 or 2 first",
        "menu_title": "📋 MENU",
        "menu_items": [
            "🔐 Enter Cookie (Paste from browser)",
            "📂 Load Cookie from file",
            "🎁 View Rewards",
            "💰 Auto Claim Rewards",
            "📊 View Open Positions",
            "🔒 Close Single Position",
            "🔐 Close All Positions",
            "🚪 Exit"
        ],
        "prompt_choice": "👉 Choose (1-8): ",
        "enter_cookie_title": "📋 MANUAL COOKIE INPUT",
        "enter_cookie_info": [
            "Paste the full Cookie string from the browser",
            "(F12 → Network Tab → Request Headers → Cookie)"
        ],
        "enter_cookie_prompt": "Enter the cookie string (press Enter twice when done):",
        "cookie_saved": "Cookie saved to 'bybit_cookies.txt'",
        "cookie_not_entered": "No cookie entered",
        "cookie_loaded_file": "Cookies loaded from file",
        "cookie_file_not_found": "bybit_cookies.txt not found",
        "fetching_rewards": "Fetching rewards list...",
        "rewards_fetched": "Rewards list fetched successfully",
        "no_claimable": "No claimable rewards found",
        "auto_claim_title": "🎁 AUTO CLAIMING REWARDS",
        "total_claimable": "Total claimable: ",
        "claiming": "Claiming: ",
        "claim_success": "✅ Claim successful",
        "claim_fail": "❌ Claim failed",
        "positions_title": "📊 OPEN POSITIONS",
        "no_positions": "No open positions found",
        "close_which": "Enter position number to close: ",
        "close_confirm": "Close {symbol}? (y/n): ",
        "close_success": "✅ {symbol} {side} position closed successfully",
        "close_fail": "Close failed: ",
        "close_all_warning": "Closing all {n} positions",
        "close_all_confirm": "⚠️ Close all positions? (yes/no): ",
        "close_all_none": "No positions to close",
        "exit_msg": "Exiting. Goodbye! 👋",
        "error_choice": "Invalid choice",
        "error_no_cookie": "Cookie required. Please use option 1 or 2 first",
        "error_api": "API Error: ",
        "error_http": "HTTP Error: ",
        "error_connection": "Connection Error: ",
        "error_invalid_num": "Invalid number",
        "press_enter": "Press Enter to continue...",
        "terminated": "Program terminated",
        "success": "SUCCESS",
        "error": "ERROR",
        "warning": "WARNING",
        "info": "INFO"
    }
}

# ============================================================
# 🖨️ PRINT HELPERS (using language)
# ============================================================
lang = "my"  # default, will be set by user

def t(key, **kwargs):
    """Get translated text, supports formatting"""
    text = TEXTS[lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def print_success(msg):
    print(f"{ANSI.GREEN}[✅ {t('success')}] {msg}{ANSI.RESET}")

def print_error(msg):
    print(f"{ANSI.RED}[❌ {t('error')}] {msg}{ANSI.RESET}")

def print_warning(msg):
    print(f"{ANSI.YELLOW}[⚠️ {t('warning')}] {msg}{ANSI.RESET}")

def print_info(msg):
    print(f"{ANSI.BLUE}[ℹ️ {t('info')}] {msg}{ANSI.RESET}")

def print_section(title):
    print(f"\n{ANSI.BG_BLUE}{ANSI.WHITE}{ANSI.BOLD}  {title}  {ANSI.RESET}\n")

def print_divider():
    print(f"{ANSI.MAGENTA}{'─' * 60}{ANSI.RESET}")

# ============================================================
# ⚙️ API Endpoints (Update from Browser if needed)
# ============================================================
REWARDS_LIST_URL = "https://api.bybit.com/v5/earn/reward/task-list"  # <-- အမှန် URL ထည့်ပါ
CLAIM_URL = "https://api.bybit.com/v5/rewards/claim"
POSITIONS_URL = "https://api.bybit.com/v5/position/list"
ORDER_URL = "https://api.bybit.com/v5/order/create"

# ============================================================
# 🤖 BYBIT BOT CLASS (unchanged, uses print functions)
# ============================================================
class BybitBot:
    def __init__(self, cookie_string=None):
        self.cookie_string = cookie_string
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Referer": "https://www.bybit.com/",
            "Origin": "https://www.bybit.com"
        }
        if self.cookie_string:
            self.headers["Cookie"] = self.cookie_string
        self.category = "linear"

    def load_cookie_from_file(self):
        try:
            with open("bybit_cookies.txt", "r") as f:
                self.cookie_string = f.read().strip()
            self.headers["Cookie"] = self.cookie_string
            print_success(t("cookie_loaded_file"))
            return True
        except FileNotFoundError:
            print_error(t("cookie_file_not_found"))
            return False

    def get_rewards_list(self):
        print_info(t("fetching_rewards"))
        try:
            resp = self.session.get(REWARDS_LIST_URL, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("retCode") == 0:
                    print_success(t("rewards_fetched"))
                    return data
                else:
                    print_error(f"{t('error_api')}{data.get('retMsg')}")
            else:
                print_error(f"{t('error_http')}{resp.status_code}")
        except Exception as e:
            print_error(f"{t('error_connection')}{e}")
        return None

    def claim_reward(self, reward_id, reward_type="airdrop"):
        payload = {"rewardId": reward_id, "rewardType": reward_type}
        try:
            resp = self.session.post(CLAIM_URL, headers=self.headers, json=payload, timeout=10)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}

    def claim_all_rewards(self):
        rewards = self.get_rewards_list()
        if not rewards:
            return
        items = rewards.get("result", {}).get("items", [])
        claimable = [item for item in items if item.get("status") == "claimable"]
        if not claimable:
            print_info(t("no_claimable"))
            return
        print_section(t("auto_claim_title"))
        print(f"{t('total_claimable')}{len(claimable)}\n")
        for idx, item in enumerate(claimable, 1):
            name = item.get('name', f'Reward #{idx}')
            reward_id = item.get('id', '')
            reward_type = item.get('type', 'airdrop')
            print(f"{ANSI.YELLOW}[{idx}/{len(claimable)}] {t('claiming')}{name}{ANSI.RESET}")
            result = self.claim_reward(reward_id, reward_type)
            if result and result.get("retCode") == 0:
                print_success(f"{name} - {t('claim_success')}")
            else:
                print_error(f"{name} - {t('claim_fail')}")
            if idx < len(claimable):
                time.sleep(1.5)

    def get_open_positions(self):
        params = {"category": self.category}
        try:
            resp = self.session.get(POSITIONS_URL, headers=self.headers, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("retCode") == 0:
                    return data.get("result", {}).get("list", [])
        except:
            pass
        return []

    def display_positions(self):
        positions = self.get_open_positions()
        if not positions:
            print_info(t("no_positions"))
            return positions
        print_section(t("positions_title"))
        print(f"{ANSI.CYAN}{'No.':<4} {'Symbol':<12} {'Side':<6} {'Size':<12} {'Entry':<12} {'Mark':<12} {'PnL':<12}{ANSI.RESET}")
        print(f"{ANSI.MAGENTA}{'─' * 75}{ANSI.RESET}")
        for idx, pos in enumerate(positions, 1):
            symbol = pos.get("symbol", "N/A")
            side = pos.get("side", "N/A")
            size = pos.get("size", "0")
            entry = pos.get("avgPrice", "0")
            mark = pos.get("markPrice", "0")
            pnl = pos.get("unrealisedPnl", "0")
            pnl_color = ANSI.GREEN if float(pnl) >= 0 else ANSI.RED
            side_color = ANSI.GREEN if side == "Buy" else ANSI.RED
            print(f"{idx:<4} {symbol:<12} {side_color}{side:<6}{ANSI.RESET} {size:<12} {entry:<12} {mark:<12} {pnl_color}{pnl:<12}{ANSI.RESET}")
        return positions

    def close_position(self, symbol, position_idx=0):
        positions = self.get_open_positions()
        if not positions or position_idx >= len(positions):
            print_error("Position not found")
            return None
        pos = positions[position_idx]
        size = pos.get("size", "0")
        side = pos.get("side", "")
        payload = {
            "category": self.category,
            "symbol": symbol,
            "side": "Sell" if side == "Buy" else "Buy",
            "orderType": "Market",
            "qty": size,
            "positionIdx": position_idx,
            "timeInForce": "IOC"
        }
        try:
            resp = self.session.post(ORDER_URL, headers=self.headers, json=payload, timeout=10)
            result = resp.json()
            if result.get("retCode") == 0:
                print_success(t("close_success", symbol=symbol, side=side))
            else:
                print_error(f"{t('close_fail')}{result.get('retMsg')}")
            return result
        except Exception as e:
            print_error(f"{t('error_connection')}{e}")
            return None

    def close_all_positions(self):
        positions = self.get_open_positions()
        if not positions:
            print_info(t("close_all_none"))
            return
        print_warning(t("close_all_warning", n=len(positions)))
        for idx, pos in enumerate(positions):
            symbol = pos.get("symbol", "Unknown")
            print_divider()
            print(f"{ANSI.YELLOW}📊 {symbol} | {pos.get('side')} | Size: {pos.get('size')}{ANSI.RESET}")
            self.close_position(symbol, idx)
            time.sleep(1)

# ============================================================
# 🧩 MENU FUNCTIONS
# ============================================================
def manual_cookie_input():
    print_section(t("enter_cookie_title"))
    for info in t("enter_cookie_info"):
        print_info(info)
    print(f"\n{ANSI.CYAN}{t('enter_cookie_prompt')}{ANSI.RESET}")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    cookie_string = " ".join(lines)
    if cookie_string:
        with open("bybit_cookies.txt", "w") as f:
            f.write(cookie_string)
        print_success(t("cookie_saved"))
        return cookie_string
    else:
        print_error(t("cookie_not_entered"))
        return None

def display_menu():
    print_section(t("menu_title"))
    for i, item in enumerate(t("menu_items"), 1):
        print(f"  {ANSI.CYAN}{i}.{ANSI.RESET} {item}")
    print()

def choose_language():
    """Language selection at startup"""
    while True:
        clear_screen()
        print(f"{ANSI.CYAN}{ANSI.BOLD}🌐 Language / ဘာသာစကား ရွေးပါ{ANSI.RESET}\n")
        print(f"  {ANSI.CYAN}1.{ANSI.RESET} 🇲🇲 မြန်မာ")
        print(f"  {ANSI.CYAN}2.{ANSI.RESET} 🇬🇧 English")
        try:
            sel = input(f"\n{ANSI.GREEN}👉 ရွေးပါ / Choose (1-2): {ANSI.RESET}").strip()
            if sel == "1":
                return "my"
            elif sel == "2":
                return "en"
            else:
                print_error("Invalid choice. Enter 1 or 2.")
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)

# ============================================================
# 🎯 MAIN
# ============================================================
def main():
    global lang
    lang = choose_language()  # set language
    bot = BybitBot()
    while True:
        clear_screen()
        print(f"\n{ANSI.CYAN}{ANSI.BOLD}╔══════════════════════════════════════╗")
        print(f"║     {t('banner')}       ║")
        print(f"╚══════════════════════════════════════╝{ANSI.RESET}\n")
        if bot.cookie_string:
            print(f"{ANSI.GREEN}{t('cookie_loaded')}{ANSI.RESET}")
        else:
            print(f"{ANSI.RED}{t('cookie_not_loaded')}{ANSI.RESET}")
        display_menu()
        try:
            choice = input(f"{ANSI.GREEN}{t('prompt_choice')}{ANSI.RESET}").strip()
        except KeyboardInterrupt:
            print("\n"); print_warning(t("terminated")); sys.exit(0)

        if choice == "1":
            cookie = manual_cookie_input()
            if cookie:
                bot = BybitBot(cookie)
        elif choice == "2":
            if not bot.load_cookie_from_file():
                pass
        elif choice in ["3","4","5","6","7"]:
            if not bot.cookie_string:
                print_error(t("error_no_cookie"))
                time.sleep(2)
                continue
            if choice == "3":
                bot.get_rewards_list()
            elif choice == "4":
                bot.claim_all_rewards()
            elif choice == "5":
                bot.display_positions()
            elif choice == "6":
                positions = bot.display_positions()
                if positions:
                    try:
                        pos_num = int(input(f"\n{ANSI.GREEN}{t('close_which')}{ANSI.RESET}"))
                        if 1 <= pos_num <= len(positions):
                            pos = positions[pos_num-1]
                            confirm = input(f"{ANSI.YELLOW}{t('close_confirm', symbol=pos['symbol'])}{ANSI.RESET}")
                            if confirm.lower() == 'y':
                                bot.close_position(pos["symbol"], pos_num-1)
                    except ValueError:
                        print_error(t("error_invalid_num"))
            elif choice == "7":
                confirm = input(f"{ANSI.RED}{t('close_all_confirm')}{ANSI.RESET}")
                if confirm.lower() == 'yes':
                    bot.close_all_positions()
            input(f"\n{ANSI.CYAN}{t('press_enter')}{ANSI.RESET}")
        elif choice == "8":
            print_success(t("exit_msg"))
            sys.exit(0)
        else:
            print_error(t("error_choice"))
            time.sleep(1)

if __name__ == "__main__":
    main()
