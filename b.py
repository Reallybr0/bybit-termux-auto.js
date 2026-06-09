import os
import time
import threading  # Coin နှစ်ခုလုံးကို တပြိုင်တည်း Run ရန်
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

# .env ဖတ်ရန်
load_dotenv()

API_KEY = "ic3mAsWXO4qhqQch1v"
API_SECRET = "tImsYPWAA9vpgo8cxbeT8VMRXgrMH1elMWV4"

# Bybit HTTP Session ဆောက်ခြင်း
session = HTTP(
    testnet=False,  # Live အစစ်အမှန် Trade မည်ဖြစ်၍ False ထားသည်
    api_key=API_KEY,
    api_secret=API_SECRET
)

CATEGORY = "linear"
TARGET_ROI = 60.0  # ပစ်မှတ်အမြတ် ၆၀ ရာခိုင်နှုန်း
WHALE_THRESHOLD_USDT = 50000  # $50,000 နှင့်အထက်ကို Whale ဟု သတ်မှတ်မည်

def get_wallet_balance():
    """ 💡 Unified Account ထဲတွင် ကုန်သွယ်ရန် ကျန်ရှိသော USDT Balance ကို ရယူခြင်း """
    try:
        response = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        if response["retCode"] == 0:
            # Wallet ထဲက ရနိုင်ချေရှိသော လက်ကျန်ငွေ (Available Balance) ကို ယူခြင်း
            coin_info = response["result"]["list"][0]["coin"][0]
            available_balance = float(coin_info["availableToWithdraw"])
            return available_balance
    except Exception as e:
        print(f"❌ Wallet Balance ဆွဲယူရခက်ခဲနေသည်: {e}")
    return 0.0

def get_long_position(symbol):
    """ သတ်မှတ်ထားသော Symbol ၏ LONG Position ကို ရှာဖွေခြင်း """
    try:
        response = session.get_positions(category=CATEGORY, symbol=symbol)
        if response["retCode"] == 0:
            for pos in response["result"]["list"]:
                if pos["side"] == "Buy" and float(pos["size"]) > 0:
                    return pos
    except Exception as e:
        print(f"❌ [{symbol}] Position စစ်ဆေးရခက်ခဲနေသည်: {e}")
    return None

def is_whale_pumping(symbol):
    """ Order Book ကိုကြည့်ပြီး Whale ရှိမရှိ စစ်ဆေးခြင်း """
    try:
        orderbook = session.get_orderbook(category=CATEGORY, symbol=symbol, limit=30)
        if orderbook["retCode"] == 0:
            bids = orderbook["result"]["b"]
            asks = orderbook["result"]["a"]
            
            total_bid_vol = sum(float(p) * float(q) for p, q in bids)
            total_ask_vol = sum(float(p) * float(q) for p, q in asks)
            
            whale_buy_count = 0
            for price, qty in bids:
                if (float(price) * float(qty)) >= WHALE_THRESHOLD_USDT:
                    whale_buy_count += 1
            
            # အဝယ်အားက အရောင်းအားထက် ၁.၅ ဆ သာနေလျှင် သို့မဟုတ် Whale Buy Order တွေ့လျှင်
            if total_bid_vol > (total_ask_vol * 1.5) or whale_buy_count > 0:
                print(f"🚨 [WHALE ALERT - {symbol}] Bids Vol: ${total_bid_vol:,.2f} | Asks Vol: ${total_ask_vol:,.2f}")
                return True
    except Exception as e:
        print(f"❌ [{symbol}] Order Book ဖတ်ရခက်ခဲနေသည်: {e}")
    return False

def close_position(symbol, qty):
    """ Position ကို စျေးကွက်ပေါက်စျေးဖြင့် ပိတ်သိမ်းခြင်း """
    try:
        order = session.place_order(
            category=CATEGORY,
            symbol=symbol,
            side="Sell",
            orderType="Market",
            qty=qty,
            reduceOnly=True
        )
        if order["retCode"] == 0:
            print(f"🎉 [{symbol}] 60% ROI ပြည့်သဖြင့် အမြတ်သိမ်းလိုက်ပါပြီ! Order ID: {order['result']['orderId']}")
            return True
    except Exception as e:
        print(f"❌ [{symbol}] အမြတ်သိမ်းရာတွင် အမှားအယွင်းရှိသည်: {e}")
    return False

def monitor_token(symbol):
    """ Coin တစ်ခုချင်းစီအတွက် သီးသန့် အလုပ်လုပ်မည့် Loop Function """
    print(f"🚀 [{symbol}] စောင့်ကြည့်ရေး Thread စတင်ပါပြီ...")
    
    while True:
        # 💡 အကောင့်ထဲက လက်ကျန်ငွေကိုပါ စက္ကန့်တိုင်း တပြိုင်တည်း ဆွဲယူပြသမည်
        balance = get_wallet_balance()
        position = get_long_position(symbol)
        
        if position:
            size = position["size"]
            entry_price = float(position["avgPrice"])

mark_price = float(position["markPrice"])
            leverage = int(float(position["leverage"]))
            unrealised_pnl = float(position["unrealisedPnl"])
            
            # ROI တွက်ချက်ခြင်း
            roi = ((mark_price - entry_price) / entry_price) * 100 * leverage
            
            status_icon = "🟢" if unrealised_pnl >= 0 else "🔴"
            status_text = "Profit" if unrealised_pnl >= 0 else "Loss"
            
            # 💡 [ပြင်ဆင်ချက်] Wallet Balance ကို Output စာကြောင်းထဲတွင် ပေါင်းထည့်ပြသခြင်း
            print(f"📊 [{symbol}] Wallet: {balance:.2f} USDT | Lev: {leverage}x | {status_icon} Current {status_text}: {unrealised_pnl:.4f} USDT | ROI: {roi:.2f}%")
            
            # ROI ၆၀% ပြည့်ခဲ့လျှင်
            if roi >= TARGET_ROI:
                if is_whale_pumping(symbol):
                    print(f"⚠️ [ALERTS - {symbol}] 60% ရောက်သော်လည်း Whale Pump နိုင်ခြေရှိ၍ အမြတ်မသိမ်းသေးဘဲ HODL ထားသည်!!!")
                else:
                    print(f"💰 [{symbol}] Whale လက္ခဏာမတွေ့ရသဖြင့် အမြတ်သိမ်းနေပါသည်...")
                    close_position(symbol, size)
        else:
            # Position မရှိသည့်တိုင်အောင် လက်ရှိ Wallet Balance ကို ပုံမှန်ပြသပေးနေမည်
            print(f"💤 [{symbol}] Wallet: {balance:.2f} USDT | လက်ရှိတွင် LONG Position မရှိသေးပါ။")
            
        time.sleep(5)  # ၅ စက္ကန့်လျှင် တစ်ကြိမ် စစ်ဆေးမည်

if name == "main":
    TARGET_TOKENS = ["XPLUSDT", "FARTCOINUSDT"]
    threads = []

    print("🤖 Bybit Multi-Token Trade, Balance & Whale Bot စတင်နေပါပြီ...")
    
    for token in TARGET_TOKENS:
        t = threading.Thread(target=monitor_token, args=(token,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
