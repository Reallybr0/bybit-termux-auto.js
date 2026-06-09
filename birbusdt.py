import requests
import json
import time
import sys
import os
from pybit.unified_trading import HTTP   # pip install pybit

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
# 🌐 LANGUAGE DICTIONARIES (အပြည့်အစုံ)
# ============================================================
TEXTS = {
    "my": {
        "banner": "🚀 BYBIT AUTO BOT (မြန်မာ)",
        "cookie_loaded": "✅ Cookie ရှိသည်",
        "cookie_not_loaded": "❌ Cookie မရှိသေး",
        "api_loaded": "✅ API Key ရှိသည်",
        "api_not_loaded": "❌ API Key မရှိသေး",
        "menu_title": "📋 MENU",
        "menu_items": [
            "🔐 Cookie ထည့်သွင်းရန် (Browser မှ Copy ကူးထည့်ပါ)",
            "📂 Cookie ဖိုင်မှ ပြန်ဖတ်ရန်",
            "🔑 API Key ထည့်သွင်းရန်",
            "🎁 Rewards ကြည့်ရှုခြင်း",
            "💰 Rewards Auto Claim",
            "📊 Positions ကြည့်ရှုခြင်း",
            "🔒 Position Close (တစ်ခုချင်း)",
            "🔐 Position Close (အားလုံး)",
            "📈 Spot Trading (BIRBUSDT)",
            "📉 Futures Trading (XPL)",
            "🚪 ထွက်မည်"
        ],
        "prompt_choice": "👉 ရွေးချယ်ပါ (1-11): ",
        "enter_cookie_title": "📋 COOKIE ထည့်သွင်းခြင်း",
        "enter_cookie_info": [
            "Browser မှ Cookie String အပြည့်အစုံကို Paste လုပ်ပါ",
            "(F12 → Network Tab → Request Headers → Cookie တစ်ကြောင်းလုံး)"
        ],
        "enter_cookie_prompt": "Cookie ရိုက်ထည့်ပါ (ပြီးလျှင် Enter နှိပ်ပါ):",
        "cookie_saved": "Cookie ကို 'bybit_cookies.txt' တွင် သိမ်းပြီးပါပြီ",
        "cookie_not_entered": "Cookie ထည့်မထားပါ",
        "cookie_loaded_file": "Cookie ဖိုင်မှ ဖတ်ယူပြီးပါပြီ",
        "cookie_file_not_found": "bybit_cookies.txt ဖိုင် မတွေ့ပါ",
        "enter_api_title": "🔑 API KEY ထည့်သွင်းခြင်း",
        "enter_api_prompt_key": "API Key ရိုက်ထည့်ပါ: ",
        "enter_api_prompt_secret": "API Secret ရိုက်ထည့်ပါ: ",
        "api_saved": "API Key သိမ်းဆည်းပြီးပါပြီ",
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
        "spot_trade_start": "--- [SPOT] {symbol} စတင်ပတ်နေသည် ---",
        "spot_buy_ok": "[✓] Spot Buy အောင်မြင်",
        "spot_sell_ok": "[✓] Spot Sell အောင်မြင်",
        "futures_trade_start": "--- [FUTURES] {symbol} စတင်ပတ်နေသည် ---",
        "futures_long_ok": "[✓] Futures Long ဖွင့်ပြီး",
        "futures_close_ok": "[✓] Futures Position ပိတ်ပြီး",
        "trade_complete": "[🎉] လုပ်ငန်းစဉ် အောင်မြင်စွာ ပြီးဆုံးပါပြီ",
        "exit_msg": "Program မှ ထွက်ခွာပါပြီ 👋",
        "error_choice": "မှားယွင်းသော ရွေးချယ်မှု",
        "error_no_cookie": "Cookie မရှိသေးပါ။ Option 1/2 အရင်လုပ်ပါ",
        "error_no_api": "API Key မရှိသေးပါ။ Option 3 အရင်လုပ်ပါ",
        "error_api": "API Error: ",
        "error_http": "HTTP Error: ",
        "error_connection": "Connection Error: ",
        "error_invalid_num": "ဂဏန်းသာထည့်ပါ",
        "error_trade": "Trade Error: ",
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
        "cookie_not_loaded": "❌ Cookie Not Loaded",
        "api_loaded": "✅ API Key Loaded",
        "api_not_loaded": "❌ API Key Not Loaded",
        "menu_title": "📋 MENU",
        "menu_items": [
            "🔐 Enter Cookie (Paste from browser)",
            "📂 Load Cookie from file",
            "🔑 Enter API Keys",
            "🎁 View Rewards",
            "💰 Auto Claim Rewards",
            "📊 View Open Positions",
            "🔒 Close Single Position",
            "🔐 Close All Positions",
            "📈 Spot Trade (BIRBUSDT)",
            "📉 Futures Trade (XPL)",
            "🚪 Exit"
        ],
        "prompt_choice": "👉 Choose (1-11): ",
        "enter_cookie_title": "📋 MANUAL COOKIE INPUT",
        "enter_cookie_info": [
            "Paste the full Cookie string from the browser",
            "(F12 → Network Tab → Request Headers → Cookie)"
        ],
        "enter_cookie_prompt": "Enter the cookie string (press Enter when done):",
        "cookie_saved": "Cookie saved to 'bybit_cookies.txt'",
        "cookie_not_entered": "No cookie entered",
        "cookie_loaded_file": "Cookies loaded from file",
        "cookie_file_not_found": "bybit_cookies.txt not found",
        "enter_api_title": "🔑 ENTER API KEYS",
        "enter_api_prompt_key": "API Key: ",
        "enter_api_prompt_secret": "API Secret: ",
        "api_saved": "API Keys saved",
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
        "spot_trade_start": "--- [SPOT] Starting {symbol} ---",
        "spot_buy_ok": "[✓] Spot Buy OK",
        "spot_sell_ok": "[✓] Spot Sell OK",
        "futures_trade_start": "--- [FUTURES] Starting {symbol} ---",
        "futures_long_ok": "[✓] Futures Long opened",
        "futures_close_ok": "[✓] Futures Position closed",
        "trade_complete": "[🎉] All operations completed",
        "exit_msg": "Exiting. Goodbye! 👋",
        "error_choice": "Invalid choice",
        "error_no_cookie": "Cookie required. Please use option 1 or 2 first",
        "error_no_api": "API Key required. Please use option 3 first",
        "error_api": "API Error: ",
        "error_http": "HTTP Error: ",
        "error_connection": "Connection Error: ",
        "error_invalid_num": "Invalid number",
        "error_trade": "Trade Error: ",
        "press_enter": "Press Enter to continue...",
        "terminated": "Program terminated",
        "success": "SUCCESS",
        "error": "ERROR",
        "warning": "WARNING",
        "info": "INFO"
    }
}

lang = "my"  # default

# ============================================================
# ⚙️ CONFIGURATION (ပြင်ဆင်ရန်)
# ============================================================
REWARDS_LIST_URL = "https://api.bybit.com/v5/earn/reward/task-list"   
CLAIM_URL = "https://api.bybit.com/v5/rewards/claim"

SPOT_SYMBOL = "BIRBUSDT"
SPOT_COIN = "BIRB"
SPOT_AMOUNT_USDT = 5
FUTURES_TOKEN = "XPL"
FUTURES_QTY = 100

# ============================================================
# 🖨️ PRINT HELPERS
# ============================================================
def t(key, **kwargs):
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
# 🤖 BYBIT BOT CLASS
# ============================================================
class BybitBot:
    def __init__(self):
        self.cookie_string = None
        self.api_key = None
        self.api_secret = None
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Referer": "https://www.bybit.com/",
            "Origin": "https://www.bybit.com"
        }
        self.pybit_session = None
        self.category = "linear"

    def set_cookie(self, cookie_str):
        self.cookie_string = cookie_str
        self.headers["Cookie"] = cookie_str

    def load_cookie_from_file(self):
        try:
            with open("bybit_cookies.txt", "r") as f:
                cookie = f.read().strip()
            if cookie:
                self.set_cookie(cookie)
                print_success(t("cookie_loaded_file"))
                return True
            return False
        except FileNotFoundError:
            print_error(t("cookie_file_not_found"))
            return False

    def set_api_keys(self, key, secret):
        self.api_key = key
        self.api_secret = secret
        self.pybit_session = HTTP(testnet=False, api_key=key, api_secret=secret)
        print_success(t("api_saved"))

    def has_api(self):
        return self.api_key is not None and self.api_secret is not None

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
        claimable = [i for i in items if i.get("status") == "claimable"]
        if not claimable:
            print_info(t("no_claimable"))
            return
        print_section(t("auto_claim_title"))
        print(f"{t('total_claimable')}{len(claimable)}\n")
        for idx, item in enumerate(claimable, 1):
            name = item.get('name', f'Reward #{idx}')
            rid = item.get('id', '')
            rtype = item.get('type', 'airdrop')
            print(f"{ANSI.YELLOW}[{idx}/{len(claimable)}] {t('claiming')}{name}{ANSI.RESET}")
            result = self.claim_reward(rid, rtype)
            if result and result.get("retCode") == 0:
                print_success(f"{name} - {t('claim_success')}")
            else:
                print_error(f"{name} - {t('claim_fail')}")
            if idx < len(claimable):
                time.sleep(1.5)

    # API ကိုသုံးပြီး ပိုမိုစိတ်ချရသော Position စနစ်သို့ ပြောင်းလဲထားပါသည်
    def get_open_positions(self):
        if not self.has_api():
            print_error(t("error_no_api"))
            return []
        try:
            resp = self.pybit_session.get_positions(category=self.category, settleCoin="USDT")
            if resp.get("retCode") == 0:
                # size > 0 ဖြစ်သော ပွင့်နေသည့် position များကိုသာ စစ်ထုတ်သည်
                return [p for p in resp.get("result", {}).get("list", []) if float(p.get("size", 0)) > 0]
        except Exception as e:
            print_error(f"API Error: {e}")
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

    def close_position(self, pos_data):
        symbol = pos_data.get("symbol")
        size = pos_data.get("size", "0")
        side = pos_data.get("side", "")
        # Long ပိတ်ရန် Sell လုပ်ရမည်၊ Short ပိတ်ရန် Buy လုပ်ရမည်
        close_side = "Sell" if side == "Buy" else "Buy"
        
        try:
            result = self.pybit_session.place_order(
                category=self.category,
                symbol=symbol,
                side=close_side,
                orderType="Market",
                qty=size,
                positionIdx=pos_data.get("positionIdx", 0),
                timeInForce="IOC"
            )
            if result.get("retCode") == 0:
                print_success(t("close_success", symbol=symbol, side=side))
            else:
                print_error(f"{t('close_fail')}{result.get('retMsg')}")
        except Exception as e:
            print_error(f"{t('error_connection')}{e}")

    def close_all_positions(self):
        positions = self.get_open_positions()
        if not positions:
            print_info(t("close_all_none"))
            return
        print_warning(t("close_all_warning", n=len(positions)))
        confirm = input(t("close_all_confirm")).strip().lower()
        if confirm == "yes" or confirm == "y":
            for pos in positions:
                self.close_position(pos)
                time.sleep(1)
        else:
            print_info(t("terminated"))

    def get_spot_balance(self, coin):
        try:
            bal = self.pybit_session.get_wallet_balance(accountType="UNIFIED", coin=coin)
            return float(bal['result']['list'][0]['coin'][0]['walletBalance'])
        except:
            return 0.0

    def find_futures_symbol(self, token_name):
        try:
            instruments = self.pybit_session.get_instruments_info(category="linear")
            for item in instruments['result']['list']:
                if item['symbol'].startswith(token_name):
                    return item['symbol']
            return f"{token_name}USDT"
        except:
            return f"{token_name}USDT"

    def run_spot_trade(self):
        if not self.has_api():
            print_error(t("error_no_api"))
            return
        symbol = SPOT_SYMBOL
        print_section(t("spot_trade_start", symbol=symbol))
        try:
            self.pybit_session.place_order(
                category="spot", symbol=symbol, side="Buy",
                orderType="Market", qty=str(SPOT_AMOUNT_USDT)
            )
            print_success(t("spot_buy_ok"))
            time.sleep(2)
            bal = self.get_spot_balance(SPOT_COIN)
            if bal > 0:
                self.pybit_session.place_order(
                    category="spot", symbol=symbol, side="Sell",
                    orderType="Market", qty=str(bal)
                )
                print_success(t("spot_sell_ok"))
            print_success(t("trade_complete"))
        except Exception as e:
            print_error(f"{t('error_trade')}{e}")

    def run_futures_trade(self):
        if not self.has_api():
            print_error(t("error_no_api"))
            return
        symbol = self.find_futures_symbol(FUTURES_TOKEN)
        print_section(t("futures_trade_start", symbol=symbol))
        try:
            self.pybit_session.place_order(
                category="linear", symbol=symbol, side="Buy",
                orderType="Market", qty=str(FUTURES_QTY),
                positionIdx=0
            )
            print_success(t("futures_long_ok"))
            time.sleep(2)
            self.pybit_session.place_order(
                category="linear", symbol=symbol, side="Sell",
                orderType="Market", qty=str(FUTURES_QTY),
                positionIdx=0
            )
            print_success(t("futures_close_ok"))
            print_success(t("trade_complete"))
        except Exception as e:
            print_error(f"{t('error_trade')}{e}")

# ============================================================
# 🧩 MENU & LANGUAGE LOGIC
# ============================================================
def choose_language():
    global lang
    while True:
        clear_screen()
        print(f"{ANSI.CYAN}{ANSI.BOLD}🌐 Language / ဘာသာစကား ရွေးပါ{ANSI.RESET}\n")
        print(f"  {ANSI.CYAN}1.{ANSI.RESET} 🇲🇲 မြန်မာ")
        print(f"  {ANSI.CYAN}2.{ANSI.RESET} 🇬🇧 English")
        sel = input("\n👉 Select (1-2): ").strip()
        if sel == "1":
            lang = "my"
            break
        elif sel == "2":
            lang = "en"
            break

def manual_cookie_input():
    print_section(t("enter_cookie_title"))
    for info in t("enter_cookie_info"):
        print_info(info)
    cookie = input(f"\n{ANSI.CYAN}{t('enter_cookie_prompt')}{ANSI.RESET} ").strip()
    if cookie:
        with open("bybit_cookies.txt", "w") as f:
            f.write(cookie)
        print_success(t("cookie_saved"))
        return cookie
    else:
        print_error(t("cookie_not_entered"))
        return None

def manual_api_input():
    print_section(t("enter_api_title"))
    key = input(f"{ANSI.CYAN}{t('enter_api_prompt_key')}{ANSI.RESET}").strip()
    secret = input(f"{ANSI.CYAN}{t('enter_api_prompt_secret')}{ANSI.RESET}").strip()
    if key and secret:
        return key, secret
    else:
        print_error("API Key/Secret empty")
        return None, None

def main():
    bot = BybitBot()
    choose_language()
    
    # စဖွင့်ချင်း ဖိုင်ထဲမှာ သိမ်းထားတဲ့ Cookie နဲ့ API ရှိရင် အလိုအလျောက် ဖတ်မည်
    bot.load_cookie_from_file()
    if os.path.exists("bybit_api.json"):
        try:
            with op
