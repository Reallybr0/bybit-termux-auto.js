import requests
import json
import time
import sys
import os
from pybit.unified_trading import HTTP

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
            "📈 Spot Trading Auto-Volume (BIRBUSDT)",
            "📉 Futures Trading (XPL)",
            "🚪 ထွက်မည်"
        ],
        "prompt_choice": "👉 ရွေးချယ်ပါ (1-11): ",
        "enter_cookie_title": "📋 COOKIE ထည့်သွင်းခြင်း",
        "enter_cookie_info": ["Browser မှ Cookie String အပြည့်အစုံကို Paste လုပ်ပါ"],
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
        "auto_claim_title": "🎁 AUTO CLAIM PRY PYU PYIT NE THAL",
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
        "spot_trade_start": "--- [SPOT VOLUME BOT] {symbol} စတင်ပတ်နေသည် ---",
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
    }
}

lang = "my"

REWARDS_LIST_URL = "https://api.bybit.com/v5/earn/reward/task-list"   
CLAIM_URL = "https://api.bybit.com/v5/rewards/claim"
SPOT_SYMBOL = "BIRBUSDT"
SPOT_COIN = "BIRB"
SPOT_AMOUNT_USDT = 5         
SPOT_VOLUME_TARGET = 100     
FUTURES_TOKEN = "XPL"
FUTURES_QTY = 100            

def t(key, **kwargs):
    text = TEXTS[lang].get(key, key)
    if kwargs: return text.format(**kwargs)
    return text

def print_success(msg): print(f"{ANSI.GREEN}[✅ {t('success')}] {msg}{ANSI.RESET}")
def print_error(msg): print(f"{ANSI.RED}[❌ {t('error')}] {msg}{ANSI.RESET}")
def print_warning(msg): print(f"{ANSI.YELLOW}[⚠️ {t('warning')}] {msg}{ANSI.RESET}")
def print_info(msg): print(f"{ANSI.BLUE}[ℹ️ {t('info')}] {msg}{ANSI.RESET}")
def print_section(title): print(f"\n{ANSI.BG_BLUE}{ANSI.WHITE}{ANSI.BOLD}  {title}  {ANSI.RESET}\n")
def print_divider(): print(f"{ANSI.MAGENTA}{'─' * 60}{ANSI.RESET}")

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
            return False

    def set_api_keys(self, key, secret):
        self.api_key = key
        self.api_secret = secret
        self.pybit_session = HTTP(testnet=False, api_key=key, api_secret=secret)
        print_success(t("api_saved"))

    def has_api(self): return self.api_key is not None and self.api_secret is not None

    def get_rewards_list(self):
        print_info(t("fetching_rewards"))
        try:
            resp = self.session.get(REWARDS_LIST_URL, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("retCode") == 0:
                    print_success(t("rewards_fetched"))
                    return data
                else: print_error(f"{t('error_api')}{data.get('retMsg')}")
            else: print_error(f"{t('error_http')}{resp.status_code}")
        except Exception as e: print_error(f"{t('error_connection')}{e}")
        return None

    def claim_reward(self, reward_id, reward_type="airdrop"):
        payload = {"rewardId": reward_id, "rewardType": reward_type}
        try:
            resp = self.session.post(CLAIM_URL, headers=self.headers, json=payload, timeout=10)
            return resp.json()
        except Exception as e: return {"error": str(e)}

    def claim_all_rewards(self):
        rewards = self.get_rewards_list()
        if not rewards: return
        items = rewards.get("result", {}).get("items", [])
        claimable = [i for i in items if i.get("status") == "claimable"]
        if not claimable:
            print_info(t("no_claimable"))
            return
        print_section(t("auto_claim_title"))
        for idx, item in enumerate(claimable, 1):
            name = item.get('name', f'Reward #{idx}')
            result = self.claim_reward(item.get('id', ''), item.get('type', 'airdrop'))
            if result and result.get("retCode") == 0: print_success(f"{name} - {t('claim_success')}")
            else: print_error(f"{name} - {t('claim_fail')}")
            time.sleep(1.5)

    def get_open_positions(self):
        if not self.has_api(): return []
        try:
            resp = self.pybit_session.get_positions(category=self.category, settleCoin="USDT")
            if resp.get("retCode") == 0:
                return [p for p in resp.get("result", {}).get("list", []) if float(p.get("size", 0)) > 0]
        except: pass
        return []

    def display_positions(self):
        positions = self.get_open_positions()
        if not positions:
            print_info(t("no_positions"))
            return positions
        print_section(t("positions_title"))
        for idx, pos in enumerate(positions, 1):
            print(f"{idx}. {pos.get('symbol')} | {pos.get('side')} | Size: {pos.get('size')} | PnL: {pos.get('unrealisedPnl')}")
        return positions

    def close_position(self, pos_data):
        try:
            self.pybit_session.place_order(
                category=self.category, symbol=pos_data.get("symbol"),
                side="Sell" if pos_data.get("side") == "Buy" else "Buy",
                orderType="Market", qty=pos_data.get("size"),
                positionIdx=pos_data.get("positionIdx", 0), timeInForce="IOC"
            )
            print_success(t("close_success", symbol=pos_data.get("symbol"), side=pos_data.get("side")))
        except Exception as e: print_error(f"Error: {e}")

    def close_all_positions(self):
        positions = self.get_open_positions()
        if not positions: return
        for pos in positions:
            self.close_position(pos)
            time.sleep(1)

    def get_spot_balance(self, coin):
        try:
            bal = self.pybit_session.get_wallet_balance(accountType="UNIFIED", coin=coin)
            return float(bal['result']['list'][0]['coin'][0]['walletBalance'])
        except: return 0.0

    def run_spot_trade(self):
        if not self.has_api(): return
        print_section(t("spot_trade_start", symbol=SPOT_SYMBOL))
        current_volume = 0.0
        while current_volume < SPOT_VOLUME_TARGET:
            try:
                self.pybit_session.place_order(category="spot", symbol=SPOT_SYMBOL, side="Buy", orderType="Market", qty=str(SPOT_AMOUNT_USDT))
                print_success(t("spot_buy_ok"))
                current_volume += SPOT_AMOUNT_USDT
                time.sleep(2)
                bal = self.get_spot_balance(SPOT_COIN)
                if bal > 0:
                    self.pybit_session.place_order(category="spot", symbol=SPOT_SYMBOL, side="Sell", orderType="Market", qty=str(bal))
                    print_success(t("spot_sell_ok"))
                    current_volume += SPOT_AMOUNT_USDT
                time.sleep(3)
            except Exception as e:
                time.sleep(5)
        print_success(t("trade_complete"))

    def run_futures_trade(self):
        if not self.has_api(): return
        symbol = f"{FUTURES_TOKEN}USDT"
        print_section(t("futures_trade_start", symbol=symbol))
        try:
            self.pybit_session.place_order(category="linear", symbol=symbol, side="Buy", orderType="Market", qty=str(FUTURES_QTY), positionIdx=0)
            print_success(t("futures_long_ok"))
            time.sleep(2)
            self.pybit_session.place_order(category="linear", symbol=symbol, side="Sell", orderType="Market", qty=str(FUTURES_QTY), positionIdx=0)
            print_success(t("futures_close_ok"))
        except Exception as e: print_error(f"Error: {e}")

def main():
    bot = BybitBot()
    bot.load_cookie_from_file()
    if os.path.exists("bybit_api.json"):
        try:
            with open("bybit_api.json", "r") as f:
                d = json.load(f)
                bot.set_api_keys(d["key"], d["secret"])
        except: pass

    while True:
        clear_screen()
        print_divider()
        print(f"   {t('banner')}   ")
        print_divider()
        print(f"{t('menu_title')}")
        for i, item in enumerate(TEXTS["my"]["menu_items"], 1):
            print(f"  {i}. {item}")
        print_divider()
        choice = input(TEXTS["my"]["prompt_choice"]).strip()
        
        if choice == "1":
            c = input("Enter Cookie: ").strip()
            if c: bot.set_cookie(c)
        elif choice == "3":
            k = input("API Key: ").strip()
            s = input("API Secret: ").strip()
            if k and s:
                bot.set_api_keys(k, s)
                with open("bybit_api.json", "w") as f: json.dump({"key": k, "secret": s}, f)
        elif choice == "4": bot.get_rewards_list()
        elif choice == "5": bot.claim_all_rewards()
        elif choice == "6": bot.display_positions()
        elif choice == "8": bot.close_all_positions()
        elif choice == "9": bot.run_spot_trade()
        elif choice == "10": bot.run_futures_trade()
        elif choice == "11": sys.exit()
        input(f"\n{t('press_enter')}")

if __name__ == "__main__":
    main()

