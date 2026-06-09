#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bybit Rewards Claim Script for Termux (Firefox + Geckodriver)
အသုံးပြုပုံ:
    python bybit_claim_complete.py
"""

import pickle
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================== CONFIGURATION ==================
HEADLESS_MODE = False   # True ဆိုရင် browser မြင်ရမှာမဟုတ်ဘူး (ပထမဆုံးအကြိမ် False ထားပြီး login လုပ်ပါ)
COOKIE_FILE = "bybit_cookies.pkl"
REWARDS_URL = "https://www.bybit.com/rewards-hub"
GECKODRIVER_PATH = "/data/data/com.termux/files/usr/bin/geckodriver"
# ===================================================

def create_driver(headless=HEADLESS_MODE):
    """Firefox driver ကို Termux အတွက် သင့်တော်အောင် ဖွင့်ပေးတယ်"""
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    
    # Termux အတွက် sandbox issues ကိုရှောင်ရန်
    options.set_preference("security.sandbox.content.level", 0)
    options.set_preference("browser.tabs.remote.autostart", False)
    options.set_preference("dom.ipc.processPrelaunch.enabled", False)
    options.set_preference("browser.launcherProcess.enabled", False)
    
    # Firefox binary လမ်းကြောင်း (တစ်ခါတလေ လိုအပ်)
    options.binary_location = "/data/data/com.termux/files/usr/bin/firefox"
    
    service = Service(executable_path=GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def save_cookies(driver):
    """လက်ရှိ session ရဲ့ cookies ကို ဖိုင်ထဲသိမ်းတယ်"""
    cookies = driver.get_cookies()
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(cookies, f)
    print(f"✅ Cookies saved to {COOKIE_FILE} ({len(cookies)} items)")

def load_cookies(driver):
    """ဖိုင်ထဲက cookies ကို driver ထဲထည့်တယ်"""
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        print(f"✅ Loaded {len(cookies)} cookies from {COOKIE_FILE}")
        return True
    except FileNotFoundError:
        print("❌ Cookie file not found. Please login manually first.")
        return False

def click_claim_button(driver):
    """Claim button ကို selectors အမျိုးမျိုးနဲ့ ရှာဖွေပြီး နှိပ်ပေးတယ်"""
    print("🔍 Looking for claim button...")
    
    # မှန်ကန်တဲ့ XPath selectors စာရင်း (ပြင်ဆင်ပြီး)
    selectors = [
        (By.XPATH, "//button[contains(text(), 'Claim')]"),
        (By.XPATH, "//button[contains(text(), 'Claim Reward')]"),
        (By.XPATH, "//button[contains(text(), 'Claim Rewards')]"),
        (By.XPATH, "//*[contains(text(), 'Claim') and (self::button or self::a)]"),
        (By.XPATH, "//*[contains(@id, 'claim') or contains(@class, 'claim')]"),
        (By.CSS_SELECTOR, "button.claim-btn, .reward-claim-btn"),
    ]
    
    for by_type, selector in selectors:
        try:
            print(f"   Trying: {selector}")
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((by_type, selector))
            )
            print(f"✅ Found with: {selector}")
            button.click()
            print("🎉 Claim button clicked successfully!")
            return True
        except Exception:
            continue
    
    print("❌ No claim button found after trying all selectors.")
    return False

def login_and_save_cookies():
    """ပထမအကြိမ် – browser ဖွင့်ပြီး user ကိုယ်တိုင် login ဝင်စေတယ်၊ ပြီးရင် cookie သိမ်းတယ်"""
    print("="*50)
    print("🖥️  Opening browser for manual login...")
    print("Please login to your Bybit account (email + 2FA if needed).")
    print("After successful login, come back here and press Enter.")
    print("="*50)
    
    driver = create_driver(headless=False)
    driver.get(REWARDS_URL)
    
    # User ကိုယ်တိုင် login လုပ်ဖို့ အချိန်ပေး
    input("⏳ Press Enter AFTER you have logged in and see the Rewards page...")
    
    # Cookie သိမ်းမယ်
    save_cookies(driver)
    
    # Claim button ကို စမ်းကြည့်မယ် (optional)
    click_claim_button(driver)
    
    print("✅ First-time setup complete. Cookies saved.")
    input("Press Enter to close browser...")
    driver.quit()

def auto_claim_with_cookies():
    """cookie ရှိပြီးသားဆိုရင် headless mode နဲ့ auto claim လုပ်တယ်"""
    print("="*50)
    print("🤖 Running in headless auto-claim mode...")
    
    driver = create_driver(headless=True)
    driver.get(REWARDS_URL)
    
    # Cookie load လုပ်ပါ
    if not load_cookies(driver):
        driver.quit()
        print("💡 Please run the script again and choose option 1 first.")
        return
    
    # Page ကို refresh လုပ်ပြီး cookies အလုပ်လုပ်အောင်
    driver.refresh()
    time.sleep(3)  # စာမျက်နှာ ပြန်တင်ဖို့အချိန်ပေး
    
    # Claim button ရှာဖွေနှိပ်ပါ
    success = click_claim_button(driver)
    
    if success:
        print("🎉 Auto-claim completed!")
    else:
        print("⚠️ Could not claim. Maybe no rewards available or page changed.")
    
    print("Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()

def main():
    """အဓိက menu – ဘာလုပ်ချင်လဲ ရွေးချယ်ပါ"""
    print("\n" + "="*50)
    print("🦊 Bybit Rewards Claimer for Termux")
    print("="*50)
    print("1. First time setup (manual login, save cookies)")
    print("2. Auto-claim using saved cookies (headless)")
    print("3. Test claim button only (browser visible, no cookie save)")
    print("4. Exit")
    
    choice = input("Choose option (1/2/3/4): ").strip()
    
    if choice == "1":
        login_and_save_cookies()
    elif choice == "2":
        auto_claim_with_cookies()
    elif choice == "3":
        driver = create_driver(headless=False)
        driver.get(REWARDS_URL)
        input("Login manually if needed, then press Enter to test claim button...")
        click_claim_button(driver)
        input("Press Enter to close browser...")
        driver.quit()
    else:
        print("Exiting. Goodbye!")

if __name__ == "__main__":
    main()
