import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()  # ~/bybit_test/.env ကို ဖတ်မယ်

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")
TESTNET = os.getenv("BYBIT_TESTNET", "False").lower() == "true"

print(f"API Key: {API_KEY[:6] if API_KEY else 'None'}...")
print(f"Testnet Mode: {TESTNET}")

if not API_KEY or not API_SECRET:
    print("ERROR: Missing API credentials in .env")
    exit(1)

# Mainnet endpoint
session = HTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=TESTNET)

# 1. Public endpoint test (server time)
print("\n1. Testing public endpoint (server time)...")
try:
    time_resp = session.get_server_time()
    if time_resp['retCode'] == 0:
        print("   ✓ Connected to Bybit server")
        print(f"   Server time: {time_resp['result']['timeSecond']}")
    else:
        print(f"   ✗ Error: {time_resp}")
        exit(1)
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    exit(1)

# 2. Private endpoint test (get wallet balance)
print("\n2. Testing private endpoint (wallet balance)...")
try:
    balance = session.get_wallet_balance(accountType="UNIFIED")
    if balance['retCode'] == 0:
        print("   ✓ Successfully authenticated with Bybit Mainnet!")
        coins = balance['result']['list'][0]['coin']
        print("   First few coins balance:")
        for coin in coins[:3]:
            print(f"     - {coin['coin']}: {coin['walletBalance']}")
    else:
        print(f"   ✗ API error: {balance['retMsg']}")
        print("     Please check:")
        print("       - API key has 'Read' permission")
        print("       - API key is for Mainnet (not testnet)")
        print("       - IP whitelist is disabled or includes your IP")
except Exception as e:
    print(f"   ✗ Error: {e}")
