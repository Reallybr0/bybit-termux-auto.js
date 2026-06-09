import requests
import json
import time
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style, Back

# Initialize colorama for cross-platform colored terminal
init(autoreset=True)

# ============================================================
# 🎨 CONFIGURATION - သင့် Cookies နှင့် ဆက်တင်များ ဒီမှာထည့်ပါ
# ============================================================
COOKIE_STRING = "bybit_lang=en-US; bybit_uid=559636125; csrf_token=xxx; ..."  # သင့် Cookie အပြည့်အစုံထည့်ပါ

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Cookie": COOKIE_STRING,
    "Content-Type": "application/json",
    "Referer": "https://www.bybit.com/",
    "Origin": "https://www.bybit.com"
}

# ============================================================
# 🎨 TERMINAL UI HELPERS
# ============================================================
def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display fancy banner"""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════╗
║          🚀  BYBIT AUTO BOT v2.0  🚀                    ║
║     Reward Claimer • Position Manager                   ║
╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

def print_success(msg):
    print(f"{Fore.GREEN}[✅ SUCCESS] {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}[❌ ERROR] {msg}{Style.RESET_ALL}")

def print_warning(msg):
    print(f"{Fore.YELLOW}[⚠️ WARNING] {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.BLUE}[ℹ️ INFO] {msg}{Style.RESET_ALL}")

def print_section(title):
    print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT}  {title}  {Style.RESET_ALL}\n")

def print_divider():
    print(f"{Fore.MAGENTA}{'─' * 60}{Style.RESET_ALL}")

# ============================================================
# 📡 API FUNCTIONS
# ============================================================

def get_rewards_list():
    """ရရှိနိုင်သော Reward များစာရင်းရယူခြင်း"""
    print_info("Reward စာရင်းများ ရယူနေသည်...")
    url = "https://api.bybit.com/v5/rewards/task-list"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("retCode") == 0:
                print_success("Reward စာရင်းများ ရယူပြီးပါပြီ")
                return data
            else:
                print_error(f"API Error: {data.get('retMsg', 'Unknown error')}")
                return None
        else:
            print_error(f"HTTP Error: {resp.status_code}")
            return None
    except Exception as e:
        print_error(f"Connection Error: {e}")
        return None

def claim_reward(reward_id, reward_type="airdrop"):
    """Reward တစ်ခုချင်း Claim လုပ်ခြင်း"""
    url = "https://api.bybit.com/v5/rewards/claim"
    payload = {
        "rewardId": reward_id,
        "rewardType": reward_type
    }
    
    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def get_open_positions(category="linear"):
    """ဖွင့်ထားသော Position များ ရယူခြင်း"""
    print_info("Open Positions များ ရယူနေသည်...")
    url = "https://api.bybit.com/v5/position/list"
    params = {"category": category}
    
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("retCode") == 0:
                positions = data.get("result", {}).get("list", [])
                print_success(f"Open Positions {len(positions)} ခုတွေ့ရှိသည်")
                return positions
            else:
                print_error(f"API Error: {data.get('retMsg', 'Unknown error')}")
                return []
        else:
            print_error(f"HTTP Error: {resp.status_code}")
            return []
    except Exception as e:
        print_error(f"Connection Error: {e}")
        return []

def close_position(symbol, position_idx=0, category="linear"):
    """Position တစ်ခုကို Close လုပ်ခြင်း"""
    print_info(f"{symbol} အတွက် Position Close လုပ်နေသည်...")
    
    # Position info ရယူခြင်း
    url_info = "https://api.bybit.com/v5/position/list"
    params = {"category": category, "symbol": symbol}
    
    try:
        resp = requests.get(url_info, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            print_error("Position အချက်အလက် ရယူ၍မရပါ")
            return None
        
        data = resp.json()
        positions = data.get("result", {}).get("list", [])
        
        if not positions or position_idx >= len(positions):
            print_error(f"Position မရှိဘူး - Index: {position_idx}")
            return None
        
        pos = positions[position_idx]
        size = pos.get("size", "0")
        side = pos.get("side", "")
        
        # Close order တင်ခြင်း
        url_close = "https://api.bybit.com/v5/order/create"
        payload = {
            "category": category,
            "symbol": symbol,
            "side": "Sell" if side == "Buy" else "Buy",  # ဆန့်ကျင်ဘက်
            "orderType": "Market",
            "qty": size,
            "positionIdx": position_idx,
            "timeInForce": "IOC"
        }
        
        resp_close = requests.post(url_close, headers=HEADERS, json=payload, timeout=10)
        result = resp_close.json()
        
        if result.get("retCode") == 0:
            print_success(f"✅ {symbol} {side} Position (Size: {size}) ကို Market Order ဖြင့် Close လုပ်လိုက်ပါပြီ")
            return result
        else:
            print_error(f"Close လုပ်၍မရပါ: {result.get('retMsg', 'Unknown error')}")
            return result
            
    except Exception as e:
        print_error(f"Close Position Error: {e}")
        return None

def close_all_positions(category="linear"):
    """ဖွင့်ထားသမျှ Position အားလုံးကို Close လုပ်ခြင်း"""
    print_section("🔒 ALL POSITIONS CLOSE")
    print_warning("ဖွင့်ထားသော Position အားလုံးကို Close လုပ်ပါမည်!")
    
    positions = get_open_positions(category)
    
    if not positions:
        print_info("ပိတ်ရန် Position မရှိပါ")
        return
    
    for idx, pos in enumerate(positions):
        symbol = pos.get("symbol", "Unknown")
        side = pos.get("side", "")
        size = pos.get("size", "0")
        unrealised_pnl = pos.get("unrealisedPnl", "0")
        
        print_divider()
        print(f"{Fore.YELLOW}📊 {symbol} | {side} | Size: {size} | PnL: {unrealised_pnl}{Style.RESET_ALL}")
        
        close_position(symbol, idx, category)
        time.sleep(1)  # Rate limit အတွက် ခဏစောင့်ပါ

# ============================================================
# 🎯 MAIN MENU
# ============================================================

def display_menu():
    """Main menu display"""
    print_section("📋 ရွေးချယ်စရာများ")
    menu_items = [
        "🎁 Rewards စာရင်းကြည့်ရှုခြင်း",
        "💰 Rewards Claim လုပ်ခြင်း (Auto)",
        "📊 Open Positions ကြည့်ရှုခြင်း",
        "🔒 Position တစ်ခုချင်း Close လုပ်ခြင်း",
        "🔐 Position အားလုံး Close လုပ်ခြင်း",
        "⚙️  ဆက်တင်များ ပြောင်းလဲခြင်း",
        "🚪 ထွက်မည်"
    ]
    
    for i, item in enumerate(menu_items, 1):
        print(f"  {Fore.CYAN}{i}.{Style.RESET_ALL} {item}")
    print()

def claim_all_rewards(rewards_data):
    """Claimable reward အားလုံးကို Auto Claim လုပ်ခြင်း"""
    if not rewards_data:
        print_error("Reward data မရှိပါ")
        return
    
    items = rewards_data.get("result", {}).get("items", [])
    if not items:
        print_info("Reward မရှိပါ")
        return
    
    claimable = [item for item in items if item.get("status") == "claimable"]
    
    if not claimable:
        print_info("Claim လုပ်နိုင်သော Reward မရှိပါ")
        return
    
    print_section("🎁 AUTO CLAIMING REWARDS")
    print(f"စုစုပေါင်း Claim လုပ်နိုင်သော Rewards: {len(claimable)} ခု\n")
    
    for idx, item in enumerate(claimable, 1):
        name = item.get('name', item.get('title', f'Reward #{idx}'))
        reward_id = item.get('id', item.get('rewardId', ''))
        reward_type = item.get('type', 'airdrop')
        
        print(f"{Fore.YELLOW}[{idx}/{len(claimable)}] Claiming: {name}{Style.RESET_ALL}")
        result = claim_reward(reward_id, reward_type)
        
        if result and result.get("retCode") == 0:
            print_success(f"✅ {name} - Claim အောင်မြင်ပါသည်")
        else:
            print_error(f"❌ {name} - Claim မအောင်မြင်ပါ: {result.get('retMsg', 'Unknown error')}")
        
        if idx < len(claimable):
            time.sleep(1.5)  # Rate limiting
        print_divider()

def display_positions_table(positions):
    """Position များကို Table ပုံစံဖြင့် ပြသခြင်း"""
    if not positions:
        print_info("ဖွင့်ထားသော Position မရှိပါ")
        return
    
    print_section("📊 OPEN POSITIONS")
    print(f"{Fore.CYAN}{'No.':<4} {'Symbol':<12} {'Side':<6} {'Size':<12} {'Entry Price':<12} {'Mark Price':<12} {'PnL':<12}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'─' * 75}{Style.RESET_ALL}")
    
    for idx, pos in enumerate(positions, 1):
        symbol = pos.get("symbol", "N/A")
        side = pos.get("side", "N/A")
        size = pos.get("size", "0")
        entry_price = pos.get("avgPrice", "0")
        mark_price = pos.get("markPrice", "0")
        unrealised_pnl = pos.get("unrealisedPnl", "0")
        
        pnl_color = Fore.GREEN if float(unrealised_pnl) >= 0 else Fore.RED
        side_color = Fore.GREEN if side == "Buy" else Fore.RED
        
        print(f"{idx:<4} {symbol:<12} {side_color}{side:<6}{Style.RESET_ALL} {size:<12} {entry_price:<12} {mark_price:<12} {pnl_color}{unrealised_pnl:<12}{Style.RESET_ALL}")

# ============================================================
# 🚀 MAIN PROGRAM
# ============================================================

def main():
    """Main program loop"""
    current_category = "linear"
    
    while True:
        clear_screen()
        print_banner()
        display_menu()
        
        try:
            choice = input(f"{Fore.GREEN}👉 ရွေးချယ်ပါ (1-7): {Style.RESET_ALL}").strip()
        except KeyboardInterrupt:
            print("\n")
            print_warning("Program ကို ရပ်တန့်လိုက်ပါသည်")
            sys.exit(0)
        
        if choice == "1":
            # Rewards List
            rewards = get_rewards_list()
            if rewards:
                items = rewards.get("result", {}).get("items", [])
                print_section(f"🎁 REWARDS LIST ({len(items)} items)")
                for idx, item in enumerate(items, 1):
                    name = item.get("name", item.get("title", f"Item #{idx}"))
                    status = item.get("status", "unknown")
                    status_color = Fore.GREEN if status == "claimable" else Fore.YELLOW
                    print(f"  {idx}. {name} - Status: {status_color}{status}{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{Style.RESET_ALL}")
            
        elif choice == "2":
            # Auto Claim Rewards
            rewards = get_rewards_list()
            claim_all_rewards(rewards)
            input(f"\n{Fore.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{Style.RESET_ALL}")
            
        elif choice == "3":
            # View Open Positions
            positions = get_open_positions(current_category)
            display_positions_table(positions)
            input(f"\n{Fore.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{Style.RESET_ALL}")
            
        elif choice == "4":
            # Close Single Position
            positions = get_open_positions(current_category)
            display_positions_table(positions)
            
            if positions:
                try:
                    pos_num = int(input(f"\n{Fore.GREEN}Close လုပ်လိုသော Position နံပါတ် ထည့်ပါ (1-{len(positions)}): {Style.RESET_ALL}"))
                    if 1 <= pos_num <= len(positions):
                        pos = positions[pos_num - 1]
                        confirm = input(f"{Fore.YELLOW}{pos['symbol']} {pos['side']} (Size: {pos['size']}) - Close လုပ်မှာ သေချာပါသလား? (y/n): {Style.RESET_ALL}")
                        if confirm.lower() == 'y':
                            close_position(pos["symbol"], pos_num - 1, current_category)
                    else:
                        print_error("မှားယွင်းသော နံပါတ်")
                except ValueError:
                    print_error("ဂဏန်းသာ ထည့်ပါ")
            input(f"\n{Fore.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{Style.RESET_ALL}")
            
        elif choice == "5":
            # Close All Positions
            confirm = input(f"{Fore.RED}⚠️ ဖွင့်ထားသမျှ Position အားလုံး Close လုပ်မှာ သေချာပါသလား? (yes/no): {Style.RESET_ALL}")
            if confirm.lower() == 'yes':
                close_all_positions(current_category)
            else:
                print_info("လုပ်ဆောင်ချက် ပယ်ဖျက်လိုက်ပါသည်")
            input(f"\n{Fore.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{Style.RESET_ALL}")
            
        elif choice == "6":
            # Settings
            print_section("⚙️ SETTINGS")
            print(f"Current Category: {Fore.GREEN}{current_category}{Style.RESET_ALL}")
            print("Available: linear, inverse, option")
            new_cat = input("Category အသစ်ထည့်ပါ (သို့) Enter နှိပ်၍ မပြောင်းပါ: ").strip()
            if new_cat in ["linear", "inverse", "option"]:
                current_category = new_cat
                print_success(f"Category ကို {current_category} သို့ပြောင်းလိုက်ပါသည်")
            elif new_cat == "":
                print_info("မပြောင်းလဲပါ")
            else:
                print_error("မှားယွင်းသော Category")
            input(f"\n{Fore.CYAN}Enter နှိပ်၍ ဆက်သွားပါ...{Style.RESET_ALL}")
            
        elif choice == "7":
            # Exit
            print_success("Program မှ ထွက်ခွာပါပြီ။ ကျေးဇူးတင်ပါသည်! 👋")
            time.sleep(1)
            sys.exit(0)
        
        else:
            print_error("မှားယွင်းသော ရွေးချယ်မှု - 1 မှ 7 အတွင်းသာ ရွေးပါ")
            time.sleep(1)

if __name__ == "__main__":
    try:
        # Required library check
        import colorama
    except ImportError:
        print("colorama library လိုအပ်ပါသည်။ အောက်ပါ command ဖြင့် install လုပ်ပါ:")
        print("pip install colorama")
        print("\nသို့မဟုတ် colorama မပါဘဲ သုံးလိုပါက အောက်ပါအတိုင်း ပြောင်းလဲနိုင်ပါသည်...")
        sys.exit(1)
    
    main()
