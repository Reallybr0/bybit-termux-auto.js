from pybit.unified_trading import HTTP
import time
import sys

# --- Configuration ---
API_KEY = "9ipCHT3pNd5I8BOr0p"  # ကိုယ့် API Key ထည့်
API_SECRET = "bXaxjRmnQVEKePzyBf1ApW9rGdTRsIFQZTT6"  # ကိုယ့် Secret ထည့်
SYMBOL = "XPLUSDT"
LEVERAGE = 35
RISK_PERCENT = 0.3  # 30%

print("Starting Bybit Bot...")

# Connect to Bybit (Mainnet)
session = HTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=False)

def get_wallet_balance():
    """Get available USDT balance"""
    try:
        resp = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        balance = float(resp['result']['list'][0]['coin'][0]['walletBalance'])
        print(f"Balance: {balance} USDT")
        return balance
    except Exception as e:
        print(f"Error fetching balance: {e}")
        sys.exit(1)

def set_leverage():
    """Set leverage to 35x"""
    try:
        resp = session.set_leverage(category="linear", symbol=SYMBOL, buyLeverage=str(LEVERAGE), sellLeverage=str(LEVERAGE))
        print(f"Leverage set to {LEVERAGE}x.")
    except Exception as e:
        print(f"Leverage setting error: {e}")

def open_long():
    """Open a long position with 30% of balance"""
    balance = get_wallet_balance()
    if balance <= 0:
        print("Insufficient balance.")
        return

    # Calculate order quantity
    qty = (balance * RISK_PERCENT) / 10  # အကြမ်းဖျင်း တွက်ချက်မှု
    qty = round(qty, 2)
    
    print(f"Opening LONG for {SYMBOL}, Qty: {qty}")
    
    try:
        # Place market order
        order = session.place_order(
            category="linear",
            symbol=SYMBOL,
            side="Buy",
            orderType="Market",
            qty=str(qty),
            positionIdx=1  # 1 = Long position
        )
        print("Order successful:", order)
    except Exception as e:
        print(f"Order failed: {e}")

if __name__ == "__main__":
    print(f"Place Long order for {SYMBOL} with 35x leverage, 30% of balance...")
    set_leverage()
    open_long()
    print("Bot execution finished.")
