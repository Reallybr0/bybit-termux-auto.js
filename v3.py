import requests
import json
import time
import os
import sys
from datetime import datetime

# ============================================================
# 🎨 ANSI COLOR CODES (no colorama needed)
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

def print_success(msg):
    print(f"{ANSI.GREEN}[✅ SUCCESS] {msg}{ANSI.RESET}")

def print_error(msg):
    print(f"{ANSI.RED}[❌ ERROR] {msg}{ANSI.RESET}")

def print_warning(msg):
    print(f"{ANSI.YELLOW}[⚠️ WARNING] {msg}{ANSI.RESET}")

def print_info(msg):
    print(f"{ANSI.BLUE}[ℹ️ INFO] {msg}{ANSI.RESET}")

def print_section(title):
    print(f"\n{ANSI.BG_BLUE}{ANSI.WHITE}{ANSI.BOLD}  {title}  {ANSI.RESET}\n")

def print_divider():
    print(f"{ANSI.MAGENTA}{'─' * 60}{ANSI.RESET}")

# ============================================================
# 🔐 COOKIE & CONFIG (သင့် Cookie ကို ဒီမှာထည့်ပါ)
# ============================================================
COOKIE_STRING = ""  # ဒီနေရာမှာ Cookie string ထည့်ပါ သို့မဟုတ် menu မှတဆင့် ထည့်ပါ

# ============================================================
# 🤖 BYBIT BOT CLASS
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
            print_success("Cookie ဖိုင်မှ ဖတ်ယူပြီးပါပြီ")
            return True
        except FileNotFoundError:
            print_error("bybit_cookies.txt ဖိုင် မတွေ့ပါ")
            return False

    def get_rewards_list(self):
        print_info("Reward စာရင်းများ ရယူနေသည်...")
        url = "https://api.bybit.com/v5/rewards/task-list"
        try:
            resp = self.session.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("retCode") == 0:
                    print_success("Reward စာရင်းများ ရယူပြီးပါပြီ")
                    return data
                else:
                    print_error(f"API Error: {data.get('retMsg')}")
            else:
                print_error(f"HTTP Error: {resp.status_code}")
        except Exception as e:
            print_error(f"Connection Error: {e}")
        return None

    def claim_reward(self, reward_id, reward_type="airdrop"):
        url = "https://api.bybit.com/v5/rewards/claim"
        payload = {"rewardId": reward_id, "rewardType": reward_type}
        try:
            resp = self.session.post(url, headers=self.headers, json=payload, timeout=10)
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
            print_info("Claim လုပ်နိုင်သော Reward မရှိပါ")
            return
        print_section("🎁 AUTO CLAIMING REWARDS")
        print(f"စုစုပေါင်း: {len(claimable)} ခု\n")
        for idx, item in enumerate(claimable, 1):
            name = item.get('name', f'Reward #{idx}')
            reward_id = item.get('id', '')
            reward_type = item.get('type', 'airdrop')
            print(f"{ANSI.YELLOW}[{idx}/{len(claimable)}] Claiming: {name}{ANSI.RESET}")
            result = self.claim_reward(reward_id, reward_type)
            if result and result.get("retCode") == 0:
                print_success(f"✅ {name} - Claim အောင်မြင်ပါသည်")
            else:
                print_error(f"❌ {name} - Claim မအောင်မြင်ပါ")
            if idx < len(claimable):
                time.sleep(1.5)

    def get_open_positions(self):
        url = "https://api.bybit.com/v5/position/list"
        params = {"category": self.category}
        try:
            resp = self.session.get(url, headers=self.headers, params=params, timeout=10)
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
            print_info("ဖွင့်ထားသော Position မရှိပါ")
            return positions
        print_section("📊 OPEN POSITIONS")
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
            print_error("Position ရှာမတွေ့ပါ")
            return None
        pos = positions[position_idx]
        size = pos.get("size", "0")
        side = pos.get("side", "")
        url = "https://api.bybit.com/v5/order/create"
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
            resp = self.session.post(url, headers=self.headers, json=payload, timeout=10)
            result = resp.json()
            if result.get("retCode") == 0:
                print_success(f"✅ {symbol} {side} Position Close အောင်မြင်ပါသည်")
            else:
                print_error(f"Close မအောင်မြင်ပါ: {result.get('retMsg')}")
            return result
        except Exception as e:
            print_error(f"Error: {e}")
            return None

    def close_all_positions(self):
        positions = self.get_open_positions()
        if not positions:
            print_info("ပိတ်ရန် Position မရှိပါ")
            return
        print_warning(f"Position {len(positions)} ခုလုံး Close လုပ်ပါမည်")
        for idx, pos in enumerate(positions):
            symbol = pos.get("symbol", "Unknown")
            print_divider()
            print(f"{ANSI.YELLOW}📊 {symbol} | {pos.get('side')} | Size: {pos.get('size')}{ANSI.RESET}")
            self.close_position(symbol, idx)
            time.sleep(1)

# ============================================================
# 🎯 MAIN MENU
# ============================================================
def manual_cookie_input():
    print_section("📋 MANUAL COOKIE INPUT")
    print_info("Browser မှ Cookie String အပြည့်အစုံကို Paste လုပ်ပါ")
    print_info("(F12 → Network Tab → Request Headers → Cookie တစ်ကြောင်းလုံး)")
    print(f"\n{ANSI.CYAN}Cookie ရိုက်ထည့်ပါ (ပြီးလျှင် Enter နှစ်ချက်နှိပ်ပါ):{ANSI.RESET}")
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
        print_success("Cookie ကို 'bybit_cookies.txt' တွင် သိမ်းဆည်းပြီးပါပြီ")
        return cookie_string
    else:
        print_error("Cookie ထည့်မထားပါ")
        return None

def display_menu():
    print_section("📋 MENU")
    menu_items = [
        "🔐 Cookie ထည့်သွင်းရန် (Browser မှ Copy ကူးထည့်ပါ)",
        "📂 Cookie ဖိုင်မှ ပြန်ဖတ်ရန်",
        "🎁 Rewards ကြည့်ရှုခြင်း",
        "💰 Rewards Auto Claim",
        "📊 Positions ကြည့်ရှုခြင်း",
        "🔒 Position Close (တစ်ခုချင်း)",
        "🔐 Position Close (အားလုံး)",
        "🚪 ထွက်မည်"
    ]
    for i, item in enumerate(menu_items, 1):
        print(f"  {ANSI.CYAN}{i}.{ANSI.RESET} {item}")
    print()

def main():
    bot = BybitBot(COOKIE_STRING) if COOKIE_STRING else BybitBot()
    while True:
        clear_screen()
        print(f"\n{ANSI.CYAN}{ANSI.BOLD}╔══════════════════════════════════════╗")
        print(f"║     🚀 BYBIT BOT v3.0 (No colorama)  ║")
        print(f"╚══════════════════════════════════════╝{ANSI.RESET}\n")
        if bot.cookie_string:
            print(f"{ANSI.GREEN}✅ Cookie Loaded{ANSI.RESET}")
        else:
            print(f"{ANSI.RED}❌ Cookie Not Loaded - Option 1 or 2 အရင်လုပ်ပါ{ANSI.RESET}")
        display_menu()
        try:
            choice = input(f"{ANSI.GREEN}👉 ရွေးချယ်ပါ (1-8): {ANSI.RESET}").strip()
        except KeyboardInterrupt:
            print("\n"); print_warning("Program ရပ်တန့်လိုက်ပါသည်"); sys.exit(0)
        if choice == "1":
            cookie = manual_cookie_input()
            if cookie:
                bot = BybitBot(cookie)
        elif choice == "2":
            if not bot.load_cookie_from_file():
                pass
        elif choice in ["3","4","5","6","7"]:
            if not bot.cookie_string:
                print_error("Cookie မရှိသေးပါ။ Option 1/2 အရင်လုပ်ပါ")
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
                        pos_num = int(input(f"\n{ANSI.GREEN}Close လုပ်လိုသော Position နံပါတ်: {ANSI.RESET}"))
                        if 1 <= pos_num <= len(positions):
                            pos = positions[pos_num-1]
                            confirm = input(f"{ANSI.YELLOW}Close {pos['symbol']}? (y/n): {ANSI.RESET}")
                            if confirm.lower() == 'y':
                                bot.close_position(pos["symbol"], pos_num-1)
                    except ValueError:
                        print_error("ဂဏန်းသာထည့်ပါ")
            elif choice == "7":
                confirm = input(f"{ANSI.RED}⚠️ အားလုံး Close လုပ်မှာသေချာပါသလား? (yes/no): {ANSI.RESET}")
                if confirm.lower() == 'yes':
                    bot.close_all_positions()
            input(f"\n{ANSI.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{ANSI.RESET}")
        elif choice == "8":
            print_success("Program မှ ထွက်ခွာပါပြီ 👋")
            sys.exit(0)
        else:
            print_error("မှားယွင်းသော ရွေးချယ်မှု"); time.sleep(1)

if __name__ == "__main__":
    main()
